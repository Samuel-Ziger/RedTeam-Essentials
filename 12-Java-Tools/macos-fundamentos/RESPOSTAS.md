# Respostas orientativas

## Por que administrador não equivale a acesso irrestrito?

Porque autorização administrativa, SIP, SSV, sandbox, TCC e proteções de
hardware operam em camadas distintas. `sudo` eleva uma decisão Unix; não
remove automaticamente as demais políticas.

## Volume e partição são sinônimos?

Não. Uma partição ocupa uma região física/lógica do dispositivo. Um container
APFS pode ocupar uma partição e compartilhar espaço entre vários volumes.

## Por que copiar arquivos não prova um backup?

Um backup exige escopo conhecido, integridade, retenção, separação do original
e restauração testada. Uma cópia inacessível ou incompleta não atende ao RPO.

## O que fazer quando um app é bloqueado?

Confirme origem, hash, assinatura, notarização e necessidade. Não remova o
atributo de quarentena nem desative Gatekeeper como primeira resposta.

## Como diferenciar causa de correlação em logs?

Construa uma linha do tempo, reproduza com uma única variável e procure a
primeira divergência. Uma mensagem próxima ao sintoma pode ser apenas efeito.

## O projeto final está concluído quando?

Quando outra pessoa consegue entender o baseline, repetir uma mudança,
restaurar a fixture e demonstrar que FileVault, SIP e Gatekeeper permaneceram
ativos.
