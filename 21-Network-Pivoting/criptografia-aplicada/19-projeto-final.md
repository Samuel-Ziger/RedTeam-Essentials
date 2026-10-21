# 19 — Projeto final: serviço interno protegido

Projete um serviço `api.example.test` apenas em loopback. Crie raiz e emissora
de laboratório, emita certificado SAN correto, configure TLS, audite o leaf e
documente renovação. Opcionalmente exija certificado cliente sintético.

## Entregáveis

- diagrama de trust boundaries e cadeia;
- perfil de leaf com KU/EKU/SAN e validade justificados;
- configuração mínima/máxima de TLS e matriz de clientes;
- alerta de expiração e runbooks de rotação/comprometimento;
- testes de nome errado, expiração simulada, CA errada e chave incorreta;
- cleanup que remove chaves e não instala a raiz globalmente.

O projeto não precisa expor porta externa nem consultar uma CA pública.
