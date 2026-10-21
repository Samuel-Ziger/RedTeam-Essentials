# 04 — ELF, linking e loader dinâmico

## Objetivos

- ler headers ELF sem confundir seções e segmentos;
- explicar linkedição estática, dinâmica, relocations e symbol resolution;
- acompanhar `execve` até o entry point;
- reconhecer PIE, ASLR, RELRO, NX e stack canary.

## Objetos ELF

O ELF header identifica classe, endianness, tipo, arquitetura e tabelas. A tabela
de **seções** serve principalmente a linker e ferramentas. A tabela de
**program headers** descreve segmentos que o loader deve mapear. Um executável
stripado pode funcionar sem nomes de seção.

Tipos comuns:

- `ET_REL`: objeto relocável;
- `ET_EXEC`: executável com endereços tradicionais;
- `ET_DYN`: biblioteca compartilhada ou PIE;
- `ET_CORE`: core dump.

```bash
file /bin/true
readelf -hW /bin/true
readelf -lW /bin/true
readelf -dW /bin/true
readelf -rW /bin/true
```

## Do `execve` ao `main`

O kernel valida o formato, cria novo espaço de endereços, mapeia segmentos e,
para binário dinâmico, transfere o controle ao interpretador indicado por
`PT_INTERP`. O loader resolve dependências e relocations, depois chama o entry
point. O runtime prepara argumentos, ambiente e inicializadores antes de `main`.

`main` não é o primeiro código executado pelo processo.

## Resolução dinâmica

Bibliotecas são encontradas conforme o loader, tags `RPATH/RUNPATH`, cache e
caminhos confiáveis. Variáveis como `LD_PRELOAD` são poderosas para depuração,
mas são filtradas em execução segura e não devem ser usadas como mecanismo de
produção improvisado.

```bash
ldd /bin/true
LD_DEBUG=libs /bin/true 2>loader.log
objdump -T /bin/true | head
```

Não rode `ldd` em binário não confiável. Prefira `readelf -d` e inspecione de
forma estática.

## Mitigações

- PIE permite randomizar o executável;
- NX impede execução em mapeamentos sem permissão executável;
- RELRO protege estruturas de relocations após inicialização;
- canary detecta certas corrupções de stack;
- CFI e shadow stack dependem de toolchain e hardware.

Mitigação reduz classes de impacto; não corrige bug de memória.

## Seções, segmentos e relocations

O linker usa seções como `.text`, `.data`, `.bss`, tabelas de símbolos e
relocations para construir o artefato. O loader do kernel trabalha principalmente
com program headers `PT_LOAD`, permissões, offsets e alinhamento. Várias seções
podem ocupar um segmento; uma seção ausente após `strip` não impede que os bytes
necessários sejam mapeados.

Uma relocation descreve um valor que só pode ser finalizado quando endereço de
símbolo ou local de carga é conhecido. Em linking dinâmico, PLT/GOT mediam
resolução de funções e dados. Lazy binding posterga parte do trabalho; binding
imediato combinado com RELRO pode tornar a GOT somente leitura após a resolução.
Confirme tags e segmentos no arquivo, não apenas flags passadas ao compilador.

## Diagnóstico do carregamento

Quando um executável falha com “arquivo não encontrado” apesar de existir,
verifique primeiro o `PT_INTERP`: o loader solicitado pode estar ausente.
Depois examine arquitetura, ABI, dependências, `RUNPATH`, permissões de cada
diretório e mount `noexec`. `ldd` pode executar mecanismos do alvo e não deve
ser aplicado a conteúdo não confiável.

Use uma sequência de evidência estática para binários externos:

```bash
file -- binario
readelf -hW -lW -dW -- binario
objdump -p -- binario
```

Em um binário próprio, complemente com `LD_DEBUG`, `strace` filtrado e mapas do
processo. ASLR randomiza regiões, mas offsets relativos dentro do mesmo módulo
podem permanecer; compare o mapeamento, não um único endereço.

## Falhas comuns

- confundir section header flags com permissões finais de páginas;
- assumir que PIE e ASLR são a mesma propriedade;
- considerar `main` o entry point;
- confiar em `ldd` para analisar arquivo não confiável;
- declarar “full RELRO” sem confirmar `GNU_RELRO` e binding.

## Prática A

Use [`elf_inspector.c`](exemplos/c/elf_inspector.c) para ler um header. Compare a
saída com `readelf`, depois compile o mesmo programa como PIE e não PIE. Observe
tipo ELF, endereços em execuções sucessivas e `PT_GNU_STACK`.

## Exercícios

1. Compile uma matriz PIE/não PIE e RELRO parcial/completo; compare headers,
   relocations e mapas em três execuções.
2. Use um interpretador propositalmente inexistente numa cópia descartável e
   diagnostique a mensagem sem alterar o binário original.
3. Localize entry point, `_start`, inicializadores e `main` de um programa
   próprio e desenhe a ordem.
4. Compare linking estático e dinâmico quanto a tamanho, dependências, símbolos
   e atualização de bibliotecas.

## Checklist de domínio

- [ ] Distingo seções de segmentos e `ET_EXEC` de PIE `ET_DYN`.
- [ ] Explico `PT_INTERP`, relocations, PLT, GOT e resolução de símbolos.
- [ ] Verifico mitigações no artefato em vez de confiar apenas em flags.
- [ ] Diagnostico loader ausente sem executar binário não confiável.
- [ ] Sei qual tabela determina o mapeamento e as permissões finais.

Fonte: [`elf(5)`](https://man7.org/linux/man-pages/man5/elf.5.html).
