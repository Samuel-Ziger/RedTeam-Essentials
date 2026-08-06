# Enumeracao Web Avancada

> Diretorios, virtual hosts, parametros HTTP e zone transfer DNS — fluxo operacional para labs e engagements autorizados.
> Complementa [recon-web-pratico.md](recon-web-pratico.md) com comandos mais densos (gobuster/feroxbuster, wfuzz, dig axfr).

**Credito:** adaptado (MIT) do material HexSec / Leonardo Tamiano — reescrito em portugues, sem links de video.

---

## Etica e escopo

- Use **somente** alvos com autorizacao escrita ou o [`docker-lab`](../docker-lab/README.md) em `127.0.0.1`.
- Zone transfer (`AXFR`) e fuzz agressivo geram ruido e podem violar politicas — trate como tecnica de lab/escopo explicito.
- Rate-limit (`-t`, delay) para nao derrubar o alvo; documente evidencias minimas no [REPORT-TEMPLATE](../REPORT-TEMPLATE.md).

---

## Pre-requisitos

```bash
# Wordlists (apos linux_postinstall.sh)
export SECLISTS=~/Pentest/Wordlists/SecLists
export WL_WEB=$SECLISTS/Discovery/Web-Content
export WL_DNS=$SECLISTS/Discovery/DNS
export WL_PARAM=$SECLISTS/Discovery/Web-Content/burp-parameter-names.txt

# Lab local
cd docker-lab && docker compose up -d --build
# Exemplos de alvos: DVWA :8081, Juice Shop :8082, WebGoat :8084
```

Ferramentas tipicas: `gobuster`, `feroxbuster`, `ffuf`, `wfuzz`, `dig`. Instalacao via [`04-Automation/linux_postinstall.sh`](../04-Automation/linux_postinstall.sh) + SecLists.

---

## 1. Enumeracao de diretorios e arquivos

### 1.1 gobuster dir

```bash
# Baseline — raft medium + extensoes PHP (lab DVWA)
gobuster dir \
  -u http://127.0.0.1:8081/ \
  -w $WL_WEB/raft-medium-directories.txt \
  -x php,txt,bak,old \
  -t 40 \
  -o gobuster_dvwa.txt

# Excluir respostas por tamanho (ruido 403/pagina custom)
# 1) Pegue o length de uma resposta "vazia" com curl -I / -w
# 2) Filtre com --exclude-length
gobuster dir \
  -u http://127.0.0.1:8081/ \
  -w $WL_WEB/common.txt \
  -x php \
  --exclude-length 150,151 \
  -b 404,403 \
  -o gobuster_filtered.txt
```

Notas:

- `-x php,txt` testa `FUZZ` e `FUZZ.php` / `FUZZ.txt`.
- `-b` (blacklist status) e `--exclude-length` reduzem falso positivo quando o servidor devolve sempre 200.
- Em engagement real, ajuste wordlist (raft-large so quando ja houver sinal).

### 1.2 feroxbuster (recursivo)

```bash
feroxbuster \
  -u http://127.0.0.1:8081/ \
  -w $WL_WEB/raft-medium-directories.txt \
  -x php \
  -t 30 \
  --extract-links \
  -o ferox_dvwa.txt

# Filtrar por status / tamanho
feroxbuster -u http://127.0.0.1:8081/ -w $WL_WEB/common.txt \
  --dont-filter -C 404,403 --filter-size 1234
```

Use ferox quando quiser recursao automatica e extracao de links; gobuster quando quiser corridas simples e previsiveis.

### 1.3 ffuf (alternativa)

```bash
ffuf -u http://127.0.0.1:8081/FUZZ -w $WL_WEB/raft-medium-words.txt \
  -e .php,.bak,.txt -mc all -fc 404 -t 50 -o ffuf_dirs.json -of json
```

---

## 2. Virtual hosts (mesmo IP, Host diferente)

Apps e labs frequentemente servem varios hostnames no mesmo socket.

```bash
# gobuster vhost — append do dominio base
gobuster vhost \
  -u http://127.0.0.1:8082/ \
  --domain juice.lab \
  --append-domain \
  -w $WL_DNS/subdomains-top1million-5000.txt \
  -t 40 \
  -o vhosts_gobuster.txt

# Sem --append-domain: a wordlist ja precisa conter FQDNs completos
# Com --append-domain: wordlist = "admin", "dev" -> Host: admin.juice.lab
```

Com ffuf (mesmo conceito):

```bash
# Calibre o tamanho da resposta default
ffuf -u http://127.0.0.1:8082/ \
  -H "Host: FUZZ.juice.lab" \
  -w $WL_DNS/subdomains-top1million-5000.txt \
  -fs 12345
```

No `docker-lab`, vhosts reais dependem do mapeamento `/etc/hosts` e da config do container — use para treinar sintaxe; em engajamento, calibre `-fs` / `--exclude-length` contra a pagina default.

---

## 3. Enumeracao de parametros HTTP

### 3.1 GET com ffuf (hide by size)

```bash
# Baseline: tamanho da resposta sem parametro util
curl -s -o /dev/null -w '%{size_download}\n' \
  'http://127.0.0.1:8081/vulnerabilities/sqli/?id=1&Submit=Submit'

ffuf -u 'http://127.0.0.1:8081/vulnerabilities/sqli/?FUZZ=1&Submit=Submit' \
  -w $WL_PARAM \
  -fs 0 \
  -mc all \
  -t 30
# Troque -fs 0 pelo size "normal" observado; hits mudam o body
```

### 3.2 POST com wfuzz

```bash
wfuzz -c \
  -z file,$WL_PARAM \
  -d 'FUZZ=test&Submit=Submit' \
  --hh 1234 \
  http://127.0.0.1:8081/vulnerabilities/sqli/
```

- `--hh` / `-fs`: esconde respostas com aquele **tamanho** (hide by size).
- `--hc` / `-fc`: esconde por status code.
- Comece com wordlist curta (`burp-parameter-names.txt`); amplie se houver indicios.

### 3.3 POST com ffuf

```bash
ffuf -u http://127.0.0.1:8081/vulnerabilities/sqli/ \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'FUZZ=1&Submit=Submit' \
  -w $WL_PARAM \
  -fs 1234
```

API (VAmPI `:8087`): `ffuf -u http://127.0.0.1:8087/FUZZ -w $WL_WEB/api/objects.txt -mc all -fc 404`.

---

## 4. DNS zone transfer (AXFR) — somente lab/autorizado

Uma zona DNS mal configurada pode permitir que um cliente peca a **transferencia completa** da zona (`AXFR`) a um nameserver autoritativo. Em producao isso e falha grave de configuracao; em prova/lab, e check classico.

```bash
# 1) Ache NS do dominio (lab ou escopo)
dig NS lab.local +short

# 2) Tente AXFR contra o nameserver autorizado do laboratorio
dig axfr @ns1.lab.local lab.local

# Variante explicita
dig axfr @192.0.2.53 exemplo.lab
```

**Regras deste repo:**

- Nao rode `dig axfr` contra dominios de terceiros, ISPs ou clientes sem clausula clara no ROE.
- Sucesso tipico em lab: lista de registros A/AAAA/MX/TXT — documente o NS e um trecho; nao cole a zona inteira se for enorme.
- Falha comum: `Transfer failed` — nameserver corretamente restrito.

---

## 5. Checklist operacional

- [ ] Subir / confirmar alvo (`docker-lab` ou URL do escopo)
- [ ] Definir `$SECLISTS` (via `linux_postinstall`)
- [ ] Directory bust (gobuster/ferox/ffuf) com `-x` adequado a stack
- [ ] Aplicar `--exclude-length` / `-fs` apos calibrar baseline
- [ ] Vhost enum com `--append-domain` ou header `Host`
- [ ] Param fuzz GET e POST (hide by size)
- [ ] (Se DNS no escopo) listar NS e testar AXFR **so se autorizado**
- [ ] Salvar outputs em pasta do engagement; gerar INDEX com `organize_logs`
- [ ] Evidencias curtas no [REPORT-TEMPLATE](../REPORT-TEMPLATE.md)

---

## 6. Lab map (docker-lab)

| Alvo | URL | Uso neste guia |
|------|-----|----------------|
| DVWA | http://127.0.0.1:8081 | dirs PHP, params SQLi |
| Juice Shop | http://127.0.0.1:8082 | dirs/API, vhost pratica |
| WebGoat | http://127.0.0.1:8084/WebGoat | surface Java |
| VAmPI | http://127.0.0.1:8087 | fuzz de paths API |

```bash
cd docker-lab && docker compose up -d --build
```

Detalhes: [docker-lab/README.md](../docker-lab/README.md).

---

## 7. Como reportar

1. Titulo: "Enumeracao de diretorios revelou `/backup` / painel X".
2. Metodo: ferramenta + wordlist (nome, nao milhares de linhas).
3. Evidencia: 1–2 paths relevantes + status/size.
4. Vhost/param: hostname ou parametro novo e por que importa.
5. AXFR (se aplicavel): NS, trecho de registros, impacto (mapeamento interno).
6. Remediacao: desabilitar listing, harden DNS (sem AXFR publico), WAF/rate-limit.

---

## Referencias

- [SecLists](https://github.com/danielmiessler/SecLists) — instalada por `linux_postinstall.sh`
- [gobuster](https://github.com/OJ/gobuster) / [feroxbuster](https://github.com/epi052/feroxbuster) / [ffuf](https://github.com/ffuf/ffuf)
- [recon-web-pratico.md](recon-web-pratico.md) — sequencia ffuf/katana/nuclei
- Lab: [docker-lab/README.md](../docker-lab/README.md)
- Relatorio PDF: [report/README.md](../report/README.md)
