# 06 — Probabilidade, entropia e segurança

Para `n` resultados equiprováveis, a surpresa máxima é `log2(n)` bits. Uma
senha escolhida por hábitos humanos não ganha entropia apenas por ter muitos
caracteres possíveis. Min-entropia considera o resultado mais provável e é
mais útil contra adivinhação.

“128 bits de segurança” é uma estimativa de trabalho, não o tamanho de qualquer
campo. Uma chave uniforme de 128 bits, um hash de 256 bits e uma senha de vinte
caracteres não oferecem automaticamente a mesma resistência. Orçamento,
paralelismo, memória, número de alvos e vida útil alteram o risco.

## Prática

Compare uma escolha entre quatro palavras realmente aleatórias com uma frase
humana previsível. Declare o modelo em vez de inventar uma pontuação.
