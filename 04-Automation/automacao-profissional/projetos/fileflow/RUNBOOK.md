# Runbook do FileFlow

## Escopo

O FileFlow copia arquivos regulares permitidos de uma raiz local para outra. Não
remove origem, não segue links, não sobrescreve e não sincroniza deleções.

## Verificação inicial

~~~bash
PYTHONPATH=src python3 -m fileflow.cli --help
PYTHONPATH=src python3 -m fileflow.cli --version
PYTHONPATH=src python3 -m unittest discover -s tests -v
~~~

Use somente diretórios específicos. Nunca use home, raiz do repositório ou raiz do
sistema como destino de teste.

## Primeiro dry-run

~~~bash
PYTHONPATH=src python3 -m fileflow.cli \
  --source fixtures/inbox \
  --target /tmp/fileflow-lab-target \
  --extensions .txt,.log \
  --max-files 100 \
  --max-total-bytes 1000000
~~~

Verifique counts, operations, caminhos relativos, actions e planDigest. Confirme
que o destino não foi criado.

## Apply

Salve o manifesto em arquivo explicitamente e use run ID sem dado pessoal:

~~~bash
PYTHONPATH=src python3 -m fileflow.cli \
  --source fixtures/inbox \
  --target /tmp/fileflow-lab-target \
  --extensions .txt,.log \
  --max-files 100 \
  --max-total-bytes 1000000 \
  --manifest /tmp/fileflow-plan.json \
  --audit /tmp/fileflow-audit.jsonl \
  --run-id lab-001 \
  --apply
~~~

Repita o dry-run. O esperado é skip para arquivos iguais.

## Conflito

Se houver conflict, preserve origem, destino e manifesto. Compare hashes. Não
remova nem sobrescreva automaticamente. Decida qual arquivo pertence ao processo e
use um destino novo ou resolva fora da ferramenta.

## Fonte alterada

Se a fonte mudar depois do plano, o executor aborta antes da primeira cópia quando
a divergência já é observável. Gere novo plano. Não edite o manifesto para forçar.

## Destino concorrente

Se um destino aparecer durante apply, ele é preservado. Reexecute dry-run para
classificá-lo como skip ou conflict. Nunca apague sem identificar o owner.

## Falha parcial

O executor valida todas as fontes antes do primeiro efeito, mas falha de I/O ou
audit pode ocorrer depois de algumas cópias. Liste o destino e gere novo plano.
Arquivos confirmados por hash virarão skip; pendentes continuarão copy. Não confie
somente no último código de saída.

## Auditoria indisponível

Se a mensagem disser que o efeito foi confirmado e a auditoria falhou, não repita
cegamente. Gere novo plano e confirme o destino. Corrija permissão/espaço do audit
path e use novo run ID para a retomada.

## Symlink ou tipo especial

O FileFlow recusa a origem. Preserve o caminho e descubra por que apareceu. Não
substitua por opção de seguir link; isso muda o modelo de segurança.

## Evidência para suporte

Compartilhe versão, comando sem caminhos pessoais, planDigest, counts, código e
primeira mensagem. Manifesto e audit não contêm caminhos absolutos nem conteúdo,
mas nomes relativos ainda podem ser sensíveis; revise antes de compartilhar.

## Remoção

O projeto não instala agenda ou credencial. Remova apenas o artifact instalado e
os diretórios de laboratório explicitamente identificados. Dados copiados pertencem
ao operador e não são apagados automaticamente.

