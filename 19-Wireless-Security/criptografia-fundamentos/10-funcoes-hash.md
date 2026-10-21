# 10 — Funções hash e propriedades

Hash criptográfico transforma entrada arbitrária em digest de tamanho fixo.
Propriedades principais: resistência a preimagem, segunda preimagem e colisão;
elas têm modelos e custos diferentes. Hash não criptografa e não prova autoria.

SHA-256/SHA-512, SHA-3 e BLAKE2 têm usos atuais conforme o ecossistema. MD5 e
SHA-1 não devem ser usados quando colisões importam. Um checksum detecta erro
acidental; um hash sem autenticação também pode ser recalculado pelo atacante.

## Prática

Execute `hash_mac.py digest arquivo`. Altere um byte, compare o digest e depois
explique por que publicar o digest no mesmo canal não autentica o download.
