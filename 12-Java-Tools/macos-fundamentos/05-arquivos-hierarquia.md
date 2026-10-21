# 05 — Arquivos, caminhos e hierarquia

macOS segue convenções Unix e acrescenta bundles, metadados e uma separação de
volumes que o Finder normalmente oculta. Caminhos absolutos começam em `/`;
`~` representa o diretório pessoal da conta atual.

## Diretórios importantes

| Caminho | Papel |
|---|---|
| `/System` | sistema protegido |
| `/Library` | recursos para todas as contas |
| `~/Library` | preferências e estado da conta |
| `/Applications` | aplicativos do computador |
| `~/Applications` | aplicativos da conta, quando usado |
| `/Users` | diretórios pessoais |
| `/Volumes` | pontos de montagem |

```zsh
pwd
ls -laOe@
stat -x exemplo.txt
file exemplo.txt
mdls exemplo.txt
```

Aspas protegem espaços e caracteres do shell: `stat -x -- "$path"`. Não use
`sudo` para contornar um caminho que você ainda não entendeu.

## Prática

Monte uma árvore de fixture com nomes contendo espaços. Crie link simbólico,
compare inode e caminho, compacte, extraia e confirme hashes.
