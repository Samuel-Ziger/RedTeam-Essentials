# 12 — MAC e HMAC

Um MAC usa chave secreta para autenticar mensagem e contexto. Quem possui a
chave pode criar e verificar tags; portanto MAC não oferece não repúdio entre
participantes. HMAC compõe uma função hash de modo resistente a problemas como
length extension e é preferível a `hash(chave || mensagem)`.

Autentique uma codificação não ambígua que inclua versão, propósito e metadados
relevantes. Compare tags em tempo constante e devolva um único erro externo.
Nunca processe conteúdo não autenticado como confiável.

## Prática

Gere e verifique uma tag com `hash_mac.py`; altere mensagem, tag e contexto e
confirme três falhas fechadas.
