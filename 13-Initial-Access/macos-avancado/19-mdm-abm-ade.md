# 19 — MDM, Apple Business Manager e ADE

ABM registra propriedade organizacional, atribui dispositivos ao serviço de
gerenciamento e distribui apps/licenças. ADE integra enrollment ao Setup
Assistant. MDM envia comandos/perfis e recebe status conforme protocolo.

## Ciclo de vida

compra→atribuição→enrollment→bootstrap→configuração→compliance→update→
suporte→offboarding→erase/liberação. Cada transição precisa owner e evidência.

Supervisão, propriedade e tipo de enrollment afetam controles e privacidade.
BYOD exige minimização diferente de dispositivo corporativo.

O lab modela objetos e estados em JSON. APNs, TLS, DNS, portas e enrollment real
ficam para redes. Não associe serial real a fixtures.

## Prática

Modele cinco Macs sintéticos em estados distintos, defina transições válidas e
produza fila de remediação sem chamar um MDM.
