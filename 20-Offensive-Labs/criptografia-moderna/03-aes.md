# 03 — AES e seu modelo

AES é uma permutação de blocos de 128 bits com chaves de 128, 192 ou 256 bits.
SubBytes, ShiftRows, MixColumns e AddRoundKey criam não linearidade e difusão.
Esses detalhes ajudam a compreender o projeto, mas aplicações não chamam “AES
puro”: usam um modo ou uma API AEAD.

AES-128 e AES-256 são escolhas amplamente usadas; requisitos regulatórios podem
definir uma delas. Tamanho maior não compensa nonce repetido, chave exposta,
modo inadequado ou endpoint comprometido. Use implementação acelerada da
biblioteca, nunca tabelas artesanais.

## Prática

Liste tudo que ainda precisa ser definido depois da frase “usaremos AES-256”.
