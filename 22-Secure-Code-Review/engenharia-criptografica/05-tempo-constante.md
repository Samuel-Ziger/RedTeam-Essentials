# 05 — Tempo constante e canais laterais

Código constant-time evita branches e acessos dependentes de segredo dentro do
modelo da plataforma. Compilador, CPU, cache, runtime e vizinhança ainda afetam
observação; por isso aplicações usam implementações dedicadas e isolamento.

Compare tags por API constante, unifique erros e limite medições repetidas.
Padding, parsing e acesso a KMS também vazam sinais de rede. Teste estatístico
ajuda a encontrar regressões, mas não prova ausência de canal.

## Prática

Revise caminhos de sucesso/falha e marque onde tempo, tamanho, status ou log
dependem de dado secreto.
