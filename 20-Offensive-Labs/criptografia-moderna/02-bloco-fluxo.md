# 02 — Cifras de bloco e de fluxo

Cifra de bloco transforma blocos fixos sob uma chave; um modo define como tratar
mensagens maiores. Cifra de fluxo gera um fluxo combinado com plaintext; repetir
o fluxo expõe relações entre mensagens. Em ambos os casos, confidencialidade sem
autenticação permite alterações não detectadas.

Não escolha entre “bloco ou fluxo” isoladamente: escolha uma construção AEAD
suportada no ambiente. AES-GCM aproveita aceleração AES; ChaCha20-Poly1305 é uma
alternativa forte em plataformas sem ela. Perfil, interoperabilidade e gestão
de nonce importam mais que benchmarks sem contexto.

## Verificação

Por que XOR de dois ciphertexts produzidos pelo mesmo fluxo é perigoso?
