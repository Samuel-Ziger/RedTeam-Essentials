# 13 — Fundamentos de VPN

VPN cria conectividade lógica protegida sobre rede não confiável. Propriedades
podem incluir autenticação de peers/usuários, confidencialidade, integridade,
anti-replay e separação de rotas. Verifique quais realmente são fornecidas.

Modelos: site-to-site, acesso remoto, host-to-host e overlay entre workloads.
Full tunnel envia todo tráfego do cliente; split tunnel envia apenas prefixos
selecionados. Full aumenta controle/custo/latência; split reduz backhaul, mas cria
duas fronteiras simultâneas. Escolha por risco e requisitos.

Autenticação pode usar PSK, certificados ou identidade federada. Certificados
escalam melhor, mas exigem emissão, armazenamento, revogação e renovação.

## O que VPN não faz

Não torna endpoint confiável, não corrige autorização da aplicação, não impede
phishing e não garante anonimato. Aplique menor privilégio depois do túnel.
