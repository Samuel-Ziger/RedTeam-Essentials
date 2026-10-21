# 07 — Contas, SIDs, tokens, permissões e UAC

Segurança local separa identidade, autenticação e autorização. Uma pessoa prova
quem é; o sistema cria um token; objetos avaliam esse token contra descritores
de segurança. Compreender o fluxo evita tratar “administrador” como solução
universal.

## Objetivos

- distinguir conta, SID, grupo, token, privilégio e ACL;
- aplicar privilégio mínimo a uma conta cotidiana;
- prever herança e permissões efetivas em uma fixture;
- explicar o que UAC faz e o que não faz;
- criar e remover uma identidade temporária sem depender de idioma do sistema.

## Identidade e autorização

Uma conta local recebe um Security Identifier. O nome pode mudar; o SID continua
identificando a entidade. Grupos agregam membros e simplificam concessões. Ao
iniciar uma sessão, o Windows constrói um token com SID da conta, grupos,
privilégios e outros atributos. O acesso a um objeto é decidido usando esse
contexto e o descritor de segurança do objeto.

```powershell
Get-LocalUser | Select-Object Name, Enabled, LastLogon, SID
Get-LocalGroup | Select-Object Name, SID
whoami /user
whoami /groups
whoami /priv
```

Não publique lista de contas reais. Faça a coleta na VM e sanitize nomes. Nomes
de grupos são localizados; scripts portáveis devem descobrir o grupo correto ou
usar SIDs conhecidos com cuidado, não assumir a palavra `Administrators`.

## ACL, ACE e herança

Uma ACL contém entradas de controle de acesso associadas a identidades. Cada ACE
descreve permitir ou negar um conjunto de direitos, além de regras de herança.
Proprietário tem papel distinto de uma permissão simples. `Read`, `Write`,
`Modify` e `FullControl` não são equivalentes; `Modify` normalmente permite
exclusão, enquanto `FullControl` inclui alterar permissões e tomar ações maiores.

```powershell
$fixture = 'C:\RTE-Lab\dados'
$acl = Get-Acl -LiteralPath $fixture
$acl | Select-Object Owner, AreAccessRulesProtected, AccessToString
$acl.Access |
  Select-Object IdentityReference, FileSystemRights, AccessControlType,
    IsInherited, InheritanceFlags, PropagationFlags
```

Permissão efetiva resulta da combinação do token, ACEs aplicáveis, herança e
contexto da operação. Uma entrada `Deny` explícita pode superar concessões e
torna o modelo difícil de manter. Prefira grupos e concessões mínimas. Não
“corrija” acesso dando `Everyone: FullControl`.

Atributo ReadOnly não é ACL. O primeiro é metadado de arquivo; a segunda decide
operações conforme identidade. O laboratório deve demonstrar essa diferença.

## UAC e elevação

Um membro do grupo administrativo normalmente opera aplicações com token
filtrado. Quando uma ação requer elevação, o UAC pede consentimento ou credencial
e cria um processo em outro contexto. A janela elevada não transforma todas as
janelas já abertas nem concede privilégio à pessoa para sempre.

UAC reduz alterações administrativas acidentais e torna a fronteira visível,
mas não é uma fronteira de segurança completa contra código já executado pelo
mesmo usuário. A estratégia correta é conta cotidiana comum, elevação pontual,
software confiável e sistema atualizado.

Cancelar um prompt é uma opção válida. Leia editor, origem e ação solicitada.
Prompts inesperados são motivo para interromper o fluxo, não para treinar o
reflexo de clicar “Sim”.

## Autenticação e recuperação doméstica

Senha, PIN do Windows Hello e conta não são o mesmo objeto. Um PIN do Hello é
associado ao dispositivo e protegido pelo mecanismo disponível; a senha da conta
pode ter outro alcance. Métodos biométricos desbloqueiam credenciais e exigem
alternativa de recuperação. Nunca registre segredo real no laboratório.

Desabilitar uma conta impede novas autenticações, mas não apaga perfil ou dados.
Excluir conta antes de decidir o destino do perfil pode produzir perda. O lab
usa conta temporária e fixtures, nunca a única conta administrativa.

## Prática controlada

Crie uma conta local comum temporária por interface suportada, sem usar um
segredo real. Crie `C:\RTE-Lab\dados`, exporte sua ACL e gere três arquivos com
hashes. Conceda leitura por uma entrada explícita apenas nessa pasta, teste
leitura e tentativa de escrita na sessão temporária e registre a matriz
`identidade × operação × resultado`.

Depois remova somente a entrada criada, compare a ACL com a baseline, desabilite
e exclua a conta e confirme que nenhuma sessão a utiliza. Restaure snapshot se
o estado final divergir. Não altere ACL de perfil, `Windows` ou `Program Files`.

## Exercícios

1. Desenhe conta → SID → grupos → token → ACL → decisão.
2. Explique nome de conta versus SID e autenticação versus autorização.
3. Preveja o efeito da herança antes de criar a ACE do laboratório.
4. Compare usuário comum, administrador não elevado e processo elevado.
5. Demonstre por que ReadOnly não impede escrita da mesma maneira que uma ACL.

## Checklist de domínio

- [ ] Distingo conta, grupo, SID, token, privilégio, ACL e ACE.
- [ ] Uso conta comum e elevação somente no passo necessário.
- [ ] Não codifico nome localizado de grupo sem descoberta.
- [ ] Prevejo herança e valido permissão efetiva com duas identidades.
- [ ] Não uso `Deny` ou `FullControl` como atalho.
- [ ] Entendo que UAC não substitui privilégio mínimo.
- [ ] A conta e a ACE temporárias foram removidas com evidência do rollback.
