# Lab 02 — PE, ABI e carregamento seguro de DLL

**Classe:** B — compilação e alteração somente dos binários próprios na pasta da fixture.

## Propósito

Relacionar bytes do formato PE, contrato de ABI e decisões do loader. Você compilará a DLL didática e seu consumidor, inspecionará cabeçalhos e demonstrará falha controlada quando a dependência fica ausente ou incompatível. Não há carregamento em outro processo, hooking ou alteração global do caminho de DLLs.

## Pré-condições

- Lab 01 e capítulos 06–07 concluídos;
- Developer PowerShell do Visual Studio com compilador C;
- exemplos `dll/` e `Get-RtePeSummary.ps1` revisados;
- snapshot e pasta de trabalho sem dados reais.

Leia o `build.ps1`, `rte_math.h`, implementação e consumidor antes de executar. Confirme que o consumidor resolve seu próprio diretório, usa caminho absoluto e libera o módulo.

## Build reproduzível

1. Registre versão da toolchain e arquitetura do terminal.
2. Execute `exemplos\dll\build.ps1`.
3. Guarde stdout, códigos de saída e hashes SHA-256 da DLL e do consumidor.
4. Execute o consumidor e confirme exatamente `api_version=1` e `sum=42`.
5. Repita o build limpo e explique quais bytes podem variar e por quê.

Não versionar `.exe`, `.dll`, `.obj`, `.lib`, `.exp` ou `.pdb`. Eles são artefatos reconstruíveis e ficam apenas no laboratório.

## Inspeção estrutural

Execute o parser didático nos dois PEs. Registre `Machine`, `Format`, número de seções, entry point, tamanho da imagem e subsistema. Para cada seção, relacione RVA, tamanho virtual, offset e tamanho bruto. Confirme que todos os intervalos permanecem dentro do arquivo.

Compare a visão do parser com `dumpbin /headers` e `dumpbin /imports`. Diferenças de cobertura são esperadas: o script não é parser completo. Assinatura ausente em uma fixture própria não significa conteúdo malicioso; procedência vem do seu build reproduzível e hashes.

## Experimento de carregamento

Primeiro renomeie `rte_math.dll` para `rte_math.dll.off`. Execute o consumidor uma vez e capture somente esse processo no ProcMon. Identifique as tentativas relevantes, o resultado final e a mensagem da aplicação. Restaure o nome e prove recuperação.

Depois altere `rte_api_version` para retornar `2`, faça novo build e execute. O consumidor deve detectar incompatibilidade antes de usar a operação. Essa mudança simula contrato incompatível, não corrupção de memória. Restaure a versão `1`, recompile e valide.

Não copie DLL para diretório do sistema, não mude `PATH`, não use nome de biblioteca de terceiros e não desative proteção. A busca é restrita ao diretório calculado pelo consumidor.

## Evidência e raciocínio

Construa uma sequência: abrir executável → mapear imagem → resolver dependência pelo caminho permitido → localizar exports → conferir versão da ABI → chamar função → liberar módulo. Marque o que foi inferido do código e o que foi observado.

Explique a diferença entre offset no arquivo, RVA e endereço virtual; import estático e resolução dinâmica; compatibilidade de ABI e igualdade de código-fonte. Mostre que a mensagem de falha não expõe caminho sensível na entrega pública.

## Critérios de aceite

- build e saída saudável são reproduzíveis;
- parser rejeita arquivo não PE e não altera o alvo;
- falta da DLL e ABI incompatível produzem falhas distintas e compreensíveis;
- ProcMon está filtrado apenas no consumidor;
- nenhum caminho de busca global ou proteção foi modificado.

## Cleanup e revisão

Execute a limpeza do build, apague PML/CSV bruto e preserve relatório, hashes e comandos. Confirme que o código voltou à ABI versão 1.

Responda: por que assinatura e hash respondem perguntas diferentes? Um import ausente é detectado em qual fase? Por que `DllMain` deve permanecer mínimo? Como o caminho absoluto reduz ambiguidade sem provar que a DLL é confiável?

