# 23 — Privacidade e anonimato: fundamentos e limites

Este módulo inicia uma trilha de três partes sobre privacidade digital,
anonimato e investigação defensiva. Ele ensina a modelar quem observa cada
trecho de uma comunicação, quais metadados continuam expostos e por que VPN,
Tor, proxy ou janela privativa não tornam alguém invisível.

Não é um manual para fugir de investigação. Técnicas associadas a agentes de
ameaça aparecem apenas como modelos conceituais e são ligadas aos rastros que
interessam à defesa. Não há instruções para apagar logs, falsificar identidade,
fraudar serviços ou ocultar crimes.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Estudantes de redes, segurança, desenvolvimento e privacidade. |
| Pré-requisitos | Módulos 14–18 de redes e 19–22 de criptografia. |
| Tempo estimado | 140–220 horas. |
| Ambiente | Fixtures sintéticas e observação do próprio navegador/rede; nenhuma coleta sobre terceiros. |
| Evidência final | Modelo de ameaça, matriz de observadores, plano de privacidade e relatório de limitações. |
| Critério de conclusão | Explicar o que cada intermediário vê, escolher controles proporcionais e declarar riscos residuais. |

## Comece aqui

- [Curso completo](privacidade-anonimato-fundamentos/README.md)
- [Laboratórios](privacidade-anonimato-fundamentos/laboratorios/README.md)
- [Ferramentas offline](privacidade-anonimato-fundamentos/exemplos/README.md)
- [Consulta rápida](privacidade-anonimato-fundamentos/CHEATSHEET.md)

## Progressão

1. **Módulo 23:** identidade, metadados, rota, observadores, VPN, Tor,
   fingerprinting, vazamentos e modelagem de ameaça.
2. **[Módulo 24](../24-Lateral-Movement/README.md):** VPN própria em VPS,
   WireGuard, firewall, DNS, IPv4/IPv6, clientes, operação e recuperação.
3. **[Módulo 25](../25-Cursos/README.md):** telemetria, correlação, atribuição
   defensiva, evidência, privacidade e resposta a incidentes.

## Princípio central

Anonimato não é um botão. Um túnel muda o ponto de confiança e o endereço IP
visível ao destino, mas contas, pagamentos, cookies, características do
dispositivo, horários, volume de tráfego e comportamento podem religar
atividades. O objetivo profissional é reduzir exposição de modo verificável,
sem prometer anonimato absoluto.

## Vídeos em português

Os vídeos complementam o material autocontido; compare afirmações comerciais
com as fontes oficiais registradas no curso.

1. [Privacidade na Internet: roteamento aleatorizado com Tor](https://www.youtube.com/watch?v=J2jzgYwMDhk) — **NIC.br**.
2. [Como ficar anônimo na internet? VPN vs Proxy vs Tor](https://www.youtube.com/watch?v=YH_zrhtDJOQ) — **Gabriel Pato**.
3. [VPN: você pode ser rastreado?](https://www.youtube.com/watch?v=1Ppxzy1v37w) — **CanalJMS**.
4. [DNS — Sistema de Nomes de Domínio](https://www.youtube.com/watch?v=xlAgp6PHKsY) — **NIC.br**.
5. [IP, DNS, DHCP e roteamento](https://www.youtube.com/watch?v=z2vnQcb8nGI) — **Cyber Security Br**.
