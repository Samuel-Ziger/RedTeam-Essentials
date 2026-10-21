# 06 — Memória, segredo e zeroização

Segredos aparecem em heap, stack, cópias, core dumps, swap, logs e snapshots.
Reduza duração e cópias, use handles de HSM/KMS quando possível, desative dumps
em processos adequados e controle debugging. Garbage collection impede prometer
zeroização de strings imutáveis.

Zeroizar um buffer é defesa parcial, não apaga cópias do runtime ou hardware.
O desenho deve limitar impacto mesmo se memória de um processo for capturada:
chaves por tenant/época, privilégios mínimos e rotação.

## Prática

Faça um mapa de todas as representações de uma chave desde a geração até a
destruição.
