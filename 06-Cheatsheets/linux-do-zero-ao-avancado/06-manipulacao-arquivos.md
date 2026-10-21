# 06 — Arquivos, diretórios, links e metadados

## Objetivos

- criar, copiar, mover e remover entradas preservando limites de argumentos;
- explicar a relação entre nome, inode, hard link e link simbólico;
- preservar ou comparar conteúdo, metadados e estrutura conforme o requisito;
- usar busca, archive e sincronização com pré-visualização e alvo validado.

## Criar e inspecionar

```bash
lab="$(mktemp -d)"
mkdir -p -- "$lab/origem/sub" "$lab/destino"
printf '%s\n' 'primeira linha' 'segunda linha' > "$lab/origem/notas.txt"
install -m 0640 -- "$lab/origem/notas.txt" "$lab/destino/notas.txt"
stat -- "$lab/destino/notas.txt"
```

`touch` cria arquivo vazio se ausente ou atualiza timestamps se existente.
`install` combina cópia, modo e, com privilégio, propriedade; é útil em
scripts de implantação.

## Copiar, mover e remover

```bash
cp -a -- "$lab/origem/." "$lab/destino/copia/"
mv -- "$lab/destino/notas.txt" "$lab/destino/notas-renomeadas.txt"
rm -- "$lab/destino/notas-renomeadas.txt"
```

- `cp -a` tenta preservar estrutura e metadados; suporte depende do destino.
- `mv` no mesmo filesystem geralmente renomeia entradas; entre filesystems
  copia e remove, portanto não possui a mesma atomicidade.
- `rm` remove nomes. Dados permanecem enquanto houver hard links ou descritores
  abertos e podem continuar recuperáveis no meio físico.
- `rmdir` remove somente diretórios vazios.

Antes de remoção recursiva, imprima o caminho absoluto e liste o alvo. Em
scripts, recuse valor vazio, `/`, `$HOME` e outros alvos amplos. Prefira lixeira
em trabalho interativo quando a recuperação for importante.

## Inodes, hard links e links simbólicos

```bash
printf '%s\n' 'conteudo' > "$lab/origem/base.txt"
ln -- "$lab/origem/base.txt" "$lab/origem/hard.txt"
ln -s -- base.txt "$lab/origem/simbolico.txt"
ls -li -- "$lab/origem"/*
readlink -- "$lab/origem/simbolico.txt"
```

Um hard link é outro nome para o mesmo inode. Normalmente não cruza
filesystems e não é permitido para diretórios por usuários comuns. Um symlink
é um objeto que contém outro caminho, pode cruzar filesystems e pode ficar
quebrado. Alterar o arquivo por um hard link aparece no outro; substituir o
nome por outro inode é diferente de alterar o inode original.

## Timestamps e tamanho

- `mtime`: conteúdo do arquivo foi modificado;
- `ctime`: metadados do inode mudaram; não significa criação;
- `atime`: acesso, sujeito a opções de montagem e otimizações;
- birth/creation time: disponível apenas em combinações compatíveis.

```bash
stat -- "$lab/origem/base.txt"
du -h -- "$lab/origem/base.txt"
du -h --apparent-size "$lab/origem/base.txt"
```

Tamanho aparente e blocos alocados diferem em arquivos esparsos, compressão e
deduplicação.

## Localizar sem quebrar nomes

```bash
find "$lab" -type f -name '*.txt' -printf '%s\t%p\0' |
    sort -z -n |
    tr '\0' '\n'

find "$lab" -type f -mtime -1 -exec stat --format='%n %s' -- {} +
```

`find -exec ... {} +` agrupa argumentos e preserva nomes. Leia a expressão de
`find` como predicados; ações como `-delete` mudam o sistema e exigem uma
primeira execução somente com `-print`.

## Arquivar e comprimir

`tar` empacota uma árvore; gzip, xz e zstd comprimem fluxos. Extensão indica
convenção, não garantia.

```bash
tar -C "$lab/origem" -czf "$lab/arquivo.tar.gz" .
tar -tzf "$lab/arquivo.tar.gz"
mkdir -- "$lab/restaurado"
tar -C "$lab/restaurado" -xzf "$lab/arquivo.tar.gz"
diff -ru -- "$lab/origem" "$lab/restaurado"
```

Antes de extrair arquivo de origem desconhecida, liste entradas e use diretório
isolado. Entradas absolutas, `..`, links e permissões podem causar efeitos
inesperados; use as proteções do extrator da sua distro.

## Sincronização

`rsync -a` preserva uma árvore incrementalmente. A barra final importa:

```bash
rsync -a --dry-run --itemize-changes -- "$lab/origem/" "$lab/espelho/"
rsync -a -- "$lab/origem/" "$lab/espelho/"
```

Sem barra em `origem`, o diretório pode ser criado dentro do destino. Opções
de exclusão como `--delete` são destrutivas e devem vir depois de dry-run,
backup e validação dos caminhos.

## Limpeza do laboratório

```bash
test -n "$lab" && test "$lab" != / && rm -rf -- "$lab"
```

## Exercícios

1. Demonstre diferença entre alterar conteúdo e substituir um nome por `mv`.
2. Remova o arquivo-base e descubra o comportamento dos dois tipos de link.
3. Crie um arquivo esparso com `truncate -s 1G` e compare `stat`, `du` e `ls`.
4. Faça um arquivo `tar`, liste, restaure e compare antes de chamar isso de
   backup.

## Checklist de domínio

Consigo manipular qualquer nome com segurança, prever efeitos sobre inode e
links e validar uma cópia por conteúdo e metadados.
