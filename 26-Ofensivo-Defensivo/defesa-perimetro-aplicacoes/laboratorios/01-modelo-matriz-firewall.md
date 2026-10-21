# Laboratório 01 — Modelo de ameaça e matriz de firewall

## Objetivo

Transformar um diagrama de edge/origem/API/dados em política verificável.

## Red

1. Copie apenas a estrutura de `fixtures/politica-edge.json` para sua entrega.
2. Liste caminhos público, administrativo, direto à origem e de saída.
3. Para cada caminho proibido, escreva um teste negativo abstrato com teto zero
   de tráfego externo: o teste será revisão da fixture, não conexão.

## Blue

1. Defina default deny, IPv4/IPv6, estado, logs e owner.
2. Especifique autenticação edge→origem e do plano administrativo.
3. Execute `control_plane_audit.py` e preserve o JSON de resultado.

## Purple

Compare hipótese e controle. Adicione caso positivo para cada regra negativa,
procedimento de rollback e critério de expiração. Falha se existir `any/any`,
origem direta, IPv6 implícito ou administração sem MFA resistente a phishing.
