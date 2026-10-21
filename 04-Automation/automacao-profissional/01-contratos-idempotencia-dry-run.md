# 01 — Contratos, idempotência e dry-run

Uma automação confiável pode ser inspecionada, repetida e interrompida sem exigir
adivinhação. Isso começa por separar quatro coisas: **intenção**, **plano**,
**efeito confirmado** e **evidência**.

## Objetivos

- escrever contratos observáveis para jobs e ferramentas;
- distinguir idempotência, deduplicação e “exatamente uma vez”;
- implementar dry-run a partir do mesmo plano usado na aplicação;
- modelar commit, falha parcial e compensação sem prometer rollback falso;
- definir códigos de saída e manifestos para humanos e máquinas.

## 1. Contrato do job

O contrato existe na fronteira, não apenas na implementação:

| Elemento | Perguntas obrigatórias |
|---|---|
| entrada | schema, tamanho, origem, encoding e versão? |
| identidade | o que torna duas solicitações a mesma operação? |
| pré-condição | que estado precisa existir antes? |
| plano | como a decisão é representada e revisada? |
| efeito | quais recursos podem mudar? |
| pós-condição | como confirmar sucesso? |
| limite | tempo, itens, bytes, tentativas e concorrência? |
| recuperação | repetir, retomar, compensar ou intervir? |
| evidência | manifesto, eventos, métricas e código de saída? |

Exemplo de contrato de processo:

~~~text
0 = plano ou aplicação concluída conforme contrato
2 = uso ou entrada inválida; nenhum efeito iniciado
3 = conflito de estado; nenhum efeito novo iniciado
4 = falha operacional; consultar manifesto e audit log
5 = conclusão parcial; retomar apenas itens pendentes
~~~

Não existe tabela universal de códigos. Documente e teste a sua. Dados
estruturados vão para stdout; diagnóstico humano vai para stderr. Assim um pipeline
não recebe mensagens misturadas ao JSON.

## 2. Idempotência como propriedade observável

Uma operação é idempotente quando repeti-la com a mesma intenção produz o mesmo
estado final relevante. Ela ainda pode registrar nova tentativa ou atualizar uma
métrica. A propriedade se refere ao efeito de negócio declarado.

~~~text
aplicar(aplicar(estado, comando), comando) == aplicar(estado, comando)
~~~

Exemplos:

- garantir que um diretório exista é idempotente;
- copiar por hash para um destino ausente pode ser idempotente;
- adicionar 10 ao saldo não é; definir o saldo da versão 8 pode ser;
- enviar a mesma mensagem duas vezes não é idempotente sem deduplicação.

Prefira declarar o resultado:

~~~text
observado == desejado       -> skip
observado ausente           -> create
observado diferente seguro  -> update condicionado
observado conflitante       -> conflict
~~~

A comparação precisa ser forte o suficiente. Tamanho igual não prova conteúdo
igual; nome igual não prova identidade. Escolha hash, versão, ETag ou chave de
domínio conforme o recurso.

## 3. Chave de idempotência e deduplicação

Uma chave associa tentativas à mesma intenção. Ela deve ter escopo e vida útil:

~~~text
tenant:processo:janela_logica:identidade_entrada:versao_contrato
~~~

Guarde chave, digest da entrada, estado e resultado. Chave igual com payload
diferente é conflito, não reaproveitamento silencioso.

~~~json
{
  "key": "reports:2026-10-05:sha256-...:v1",
  "status": "succeeded",
  "resultDigest": "sha256-...",
  "committedAt": "2026-10-05T14:10:00Z"
}
~~~

### O mito de exatamente uma vez

Entre processo, fila, rede e serviço remoto, uma resposta pode se perder depois
do efeito. O cliente não sabe se deve repetir. Em vez de afirmar “exatamente uma
vez” de ponta a ponta, combine entrega ao menos uma vez, consumidor idempotente,
chave estável, reconciliação e commit durável do resultado.

## 4. Plan, apply e reconcile

Separe funções:

~~~text
entrada + estado observado  -> Plan imutável
Plan + adapters             -> ExecutionReport
estado desejado + observado -> ReconciliationReport
~~~

Um plano inclui versão, origem, operações ordenadas, razão, pré-condição e
identidade. Exemplo conceitual:

~~~python
from dataclasses import dataclass

@dataclass(frozen=True)
class CopyOperation:
    operation_id: str
    source: str
    target: str
    expected_sha256: str
    action: str
    reason: str

def decide(source_hash: str, target_hash: str | None) -> str:
    if target_hash is None:
        return "copy"
    return "skip" if target_hash == source_hash else "conflict"
~~~

O domínio decide; o adapter lê ou grava. Isso torna a regra testável sem tocar no
filesystem.

## 5. Dry-run fiel

Dry-run executa descoberta, parse, validação, leitura de estado e planejamento
reais, mas bloqueia mutação.

1. usa o mesmo planejador da aplicação;
2. falha para entrada inválida e conflito;
3. apresenta plano com razões;
4. não cria diretório, lock, cache, audit log nem checkpoint;
5. avisa que o estado pode mudar antes do apply;
6. permite vincular apply a um digest do plano.

Um teste forte injeta adapters que lançam se qualquer método de escrita for
chamado. Verificar apenas o destino final pode esconder efeitos temporários.

## 6. Concorrência e pré-condições

Entre planejar e aplicar, outro processo pode modificar o recurso: uma condição
TOCTOU. Revalide no ponto do efeito e use operação condicional:

- criação exclusiva de arquivo;
- If-Match com ETag;
- compare-and-set por versão;
- transação com restrição única;
- lease com expiração e fencing token.

Lock local não protege outro host nem serviço externo. Documente onde o controle
vale.

## 7. Atomicidade, commit e compensação

Um workflow com vários sistemas raramente é atômico. Modele cada etapa:

| Etapa | Efeito | Confirmação | Inversa segura? |
|---|---|---|---|
| gerar temporário | local descartável | hash | sim |
| publicar destino | arquivo visível | criação exclusiva | talvez |
| notificar | mensagem externa | ID de entrega | geralmente não |

Compensar é uma nova operação de negócio. Remover um destino pode destruir uma
atualização de terceiros. Use versão e ownership antes da compensação.

Padrões úteis incluem write-temp/verify/publish, outbox, saga e checkpoint após
efeito confirmado.

## 8. Manifesto e relatório

Plano e resultado são documentos diferentes. O resultado referencia o plano e
atribui estado terminal a cada operação:

~~~text
planned -> running -> succeeded | skipped | failed | uncertain | cancelled
~~~

Uncertain significa que houve timeout depois do envio e ainda não foi possível
reconciliar. Marcar failed e repetir automaticamente pode duplicar o efeito.

~~~text
total_planejado = success + skipped + failed + uncertain + cancelled
~~~

## Falhas comuns

| Erro | Consequência | Correção |
|---|---|---|
| dry-run usa outro algoritmo | simula uma coisa e executa outra | plano comum |
| chave deriva da tentativa | retry parece operação nova | derivar da intenção |
| sucesso antes do commit | falso positivo | confirmar antes de emitir |
| compensação sem versão | apaga trabalho de terceiros | condicionar ao estado criado |
| plano sem pré-condição | aplica dado obsoleto | revalidar no efeito |

## Exercícios

### Nível 1 — contratos

Defina idempotência para criar pasta, enviar relatório e atualizar cadastro.
**Aceite:** cada definição identifica estado desejado, chave e confirmação.

### Nível 2 — plan/apply

Implemente planejador puro e executor falso. **Aceite:** dry-run usa o plano real,
nenhum método mutável é chamado e as contagens reconciliam.

### Nível 3 — falha incerta

Simule timeout após envio de escrita. **Aceite:** o item fica uncertain, uma
consulta reconcilia o estado e o retry não duplica o efeito.

## Checklist

- [ ] Entrada, efeito, limites e pós-condição estão documentados.
- [ ] A chave representa a intenção e detecta payload divergente.
- [ ] Dry-run e apply compartilham o mesmo plano.
- [ ] O executor revalida pré-condições.
- [ ] Falha parcial e estado incerto são observáveis.
- [ ] Compensação não promete rollback impossível.

