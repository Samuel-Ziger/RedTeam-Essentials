# 11 — Cloudflare: origem, regras e operação

Ativar proxy não encerra o projeto. A operação precisa proteger origem, plano de
controle, certificados, bypasses administrativos e continuidade.

## Origem

- aceite tráfego apenas pelo caminho aprovado;
- mantenha TLS estrito até a origem;
- considere autenticação mútua ou túnel quando compatível;
- não exponha portas alternativas e painéis no mesmo endereço;
- atualize allowlists de forma automatizada e atômica;
- monitore conexão direta e mudança de DNS.

Endereços publicados pelo provedor não autenticam, sozinhos, uma requisição.
Combine rede e criptografia/identidade.

## Plano de controle

Use SSO quando possível, MFA resistente a phishing para administradores,
privilégio mínimo, tokens separados por automação, escopos estreitos,
rotação, logs e contas de emergência controladas. API token não deve aparecer
em repositório, CI log ou screenshot.

## Mudanças

Mantenha uma representação versionada das regras e um inventário de recursos
criados no painel. Exija revisão para `allow`, `skip`, desativação de ruleset,
origem e DNS. Use expiração em exceções de incidente.

## Falha e rollback

Documente o que ocorre se DNS, edge, origem ou integração de identidade falhar.
"Desativar tudo" não é rollback aceitável. Prepare regra anterior, canário,
contatos, decisão de fail-open/fail-closed por rota e página de status.

## Exercício Purple

Red revisa caminhos de acesso e permissões sem tentar contornar o provedor.
Blue demonstra auditoria de uma mudança e alerta de acesso direto. Purple faz
tabletop de perda de uma credencial administrativa e mede tempo de revogação.
