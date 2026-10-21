# Glossário

| Termo | Definição curta |
|---|---|
| adapter | implementação que traduz uma porta do núcleo para tecnologia externa |
| ADR | registro curto de uma decisão arquitetural, contexto e consequências |
| artefato | arquivo produzido para distribuição ou implantação |
| atomicidade | propriedade de uma operação que confirma tudo ou não confirma nada no limite declarado |
| backoff | aumento deliberado do intervalo entre novas tentativas |
| bundle | conjunto de recursos transformados e empacotados para execução |
| canário | valor sintético reconhecível usado para detectar vazamento ou caminho inesperado |
| canonicalização | escolha de uma representação única para valores equivalentes |
| capability | capacidade explícita concedida a componente ou extensão |
| circuit breaker | controle que interrompe chamadas repetidamente falhas e testa recuperação depois |
| collation | regras culturais de comparação e ordenação de texto |
| command | ação da interface representada por contrato reutilizável |
| commit | ponto em que um novo estado se torna o estado confirmado |
| composition root | lugar onde implementações concretas são criadas e conectadas |
| configuração | valor externo que varia comportamento entre execuções |
| contrato | comportamento observável, pré-condições, pós-condições e falhas prometidas |
| correlação | identificador que liga eventos pertencentes à mesma operação |
| CSP | política do navegador que restringe origens e tipos de conteúdo executável |
| debounce | adia execução até cessar uma sequência rápida de eventos |
| deep link | endereço que abre diretamente um estado ou recurso significativo |
| degradação graciosa | preservação da função essencial quando capacidade secundária falha |
| DTO | estrutura criada para transportar dados entre fronteiras |
| feature flag | configuração controlada que ativa comportamento sem novo artefato |
| fixture | entrada estável preparada para reproduzir um cenário de teste |
| fluxo unidirecional | eventos geram estado, que gera apresentação |
| framing | regra para delimitar mensagens em um fluxo de bytes |
| graceful shutdown | encerramento que para novas tarefas e conclui/cancela as atuais de modo definido |
| i18n | preparação técnica para múltiplos idiomas/culturas |
| idempotência | propriedade em que repetir a mesma operação não cria efeito adicional indevido |
| invariante | condição que deve permanecer verdadeira em todos os estados válidos |
| jitter | variação aleatória controlada aplicada a intervalos de retry |
| l10n | adaptação concreta para idioma/cultura |
| landmark | região semântica de página usada para navegação assistiva |
| lockfile | registro resolvido de versões usado para instalações repetíveis |
| local-first | dados e resposta locais são centrais à experiência |
| manifest | documento que declara identidade, versão, conteúdo ou capacidades |
| migração | transformação de formato/schema entre versões |
| orçamento de desempenho | limite mensurável associado a cenário, ambiente, volume e percentil |
| origin | combinação de esquema, host e porta que delimita políticas e Storage na web |
| pacote self-contained | artefato que inclui runtime necessário |
| percentil | valor abaixo do qual cai determinada fração das observações, como p95 |
| presenter | componente que converte resultado/estado em dados de apresentação |
| progressive enhancement | construção que preserva uma base semântica funcional antes de capacidades adicionais |
| proveniência | evidência verificável sobre origem e processo de produção de um artefato |
| pseudolocalização | transformação de texto que simula expansão e caracteres de outros idiomas |
| reducer | função pura que calcula estado a partir de estado e evento |
| reflow | reorganização do conteúdo para permanecer utilizável em zoom ou viewport estreito |
| request ID | identificador de uma tentativa usado para correlacionar ou descartar resposta antiga |
| retry | nova tentativa deliberada sob política de limite, atraso e idempotência |
| rollback | retorno controlado a estado ou versão anterior conhecido |
| rollout | liberação gradual de uma versão ou funcionalidade |
| runbook | procedimento operacional reproduzível com verificações e condições de parada |
| sanitização de diagnóstico | remoção ou transformação de dados que não podem compor a evidência |
| SBOM | inventário dos componentes de software presentes em um artefato |
| schema | contrato estrutural e semântico de dados |
| selector | função pura que deriva uma visão de um estado existente |
| SemVer | convenção de versão maior, menor e patch vinculada a compatibilidade declarada |
| snapshot | fotografia coerente de estado usada para persistir, comparar ou recuperar |
| SLO | objetivo mensurável para uma característica de serviço ou produto |
| stdout/stderr | canais de resultado e diagnóstico de um processo CLI |
| telemetria | dados enviados para observar uso e falhas, sob política |
| throttle | limita quantas execuções ocorrem em uma janela de tempo |
| timeout | limite após o qual a espera termina com resultado definido |
| TTY | terminal interativo conectado à entrada/saída |
| view-model | estado e comandos preparados para uma view, sem depender de widgets concretos |
| WCAG | diretrizes W3C para acessibilidade de conteúdo web |
