# Lab 05 — Backup, manifesto e restauração

## Objetivo

Demonstrar integridade e restauração de uma árvore sintética.

## Procedimento

1. Crie uma origem com subdiretórios, arquivo vazio e nomes com espaço.
2. Execute `Backup-RteFixture.py --dry-run` e revise o plano.
3. Execute para um destino novo fora da origem.
4. Valide `manifest.json` e hashes com `--verify`.
5. Copie a restauração para terceiro caminho e compare conteúdo.
6. Registre RPO, RTO e o risco de origem/destino no mesmo dispositivo.

## Critério

O segundo uso do mesmo destino falha antes de sobrescrever. O cleanup remove
somente as três árvores sintéticas criadas.
