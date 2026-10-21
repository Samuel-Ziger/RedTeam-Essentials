# Privacidade e anonimato — fundamentos, arquitetura e limites

Curso autocontido para compreender privacidade como propriedade de um sistema,
não como produto. Você começa pelas definições, desenha a rota de uma conexão,
identifica observadores e termina com um modelo de ameaça testável.

## Resultado de aprendizagem

Ao concluir, você será capaz de:

- distinguir privacidade, anonimato, pseudonimato, confidencialidade e
  desvinculação;
- explicar o que rede local, ISP, resolvedor DNS, provedor VPN, rede Tor,
  destino, aplicação e provedor de identidade podem observar;
- avaliar VPN, proxy, Tor e modo privativo contra um modelo de ameaça explícito;
- reconhecer correlação por conta, cookies, fingerprint, tempo, volume e
  comportamento;
- executar testes apenas sobre o próprio ambiente e documentar risco residual;
- formular recomendações defensivas sem prometer “anonimato de 100%”.

## Rota

| # | Capítulo |
|---:|---|
| 00 | [Escopo ético e método](00-escopo-etica-metodo.md) |
| 01 | [Vocabulário de privacidade](01-vocabulario-privacidade.md) |
| 02 | [Modelagem de ameaça](02-modelagem-ameaca.md) |
| 03 | [Identificadores e metadados](03-identificadores-metadados.md) |
| 04 | [A rota de uma comunicação](04-rota-comunicacao.md) |
| 05 | [IP, NAT, CGNAT e atribuição](05-ip-nat-cgnat.md) |
| 06 | [DNS e visibilidade](06-dns-visibilidade.md) |
| 07 | [TLS, HTTPS e limites](07-tls-https-limites.md) |
| 08 | [VPN: túnel e troca de confiança](08-vpn-confianca.md) |
| 09 | [Proxies, relays e bastions](09-proxies-relays.md) |
| 10 | [Tor e onion routing](10-tor-onion-routing.md) |
| 11 | [Comportamentos adversários vistos pela defesa](11-adversarios-observaveis.md) |
| 12 | [Estado do navegador e rastreamento](12-navegador-rastreamento.md) |
| 13 | [Fingerprinting e padronização](13-fingerprinting.md) |
| 14 | [Contas, contexto e correlação](14-contas-correlacao.md) |
| 15 | [Dispositivos móveis, Wi-Fi e localização](15-mobile-localizacao.md) |
| 16 | [Vazamentos de DNS, IPv6 e WebRTC](16-vazamentos.md) |
| 17 | [Tempo, volume e adversário global](17-correlacao-trafego.md) |
| 18 | [Projeto final: plano de privacidade](18-projeto-final.md) |

## Como estudar

1. Leia em ordem e mantenha um diário de hipóteses.
2. Faça o exercício “Prática segura” de cada capítulo.
3. Execute os [laboratórios](laboratorios/README.md) com as fixtures locais.
4. Use `python3 exemplos/privacy_model.py fixtures/cenario-pesquisa.json`.
5. Compare sua resposta com [RESPOSTAS.md](RESPOSTAS.md) somente depois.

## Modelo de responsabilidade

O curso protege jornalistas, pesquisadores, administradores, organizações e
usuários comuns por meio de minimização e arquitetura segura. Ele não cobre
anti-forense operacional, destruição de evidência, fraude de identidade,
aquisição clandestina de infraestrutura ou evasão de autoridades. Quando um
conceito ofensivo é citado, a finalidade é reconhecer e responder a sinais.

## Baseline de alto impacto

Antes de procurar uma cadeia complexa de ferramentas, mantenha endpoint e
navegador atualizados, use HTTPS, MFA e gerenciador de senhas, minimize dados e
permissões, separe perfis de trabalho/pessoal, escolha VPN ou Tor somente quando
o modelo de ameaça justificar e teste DNS/IPv6/falha. Essas medidas reduzem
exposição; nenhuma delas autoriza a afirmação “estou 100% anônimo”.

## Materiais

- [Laboratórios](laboratorios/README.md)
- [Código e fixture](exemplos/README.md)
- [Glossário](GLOSSARIO.md)
- [Cheatsheet](CHEATSHEET.md)
- [Respostas orientativas](RESPOSTAS.md)
- [Referências](REFERENCIAS.md)
