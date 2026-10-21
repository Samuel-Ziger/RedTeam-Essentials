# 00 — Método e laboratório

## Objetivos

- separar observação, hipótese, mudança e validação;
- preparar um Mac sem dados pessoais ou uma VM autorizada;
- produzir evidência sem coletar identificadores desnecessários.

## Ambiente

Use um Mac suportado com uma conta de estudante separada. Em hardware real,
confirme um backup restaurável antes de alterar armazenamento, contas ou boot.
VMs de macOS devem respeitar licença e hardware autorizados. Não publique serial,
UUID de hardware, Conta Apple, nomes reais ou conteúdo do Keychain.

Crie um diário com: objetivo, estado inicial, comando/gesto, saída sanitizada,
pós-condição e reversão. Um print sem contexto não é evidência suficiente.

## Ciclo de experimento

1. Defina uma pergunta verificável.
2. Colete o baseline com conta sem privilégio.
3. Exporte o objeto que será alterado.
4. Mude apenas uma variável.
5. Compare resultado observado e esperado.
6. Reverta e confirme as proteções.

## Prática

Registre `sw_vers`, `uname -m`, estado de FileVault, SIP e Gatekeeper sem serial.
Classifique cada dado como necessário, sensível ou descartável. O laboratório
termina com um checklist de restauração, não apenas com comandos executados.
