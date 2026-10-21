# Laboratório 01 — Contrato, plan/apply e arquivos seguros

## Objetivo

Projetar uma ferramenta local antes de automatizar efeitos. Você criará
report-organizer, que planeja a cópia de arquivos sintéticos para um destino sem
remover origem nem sobrescrever colisão.

## Cenário

~~~text
report-organizer --source DIR --target DIR [--apply]
                 [--extensions .txt,.log] [--format text|json]
~~~

O padrão é dry-run. Arquivo ausente no destino vira copy; hash igual vira skip;
hash diferente, link ou tipo especial vira conflict. Qualquer conflito conhecido
bloqueia todo apply.

## Etapa A — decidir e contratar

Entregue matriz de candidato, mapa do processo e contrato contendo:

- pessoa/tarefa e não objetivos;
- entradas, encoding, limites e raízes;
- efeitos e pós-condições;
- códigos para uso, conflito e falha operacional;
- cancelamento e recuperação;
- critérios para subir do plan ao apply.

## Etapa B — planejador puro

Modele Operation e Plan imutáveis. O planejador recebe observações e não escreve.
Cada operação possui ID, caminho relativo, tamanho, hash, action e reason.

Teste ordem de descoberta diferente, case, Unicode, absoluto, ponto-ponto, link,
limite de quantidade e limite de bytes.

## Etapa C — executor

Copie para temporário no mesmo diretório, valide e publique por criação exclusiva.
Revalide fonte e destino. Injete destino concorrente depois do plano.

## Etapa D — dry-run sentinela

Use fake que lança em mkdir, write, audit ou checkpoint. O dry-run deve produzir o
mesmo plano sem chamar mutação.

## Evidências e aceite

- duas execuções deixam o mesmo estado;
- conflito aborta antes da primeira cópia;
- destino concorrente é preservado;
- hash da fonte alterada invalida apply;
- stdout JSON é parseável e stderr separado;
- nenhuma entrada escapa da raiz.

## Extensão

Compare seu contrato com as cinco implementações de batch-plan em exemplos/ e
registre como cada runtime representa erro, ausência, ordenação e processo.

