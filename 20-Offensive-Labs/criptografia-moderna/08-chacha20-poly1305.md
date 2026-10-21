# 08 — ChaCha20-Poly1305

ChaCha20 gera fluxo com adições, XOR e rotações; Poly1305 autentica a mensagem
com chave de uso único derivada por nonce. A construção padronizada usa chave de
256 bits e nonce de 96 bits, com o mesmo requisito crítico de não repetição por
chave.

É comum em protocolos modernos e eficiente sem instruções AES. Não use ChaCha20
sozinho nem Poly1305 diretamente sem compreender a derivação. A API AEAD mantém
o contrato menor e reduz oportunidades de composição errada.

## Verificação

Quando desempenho pode favorecer ChaCha20-Poly1305 e qual requisito permanece
idêntico ao AES-GCM?
