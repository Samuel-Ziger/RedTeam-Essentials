# 11 - Python Tools

> Ferramentas em Python 3.9+ (stdlib apenas) para automacao didatica de tarefas comuns de Red Team / pentest.

## Sumario

| Script | O que faz | Saida |
|--------|-----------|-------|
| [`subdomain_enum.py`](subdomain_enum.py) | Coleta subdominios via crt.sh, HackerTarget e AlienVault OTX. Resolve cada um via `getaddrinfo` em asyncio. | JSON |
| [`port_scanner.py`](port_scanner.py) | Scanner TCP assincrono educacional com banner grab e top100/top1000. | JSON |
| [`jwt_analyzer.py`](jwt_analyzer.py) | Analisador estatico de JWT (alg=none, kid SSRF, exp ausente, bruteforce HS\*). | JSON |
| [`hash_identifier.py`](hash_identifier.py) | Identifica o tipo provavel de um hash e sugere modo do hashcat / formato do john. | stdout |

> **Etico primeiro.** Todos os scripts pedem confirmacao (`AUTORIZADO`) antes de qualquer query ativa. Configure `RTE_SKIP_AUTH=1` para automacao em ambiente fechado.

---

## Instalacao

Nada para instalar. Python 3.9+ e stdlib bastam. Para rodar nos exemplos:

```bash
cd 11-Python-Tools
python3 subdomain_enum.py -d exemplo.com --resolve --sources crtsh,hackertarget
python3 port_scanner.py    -t scanme.nmap.org -p top100 --banner
python3 jwt_analyzer.py    -t "$(cat token.txt)"
python3 hash_identifier.py '$2b$12$abcdefghijklmnopqrstuvabcdefghijklmnopqrstuvwxyz12'
```

---

## Padroes

Todos os scripts:

1. Importam `lib/python/rte_common.py` para logging colorido, validacao e export padronizado.
2. Aceitam `-o ./output` e geram arquivos `JSON` com timestamp UTC.
3. Bloqueiam execucao ate confirmacao etica (`AUTORIZADO`).
4. Sao testados via `python -m py_compile` no CI (`.github/workflows/python.yml`).

## Como contribuir

Adicione um novo script com header docstring no formato dos existentes, importe `rte_common`, e escreva pelo menos um exemplo de uso no proprio docstring. Vale a pena rodar `ruff check 11-Python-Tools/` antes de abrir PR.
