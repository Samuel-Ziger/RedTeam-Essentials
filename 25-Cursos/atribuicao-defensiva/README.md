# Rastreabilidade e atribuição defensiva

Curso avançado de Blue Team para reconstruir eventos com telemetria autorizada.
O objetivo não é “descobrir uma pessoa pelo IP”, mas produzir conclusões
proporcionais à evidência e úteis para contenção, recuperação e melhoria.

## Resultado de aprendizagem

- planejar telemetria antes do incidente;
- normalizar relógios, IDs, endereços, portas e proveniência;
- correlacionar endpoint, identidade, rede, DNS, aplicação e nuvem;
- interpretar NAT, CGNAT, VPN, proxy e Tor sem conclusões simplistas;
- detectar proxy não autorizado e tentativa de remoção de indicadores;
- preservar integridade e cadeia de custódia;
- trabalhar com hipóteses concorrentes, confiança e falsos positivos;
- respeitar minimização, LGPD, contratos e processo jurídico.

## Rota

| # | Capítulo |
|---:|---|
| 00 | [Autoridade, ética e objetivo](00-autoridade-etica.md) |
| 01 | [Atribuição como inferência](01-atribuicao-inferencia.md) |
| 02 | [Arquitetura de telemetria](02-arquitetura-telemetria.md) |
| 03 | [Tempo, fuso e clock skew](03-tempo-clock-skew.md) |
| 04 | [Endpoint e processo](04-endpoint-processo.md) |
| 05 | [Identidade e autenticação](05-identidade-autenticacao.md) |
| 06 | [Fluxos, firewall e roteamento](06-fluxos-firewall.md) |
| 07 | [DNS, proxy e TLS](07-dns-proxy-tls.md) |
| 08 | [NAT, CGNAT e registros de tradução](08-nat-cgnat.md) |
| 09 | [VPN, Tor e infraestrutura intermediária](09-vpn-tor.md) |
| 10 | [Web, API e sessão](10-web-api-sessao.md) |
| 11 | [Nuvem e SaaS](11-nuvem-saas.md) |
| 12 | [E-mail e colaboração](12-email-colaboracao.md) |
| 13 | [Correlação e grafos](13-correlacao-grafos.md) |
| 14 | [Detecção de proxy e remoção de indicadores](14-deteccao-evasao.md) |
| 15 | [Lacunas, integridade e anti-tamper](15-lacunas-integridade.md) |
| 16 | [Preservação e cadeia de custódia](16-cadeia-custodia.md) |
| 17 | [Hipóteses, confiança e falsos positivos](17-hipoteses-confianca.md) |
| 18 | [Privacidade, jurídico e comunicação](18-privacidade-juridico.md) |
| 19 | [Projeto final: investigação sintética](19-projeto-final.md) |

## Prática

```bash
python3 exemplos/telemetry_correlator.py fixtures/eventos-sinteticos.json
python3 exemplos/evidence_manifest.py fixtures/evidencias-demo
```

O primeiro comando correlaciona eventos sintéticos. O segundo cria um manifesto
em memória e imprime hashes; não altera as evidências.

## Materiais

- [Laboratórios](laboratorios/README.md)
- [Ferramentas](exemplos/README.md)
- [Glossário](GLOSSARIO.md)
- [Cheatsheet](CHEATSHEET.md)
- [Respostas](RESPOSTAS.md)
- [Referências](REFERENCIAS.md)

