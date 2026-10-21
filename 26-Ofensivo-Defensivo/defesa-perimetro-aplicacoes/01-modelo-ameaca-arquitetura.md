# 01 — Modelo de ameaça e arquitetura

Comece pelo fluxo, não pelo produto. Uma aplicação comum pode atravessar DNS,
CDN, proteção DDoS, WAF, load balancer, proxy, gateway de API, serviço,
cache, fila, banco e provedor de identidade. Cada salto cria uma fronteira de
confiança e pode reescrever IP, host, esquema, caminho ou cabeçalho.

```text
cliente → DNS/CDN/WAF → origem privada → gateway → aplicação → dados
             │                   │              │
             └→ edge logs       └→ access log    └→ audit log
```

## Inventário mínimo

Para cada componente, registre exposição, protocolo, identidade entre saltos,
fonte da configuração, logs, retenção, owner, dependência e procedimento de
falha. Modele os ativos principais: disponibilidade, credenciais, sessões,
dados, integridade de regras e segredos do plano de controle.

## Ameaças úteis

- acesso direto à origem contornando a borda;
- regra ampla que bloqueia cliente legítimo ou regra estreita que não cobre API;
- confiança em `X-Forwarded-For` vindo de fonte não confiável;
- diferença de parsing entre proxy e aplicação;
- abuso de login, cadastro, busca, checkout ou recuperação;
- roubo da conta administrativa do WAF;
- fail-open acidental, log incompleto ou rollout sem rollback.

## Requisitos verificáveis

Troque "ter WAF" por sentenças testáveis: "a origem aceita HTTPS somente dos
endereços/identidades da borda"; "o cabeçalho de IP do cliente é removido e
recriado apenas pelo proxy confiável"; "mudanças de regra exigem revisão e geram
auditoria".

## Exercício Red/Blue

Red desenha três caminhos alternativos que uma configuração incorreta poderia
deixar expostos. Blue define uma observação e um controle preventivo para cada
caminho. Purple elimina caminhos sem evidência ou fora do escopo.
