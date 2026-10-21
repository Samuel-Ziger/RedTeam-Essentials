# 19 — WinDbg e projeto integrador de diagnóstico

WinDbg permite examinar estado preservado em dumps, navegar por módulos, threads, exceções e stacks e relacionar endereços ao código por meio de símbolos. A ferramenta não “descobre a causa” sozinha: ela fornece evidências de uma fotografia. O projeto final integra arquitetura NT, PE/DLL, PowerShell, observabilidade, desempenho e mitigações em uma investigação segura.

## Objetivos

Ao concluir, você deverá conseguir:

- explicar a relação entre executável, PDB, símbolo e endereço;
- abrir um mini dump de fixture própria e verificar sua qualidade;
- localizar exceção, contexto, thread e primeiro frame do seu código;
- separar causa, consequência e hipótese;
- corrigir uma falha benigna e provar a regressão;
- entregar pacote reproduzível, minimizado e com limpeza definida.

## Símbolos e identidade do build

Um símbolo associa endereços a nomes, arquivos e linhas. O PDB precisa corresponder ao binário analisado; um PDB “parecido” pode produzir stacks enganosas. Preserve executável, DLL, PDB, configuração de compilação, commit e hash como uma unidade.

Símbolos públicos do Windows ajudam a resolver componentes do sistema, mas não substituem os símbolos privados da fixture. Configure cache local e servidor oficial conforme a política do laboratório. Não envie dump privado a serviço externo.

Antes da análise, registre:

- arquitetura do processo e do depurador;
- versão e hash de cada binário próprio;
- caminho dos símbolos e resultado do carregamento;
- método e horário da captura;
- ação exata que reproduziu a falha.

## Fluxo de triagem de user-mode dump

Abra somente um mini dump da aplicação fixture. O fluxo inicial é:

```text
.sympath                 ; revisar caminho de símbolos
.reload /f               ; recarregar e observar diagnósticos
lm                       ; listar módulos e versões
!analyze -v              ; resumo automatizado da exceção
.ecxr                    ; contexto do registro de exceção, quando aplicável
k                        ; stack da thread atual
~                        ; lista de threads
```

Comandos variam conforme tipo do dump e extensão carregada. Leia a saída em vez de copiar comandos mecanicamente. `!analyze -v` produz uma hipótese automatizada; ele não substitui inspeção.

Primeiro confirme exception code, endereço e módulo. Depois selecione o contexto correto e leia a stack do ponto da falha para os chamadores. Procure o primeiro frame do seu código com símbolos confiáveis. Analise parâmetros e estado que realmente estejam disponíveis. Valores ausentes em mini dump continuam desconhecidos.

Uma exceção em função do sistema pode ter sido causada por um ponteiro inválido enviado pela aplicação. Inversamente, o primeiro frame próprio pode apenas estar tratando uma falha originada antes. Compare fonte, logs e trace.

## Limites e proteção de dados

Dump pode conter caminhos, argumentos, trechos de arquivo e segredos presentes na memória. Neste módulo:

- capture somente a fixture compilada para o curso;
- use dados artificiais e conta sem privilégios;
- prefira mini dump;
- armazene em diretório com acesso limitado;
- registre hash e retenção;
- exclua o dump depois que o relatório minimizado for validado.

Não capture LSASS, navegador, gerenciador de senhas, antivírus, processo de terceiro nem dump completo do host. Kernel dump também fica fora do exercício principal.

## Projeto: Diagnostic Workbench

Você construirá uma pequena aplicação local que lê um conjunto de arquivos fixture, chama uma DLL própria para calcular uma estatística e exporta um relatório JSON. Um modo explícito de teste produz uma destas falhas benignas:

1. DLL renomeada, causando falha de carregamento;
2. versão de ABI incompatível detectada antes da chamada;
3. entrada inválida rejeitada com código documentado;
4. exceção controlada em build de laboratório para gerar mini dump.

Nenhuma falha deve envolver corrupção explorável, processo remoto ou desativação de proteção. A implementação detalhada está em `projetos/diagnostic-workbench/README.md`.

### Fase 1 — contrato e build

Defina entrada, saída, versão do esquema, códigos de erro e ABI. Compile executável e DLL com símbolos e mitigações padrão. Registre comandos, toolchain e hashes. Teste execução saudável antes de injetar qualquer falha.

### Fase 2 — observabilidade

Adicione logs estruturados com UTC e correlation ID. Use ProcMon com filtro no executável, Process Explorer para módulos e uma captura ETW curta somente se responder a uma pergunta. Exporte evidência mínima.

### Fase 3 — automação

Crie módulo PowerShell que prepara fixtures, executa cenário, valida JSON e limpa o diretório. Use `ShouldProcess` em alterações, Pester para contrato e PSScriptAnalyzer. Repetir a preparação deve produzir o mesmo estado.

### Fase 4 — desempenho

Defina orçamento, aqueça, faça pelo menos vinte repetições e informe mediana e p95. Se capturar WPR, delimite somente uma execução representativa. Não altere proteção para melhorar números.

### Fase 5 — falha e correção

Ative uma falha benigna, reproduza uma vez, capture somente a evidência necessária e formule hipóteses. Para exceção controlada, abra o mini dump no WinDbg, confirme símbolos e encontre o primeiro frame próprio. Corrija, acrescente teste de regressão e repita o cenário saudável.

### Fase 6 — entrega e limpeza

Entregue fonte, build reproduzível, hashes, testes, relatório causal, comparação de desempenho, inventário defensivo redigido e instruções de limpeza. Não inclua dump ou ETL bruto no pacote público; entregue apenas sumário sanitizado, salvo exigência do ambiente fechado.

## Rubrica

| Critério | Peso | Evidência esperada |
|---|---:|---|
| Modelo NT, PE e DLL correto | 20% | contrato, ABI, carregamento e explicação |
| Reprodutibilidade | 20% | versão, comandos, hashes e fixture |
| Investigação causal | 20% | hipótese, evidência, limites e conclusão |
| Automação segura | 15% | módulo, testes, idempotência e limpeza |
| Correção e regressão | 15% | patch focal e teste que falhava antes |
| Minimização de dados | 10% | retenção, acesso e relatório sanitizado |

Uma entrega sem limpeza, com símbolos incompatíveis ou baseada apenas em `!analyze -v` não atinge os critérios mínimos.

## Exercícios

1. Compare uma stack com e sem PDB correto e registre a diferença.
2. Analise uma exceção controlada e marque fatos, inferências e dados ausentes.
3. Faça revisão cruzada do relatório: outra pessoa consegue reproduzir sem informação oral?
4. Execute o procedimento de limpeza e confirme que apenas o relatório minimizado permaneceu.

## Checklist

- [ ] Binário e PDB pertencem exatamente ao mesmo build.
- [ ] O dump é somente da fixture própria e possui retenção curta.
- [ ] A causa não foi deduzida apenas do resumo automatizado.
- [ ] A correção possui teste de regressão e nova medição.
- [ ] A entrega é reproduzível, segura e livre de artefatos sensíveis.

