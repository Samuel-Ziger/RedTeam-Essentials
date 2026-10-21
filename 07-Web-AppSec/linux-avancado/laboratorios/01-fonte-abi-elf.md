# Lab 01 — Fonte, ABI e ELF

**Classe:** A/B. **Duração:** 8–12 h.

## Pré-requisitos e preparação

Conclua os capítulos 00–06 e leia o catálogo de exemplos. Use fonte do kernel
correspondente à VM, compilador registrado e diretório temporário. Não analise
binário externo executando-o. Crie uma fixture própria cuja saída contenha PID e
um texto constante para provar que as variantes mantêm comportamento.

## Pergunta

Como uma chamada `getpid()` do programa se relaciona ao ELF, loader, libc,
instrução de transição e implementação do kernel desta VM?

## Procedimento

1. Registre kernel, libc, compilador e arquitetura.
2. Compile um programa mínimo com debug, PIE e não PIE.
3. Inspecione headers, segments, interpreter, symbols e relocations.
4. Execute o `elf_inspector` e compare com `readelf`.
5. Desmonte o wrapper e observe com `strace`.
6. Localize syscall table e `SYSCALL_DEFINE` no checkout correto.
7. Leia um commit que alterou esse caminho sem mudar a ABI.

## Matriz de build

Produza debug PIE, debug não PIE, release PIE e uma variante com binding
imediato. Para cada uma, registre build ID, tipo ELF, interpreter, `PT_LOAD`,
`GNU_RELRO`, stack, símbolos e relocations. Execute três vezes e compare mapas;
endereços absolutos podem variar, mas o resultado funcional deve ser idêntico.

No caminho da syscall, marque:

1. chamada C e wrapper da libc;
2. convenção de registradores da arquitetura;
3. instrução de transição;
4. tabela ou macro de entrada no kernel;
5. retorno negativo e conversão para `errno`;
6. possível caminho vDSO e como ele foi excluído ou confirmado.

## Controles e falhas seguras

Use um executável com `PT_INTERP` inválido apenas em cópia para reproduzir a
mensagem “não encontrado”. Diagnostique por headers sem `ldd`. Compare também
um `read` interrompido e um retorno parcial sintético; documente por que repetir
a operação inteira seria incorreto.

Controle negativo: um binário estático ou uma função confirmada na vDSO. Se a
toolchain não suportar uma variante, registre a limitação em vez de trocar de
ambiente sem atualizar os metadados.

## Evidência

- diagramas PIE e não PIE;
- hashes dos binários;
- trecho de desmontagem anotado;
- caminho da fonte com commit;
- tabela “contrato estável versus detalhe interno”.

## Critério

Aprova quando outra pessoa encontra a mesma entrada usando apenas commit e
comandos, e quando a conclusão diferencia wrapper libc, vDSO possível e syscall.

Também deve explicar por que seções não definem diretamente as páginas mapeadas,
como a UAPI difere de estrutura interna e qual detalhe observado pode mudar entre
releases sem quebrar o programa.

## Perguntas para defesa

- Qual evidência prova que o kernel executado corresponde ao checkout?
- O que o `strace` não consegue mostrar neste caso?
- Como PIE, ASLR, NX e RELRO se relacionam sem serem equivalentes?
- Qual campo de uma UAPI precisaria de regra de compatibilidade 32-bit?

## Cleanup

Remova somente o diretório de build criado pelo lab e preserve relatório/hashes.
Confirme que nenhum processo da fixture permaneceu e que dados brutos estão
separados dos binários temporários.
