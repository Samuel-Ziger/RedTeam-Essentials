# 07 — Aleatoriedade, CSPRNG, nonce, salt e IV

Use o gerador criptográfico do sistema (`secrets`, `os.urandom` ou a API da
biblioteca). PRNGs de simulação, timestamps e identificadores sequenciais não
geram chaves. Testes estatísticos podem detectar defeitos grosseiros, mas não
provam imprevisibilidade.

Um **salt** individualiza KDFs e normalmente pode ser público. Um **nonce** deve
ser único no escopo exigido pelo algoritmo; alguns esquemas pedem aleatoriedade,
outros aceitam contadores persistentes. **IV** é um termo de modo específico.
Nenhum deles é sinônimo de chave e nunca se corrige reutilização apenas
aumentando o tamanho.

## Verificação

Explique por que guardar nonce ao lado do ciphertext costuma ser correto e por
que repetir nonce com a mesma chave pode ser catastrófico.
