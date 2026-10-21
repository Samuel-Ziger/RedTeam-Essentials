# 09 — Handshake TLS 1.3

ClientHello oferece versões, grupos, key share, algoritmos de assinatura, SNI e
ALPN. ServerHello seleciona e estabelece segredo; mensagens cifradas trazem
certificado, verificação e Finished. O transcript entra nas derivações e impede
alteração silenciosa da negociação.

Chaves de tráfego são derivadas por direção e fase. Resumption PSK e tickets
possuem ciclo de vida próprio. O handshake autentica servidor por padrão; cliente
por certificado requer mTLS e política de identidade.

## Verificação

Marque no fluxo onde surgem autenticação, acordo de chave, confirmação do
transcript e chaves de aplicação.
