# Lab 04 — ETW, WPR/WPA e desempenho

**Classe:** B — captura curta de fixture própria, com ETL tratado como dado sensível.

## Propósito

Transformar uma percepção de lentidão em experimento mensurável. O gate combina ETW, Event Log, Sysinternals e análise de desempenho para testar uma hipótese, sem “otimizadores” nem desativação de serviços ou proteções.

## Pré-condições

- Lab 03 e capítulos 14–16 concluídos;
- guia transversal de tracing e debugging revisado;
- Windows Performance Toolkit instalado por fonte oficial;
- conjunto fixture fixo, sem documentos reais;
- snapshot, espaço para ETL e diretório com acesso restrito.

Defina limite de tamanho e retenção antes de capturar. Se o ETL crescer além do limite, pare a sessão; não mova a captura indiscriminadamente para outro volume.

## Cenário e hipótese

Use uma operação local, por exemplo calcular SHA-256 de 500 arquivos sintéticos. Registre tamanho e hash do manifesto de entrada. Escreva uma hipótese específica: “a primeira execução é mais lenta por leitura e carregamento; após duas rodadas de aquecimento, o p95 ficará abaixo de X ms”.

Fixe versão do script, estado de energia e concorrência conhecida. Faça duas rodadas de aquecimento que não entram nas estatísticas. Em seguida execute vinte repetições, guardando duração individual e resultado funcional.

Calcule mínimo, mediana, p95 e máximo sem remover outliers. Se uma interrupção externa ocorreu, registre-a; não apague silenciosamente a amostra.

## Captura orientada por pergunta

Escolha um perfil WPR que cubra apenas CPU e File I/O necessários. Anote providers/perfil, buffers quando visíveis, horário de início e final. Capture uma execução representativa, não as vinte. Pare imediatamente depois e confirme se houve perda ou aviso.

No WPA:

1. selecione a região temporal da fixture;
2. filtre pelo processo correto e confirme PID/horário;
3. examine CPU Usage e File I/O com unidades visíveis;
4. agrupe por processo, thread, caminho sanitizado e stack conforme necessário;
5. confirme símbolos antes de nomear funções;
6. exporte somente tabela ou screenshot que sustente a conclusão.

Um hotspot não é automaticamente defeito. Diferencie tempo de CPU, espera, duração da operação e bytes transferidos. Se stacks não resolverem, declare o limite.

## Alteração única

Escolha uma mudança benigna derivada da evidência, como processar a lista já enumerada em vez de enumerar novamente. Não altere Defender, mitigação, cache do sistema ou serviço. Repita aquecimento e vinte medições com o mesmo conjunto.

Compare diferença absoluta e relativa, dispersão e resultado funcional. Se não houver melhoria consistente, rejeite a hipótese ou proponha próximo teste; não reformule a métrica depois de ver o resultado.

## Correlação

Consulte Event Log somente na janela do experimento e registre provider, canal, ID, record ID e UTC. Ausência de evento não invalida ETW. Explique a diferença entre counter amostrado, evento de trace e registro persistido.

## Critérios de aceite

- cenário, entrada, orçamento e hipótese foram escritos antes da medição;
- duas rodadas de aquecimento e vinte amostras brutas estão preservadas;
- ETL cobre apenas uma janela curta e não contém dados reais;
- uma única variável mudou e a função continuou correta;
- conclusão admite ruído, símbolos ausentes e limites estatísticos.

## Cleanup e revisão

Confirme que nenhuma sessão permaneceu ativa. Exporte relatório sanitizado, registre hash e apague ETL bruto conforme retenção. Restaure a fixture e remova arquivos temporários.

Responda: p95 com vinte amostras representa o quê? Que evidência separa CPU de espera por I/O? A captura alterou a duração? Por que melhoria em uma VM não pode ser generalizada automaticamente para outro hardware?

