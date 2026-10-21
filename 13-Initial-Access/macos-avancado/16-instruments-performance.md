# 16 — Instruments, amostragem e performance

Instruments combina templates como Time Profiler, Allocations, Points of
Interest e System Trace. Comece por uma hipótese e workload reproduzível; uma
trace enorme sem pergunta aumenta ruído e risco de dados sensíveis.

## Experimento

1. fixe versão, hardware, energia e entrada;
2. aqueça quando relevante;
3. execute múltiplas amostras;
4. compare percentis e intervalos, não só média;
5. associe custo a stack e fase;
6. mude uma variável e repita.

`sample` captura stacks de um processo; `spindump` ajuda em hangs. Use somente
processos próprios e revise o artefato antes de compartilhar.

## Prática

Perfil um parser do curso com arquivos sintéticos de tamanhos crescentes.
Formule complexidade esperada, meça wall/CPU e explique a maior stack.
