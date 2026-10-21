# 08 — Cifras clássicas e lições modernas

César substitui letras por um deslocamento; Vigenère repete uma chave; análise
de frequência e periodicidade revelam estrutura. Essas cifras ensinam espaço
de chaves, texto conhecido e diferença entre confusão e difusão, mas não devem
proteger informação.

O erro recorrente é confundir complexidade visual com segurança. Um algoritmo
caseiro pode parecer incompreensível e ainda preservar padrões, ter poucas
chaves ou falhar sob entradas escolhidas. Algoritmos modernos são públicos,
analisados e usados dentro de construções com garantias claras.

## Prática

Implemente César apenas no papel, conte as chaves possíveis e explique por que
aumentar o alfabeto não resolve o problema estrutural.
