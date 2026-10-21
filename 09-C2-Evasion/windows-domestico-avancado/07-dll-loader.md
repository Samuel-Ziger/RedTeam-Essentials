# 07 — DLLs, ABI, linking e loader seguro

DLL compartilha código e dados por um contrato binário. O loader resolve imagens
no processo chamador; ele não transforma a DLL em programa autônomo. Projeto
seguro controla ABI, caminho, dependências, inicialização e ownership.

## Objetivos

- distinguir linking implícito, explícito e delay-load;
- versionar ABI de funções exportadas;
- explicar loader lock e restrições de `DllMain`;
- carregar plugin próprio por caminho absoluto e flags seguras;
- diagnosticar falha de dependência sem baixar DLL avulsa.

## Três formas de dependência

No linking implícito, a import library permite ao linker registrar imports e o
loader resolve dependências ao iniciar/mapeá-las. No linking explícito, o código
chama `LoadLibraryExW`, resolve exports por `GetProcAddress` e libera com
`FreeLibrary`. Delay-load registra dependência, mas posterga resolução até uso.

Cada forma muda o momento e a forma da falha. Nenhuma autoriza procurar arquivo
de origem desconhecida quando a dependência não existe.

## ABI como contrato

Nome exportado, calling convention, tipos, alinhamento, tamanho de estruturas,
tratamento de erro e ownership de buffers compõem a ABI. Alterar `int` para tipo
de outro tamanho ou fazer consumidor liberar memória com allocator diferente pode
quebar mesmo que compile.

O exemplo exporta:

```c
RTE_API int rte_add(int left, int right);
RTE_API unsigned int rte_api_version(void);
```

Consumidor consulta `rte_api_version` antes de depender do contrato. Em sistema
real, prefira export versionado, estrutura com campo `size/version` ou nomes
compatíveis, e mantenha testes entre versões.

## DllMain e loader lock

O sistema chama `DllMain` em eventos de attach/detach sob loader lock. Trabalho
complexo pode gerar deadlock ou dependência circular. Evite carregar outras DLLs,
esperar threads, usar sincronização complexa ou executar I/O significativo.
Inicialização explícita após carga é mais testável.

A DLL do curso não precisa de `DllMain`: comportamento padrão é suficiente.
Menos código nessa fase reduz risco.

## Ordem de busca e caminho seguro

Carregar apenas pelo nome permite que diretórios e políticas influenciem a
resolução. A ordem depende de versão, configuração e flags. O consumidor do curso
obtém o caminho de seu próprio executável, anexa `rte_math.dll` com função segura
e chama:

```c
LoadLibraryExW(
    path,
    NULL,
    LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_SYSTEM32
);
```

Assim o alvo primário é absoluto e dependências ficam limitadas aos locais
previstos. O diretório deve ter ACL apropriada; caminho absoluto em diretório
gravável por qualquer usuário não resolve a confiança.

Side-by-side assemblies, manifests e API sets tratam outros cenários. Não altere
PATH global, current directory ou chaves do sistema para “fazer carregar”.

## Arquitetura e dependências

Processo x64 carrega DLL x64; processo x86 carrega DLL x86. `Machine` no PE ajuda
a diagnosticar `ERROR_BAD_EXE_FORMAT`. Uma dependência ausente pode aparecer como
falha na DLL principal; use `dumpbin /dependents`, ProcMon filtrado e ferramenta
oficial, não copiadores de DLL.

Assinatura/hashes ajudam procedência, mas a DLL própria de desenvolvimento pode
ser não assinada. Preserve build, fonte e PDB para estabelecer identidade.

## Ciclo do exemplo

`build.ps1` compila DLL e consumidor com warnings como erro. O consumidor:

1. constrói caminho absoluto;
2. carrega com flags explícitas;
3. valida cada export;
4. converte o ponteiro com tamanho verificado;
5. consulta versão e soma;
6. chama `FreeLibrary` e trata erro.

Ele não abre, escreve ou cria thread em outro processo. O laboratório não aborda
injeção, sideloading ofensivo, hooking ou proxy DLL.

## Falhas controladas

Renomeie a DLL própria e registre código de erro e evento do ProcMon. Restaure e
valide. Compile uma versão sem um export e observe falha de lookup. Depois evolua
a API para v2 preservando v1 ou fazendo consumidor rejeitar de forma clara.

Não substitua DLL de sistema, não copie para diretórios do Windows e não altere
search path global.

## Exercícios

1. Compare implicit, explicit e delay-load por momento de resolução e erro.
2. Desenhe ownership do `HMODULE` e dos ponteiros de função.
3. Explique loader lock e mova inicialização para função explícita no papel.
4. Produza matriz consumidor/DLL v1-v2 e resultado esperado.
5. Capture somente o consumidor no ProcMon e explique a busca observada.

## Checklist de domínio

- [ ] DLL executa no processo que a carrega; não é programa autônomo.
- [ ] ABI inclui tipos, calling convention, versão e ownership.
- [ ] `DllMain` permanece mínimo ou ausente.
- [ ] Carga usa caminho absoluto, flags e diretório controlado.
- [ ] Arquitetura do processo e da DLL é compatível.
- [ ] Falhas resultam em diagnóstico, não download de DLL avulsa.
- [ ] Nenhuma técnica de manipulação de outro processo aparece na prática.
