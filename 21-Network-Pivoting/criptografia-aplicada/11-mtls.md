# 11 — mTLS e identidade de serviço

mTLS autentica ambos os lados por certificados, mas autorização ainda precisa
mapear identidade a ação e recurso. Defina namespace, emissor, SAN/EKU, duração,
rotação e comportamento de revogação. Não autorize apenas porque a cadeia fecha.

Proxies e service meshes podem terminar mTLS; a aplicação precisa saber qual
componente atesta a identidade e impedir headers forjados fora dessa fronteira.
Logs registram fingerprint/key ID e decisão, não chave ou certificado completo.

## Prática

Modele um serviço A chamando B: emissão, validação, policy, rotação e resposta a
certificado de A comprometido.
