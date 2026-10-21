# 11 — Contas de serviço, gMSA e Windows LAPS

Contas de serviço devem ter owner, finalidade, logon permitido, direitos,
dependências, rotação e retirada. Senha estática compartilhada é o pior caso.

## Tipos

- virtual account/built-in identity para serviço local;
- standalone MSA para cenários específicos;
- gMSA com senha gerenciada e hosts autorizados;
- conta comum apenas quando compatibilidade exige, com vault/rotação.

gMSA depende de AD/KDS, tempo e distribuição correta. O curso projeta objetos,
ACL e rollout, mas não cria KDS root key ou instala a conta antes de redes.

## Windows LAPS

LAPS gerencia senha de administrador local e pode armazená-la em AD ou Entra,
com ACLs, histórico/expiração e proteções conforme plataforma. Determine quem
pode ler, auditar, rotacionar e recuperar. Nunca exporte senhas para relatório.

## Break-glass

Conta de emergência tem uso raro, monitorado e testado, segredo em controle
forte, dupla aprovação quando aplicável e rotação após uso.

## Exercício

Modele inventário de contas de serviço e matriz LAPS sem qualquer segredo.

