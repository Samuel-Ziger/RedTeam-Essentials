# 03 — Pipelines de dados, schema e reconciliação

Um pipeline confiável não é uma sequência longa de transformações. É uma rede de
fronteiras com contratos claros, contagens reconciliáveis e dados cuja origem pode
ser explicada.

## Objetivos

- separar ingestão, decode, validação, transformação e publicação;
- escolher entre lote, streaming, quarentena e falha total;
- versionar schemas e preservar proveniência suficiente;
- construir saída determinística e contagens reconciliadas;
- retomar processamento sem perder ou duplicar registros.

## 1. Estágios e contratos

~~~text
source -> bytes -> decode -> parse -> validate -> normalize
       -> enrich -> aggregate -> serialize -> stage -> publish
~~~

Cada seta é uma fronteira. Defina tipo de entrada, tipo de saída, erro possível e
efeito. Um estágio que mistura download, regra de negócio e escrita dificulta retry
e teste: repetir a regra também repete o download e talvez a publicação.

Prefira um envelope interno estável:

~~~json
{
  "recordId": "src-20261005-000042",
  "source": {"name": "input.csv", "line": 43},
  "schemaVersion": 2,
  "data": {"customerId": "c-7", "amountMinor": 1250}
}
~~~

A origem ajuda a diagnosticar sem copiar toda a linha sensível para logs.

## 2. Validação em camadas

Valide na ordem em que a evidência nasce:

1. transporte: tamanho, checksum, compressão e tipo esperado;
2. bytes: encoding e sequência válida;
3. sintaxe: CSV/JSON bem formado;
4. estrutura: campos, tipos, limites e versão;
5. semântica: datas possíveis, valores e relações;
6. referência: entidade externa existe e pode ser usada;
7. lote: unicidade, soma e invariantes globais.

Um JSON parseável ainda pode ser inválido para o domínio. Não converta tudo para
string para “facilitar”; isso empurra o erro para uma etapa menos explicável.

## 3. Política de registro inválido

Escolha explicitamente:

- **fail-fast:** um erro invalida o lote; adequado quando atomicidade é essencial;
- **quarentena:** registros inválidos são separados com razão e origem;
- **limite de erro:** processa até N erros ou X% antes de abortar;
- **best effort:** continua e relata cada estado; adequado a itens independentes.

Quarentena não é lixeira eterna. Defina acesso, retenção, correção, replay e
proteção de dados. O replay precisa preservar a identidade original.

## 4. Reconciliação

Toda execução termina com uma equação verdadeira:

~~~text
recebidos = aceitos + rejeitados
aceitos = publicados + duplicados + pendentes + falhos
~~~

Defina se cabeçalho, linha vazia e registro filtrado entram em recebidos. Sem essa
semântica, duas equipes podem produzir contagens diferentes e ambas parecerem
corretas.

Reconcilie também valor quando o domínio permitir:

~~~text
soma_entrada_aceita = soma_publicada + soma_pendente
~~~

Use inteiro de unidade mínima ou decimal com regra explícita para dinheiro.

## 5. Lote ou streaming

Streaming reduz pico de memória e antecipa resultados. Lote facilita validação
global, ordenação e commit conjunto.

| Necessidade | Estratégia comum |
|---|---|
| transformar item independente | streaming |
| detectar duplicata global | índice, partição ou segunda fase |
| ordenar tudo | sort externo ou lote limitado |
| atomicidade do conjunto | staging + validação + publish |
| baixa latência contínua | stream com checkpoint |

Streaming não significa um byte por vez. Trabalhe em blocos e imponha backpressure
para que o produtor não acumule fila ilimitada.

## 6. Schema e evolução

Versione o documento no conteúdo, não apenas no nome do arquivo. Defina:

- campos obrigatórios e opcionais;
- tratamento de campo desconhecido;
- defaults aplicados apenas quando semanticamente seguros;
- compatibilidade de leitura e escrita;
- migração encadeada e testada;
- recusa de versão futura sem sobrescrever o original.

Uma migração é transformação de dados e precisa de fixtures no limite, falha no
último item e propriedade de idempotência. Nunca marque v2 antes de concluir a
conversão inteira.

## 7. Determinismo

Mesma entrada, configuração e versão devem produzir a mesma saída, exceto campos
declaradamente variáveis. Para isso:

- injete relógio, IDs e aleatoriedade;
- ordene por chave total e estável;
- fixe locale e representação numérica;
- normalize fim de linha quando o contrato mandar;
- serialize campos de maneira canônica;
- separe generatedAt do conteúdo usado no digest.

Determinismo melhora testes, cache, auditoria e diagnóstico.

## 8. Checkpoint e publicação

O checkpoint representa o último efeito **confirmado**, não o último registro
lido. Grave na ordem:

~~~text
processar -> publicar idempotentemente -> confirmar -> avançar checkpoint
~~~

Se o processo cair depois de publicar e antes do checkpoint, o item reaparece. O
sink precisa reconhecer a chave e devolver o resultado anterior. Se cair antes de
publicar, o checkpoint antigo garante que o item será refeito.

Para saída em arquivo, prefira staging completo, validação e publicação atômica.
Não deixe o arquivo final parecer válido durante a escrita.

## 9. Privacidade e minimização

Pipeline tende a replicar dados em temporários, logs, quarentena e artefatos.
Inventarie cada cópia. Use identificador, hash ou contagem quando o conteúdo não
for necessário. Defina retenção e remoção para staging e falhas.

Dados sintéticos devem preservar formato e casos-limite sem carregar pessoas
reais. Sanitizar não é apenas trocar nome: combinações e metadados também identificam.

## Falhas e diagnóstico

| Sintoma | Hipótese | Teste |
|---|---|---|
| contagens não fecham | estado sem categoria | enumerar todos os terminais |
| resultado muda a cada execução | ordem/relógio implícito | fixar dependências e comparar bytes |
| memória cresce com volume | materialização acidental | medir por blocos crescentes |
| replay duplica saída | checkpoint antes do commit | falhar em cada fronteira |
| erro sem linha de origem | proveniência perdida | propagar recordId e localização |

## Exercícios

### Nível 1 — pipeline local

Converta CSV para JSONL com schema e relatório. **Aceite:** fixtures cobrem Unicode,
linha truncada, tipo errado e contagens reconciliadas.

### Nível 2 — streaming

Processe arquivo maior que a memória-alvo. **Aceite:** uso de memória permanece
limitado e a saída é byte a byte determinística.

### Nível 3 — retomada

Injete falha antes e depois da publicação do item 501. **Aceite:** retomada não
perde nem duplica e a evidência explica cada item.

## Checklist

- [ ] Cada estágio tem entrada, saída e erro definidos.
- [ ] Schema e política de evolução estão versionados.
- [ ] Contagens e, quando aplicável, valores reconciliam.
- [ ] Relógio, ordem e IDs não introduzem acaso oculto.
- [ ] Checkpoint avança somente depois do efeito confirmado.
- [ ] Temporários, quarentena e logs minimizam dados.

