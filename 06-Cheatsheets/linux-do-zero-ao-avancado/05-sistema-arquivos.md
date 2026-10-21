# 05 — Hierarquia, caminhos e tipos de arquivo

## Objetivos

- resolver caminhos absolutos, relativos, físicos e simbólicos;
- reconhecer a finalidade dos diretórios essenciais do sistema;
- diferenciar arquivo regular, diretório, link, socket, FIFO e dispositivo;
- descobrir a montagem e o filesystem responsáveis por qualquer caminho.

## Uma única árvore

Linux apresenta arquivos locais, dispositivos e montagens em uma única árvore
iniciada em `/`. Não confunda `/`, raiz da árvore, com `/root`, diretório
pessoal tradicional do administrador.

- caminho absoluto começa em `/`: `/etc/hosts`;
- caminho relativo começa no diretório atual: `docs/nota.txt`;
- `.` representa o diretório atual;
- `..` representa o diretório pai;
- `~` é uma expansão feita pela shell para um diretório pessoal.

```bash
pwd
printf '%s\n' "$PWD" "$OLDPWD" "$HOME"
realpath -- /etc/../etc/hosts
basename -- /var/log/syslog
dirname -- /var/log/syslog
```

## Diretórios essenciais

| Caminho | Responsabilidade comum |
|---------|------------------------|
| `/boot` | kernel, initramfs e arquivos de boot |
| `/dev` | nós de dispositivos |
| `/etc` | configuração específica do host |
| `/home` | diretórios pessoais comuns |
| `/opt` | software adicional autocontido |
| `/proc` | interface virtual de processos e kernel |
| `/root` | home tradicional do UID 0 |
| `/run` | estado volátil do boot atual |
| `/srv` | dados servidos por este host |
| `/sys` | objetos do kernel e dispositivos |
| `/tmp` | temporários; política de limpeza varia |
| `/usr` | programas e dados compartilháveis, geralmente somente leitura operacional |
| `/var` | dados variáveis: logs, filas, cache e estado |

Em sistemas com `/usr` merge, `/bin`, `/sbin` e `/lib*` podem ser links para
subdiretórios de `/usr`. Scripts não devem inferir layout apenas pela aparência.
Use `command -v` para localizar executáveis.

## Tipos de arquivo

O primeiro caractere de `ls -l` indica o tipo:

| Caractere | Tipo |
|-----------|------|
| `-` | arquivo regular |
| `d` | diretório |
| `l` | link simbólico |
| `b` | dispositivo de bloco |
| `c` | dispositivo de caractere |
| `p` | FIFO/pipe nomeado |
| `s` | socket Unix |

```bash
ls -ld /etc/hosts /etc /dev/null /dev/loop0 2>/dev/null
file /bin/sh /etc/hosts
stat /etc/hosts
```

Extensão não determina o tipo no kernel. `file` inspeciona metadados e
conteúdo; a linha `#!` informa qual interpretador deve abrir um script.

## Nomes não são texto simples para todos os programas

Em filesystems Unix, um nome pode conter quase qualquer byte, exceto `/` e NUL.
Espaços, quebras de linha e caracteres iniciados por `-` são válidos. Portanto:

```bash
diretorio="$(mktemp -d)"
touch -- "$diretorio/relatorio final.txt"
find "$diretorio" -type f -print0 | while IFS= read -r -d '' arquivo; do
    printf '<%s>\n' "$arquivo"
done
rm -rf -- "$diretorio"
```

`find ... -print0` e consumidores com delimitador NUL evitam interpretar
espaços e quebras de linha como separadores. Não analise a saída de `ls` em
scripts.

## Case, Unicode e portabilidade

Filesystems Linux comuns diferenciam maiúsculas de minúsculas: `Nota` e `nota`
podem coexistir. Unicode visualmente igual pode possuir sequências de bytes
diferentes. Evite depender de normalização implícita e use nomes simples em
automações portáveis.

```bash
locale
printf '%s' 'ç' | wc -c
printf '%s' 'ç' | wc -m
```

Bytes e caracteres não são sinônimos em UTF-8.

## Montagens e limites

Um filesystem é anexado a um ponto da árvore. O conteúdo preexistente sob o
ponto fica oculto enquanto a montagem estiver ativa, não apagado.

```bash
findmnt
findmnt -T "$HOME"
df -hT
df -ih
```

`df -h` observa blocos; `df -i` observa inodes. Um volume pode ter espaço em
bytes e ainda falhar por esgotamento de inodes.

## Exercícios

1. Classifique dez caminhos do seu sistema por responsabilidade e filesystem.
2. Encontre links do `/usr` merge sem segui-los inadvertidamente.
3. Crie nomes com espaço e quebra de linha em um diretório temporário e processe
   todos com NUL.
4. Compare `df -h`, `df -i` e `du -sh` e explique o que cada um mede.

## Checklist de domínio

Valide sempre o caminho real, a montagem responsável e o tipo do objeto antes
de modificar conteúdo ou metadados.

Consigo navegar sem depender de interface gráfica, explicar FHS versus layout
real, identificar tipos e escrever comandos seguros para qualquer nome válido.
