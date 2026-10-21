# Laboratório 05 — Capstone FileFlow operável

## Objetivo

Concluir e defender uma automação instalável, idempotente, auditável e recuperável.
Use o FileFlow de projetos/ ou aplique o mesmo contrato ao projeto autoral aprovado.

## Fase 1 — baseline

Execute testar-curso.sh e preserve o resultado. Leia arquitetura, limitações e
testes do FileFlow. Registre três riscos ainda não cobertos e converta-os em testes.

## Fase 2 — evolução

Implemente:

- limites de arquivos e bytes;
- digest canônico do plano;
- run ID e operation IDs;
- revalidação integral antes do primeiro efeito;
- relatório por outcome;
- fault injection e retomada;
- configuração versionada ou flags equivalentes;
- package e smoke test fora do checkout.

## Fase 3 — operação

Produza runbook para primeiro uso, conflito, origem alterada, falha parcial, audit
indisponível, upgrade, rollback e remoção. Inclua limites e ações proibidas.

## Fase 4 — game day

Uma segunda pessoa opera apenas pelo runbook. Injete, sem avisar a ordem:

1. symlink na origem;
2. destino concorrente;
3. fonte modificada após o plano;
4. falha depois de uma publicação;
5. sink de auditoria indisponível;
6. versão de configuração futura.

Ela deve preservar evidência, classificar efeitos confirmados/incertos e escolher
retomar, reconciliar ou parar sem editar estado manualmente.

## Entrega

- proposta e ADRs;
- código e suíte;
- threat model e matriz de permissões;
- fixtures sintéticas;
- artifact, digest, SBOM e inventário;
- manifesto/relatório do game day;
- runbook e matriz de compatibilidade;
- autoavaliação pela rubrica do capítulo 14.

## Critério final

O lab termina quando outra pessoa instala, planeja, aplica, repete, diagnostica uma
falha e remove a ferramenta em ambiente limpo. Exige 75 pontos e nenhum gate de
dry-run/idempotência, segurança de efeitos, testes de falha ou operação zerado.

