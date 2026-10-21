# Docker Lab — Módulo 30

> Lab pentest local com perfis explícitos. Apenas para uso em maquina pessoal isolada.

## Pre-requisitos

- Docker Engine 24+ (ou Docker Desktop 4.20+).
- Docker Compose plugin (`docker compose version` >= v2).
- 4 GB RAM livres e 5-8 GB de disco para imagens.

> **Atencao.** Somente o gateway HTTP expoe portas, sempre em `127.0.0.1`.
> Nunca rode em VPS publica - sao alvos intencionalmente vulneraveis.

## Servicos

| Servico | Imagem | URL local | Foco |
|---------|--------|-----------|------|
| DVWA | `vulnerables/web-dvwa` | http://127.0.0.1:8081 | OWASP Top 10 classico (PHP) |
| Juice Shop | `bkimminich/juice-shop` | http://127.0.0.1:8082 | OWASP Juice Shop (Node) |
| bWAPP (`extended`/`full`) | `raesene/bwapp` | http://127.0.0.1:8083 | 100+ bugs web |
| WebGoat (`extended`/`full`) | `webgoat/webgoat` | http://127.0.0.1:8084 | Java vulneravel |
| VAmPI (`api`/`full`) | `erev0s/vampi` | http://127.0.0.1:8087 | OWASP API Top 10 |
| Attacker (Kali) | build `Dockerfile.kali-pentest` (`rte/kali-pentest`) | --- | Estacao atacante (nmap, sqlmap, NetExec, Impacket) |

Rede interna: `172.28.0.0/24`. Da estacao atacante voce alcanca os alvos por IP fixo:

- `dvwa` -> 172.28.0.10
- `juiceshop` -> 172.28.0.11
- ...

Os alvos ficam apenas na rede interna, sem publicacao direta e sem rota de
internet. Um gateway Nginx conecta essa rede a uma segunda bridge e entrega as
URLs acima exclusivamente no loopback do host. A estacao atacante tem egress
separado para instalar/atualizar ferramentas, mas os alvos nao compartilham
essa rede.

## Comandos uteis

```bash
# A partir da raiz do repositorio, entrar no lab e subir o perfil basico
cd 30-Web-API-AppSec/docker-lab && docker compose up -d --build

# Se houver erro "pull access denied" para `rte/kali-pentest`, execute antes:
#
# ```bash
# docker compose build attacker
# ```

# Status
docker compose ps

# Diagnosticar Compose, containers e endpoints HTTP
bash lab-doctor.sh

# Entrar no atacante
docker compose exec attacker bash

# Labs guiados: ../acervo/labs/

# Logs de um servico
docker compose logs -f juiceshop

# Encerrar sem apagar volumes
docker compose down

```

### Perfis de serviços

O perfil básico não exige flag. Os demais são declarados no Compose:

```bash
# Web básico: DVWA + Juice Shop + estação atacante
docker compose up -d --build

# API: VAmPI e estação atacante
docker compose --profile api up -d --build

# Alvos web adicionais: bWAPP + WebGoat
docker compose --profile extended up -d --build

# Ambiente completo
docker compose --profile full up -d --build
```

Serviços iniciados explicitamente continuam na mesma rede isolada. Use
`docker compose down` antes de trocar de conjunto para evitar estado antigo.
Acrescente `--volumes` somente quando quiser apagar intencionalmente o estado.

Cada serviço possui healthcheck e limites locais de CPU/memória. WebGoat pode
levar até 90 segundos para iniciar; acompanhe com `docker compose ps --format
json` ou `bash lab-doctor.sh`.

Antes de baixar imagens, é possível validar somente a configuração:

```bash
bash lab-doctor.sh --config-only
```

O diagnóstico retorna código diferente de zero quando uma dependência, serviço
ou endpoint falha, permitindo seu uso em smoke tests locais.

As imagens estão fixadas por digest. Consulte
[`IMAGE-PINS.md`](IMAGE-PINS.md) antes de qualquer atualização.

## Exemplo de sessao

```bash
docker compose exec attacker bash
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
docker compose down

# Reset destrutivo apenas dos volumes deste projeto, quando necessario:
docker compose down --volumes
```

## Etico

Este lab e **propositadamente vulneravel**. Se algum container sair desta maquina (publicacao acidental, port-forward, expose) voce expoe a internet a alvos faceis. Mantenha as publicacoes somente no gateway e em `127.0.0.1`; considere firewall local extra (`ufw default deny incoming`).
