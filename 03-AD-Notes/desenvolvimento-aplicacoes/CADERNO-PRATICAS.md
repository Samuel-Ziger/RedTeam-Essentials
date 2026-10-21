# Caderno de práticas — Desenvolvimento de aplicações

Este caderno contém 32 práticas curtas para consolidar os capítulos antes do
capstone. Faça-as em repositório descartável ou branch própria. Cada resposta
deve incluir hipótese, implementação ou modelo, teste e conclusão; “funcionou”
sem critério observável não encerra a prática.

Os níveis indicam profundidade, não ordem rígida:

- **N1 — leitura:** identificar e explicar um contrato;
- **N2 — construção:** implementar e testar uma fatia;
- **N3 — decisão:** comparar opções e defender trade-offs com evidência.

## Produto, CLI, configuração e erro

### 01 — Do adjetivo ao SLO local (N1)

Escolha “rápido”, “intuitivo” e “confiável”. Para cada termo, escreva cenário,
ambiente, volume, medida e limite. Acrescente uma condição que invalida a
conclusão. **Aceite:** outra pessoa consegue executar a medição sem perguntar o
que o adjetivo queria dizer.

### 02 — Jornada com falha tardia (N2)

Modele a jornada de conversão de 100 arquivos quando o item 87 falha. Defina
progresso, saída parcial, cancelamento, nova tentativa e relatório. **Aceite:** o
modelo distingue “nenhum efeito”, “parcial recuperável” e “commit completo”.

### 03 — Gramática de CLI (N2)

Escreva uma gramática pequena para um comando com subcomando, opção repetível,
`--`, entrada padrão e saída JSON. Crie dez vetores válidos e dez inválidos.
**Aceite:** comportamento de opção duplicada e valor vazio está explícito.

### 04 — Canais e códigos (N2)

Implemente uma CLI que produz resultado em `stdout`, diagnóstico em `stderr` e
códigos diferentes para uso e operação. Teste como processo filho. **Aceite:** o
teste afirma os três canais, não apenas uma substring.

### 05 — Matriz de precedência (N1)

Monte tabela verdade para padrão, arquivo, ambiente e CLI, incluindo ausência,
string vazia, valor inválido e duas fontes válidas. **Aceite:** cada linha aponta
fonte vencedora ou erro antes de efeitos.

### 06 — Canário de segredo (N2)

Injete uma credencial sintética e provoque parse, autenticação falsa e exceção.
Verifique logs, mensagens e pacote de diagnóstico. **Aceite:** um teste falha se
o canário aparecer em qualquer saída.

### 07 — Taxonomia de falhas (N1)

Classifique 15 falhas entre entrada, domínio, conflito, dependência, permissão,
indisponibilidade e defeito. Para cada classe, defina retry e próxima ação.
**Aceite:** entrada inválida nunca recebe retry automático.

### 08 — Commit após validação (N2)

Receba uma lista cujo último item é inválido. Converta/valide em cópia e só
substitua o estado após sucesso integral. **Aceite:** um teste compara identidade
ou conteúdo do estado antes e depois da falha.

## Dados, estado e desktop

### 09 — Schema exato (N2)

Defina documento versionado com cinco campos e limites. Gere fixtures para campo
ausente, extra, tipo errado, excesso e versão futura. **Aceite:** exportador e
importador compartilham a mesma regra sem aceitar dado assimétrico.

### 10 — Round-trip sem ilusão (N2)

Execute domínio → serialização → parse → domínio para Unicode, limites e lista
vazia. Diferencie igualdade semântica de igualdade byte a byte. **Aceite:** data,
ordem e normalização têm política declarada.

### 11 — Migração pura (N3)

Implemente `v1 → v2` como função sem I/O. Valide entrada e saída e preserve a
fixture original. **Aceite:** repetir migração tem resultado definido e versão
futura é recusada.

### 12 — Falha no replace (N3)

Projete escrita com temporário, flush e rename, ou snapshot em chave única.
Injete falhas em três pontos. **Aceite:** cada ponto possui estado recuperável e
limite de atomicidade documentado.

### 13 — Máquina de estados (N2)

Modele tarefa `idle/loading/success/error/cancelled`. Escreva tabela evento ×
estado e implemente transição pura. **Aceite:** evento impossível relevante é
rejeitado em vez de silenciosamente ignorado.

### 14 — Corrida de respostas (N2)

Simule duas buscas: a segunda termina primeiro. Use request ID ou cancelamento
para impedir regressão. **Aceite:** teste determinístico não usa `sleep` real.

### 15 — Presenter sem widget (N2)

Crie presenter que expõe rótulos, habilitação e comandos sem importar toolkit.
Use view falsa para testar erro e tarefa longa. **Aceite:** o teste roda sem
display e sem thread principal gráfica.

### 16 — Fechamento seguro (N3)

Modele janela com alteração não salva, gravação em andamento e gravação falha.
Defina salvar, descartar e cancelar. **Aceite:** falha ao salvar não fecha a
janela nem perde a oportunidade de exportar.

## Web, acessibilidade, API e localização

### 17 — Semântica nativa (N1)

Revise uma tela e substitua cinco `div` clicáveis por elementos corretos. Registre
o que deixou de ser necessário em ARIA/JavaScript. **Aceite:** nome, papel e ação
por teclado são verificáveis na árvore de acessibilidade.

### 18 — Renderização como texto (N2)

Insira o valor sintético `<img src=x onerror=alert(1)>` como título importado.
Use APIs de texto e confirme que aparece literalmente. **Aceite:** nenhuma API
que interprete HTML recebe conteúdo externo.

### 19 — Roteiro de teclado (N2)

Documente e execute cadastro, correção, filtro, importação e exclusão usando
Tab/Shift+Tab/Enter/Espaço/Escape. **Aceite:** foco visível e retorno após ação
dinâmica têm destino lógico.

### 20 — Reflow e pseudolocale (N2)

Teste viewport estreito, zoom 400% e textos 50% maiores. **Aceite:** tarefas
essenciais continuam disponíveis e a página comum não exige rolagem horizontal.

### 21 — Estados de cliente (N1)

Desenhe estados distintos para primeira carga, refresh, offline, stale, vazio,
erro e conflito. **Aceite:** nenhum estado combina “sem dado” e “mostrando dado
anterior” na mesma flag ambígua.

### 22 — Retry com relógio falso (N2)

Implemente backoff limitado com jitter injetável para uma leitura idempotente.
**Aceite:** testes afirmam agenda, limite e cancelamento sem esperar tempo real.

### 23 — Fila offline (N3)

Modele `pending/sending/confirmed/failed/conflict` com IDs idempotentes. Simule
reinício entre envio e resposta. **Aceite:** confirmação não cria duplicata e
conflito preserva versões local/remota.

### 24 — Tempo civil e instante (N3)

Compare “executar daqui a 24 horas” com “executar amanhã às 09:00 em São Paulo”.
Modele dados e teste transição de offset de uma zona IANA. **Aceite:** a escolha
entre `Instant` e data/hora local é justificada pelo domínio.

### 25 — Dinheiro e plural (N2)

Formate zero, um e muitos itens e valores monetários em `pt-BR` e `en-US`.
**Aceite:** cálculo não usa string formatada nem `float` sem política de erro.

## Diagnóstico, extensão, entrega e qualidade

### 26 — Evento estruturado (N2)

Defina evento `document_import_failed.v1` com correlação e razão enumerada.
Produza JSON e mensagem humana separadamente. **Aceite:** não há conteúdo do
documento, token ou caminho pessoal completo.

### 27 — Pacote de suporte (N3)

Monte um pacote local com manifesto, versões e eventos sintéticos. Ofereça
prévia e exclusão de itens. **Aceite:** nada é enviado automaticamente e o
canário da prática 06 não aparece no arquivo final.

### 28 — Registry de plugins (N2)

Registre plugins por ID/API/capacidade, rejeite duplicata e ordene execução.
Injete um plugin que lança exceção. **Aceite:** host continua operacional e
identifica a extensão responsável sem revelar entrada sensível.

### 29 — Compatibilidade (N3)

Crie matriz entre duas versões de app, duas de schema e três de plugin. Defina
upgrade, downgrade e versão futura. **Aceite:** cada célula importante diz
“aceita”, “migra” ou “recusa preservando dado”.

### 30 — Build limpo (N2)

Gere artefato em diretório novo, inventarie arquivos e calcule hash. Execute
fora do workspace. **Aceite:** nenhum caminho local, fixture secreta ou cache de
desenvolvimento é requisito acidental.

### 31 — Experimento de profiling (N3)

Defina orçamento, colete baseline repetido, use profiler, faça uma alteração e
meça novamente. **Aceite:** relatório inclui correção funcional e não atribui
causa apenas por correlação temporal.

### 32 — Ensaio de release e rollback (N3)

Crie release candidata, atualize dado sintético, provoque falha pós-upgrade e
execute rollback. **Aceite:** versão antiga não sobrescreve schema futuro; o
runbook contém condição de abortar, recuperação e pós-verificação.

## Registro de aprendizagem

Ao concluir cada bloco, responda:

1. qual hipótese foi refutada?
2. que invariante agora está automatizado?
3. que falha ainda depende de teste manual?
4. qual decisão merece ADR?
5. que evidência uma pessoa revisora conseguiria reproduzir?

Use as [respostas orientativas](RESPOSTAS.md) somente depois da primeira
tentativa. Elas descrevem propriedades esperadas, não uma implementação única.
