# 08 — Permissões, ACL, atributos e umask

## Objetivos

- calcular permissões efetivas em arquivos e diretórios;
- prever o resultado de umask, setgid, sticky bit e ACL padrão;
- distinguir DAC, capabilities, opções de montagem e controle MAC;
- diagnosticar acesso negado sem recorrer a permissões universais.

## DAC: proprietário, grupo e outros

O controle discricionário tradicional associa a cada inode um UID, um GID e
três conjuntos de bits. Em `-rw-r-----`:

- `rw-`: proprietário lê e escreve;
- `r--`: grupo lê;
- `---`: demais não acessam.

```bash
stat -c 'tipo=%F modo=%A octal=%a uid=%u gid=%g nome=%n' /etc/hosts
namei -l /etc/hosts
```

O acesso a um caminho depende de todos os diretórios ancestrais, por isso
`namei -l` é valioso.

## Arquivo e diretório usam os bits de forma diferente

| Bit | Arquivo regular | Diretório |
|-----|-----------------|------------|
| `r` | ler bytes | listar nomes |
| `w` | alterar/truncar | criar, remover ou renomear entradas |
| `x` | tentar executar | atravessar/acessar entradas conhecidas |

Remover um arquivo depende principalmente da permissão no diretório pai,
não de `w` no próprio arquivo.

## Modos simbólicos e octais

`r=4`, `w=2`, `x=1`; some por classe:

```bash
lab="$(mktemp -d)"
printf '%s\n' dados > "$lab/relatorio.txt"
chmod 0640 -- "$lab/relatorio.txt"
chmod u+x,g-w,o-rwx -- "$lab/relatorio.txt"
stat -c '%A %a %n' -- "$lab/relatorio.txt"
```

Evite `chmod -R 777`: ele concede escrita e execução indiscriminadamente e
trata arquivos como diretórios. Modele quem precisa de qual operação.

## Propriedade

```bash
chgrp grupo-compartilhado caminho
sudo chown usuario:grupo caminho
```

Somente processos autorizados podem trocar o UID do inode. Uma cópia pode
receber propriedade diferente; um `mv` no mesmo filesystem preserva o inode.

## Umask

Programas solicitam um modo inicial; a umask remove bits. Arquivos comuns
partem normalmente de `0666`, pois execução deve ser explícita; diretórios
partem de `0777`.

```bash
umask
( umask 027; touch "$lab/privado"; mkdir "$lab/equipe" )
stat -c '%a %n' "$lab/privado" "$lab/equipe"
```

Com `027`, resultados comuns são `640` e `750`. ACL padrão e aplicações podem
alterar o resultado efetivo.

## Bits especiais

- **setuid em executável:** altera UID efetivo conforme o dono, quando permitido;
- **setgid em executável:** equivalente para grupo;
- **setgid em diretório:** novas entradas herdam o grupo do diretório;
- **sticky em diretório:** restringe remoção/rename em diretório compartilhado.

```bash
stat -c '%A %a %n' /tmp
find /usr/bin -xdev -perm /6000 -type f -printf '%m %u:%g %p\n' 2>/dev/null | head
```

O primeiro laboratório é apenas de inventário. Não crie executáveis setuid
para praticar; esse assunto sensível pertence ao módulo final.

## ACLs

ACLs expressam exceções além de um proprietário e um grupo:

```bash
getfacl -- "$lab" 2>/dev/null
setfacl -m "u:$(id -un):rwx" -- "$lab" 2>/dev/null
setfacl -m "d:g:$(id -gn):rwx" -- "$lab" 2>/dev/null
```

A entrada `mask` limita permissões efetivas de grupos e usuários nomeados. A
ACL default em diretório influencia novas entradas, não altera as existentes.

## Atributos e capabilities

Alguns filesystems oferecem atributos como immutable e append-only, vistos por
`lsattr` e alterados por `chattr`. Eles não substituem backup e variam por
filesystem. Capabilities dividem parte da autoridade tradicional do root:

```bash
getcap -r /usr/bin /usr/sbin 2>/dev/null | head
getpcaps "$$" 2>/dev/null || true
```

Conceder uma capability errada pode equivaler a privilégio amplo. Somente
inventarie nesta etapa.

## Camadas adicionais

DAC pode permitir e ainda assim SELinux ou AppArmor negar. Montagens podem
impor `noexec`, `nosuid`, `nodev` e somente leitura. NFS e containers acrescentam
mapeamentos. Diagnóstico correto verifica todas as camadas, não responde a tudo
com `chmod 777` ou desativando o controle de segurança.

## Exercícios

1. Crie um diretório de equipe com setgid e umask coerente.
2. Demonstre a diferença entre listar (`r`) e atravessar (`x`) um diretório.
3. Calcule resultados de umask `022`, `027` e `077` antes de testar.
4. Diagnostique acesso a um caminho usando `namei`, `stat`, `id`, `getfacl` e
   opções de montagem.

## Checklist de domínio

Consigo prever o acesso efetivo e explicar por que modo, propriedade, ACL,
umask, montagem e MAC são controles diferentes.
