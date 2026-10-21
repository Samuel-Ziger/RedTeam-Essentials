# Respostas orientativas

- AEAD autentica plaintext cifrado e AAD; não esconde tamanho ou AAD.
- GCM e ChaCha20-Poly1305 exigem nonce não repetido para a mesma chave.
- Segredo X25519 passa por KDF e a chave pública precisa ser autenticada.
- Assinatura não cifra, não garante frescor e não identifica pessoa sozinha.
- RSA-OAEP cifra material curto; RSA-PSS assina.
- Rotação de KEK pode reencapsular DEKs; rotação de DEK exige recifrar dados.
- Agilidade é uma capacidade controlada, não negociação irrestrita.
