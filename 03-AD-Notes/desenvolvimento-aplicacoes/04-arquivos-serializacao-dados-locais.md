# 04 — Arquivos, serialização e dados locais

Persistência local parece simples até ocorrer escrita interrompida, formato antigo,
duas instâncias ou documento corrompido. Assim que outra versão da aplicação
precisa ler os bytes, o formato se torna uma API. Neste capítulo, o Study Desk
ganha um documento JSON versionado, importação limitada e gravação substituível,
sem acoplar o domínio à representação externa.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- escolher um formato a partir de acesso, volume, evolução e interoperabilidade;
- separar entidade de domínio, DTO e documento persistido;
- definir schema, versão, limites e política para campos desconhecidos;
- projetar migrações sequenciais testadas com fixtures reais;
- implementar leitura limitada, importação atômica e escrita recuperável;
- detectar conflito de revisão e documentar backup, restauração e exclusão.

## Pré-requisitos

Este capítulo usa as invariantes do capítulo 00, configuração tipada do capítulo
02 e taxonomia de falhas do capítulo 03. Você deve conhecer JSON, coleções, I/O
de arquivo e testes. Detalhes internos de locking e sistemas de arquivos pertencem
aos módulos próprios; aqui tratamos o comportamento observável da aplicação.

## Modelo mental: bytes não são objetos

Persistência é uma cadeia de traduções:

```text
bytes limitados -> texto decodificado -> documento sintático -> DTO validado
                -> objetos de domínio -> estado candidato -> confirmação
```

Na gravação, o caminho inverso produz um **novo documento completo**. Cada seta
pode falhar e deve ter uma categoria: encoding inválido não é o mesmo que JSON
malformado; JSON válido não implica schema válido; schema válido não garante
invariantes de domínio.

## Escolha do formato por requisito

| Formato | Bom para | Limite importante |
|---|---|---|
| JSON | interoperabilidade e inspeção | tipos limitados; documento inteiro |
| CSV | dados tabulares simples | dialetos, encoding, fórmulas e tipos ambíguos |
| SQLite | consultas e transações locais | schema, migrações e ferramenta adicional |
| binário padronizado | volume e contrato tipado | inspeção menos direta |
| binário próprio | caso altamente específico | alto custo de evolução e ferramentas |

Para a primeira versão do Study Desk, JSON é adequado porque o conjunto é
pequeno, exportável e lido como documento completo. Se consultas parciais,
concorrência frequente ou centenas de milhares de registros se tornarem requisito,
SQLite pode ser melhor. “Banco é profissional” e “JSON é simples” não substituem
medidas.

## Entidade, DTO e envelope

Não serialize o objeto interno automaticamente. Campos privados, nomes de classes
e tipos da linguagem mudam durante refatorações. Defina um DTO de fronteira e um
envelope versionado:

```json
{
  "schemaVersion": 1,
  "exportedAt": "2026-10-05T15:00:00.000Z",
  "sessions": [
    {
      "id": "01J9Y7M6Y3A5T7K8Q2N4C6D8F0",
      "title": "Grafos",
      "minutes": 45,
      "createdAt": "2026-10-05T14:30:00.000Z"
    }
  ]
}
```

`schemaVersion` governa a forma do documento. `exportedAt` é metadado da
exportação, não a data das sessões. A versão executável não possui `revision`:
adicioná-la para detectar sobrescrita concorrente seria evolução de schema e
exigiria uma versão/migração, pois o leitor atual rejeita campos desconhecidos.

O mapeamento é explícito:

```python
from datetime import datetime, timezone
from typing import Any


def session_to_dto(session: "StudySession") -> dict[str, object]:
    if session.recorded_at.tzinfo is None or session.recorded_at.utcoffset() is None:
        raise ValueError("recorded_at deve possuir fuso explícito")
    recorded = session.recorded_at.astimezone(timezone.utc)
    return {
        "id": session.session_id,
        "title": session.title,
        "minutes": session.minutes,
        "createdAt": recorded.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    }


def require_exact_keys(value: dict[str, Any], expected: set[str]) -> None:
    unknown = set(value) - expected
    missing = expected - set(value)
    if unknown or missing:
        raise ValueError(f"campos inválidos: unknown={sorted(unknown)}, missing={sorted(missing)}")
```

Em produção, não coloque o documento completo na mensagem de exceção. O exemplo
mostra a regra; a apresentação deve converter a falha em erro seguro e localizado.

## Schema e política de compatibilidade

Para cada campo, documente:

- nome, tipo e obrigatoriedade;
- faixa, tamanho e formato;
- semântica de `null`, vazio e ausente;
- unicidade e referências;
- comportamento diante de campo desconhecido;
- versão em que foi adicionado ou removido.

Rejeitar campos desconhecidos detecta erro cedo, mas dificulta um leitor antigo
abrir documento novo. Ignorá-los melhora compatibilidade para frente, mas pode
perder dados ao regravar. Uma opção é preservar extensões desconhecidas. Escolha
de forma explícita por tipo de arquivo: a importação estrita do Study Desk rejeita
versão futura que não entende, em vez de regravar silenciosamente.

JSON também possui armadilhas: chaves duplicadas podem ser aceitas com políticas
diferentes, números podem exceder os tipos da linguagem e algumas bibliotecas
aceitam valores não padronizados como `NaN`. O Study Desk v1 usa `JSON.parse`:
quando uma chave se repete, o parser já entrega apenas o último valor e
`exactKeys` não consegue detectar a duplicata. Portanto, a versão atual **não
promete rejeição de chaves duplicadas**. Se esse requisito for necessário, adote
um parser/tokenizador que preserve ocorrências, limite recursos e tenha fixtures;
uma regex sobre texto JSON não é um substituto correto.

## Limites são parte do contrato

Um arquivo local continua sendo entrada não confiável. Pode vir de download,
backup antigo ou edição manual. Defina antes de analisar:

| Recurso | Limite da versão executável do Study Desk |
|---|---:|
| arquivo selecionado | 5.000.000 bytes antes da leitura |
| texto JSON | 5.000.000 unidades de código UTF-16 antes do parse |
| sessões | 10.000 |
| título | 80 unidades de código UTF-16, sem controles |
| duração | 1..1440 minutos |
| profundidade JSON | apenas a estrutura prevista |

No navegador, `File.size` permite recusar o arquivo antes de `file.text()`; o
domínio verifica novamente o limite de caracteres antes de `JSON.parse`. Ao ler
um stream/arquivo em outra interface, leia no máximo `limite + 1` bytes: o byte
adicional distingue “exatamente no limite” de “maior que o limite”. Não leia
tudo para só então verificar o tamanho.

```python
def read_bounded(path, max_bytes: int) -> bytes:
    with path.open("rb") as source:
        payload = source.read(max_bytes + 1)
    if len(payload) > max_bytes:
        raise ValueError(f"documento excede {max_bytes} bytes")
    return payload
```

Depois, decodifique UTF-8 estritamente. Substituir bytes inválidos por caracteres
genéricos pode alterar IDs ou texto sem consentimento.

## Migrações sequenciais

Se a versão 2 adiciona `tags` e a 3 renomeia um campo, prefira:

```text
v1 --migrate_1_to_2--> v2 --migrate_2_to_3--> v3 -> domínio atual
```

Cada função recebe documento válido da versão anterior e produz documento válido
da próxima. Isso é mais testável que um bloco com todas as combinações. Mantenha
fixtures anônimas de cada versão suportada e teste:

- migração direta para a próxima versão;
- cadeia completa até a atual;
- idempotência quando a ferramenta reaplica somente etapas necessárias;
- rejeição de versão futura e antiga demais;
- preservação de significado, não apenas de chaves.

Faça backup ou ofereça exportação antes de uma migração irreversível. Nunca
marque o schema como novo antes de terminar a transformação.

## Importação transacional do ponto de vista do usuário

O fluxo correto separa validação de confirmação:

```text
ler limitado -> decodificar -> parsear -> validar envelope -> migrar
             -> validar todos os DTOs -> construir domínio candidato
             -> mostrar resumo -> confirmar -> persistir uma vez
```

Antes da confirmação, o repositório atual permanece intocado. O resumo informa
quantos itens serão criados, substituídos ou ignorados. “Mesclar” e “substituir”
são políticas diferentes e precisam definir colisão de ID.

Não aceite caminho ou comando embutido no documento como algo a executar. Dados
continuam dados. Para CSV exportado, neutralize células que programas de planilha
podem interpretar como fórmulas se esse for um formato suportado.

## Escrita segura e recuperável

Editar o único arquivo byte a byte pode deixar metade antiga e metade nova. O
padrão de aplicação é:

1. serializar o documento completo de maneira determinística;
2. escrever um arquivo temporário no destino apropriado;
3. concluir e verificar a escrita quando o requisito exigir;
4. substituir o destino usando a API documentada;
5. manter backup ou histórico conforme o impacto de perda;
6. atualizar o estado em memória — e a revisão, se esse modelo existir — somente
   após sucesso.

Atomicidade e durabilidade reais dependem da plataforma e serão estudadas nos
módulos de sistemas operacionais. O contrato aqui é observável: uma falha antes
da substituição mantém o último documento confirmado; resíduo temporário pode ser
identificado e limpo com segurança na próxima inicialização.

Serialização determinística — ordenação estável e representação temporal única —
facilita teste, diff e diagnóstico. Não confunda ordem estética com ordem semântica;
declare a que pertence ao contrato.

## Concorrência em nível de aplicação como evolução

O schema v1 executável não possui revisão nem coordenação entre abas. Se esse
requisito for adicionado em uma versão futura, duas janelas podem ler a revisão
7: a primeira grava a 8; a segunda não deve
sobrescrever silenciosamente com base na 7. Uma porta pode exigir:

```text
save(expected_revision=7, new_document) -> revision=8 ou Conflict(actual=8)
```

Estratégias possíveis:

- escritor único;
- comparação de revisão e conflito explícito;
- armazenamento transacional;
- merge com regra de domínio;
- salvar cópia sem destruir a versão mais nova.

Data de modificação sozinha pode ter granularidade ou semântica insuficiente.
Use uma revisão controlada pelo documento se ela atende ao modelo.

## Backup, restauração e exclusão

Exportar uma vez não é automaticamente uma estratégia de backup. Documente:

- o que é incluído e excluído;
- como verificar que um backup pode ser lido;
- como restaurar sem destruir o estado atual por engano;
- quantas versões são mantidas e por quanto tempo;
- como excluir dados principais, temporários e backups conhecidos;
- quais cópias externas estão fora do controle da aplicação.

Teste restauração. Um arquivo que nunca foi restaurado é apenas uma esperança.
Dados sensíveis podem permanecer em cópias, lixeira ou sincronização escolhida
pelo usuário; comunique limites sem prometer apagamento absoluto.

## Falhas comuns e diagnóstico

| Sintoma | Hipótese | Teste direcionado |
|---|---|---|
| arquivo novo não abre na versão antiga | compatibilidade não foi definida | fixture por versão |
| dados mudam após exportar/importar | DTO não preserva semântica | teste de ida e volta |
| importação parcial aparece após erro | mutação ocorreu durante parsing | compare estado anterior/posterior |
| sessão desaparece entre janelas | sobrescrita sem revisão | simule dois leitores |
| arquivo fica truncado | escrita direta no destino | injete falha em cada etapa |
| memória cresce demais | limite aplicado depois da leitura | use stream falso maior que o teto |

Guarde uma cópia segura do artefato problemático apenas quando permitido e
anonimizado. Registre tamanho, versão do schema, etapa que falhou e código de
erro; não despeje o conteúdo inteiro no log.

## Exercícios em três níveis

### Nível 1 — schema

Defina o schema v1 do Study Desk e crie fixtures para documento mínimo, limite,
campo ausente, tipo errado, versão futura e ID duplicado.

**Critérios de aceite:** cada campo tem tipo/limite; desconhecidos possuem
política; fixtures inválidas falham na etapa e com a categoria esperadas.

### Nível 2 — leitura e migração

Implemente leitura limitada e migração v1→v2 que adiciona `tags: []`. Converta
DTOs em objetos de domínio somente depois de validar o documento.

**Critérios de aceite:** documento acima do teto não é lido integralmente;
encoding inválido é rejeitado; fixture v1 chega à v2 sem perder sessões.

### Nível 3 — repositório recuperável

Implemente importação `replace` com resumo, confirmação, escrita temporária e
revisão otimista. Injete falha antes, durante e depois da escrita temporária.

**Critérios de aceite:** nenhuma falha anterior à substituição altera o arquivo
confirmado; revisão obsoleta gera conflito; restauração de fixture é demonstrada;
temporários possuem política segura de limpeza.

## Checklist de domínio

- [ ] Escolho formato por requisito, não por moda ou familiaridade.
- [ ] Separo entidade, DTO, envelope e bytes persistidos.
- [ ] Documento tipos, limites, versão e campos desconhecidos.
- [ ] Aplico limites antes de alocar ou analisar todo o conteúdo.
- [ ] Migro sequencialmente e mantenho fixtures de cada versão suportada.
- [ ] Importo em estado candidato antes de confirmar uma única alteração.
- [ ] Escrevo sem destruir a última versão válida em uma falha intermediária.
- [ ] Detecto revisão obsoleta e sei restaurar um backup testado.
