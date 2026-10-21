# 06 — Portable Executable, COFF e validação de formato

PE/COFF descreve imagens executáveis, DLLs, drivers e objetos do ecossistema
Windows. Ler o formato é exercício de engenharia de arquivos: todo offset,
tamanho e contagem vindo do artefato deve ser validado antes do acesso.

## Objetivos

- localizar headers e tabela de seções com checagem de limites;
- distinguir RVA, virtual address e file offset;
- interpretar imports, exports, relocations e recursos em alto nível;
- relacionar PE32/PE32+, machine e arquitetura;
- separar hash, Authenticode, mitigação declarada e confiança.

## Estrutura principal

O DOS header começa por `MZ` e contém `e_lfanew`, offset para a assinatura
`PE\0\0`. Depois vêm COFF File Header, Optional Header e Section Table. “Optional”
é nome histórico; imagens carregáveis precisam dele.

Campos relevantes incluem:

- `Machine` e número de seções;
- tamanho do Optional Header e characteristics;
- magic PE32 ou PE32+;
- entry point RVA, image base e alinhamentos;
- `SizeOfImage`, `SizeOfHeaders` e subsystem;
- data directories para import, export, resource, exception, relocation e outros;
- para cada seção, nome, virtual size/address, raw size/offset e flags.

Nunca calcule `peOffset + constante` sem provar que cabe no arquivo. Contagem de
seções multiplicada pelo tamanho da entrada pode causar overflow em parser mal
feito. Estabeleça tamanho máximo, limites plausíveis e arithmetic checked.

## RVA versus offset

RVA é relativo à base da imagem quando carregada. File offset é posição no
arquivo. Para converter um RVA, encontre seção cujo intervalo virtual o contém e
relacione ao `PointerToRawData`, respeitando tamanhos/alinhamento. Dados podem
existir em memória sem bytes equivalentes no arquivo, como região zero-filled.

Image base preferida não é endereço garantido. ASLR e relocations permitem mapear
em outra base. Não some base observada e offset de arquivo como se fossem a mesma
coordenada.

## Imports e exports

Import table descreve dependências e símbolos/números a resolver. Export table
expõe nomes/ordinals/RVAs. Delay-load posterga resolução. API sets podem aparecer
como contratos encaminhados. Um import listado não prova que o caminho executou;
apenas que a imagem declara dependência daquele mecanismo.

O parser do curso lê apenas resumo seguro. `dumpbin /headers` e ferramentas do
SDK oferecem referência para comparar. Divergência exige investigar interpretação
ou formato, não “corrigir” bytes do executável.

```powershell
.\exemplos\Get-RtePeSummary.ps1 `
  -Path .\exemplos\dll\dll_consumer.exe
Get-AuthenticodeSignature -FilePath .\exemplos\dll\dll_consumer.exe
```

Use somente binário próprio ou nativo conhecido. O script não executa o arquivo.

## COFF, linker e símbolos

Compilador produz objetos COFF; linker resolve símbolos, aplica relocations e
constrói imagem. PDB guarda informação de depuração fora do PE conforme opções.
Build reproduzível precisa registrar compilador, flags, SDK e fonte. O campo
histórico chamado timestamp nem sempre representa horário real em builds
determinísticos; trate-o como valor do header, não verdade cronológica.

## Assinatura e mitigação

Authenticode usa estrutura própria e regras de hashing que excluem/normalizam
certas regiões. Logo o hash SHA-256 de todo arquivo e o digest assinado respondem
perguntas diferentes. Assinatura válida liga conteúdo ao signatário no contexto
da cadeia; não prova qualidade ou ausência de vulnerabilidade.

Flags do Optional Header podem indicar compatibilidade com ASLR, DEP/NX ou CFG,
mas o estado efetivo também depende de sistema, linker e política. Não declare
mitigação ativa só por um bit sem consultar o processo.

## Testes negativos

Copie uma fixture e produza arquivos truncados: antes de `e_lfanew`, dentro do
COFF header e antes da Section Table. O parser deve rejeitar com mensagem clara,
sem exceção de indexação ou alocação enorme. Altere assinatura apenas na cópia e
confirme rejeição. Não faça fuzzing amplo nem abra artefatos desconhecidos.

## Exercícios

1. Desenhe offsets dos headers e as validações anteriores a cada leitura.
2. Converta um RVA de seção própria para file offset com conta documentada.
3. Compare saída do parser e `dumpbin /headers`.
4. Explique PE32 versus PE32+ e `Machine` sem confundir “32” com tamanho total.
5. Crie cinco casos truncados e transforme cada falha em teste Pester.

## Checklist de domínio

- [ ] Toda leitura de campo tem limite verificado.
- [ ] RVA, image base e file offset não são misturados.
- [ ] Imports declarados não provam execução.
- [ ] Timestamp COFF não é usado sozinho numa timeline.
- [ ] Hash, assinatura e flags de mitigação têm conclusões distintas.
- [ ] Parser nunca executa o artefato analisado.
- [ ] Testes negativos usam somente cópias sintéticas.
