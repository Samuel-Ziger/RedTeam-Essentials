# Laboratórios integradores

Os seis laboratórios são gates de competência, não receitas de comandos. Cada um depende dos capítulos e do gate anterior indicados na aplicação de estudos. Realize-os em VM descartável, com conta comum e fixtures sintéticas.

| # | Laboratório | Classe | Resultado verificável |
|---:|---|---|---|
| 01 | [Processo, token e memória](01-processo-token-memoria.md) | B | mapa observado de uma fixture |
| 02 | [PE e DLL](02-pe-dll.md) | B | build reproduzível e carga segura |
| 03 | [ProcMon e Registro](03-procmon-registro.md) | B | investigação filtrada e reversível |
| 04 | [ETW e desempenho](04-etw-performance.md) | B | hipótese medida com trace mínimo |
| 05 | [Defesa local](05-defesa-local.md) | B/C | piloto documentado sem reduzir proteção |
| 06 | [Dump e projeto](06-dump-projeto.md) | C | causa, correção e regressão demonstradas |

As classes seguem o contrato do capítulo 00: A é observação; B altera somente fixture; C usa captura sensível ou política em snapshot com aprovação; D é proibida no curso. Se o alvo ficar ambíguo, o snapshot estiver ausente, a ferramenta mostrar processo externo ou uma proteção pedir para ser desativada, pare.

Para cada gate, entregue diário com hipótese, ambiente, comandos, saídas relevantes, hashes, interpretação, limitações e cleanup. “Executou sem erro” não é critério de aceite. Dumps e traces brutos não entram em repositório; preserve apenas relatório sanitizado.

