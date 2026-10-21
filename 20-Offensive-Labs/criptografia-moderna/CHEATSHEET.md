# Cheatsheet — primitivas modernas

| Caso | Padrão inicial | Regra crítica |
|---|---|---|
| cifrar registro | AES-GCM ou ChaCha20-Poly1305 | nonce único por chave |
| acordo moderno | X25519 + HKDF | autenticar transcript/peer |
| assinatura simples | Ed25519 | contexto e bytes canônicos |
| RSA cifragem | RSA-OAEP | mensagem curta/chave de dados |
| RSA assinatura | RSA-PSS | parâmetros fixos |
| dados grandes | envelope encryption | DEK por objeto/lote |

Nunca use ECB, chave como nonce, nonce derivado só de timestamp, RSA “raw”,
ChaCha20 sem autenticação ou algoritmo selecionado diretamente pelo payload.
