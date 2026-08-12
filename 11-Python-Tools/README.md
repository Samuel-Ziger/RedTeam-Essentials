# 11 - Python Tools

> Ferramentas em Python 3.10+ (stdlib apenas) para automacao didatica de tarefas comuns de Red Team / pentest.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes que dominam Python básico e operação segura do lab. |
| Pré-requisitos | Módulo [00](../00-Fundamentos/README.md), Python 3.10+ e JSON. |
| Tempo estimado | 4 horas de leitura/código e 4 horas de experimentos offline/locais. |
| Ambiente | Fixtures offline, localhost ou alvo explicitamente autorizado. |
| Evidência final | Teste automatizado e JSON sanitizado para uma ferramenta escolhida. |
| Critério de conclusão | Testes e Ruff verdes, caso de erro coberto e saída explicada. |

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

Os parsers, validadores, exportação e fluxos sem rede também possuem testes em
`tests/python/`. Execute localmente com:

```bash
python -m pip install pytest ruff
pytest
ruff check 11-Python-Tools lib/python scripts tests/python
```

## Como contribuir

Adicione um novo script com header docstring no formato dos existentes, importe `rte_common`, e escreva pelo menos um exemplo de uso no proprio docstring. Vale a pena rodar `ruff check 11-Python-Tools/` antes de abrir PR.

## Resultado esperado e cleanup

Uma execução deve produzir saída determinística quando usa fixture, erro claro
para entrada inválida e JSON sem credenciais. Use servidores em localhost para
testes de rede e remova `output/` ao terminar. Nunca use `RTE_SKIP_AUTH=1` como
atalho contra sistemas externos.

### Autoavaliação

- [ ] Consigo explicar validação, timeout e formato de saída da ferramenta.
- [ ] Adicionei um teste offline de sucesso e um de erro.
- [ ] Não incluí tokens, hashes reais ou endereços de terceiros na fixture.
- [ ] `pytest`, Ruff e `compileall` passaram.
- [ ] Removi processos locais e saídas temporárias.
