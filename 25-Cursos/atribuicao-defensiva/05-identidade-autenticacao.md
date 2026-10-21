# 05 — Identidade e autenticação

Logs de identidade mostram autenticação, emissão de token, MFA, risco, sessão,
aplicativo e mudanças de privilégio. Eles são centrais porque IP intermediado
não remove o vínculo explícito de conta.

## Perguntas

- a autenticação foi interativa, serviço ou refresh token?
- qual método MFA e qual dispositivo participaram?
- o token foi emitido antes do evento e revogado depois?
- houve mudança de senha, fator, regra ou papel?
- conta e dispositivo eram gerenciados?
- a sessão poderia ter sido roubada?

## “Viagem impossível”

Geolocalização de IP é aproximada. VPN, rede móvel, CGNAT e egress corporativo
geram saltos. Combine distância/tempo com ASN, device ID, sessão, MFA e padrão
histórico; não suspenda uma pessoa apenas pelo mapa.

## Contas de serviço

Automação precisa owner, workload, escopo e rotação. Uma conta compartilhada
destrói responsabilização. Prefira identidade de workload e credencial curta.

## Contenção

Revogar sessão/token, exigir reautenticação, desabilitar temporariamente e
remover privilégio são ações diferentes. Escolha a menor suficiente e preserve
evidência.

## Prática

Modele três explicações para login de novo ASN: viagem, VPN corporativa e token
roubado. Defina dados que diferenciam cada uma.

