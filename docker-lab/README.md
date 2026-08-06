# Docker Lab - RedTeam Essentials

> Lab pentest local que sobe em segundos com `docker compose up -d`. Apenas para uso em maquina pessoal isolada.

## Pre-requisitos

- Docker Engine 24+ (ou Docker Desktop 4.20+).
- Docker Compose plugin (`docker compose version` >= v2).
- 4 GB RAM livres e 5-8 GB de disco para imagens.

> **Atencao.** Os containers expoem apenas em `127.0.0.1`. Nunca rode em VPS publica - sao alvos intencionalmente vulneraveis.

## Servicos

| Servico | Imagem | URL local | Foco |
|---------|--------|-----------|------|
| DVWA | `vulnerables/web-dvwa` | http://127.0.0.1:8081 | OWASP Top 10 classico (PHP) |
| Juice Shop | `bkimminich/juice-shop` | http://127.0.0.1:8082 | OWASP Juice Shop (Node) |
| bWAPP | `raesene/bwapp` | http://127.0.0.1:8083 | 100+ bugs web |
| WebGoat | `webgoat/webgoat` | http://127.0.0.1:8084 | Java vulneravel |
| Vulnerable WordPress | `wpscanteam/vulnerablewordpress` | http://127.0.0.1:8085 | CMS + plugins ruins |
| NodeGoat | `owasp/nodegoat` | http://127.0.0.1:8086 | Node + Express insecure |
| VAmPI | `erev0s/vampi` | http://127.0.0.1:8087 | OWASP API Top 10 |
| Attacker (Kali) | build `Dockerfile.kali-pentest` (`rte/kali-pentest`) | --- | Estacao atacante (nmap, sqlmap, NetExec, Impacket) |

Rede interna: `172.28.0.0/24`. Da estacao atacante voce alcanca os alvos por IP fixo:

- `dvwa` -> 172.28.0.10
- `juiceshop` -> 172.28.0.11
- ...

## Comandos uteis

```bash
# Subir tudo (build da imagem Kali custom na primeira vez)
cd docker-lab && docker compose up -d --build

# Status
docker compose ps

# Entrar no atacante
docker exec -it rte-attacker bash

# Labs guiados: ../07-Web-AppSec/labs/

# Logs de um servico
docker compose logs -f juiceshop

# Reset total (apaga volumes)
docker compose down -v

# Atualizar imagens
docker compose pull && docker compose up -d
```

## Exemplo de sessao

```bash
docker exec -it rte-attacker bash
# Dentro do container:
nmap -sV -p- 172.28.0.0/24
nikto -h http://172.28.0.10
sqlmap -u "http://172.28.0.10/vulnerabilities/sqli/?id=1" --cookie='security=low; PHPSESSID=...'
curl http://172.28.0.11/rest/admin/application-version
```

## Personalizacao

- Adicione mais servicos editando `docker-compose.yml`.
- Pasta `shared/` e montada no `attacker` em `/shared` - use para trocar wordlists/scripts.
- Para um setup AD-like, considere [Game of Active Directory (GOAD)](https://github.com/Orange-Cyberdefense/GOAD).

## Tear-down + limpeza

Apos engagement de treino:

```bash
docker compose down -v
docker image prune -af
docker network prune -f
```

## Etico

Este lab e **propositadamente vulneravel**. Se algum container sair desta maquina (publicacao acidental, port-forward, expose) voce expoe a internet a alvos faceis. Sempre use `127.0.0.1` no mapping e considere firewall local extra (`ufw default deny incoming`).
