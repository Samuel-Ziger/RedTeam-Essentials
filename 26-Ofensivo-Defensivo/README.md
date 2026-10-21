# 26 — Purple Team: firewalls, WAF, bots e identidade

Especialização final para projetar e avaliar a borda de aplicações. O curso
une Red Team autorizado e Blue Team: cada controle é modelado, submetido a
testes negativos locais, observado, ajustado e testado novamente.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Desenvolvimento, AppSec, infraestrutura, SOC, Red e Blue Team. |
| Pré-requisitos | HTTP/APIs, Linux/Windows, redes, criptografia e telemetria dos módulos anteriores. |
| Tempo estimado | 220–340 horas, incluindo projeto. |
| Ambiente | Fixtures offline e serviços locais sob autoridade expressa. |
| Evidência final | Matriz de controles, resultados red/blue, telemetria, tuning, rollback e reteste. |
| Critério de conclusão | Ferramentas aprovadas, sete labs, testes automatizados e capstone. |

## O que você aprenderá

- diferenciar firewall L3/L4, proxy, gateway de API, WAF, CDN e proteção DDoS;
- construir políticas default deny, segmentação, egress e proteção da origem;
- operar OWASP CRS, Cloudflare e BunkerWeb com mudança gradual e rollback;
- entender como automação é inferida por taxa, estado, sequência, reputação,
  fingerprints e contexto — nunca por um único indicador;
- validar rate limiting, CAPTCHA/Turnstile, 2FA, WebAuthn/passkeys e recuperação;
- testar controles como Red Team sem tentar burlar serviços de terceiros;
- transformar cada teste em detecção, resposta e regressão como Blue Team.

## Duas perspectivas, uma evidência

| Tema | Red Team autorizado | Blue Team |
|---|---|---|
| Firewall | mapear superfície e provar caminhos permitidos/negados no lab | default deny, segmentação, logs e deriva |
| Origem/CDN | verificar exposição direta e confiança em headers locais | restringir origem, autenticar edge e correlacionar IDs |
| WAF/CRS | construir casos positivos, negativos e de falso positivo | score, exclusão estreita, canário e virtual patch |
| Bots | emular jornadas automatizadas sintéticas e limites de taxa | combinar sinais, responder progressivamente e medir erro |
| CAPTCHA | testar ausência, expiração, replay e binding em fixture | validar no servidor, preservar UX, privacidade e fallback |
| 2FA/passkeys | avaliar enrollment, recovery e revogação em contas de lab | MFA resistente a phishing, alertas e break-glass |
| Incidente | demonstrar impacto mínimo e reproduzível | conter, reverter, recuperar e atualizar a regressão |

O Red Team não recebe um manual para contornar controles de terceiros: recebe
metodologia e código para provar propriedades no próprio ambiente. O Blue Team
não encerra o trabalho ao bloquear: precisa explicar a decisão, tratar falsos
positivos e demonstrar recuperação. Esse encontro é o trabalho Purple.

## Rota

| # | Capítulo |
|---:|---|
| 00 | [Purple Team, autoridade e método](defesa-perimetro-aplicacoes/00-purple-team-autoridade.md) |
| 01 | [Modelo de ameaça e arquitetura](defesa-perimetro-aplicacoes/01-modelo-ameaca-arquitetura.md) |
| 02 | [Firewalls L3/L4 e estado](defesa-perimetro-aplicacoes/02-firewalls-l3-l4.md) |
| 03 | [Política, segmentação e egress](defesa-perimetro-aplicacoes/03-politica-segmentacao-egress.md) |
| 04 | [Firewalls de host e cloud](defesa-perimetro-aplicacoes/04-host-cloud-firewall.md) |
| 05 | [Proxy reverso, CDN e origem](defesa-perimetro-aplicacoes/05-proxy-cdn-origem.md) |
| 06 | [DDoS e disponibilidade](defesa-perimetro-aplicacoes/06-ddos-disponibilidade.md) |
| 07 | [WAF: arquitetura e limites](defesa-perimetro-aplicacoes/07-waf-arquitetura-limites.md) |
| 08 | [HTTP, normalização e parsing](defesa-perimetro-aplicacoes/08-http-normalizacao-parsing.md) |
| 09 | [OWASP CRS, score e tuning](defesa-perimetro-aplicacoes/09-owasp-crs-tuning.md) |
| 10 | [Cloudflare WAF](defesa-perimetro-aplicacoes/10-cloudflare-waf.md) |
| 11 | [Cloudflare: origem, regras e operação](defesa-perimetro-aplicacoes/11-cloudflare-operacao.md) |
| 12 | [BunkerWeb](defesa-perimetro-aplicacoes/12-bunkerweb.md) |
| 13 | [Ameaças automatizadas e bots](defesa-perimetro-aplicacoes/13-ameacas-automatizadas.md) |
| 14 | [Sinais e classificação de automação](defesa-perimetro-aplicacoes/14-deteccao-automacao.md) |
| 15 | [Rate limiting e quotas](defesa-perimetro-aplicacoes/15-rate-limiting.md) |
| 16 | [CAPTCHA, Turnstile e step-up](defesa-perimetro-aplicacoes/16-captcha-turnstile.md) |
| 17 | [2FA, WebAuthn, passkeys e recuperação](defesa-perimetro-aplicacoes/17-mfa-passkeys.md) |
| 18 | [APIs, mobile e service-to-service](defesa-perimetro-aplicacoes/18-api-mobile-servicos.md) |
| 19 | [Observabilidade, tuning e falsos positivos](defesa-perimetro-aplicacoes/19-observabilidade-tuning.md) |
| 20 | [Runbooks e resposta a incidentes](defesa-perimetro-aplicacoes/20-runbooks-resposta.md) |
| 21 | [Projeto final Purple Team](defesa-perimetro-aplicacoes/21-projeto-final.md) |

## Prática local

```bash
python3 rte.py analyze edge-risk 26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/fixtures/requests-sinteticas.json
python3 rte.py analyze edge-policy 26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/fixtures/politica-edge.json
python3 rte.py analyze rate-limit 26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/fixtures/eventos-rate-limit.json
bash 26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/testar-curso.sh
```

As ferramentas não abrem sockets, não consultam serviços externos e não enviam
tráfego. Elas analisam somente dados sintéticos versionados.

## Vídeos em português

Os vídeos complementam o curso; versões e configurações devem ser confirmadas
nas fontes oficiais do produto.

1. [Fundamentos de redes de computadores — curso completo](https://www.youtube.com/watch?v=vqrvOz1zSgY) — **Hardware Redes Brasil**.
2. [Protocolo TCP/IP — curso completo](https://www.youtube.com/watch?v=kP1kktlbUTs) — **Hardware Redes Brasil**.
3. [O que é uma API REST? Entenda API, HTTP e RESTful](https://www.youtube.com/watch?v=9SbUPqKEWcY) — **Mateus Battisti - Hora de Codar**.
4. [Entenda: o que é autenticação de dois fatores?](https://www.youtube.com/watch?v=eTwMEgSFvVg) — **TecMundo**.
5. [Como as passkeys começam a substituir senhas](https://www.youtube.com/watch?v=dglOJZz_5nQ) — **BBC News Brasil**.

## Materiais

- [Curso completo](defesa-perimetro-aplicacoes/README.md)
- [Laboratórios Purple Team](defesa-perimetro-aplicacoes/laboratorios/README.md)
- [Ferramentas offline](defesa-perimetro-aplicacoes/exemplos/README.md)
- [Referências oficiais](defesa-perimetro-aplicacoes/REFERENCIAS.md)
- [Glossário](defesa-perimetro-aplicacoes/GLOSSARIO.md)
- [Cheatsheet](defesa-perimetro-aplicacoes/CHEATSHEET.md)
- [Respostas e rubrica](defesa-perimetro-aplicacoes/RESPOSTAS.md)
