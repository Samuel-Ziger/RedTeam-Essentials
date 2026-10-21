# 18 — Projeto final: envelope seguro

Implemente um envelope de arquivo pequeno com AES-256-GCM, versão 1, key ID,
nonce aleatório, AAD canônica e limites. A chave entra pela API ou arquivo
protegido do laboratório e nunca integra o envelope.

## Critérios

- round trip de bytes vazios, Unicode e limite máximo;
- nonce novo por cifragem e chave exatamente de 32 bytes;
- alteração de versão, key ID, AAD, nonce, tag ou ciphertext é rejeitada;
- parser rejeita campos extras, ausentes, duplicados e Base64 inválido;
- erro externo único e nenhuma escrita parcial na falha;
- documento de rotação e compatibilidade.

Compare sua solução com `secure_envelope.py`; explique diferenças antes de
reaproveitar qualquer parte.
