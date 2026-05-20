# Recon Web Pratico

> Sequencia operacional do recon web em um engagement moderno. Foco em ferramentas atualizadas e comandos prontos.

---

## 1. Subdominios

```bash
# Passivo (rapido, sem tocar no alvo)
subfinder -d alvo.com -silent -all -o subs_passive.txt
# Tambem
amass enum -passive -d alvo.com -o subs_amass.txt
# Custom (script proprio)
python ../11-Python-Tools/subdomain_enum.py -d alvo.com --resolve -o ./output

# Ativo (consume rate limit, faz queries diretas)
dnsx -l subs_passive.txt -resp -a -aaaa -cname -o subs_alive.json -json
```

---

## 2. Probe HTTP/HTTPS

```bash
# Quais resolvem para um web server?
httpx -l subs_alive.txt -title -status-code -tech-detect -ip -cname -o web_alive.json -json
```

Resultado tipico: status 200/301/302 + framework detectado (Nuxt, Next, Spring, Django).

---

## 3. Conteudo / Fuzz de diretorios

```bash
# Wordlists comuns (apos linux_postinstall.sh)
WL=~/Pentest/Wordlists/SecLists/Discovery/Web-Content

# Fast directory bruteforce
ffuf -u https://alvo.com/FUZZ -w $WL/raft-large-words.txt -mc all -fc 404,403 -t 50 -o ffuf.json -of json

# Por extensao
ffuf -u https://alvo.com/FUZZ -w $WL/raft-medium-files.txt -e .php,.aspx,.bak,.zip,.json

# Headers/cookies/parameter fuzz
ffuf -u https://alvo.com/api -X POST -H "Authorization: Bearer FUZZ" -w tokens.txt -mc all
```

---

## 4. Crawl + JS analysis

```bash
# katana - tirar tudo que ha de URL no app
katana -u https://alvo.com -jc -kf all -d 3 -o katana_urls.txt

# gospider - alternativa
gospider -s https://alvo.com -d 3 --js -o gospider/ -t 10

# Extrair endpoints/secrets dos JS
grep -Eo "(https?://[^\s\"']+|/[a-zA-Z0-9_-]+/[a-zA-Z0-9_/-]+)" katana_urls.txt | sort -u > endpoints.txt
linkfinder -i js/ -o cli > linkfinder.txt
```

Procurar especificamente:
- API keys (`AKIA*`, `AIza*`, `ghp_*`)
- Endpoints `/api/`, `/v1/`, `/v2/`, `/graphql`
- Credenciais embutidas
- `console.log` com payload sensivel

---

## 5. Vulnerability scan automatizado

```bash
# Nuclei - templates da comunidade
nuclei -l web_alive.txt -t ~/.nuclei-templates/ -severity medium,high,critical -rl 50 -o nuclei.json -json

# Por categoria
nuclei -l web_alive.txt -t cves/ -t exposures/ -t misconfiguration/
```

Sempre revise manualmente os achados - falsos positivos sao comuns.

---

## 6. Fingerprint de tecnologia

```bash
whatweb https://alvo.com
wappalyzer https://alvo.com           # CLI atualizado
nuclei -t technologies/ -u https://alvo.com
```

Mapeie tudo: framework, versao, libs JS, CDN, WAF, CMS, language.

---

## 7. Screenshot massivo

```bash
gowitness scan file -f web_alive.txt --threads 10
# Abre report HTML
gowitness report serve
```

Visual triage rapido - elimina alvos baixos e prioriza interessantes (login pages, dashboards).

---

## 8. Parametros e Form Discovery

```bash
# Param discovery (combina varios)
arjun -u https://alvo.com/page.php -o params.txt

# Fuzz parametro GET sobre endpoints conhecidos
ffuf -u "https://alvo.com/api/item?FUZZ=test" -w $WL/burp-parameter-names.txt -fs 1234
```

---

## 9. Vhosts (mesmo IP, hostnames diferentes)

```bash
ffuf -u https://alvo.com -H "Host: FUZZ.alvo.com" -w $WL/subdomains-top1million-5000.txt -fs <baseline-size>
```

---

## 10. Conserva resultados

Use o `organize_logs.ps1`/`.sh` para arquivar tudo:

```bash
mkdir -p engagement/alvo.com/raw
mv subs_*.txt web_alive.* ffuf.json nuclei.json katana_urls.txt engagement/alvo.com/raw/
```

E gere o INDEX automatico:

```bash
pwsh ../04-Automation/organize_logs.ps1 -SourcePath engagement/alvo.com/raw -TargetName alvo_com
```

---

## Referencias

- [Project Discovery toolset](https://github.com/projectdiscovery)
- [SecLists](https://github.com/danielmiessler/SecLists)
- [Bug Bounty Roadmap](https://www.bugcrowd.com/resources/levelup/)
