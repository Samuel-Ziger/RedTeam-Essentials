# 05 — NTP, PKI e identidade de infraestrutura

Tempo correto sustenta logs, certificados, Kerberos, tokens e investigação.
Defina fontes confiáveis, hierarquia, autenticação quando suportada, monitore
offset/jitter/stratum e não aponte todos os dispositivos diretamente à Internet.

PKI emite identidade para dispositivos, usuários e serviços. O ciclo inclui
key generation, CSR, emissão, armazenamento, distribuição de trust, renovação,
revogação e destruição. Chave privada deve permanecer no endpoint/HSM quando
possível; inventarie prazo e automatize antes da expiração.

Identidade de infraestrutura inclui certificado, conta de serviço, device ID e
papel administrativo. Evite contas compartilhadas e segredos iguais em todos os
equipamentos. Bootstrap inicial é uma trust boundary e precisa de prova de posse.

## Exercício

Desenhe dependência circular: DNS precisa de tempo? NTP precisa de DNS? PKI
precisa de ambos? Defina endereços/fontes de bootstrap para quebrar o ciclo.
