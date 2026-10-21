# 13 — VFS, inodes, dentries e page cache

## Objetivos

- seguir resolução de caminho e abertura de arquivo;
- distinguir inode, dentry, file e descritor;
- relacionar buffered I/O, mmap e page cache;
- reconhecer corridas de path traversal e APIs baseadas em diretório.

## Objetos principais

- `super_block`: instância montada de um filesystem;
- `inode`: identidade e metadados de um objeto no filesystem;
- `dentry`: nome e relação no cache de caminhos;
- `file`: abertura com posição, flags e operações;
- descritor: índice por processo que referencia um `file`.

Dois descritores podem apontar para a mesma descrição aberta após `dup`,
compartilhando offset. Duas chamadas independentes a `open` criam descrições
distintas mesmo para o mesmo inode.

## Resolução de caminho

Path walk atravessa componentes, mount points, symlinks e dentries positivas ou
negativas. Permissões precisam ser verificadas nos diretórios atravessados. O
cache acelera lookup, mas invalidação e renomeação exigem sincronização.

Sequências “valide o caminho, depois abra” sofrem TOCTOU. Prefira descritor de
diretório e `openat2()` com flags de resolução adequadas quando o threat model
exigir confinamento.

```bash
namei -l ./path/to/file
stat -Lc 'dev=%d inode=%i mode=%A links=%h' FILE
ls -li FILE HARDLINK
```

## Page cache

Buffered reads e writes passam normalmente pelo page cache. Escrever pode apenas
marcar páginas sujas; writeback ocorre depois. `fsync()` pede persistência dos
dados e metadados necessários daquele arquivo, mas garantias finais dependem do
filesystem, dispositivo, cache e protocolo de energia.

`mmap(MAP_SHARED)` e `read/write` podem observar as mesmas páginas de cache. Isso
não elimina sincronização entre threads/processos nem transforma armazenamento
em memória coerente de hardware.

## Direct I/O

`O_DIRECT` procura reduzir passagem pelo page cache e impõe alinhamentos que
variam. Não significa operação síncrona nem acesso direto ao hardware. Pode ajudar
bancos que mantêm cache próprio ou piorar cargas comuns.

## Observação

```bash
cat /proc/sys/vm/dirty_background_ratio
grep -E 'Cached|Dirty|Writeback' /proc/meminfo
strace -e openat,read,write,fsync,close -- command
```

Não use `drop_caches` como rotina de tuning. Em benchmark controlado, ele exige
root, altera o sistema inteiro e produz um cenário que pode não representar uso
real.

## Lifetime e descrições abertas

O descritor é apenas um índice na tabela do processo. Após `dup` ou `fork`, mais
de um descritor pode apontar para a mesma open file description e compartilhar
offset e status flags. O inode identifica o objeto no filesystem; a dentry liga
nome a inode dentro de um mount. Renomear ou remover um nome não invalida um
arquivo já aberto: o objeto permanece enquanto referências existirem.

Essa separação explica por que logs removidos ainda ocupam espaço, por que
hardlinks compartilham conteúdo e por que locks associados à descrição aberta
diferem de locks vinculados ao processo. Diagnostique com `/proc/PID/fd`, inode,
mount e tipo de lock, não apenas com pathname antigo.

## Operações seguras por descritor

Para atuar dentro de uma árvore, abra um diretório confiável e resolva caminhos
relativamente a ele. `openat2` permite restringir symlinks, mounts e escapes com
flags `RESOLVE_*`. Ainda é preciso validar tipo, ownership e comportamento após
a abertura. O padrão “`stat`, valide, depois `open`” deixa janela para troca.

## Durabilidade ponta a ponta

`write` bem-sucedido geralmente significa bytes aceitos pelo kernel. `fsync` do
arquivo solicita dados e metadados necessários; criação ou rename também pode
exigir `fsync` do diretório para tornar o vínculo durável. O protocolo correto
para substituição é escrever temporário no mesmo filesystem, sincronizar,
renomear atomicamente e sincronizar o diretório. Atomicidade de rename não é
sinônimo de persistência após queda.

## Falhas comuns

- confundir descritor com inode ou pathname;
- assumir que unlink libera imediatamente o espaço;
- misturar offsets após `dup` sem perceber;
- usar pathname validado em chamada posterior suscetível a TOCTOU;
- tratar `O_DIRECT` como garantia de sincronismo ou acesso ao hardware.

## Prática A

1. Abra o mesmo arquivo duas vezes e compare offsets.
2. Repita com `dup`.
3. Crie hardlink e symlink; compare inode e path walk.
4. Leia arquivo maior que o cache duas vezes e registre faults e tempo.
5. Explique o que a segunda execução realmente mede.

## Exercícios

1. Demonstre offsets compartilhados com `dup` e independentes com dois `open`.
2. Mantenha um arquivo aberto, remova o nome e explique espaço e lifetime usando
   inode e `/proc/PID/fd`.
3. Implemente substituição durável por temporário, `fsync`, rename e `fsync` do
   diretório, tratando cada erro.
4. Modele uma corrida TOCTOU e refaça a operação a partir de directory fd.

## Checklist de domínio

- [ ] Distingo superblock, inode, dentry, file description e descritor.
- [ ] Explico page cache, dirty pages, writeback e `mmap` compartilhado.
- [ ] Evito validação por pathname separada do uso.
- [ ] Distingo atomicidade de rename de durabilidade após queda.
- [ ] Sei por que arquivo removido pode continuar aberto e ocupando espaço.

Fonte: [VFS](https://docs.kernel.org/filesystems/vfs.html).
