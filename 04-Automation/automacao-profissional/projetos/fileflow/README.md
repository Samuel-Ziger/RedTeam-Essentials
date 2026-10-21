# FileFlow

CLI didática para planejar e copiar arquivos locais com idempotência, limites,
integridade e evidência. O modo padrão é dry-run; apply precisa ser explícito.

O objetivo do projeto não é substituir uma ferramenta de sincronização. Ele torna
visíveis os contratos que todo executor de efeitos precisa enfrentar.

## Requisitos

- Python 3.11 ou superior;
- filesystem local com suporte a hard links;
- diretórios de laboratório controlados;
- nenhuma dependência externa de runtime.

## Uso rápido

A partir deste diretório:

~~~bash
PYTHONPATH=src python3 -m fileflow.cli --help

PYTHONPATH=src python3 -m fileflow.cli \
  --source fixtures/inbox \
  --target /tmp/fileflow-out

PYTHONPATH=src python3 -m fileflow.cli \
  --source fixtures/inbox \
  --target /tmp/fileflow-out \
  --manifest /tmp/fileflow-plan.json \
  --audit /tmp/fileflow-audit.jsonl \
  --run-id lab-001 \
  --apply
~~~

O primeiro comando de execução imprime o plano e não cria o destino. O segundo
grava o manifesto solicitado, aplica copies e registra eventos. Repetir deve produzir
skip para conteúdo igual.

## Contrato da CLI

~~~text
fileflow --source DIR --target DIR
         [--extensions .txt,.log]
         [--max-files N]
         [--max-total-bytes N]
         [--manifest FILE]
         [--audit FILE]
         [--run-id SAFE_ID]
         [--apply]
~~~

Defaults:

- extensions: .txt,.log;
- max-files: 10.000;
- max-total-bytes: 1.000.000.000;
- sem apply: dry-run;
- sucesso: código 0;
- entrada, conflito ou operação esperada falha: código 2.

Manifesto vai para stdout. Diagnóstico e resumo humano vão para stderr.
--manifest é um efeito de saída solicitado explicitamente mesmo em dry-run; a
gravação é por temporário e replace.

## Decisão por arquivo

| Estado observado | Action |
|---|---|
| destino ausente | copy |
| arquivo regular com SHA-256 igual | skip |
| conteúdo diferente | conflict |
| destino é link, diretório ou especial | conflict |

Qualquer conflito no plano bloqueia todo apply. Antes da primeira cópia, todas as
fontes de copy/skip são revalidadas por tipo, tamanho e hash.

## Controles implementados

- source e target resolvidos e não aninhados;
- extensões em allowlist sintática segura;
- apenas arquivos regulares, sem seguir symlink;
- quantidade e bytes totais limitados;
- SHA-256 lido em blocos;
- plano ordenado e digest canônico;
- operation ID derivado de caminho relativo e conteúdo;
- manifesto sem caminho absoluto nem conteúdo;
- dry-run real sem criar target/audit;
- revalidação das fontes antes do primeiro efeito;
- temporário no diretório alvo e validação de hash;
- publicação exclusiva sem sobrescrever destino;
- audit JSONL com run ID, plan digest, operation ID e caminho relativo;
- falha de audit após copy informa efeito confirmado e exige reconciliação;
- segunda execução idempotente resulta em skip.

## Exemplo de manifesto

~~~json
{
  "schemaVersion": 1,
  "counts": {"copy": 1, "skip": 0, "conflict": 0},
  "operations": [
    {
      "operationId": "...",
      "relativePath": "example.txt",
      "size": 8,
      "sha256": "...",
      "action": "copy"
    }
  ],
  "planDigest": "..."
}
~~~

O digest exclui planDigest, caminhos absolutos e campos variáveis. Mesma observação
produz os mesmos bytes canônicos e digest.

## Arquitetura

~~~text
cli -> planner -> Plan -> executor -> filesystem
                              \-----> audit JSONL
~~~

Leia [arquitetura](docs/architecture.md) e as ADRs. Planner observa e decide; executor
revalida e aplica. A apresentação não recalcula regra.

## Testes

~~~bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
~~~

A suíte cobre plano determinístico, limites, dry-run, idempotência, conflitos,
roots aninhadas, symlink, fonte/destino alterados, corrida de destino, audit,
run ID e falha do audit depois do efeito.

O runner da formação executa o projeto junto aos exemplos:

~~~bash
bash ../../testar-curso.sh
~~~

## Operação

Consulte o [runbook](RUNBOOK.md) antes de apply. Em falha parcial, gere novo plano:
copies confirmadas por hash tornam-se skips e pendentes permanecem copies. Não
apague o destino para “tentar de novo”.

## Limitações honestas

- não remove, move, renomeia ou sincroniza deleções;
- não preserva ACL, owner ou timestamps;
- não implementa checkpoint por item;
- audit local não é inviolável;
- hard link pode não estar disponível em todo filesystem;
- APIs portáveis deixam janela contra adversário local concorrente;
- manifesto revela nomes relativos e hashes, que ainda podem ser sensíveis.

Essas limitações são exercícios do capstone, não garantias implícitas.

