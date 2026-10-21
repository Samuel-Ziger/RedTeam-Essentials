# Referências comentadas

Consulte a versão vigente antes de operar um fornecedor. O curso é
autocontido; estas fontes servem para confirmar sintaxe, disponibilidade por
plano e mudanças posteriores.

## Fundamentos e WAF

- [NIST SP 800-41 Rev. 1](https://csrc.nist.gov/pubs/sp/800/41/r1/final) — política, seleção, configuração, teste, implantação e gestão de firewalls.
- [OWASP ModSecurity](https://owasp.org/projects/modsecurity) — engine WAF aberto e sua relação com o CRS.
- [OWASP Core Rule Set](https://coreruleset.org/docs/) — anomaly scoring, paranoia levels, tuning e exclusões.
- [OWASP Automated Threats](https://wiki.owasp.org/images/a/a2/Automated-threats.pdf) — taxonomia histórica de ameaças automatizadas.
- [OWASP API Security](https://owasp.org/www-project-api-security/) — riscos e materiais para APIs.

## Cloudflare

- [WAF](https://developers.cloudflare.com/waf/) — managed rules, custom rules, rate limiting e analytics.
- [Conceitos do WAF](https://developers.cloudflare.com/waf/concepts/) — rulesets, detecções e componentes.
- [Custom rules](https://developers.cloudflare.com/waf/custom-rules/) — expressões, ações e ordem.
- [Custom rules com Bot Management](https://developers.cloudflare.com/bots/additional-configurations/custom-rules/) — composição de score e contexto.
- [Turnstile](https://developers.cloudflare.com/turnstile/) — visão geral e integração.
- [Validação server-side](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/) — Siteverify, expiração e uso único.
- [Chaves de teste do Turnstile](https://developers.cloudflare.com/turnstile/troubleshooting/testing/) — testes sem segredos de produção.

## BunkerWeb

- [Quickstart](https://docs.bunkerweb.io/latest/quickstart-guide/) — modelos de implantação e requisitos atuais.
- [Security tuning](https://docs.bunkerweb.io/security-tuning/) — configurações e modos antibot.
- [Web UI](https://docs.bunkerweb.io/latest/web-ui/) — arquitetura, redes, TOTP, persistência e trusted proxies.
- [Repositório BunkerWeb](https://github.com/bunkerity/bunkerweb) — releases, issues e código-fonte.

## Identidade

- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) — autenticadores, lifecycle e resistência a phishing.
- [CISA: phishing-resistant MFA](https://www.cisa.gov/sites/default/files/2023-01/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf) — orientação sobre FIDO/WebAuthn.
- [WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/) — especificação do protocolo web.

## Comunidade e aprofundamento

- [Cloudflare Community](https://community.cloudflare.com/) — discussões de operação; confirme respostas na documentação oficial.
- [OWASP Community](https://owasp.org/community/) — capítulos, Slack e projetos.
- [BunkerWeb discussions](https://github.com/bunkerity/bunkerweb/discussions) — perguntas da comunidade e experiências; não substitui o manual.
- [Blog do OWASP CRS](https://coreruleset.org/blog/) — mudanças, releases e práticas de tuning.
