# 16 — Acesso remoto e site-to-site

Site-to-site conecta prefixos e costuma autenticar gateways. Acesso remoto
autentica pessoa/dispositivo e precisa de postura, MFA, expiração, autorização e
logs. Não dê a todo usuário a mesma rota/política.

## Plano de acesso remoto

- identidade federada e MFA resistente a phishing quando possível;
- certificado/registro do dispositivo e postura proporcional;
- pool sem overlap com LANs residenciais comuns;
- grupos -> recursos/portas, deny por padrão;
- DNS interno e comportamento de split DNS definidos;
- expiração de sessão, revogação e resposta a perda;
- logs de autenticação e decisão, com privacidade.

Em site-to-site, evite domínios de criptografia excessivos, prefixos sobrepostos
e default acidental. Monitore ambas as direções e capacidade durante rekey/falha.

## Zero trust

Acesso por aplicação pode reduzir exposição de rede, mas depende de identidade,
proxy/policy engine e disponibilidade. VPN e ZTNA podem coexistir.
