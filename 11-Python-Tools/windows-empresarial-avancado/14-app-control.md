# 14 — Application Control for Windows e AppLocker

Application Control define quais binários, scripts, installers, DLLs e drivers
podem executar conforme tipo de regra/política. AppLocker atende outros cenários
e ambos exigem entender edição, enforcement e limitações atuais.

## Regra por confiança

Publisher/signature geralmente resiste melhor a update que hash; hash é exato
e frágil; path depende fortemente de ACL — diretório gravável pelo usuário não
deve conferir confiança ampla.

## Rollout

Inventário → base policy → supplemental policies → audit → coleta de eventos
→ correção de gaps → piloto → enforce → emergency procedure → manutenção.

Inclua scripts, MSI, DLLs e drivers conforme o modelo; testar só EXEs deixa
lacunas. Política assinada pode ser mais difícil de remover: pratique em VM com
recovery e siga procedimento oficial.

## Exercício

Gere inventário de publishers/hashes de fixtures, proponha regras e eventos de
audit. Não aplique enforcement ao host nem crie regra ampla por `C:\`.

