# 04 — Tokens, privilégios, sessões e níveis de integridade

O token representa o contexto de segurança de um processo ou thread. Ele contém
identidades e atributos usados na decisão de acesso; não é uma lista simples de
“permissões”. Este capítulo observa tokens próprios sem duplicar, manipular ou
capturar tokens alheios.

## Objetivos

- distinguir token primário, identidade, grupos e privilégios;
- explicar acesso pedido, ACL, privilégio e integridade como dimensões;
- comparar sessão comum e elevada de forma segura;
- interpretar Mandatory Integrity Control e AppContainer em alto nível;
- reconhecer limites de Session 0 e processos protegidos.

## Conteúdo do token

Um token inclui SID do usuário, SIDs de grupos, privilégios, owner, primary group,
default DACL, session ID, tipo, nível de integridade e outros atributos. Grupos
podem estar habilitados, desabilitados ou usados somente para negação. Privilégio
pode estar presente e desabilitado até uma operação autorizada precisar dele.

```powershell
whoami /user
whoami /groups
whoami /priv
whoami /all
Get-Process -Id $PID | Select-Object Id, SessionId, Path
```

Sanitize nomes. Execute uma vez em Terminal comum e outra numa janela elevada
aberta por consentimento/credencial. Não habilite privilégios manualmente.

## Token primário e de thread

Processo normalmente possui token primário que define seu contexto. Uma thread
pode temporariamente operar com outro contexto autorizado para atender uma
solicitação; isso é impersonation legítima usada por serviços. O curso aborda o
modelo, não ensina a obter, duplicar ou reutilizar tokens.

Ao diagnosticar, registre se a ação ocorre como processo ou thread e qual conta
de serviço é documentada. Não conclua “roda como usuário X” apenas pelo nome da
janela.

## Security Reference Monitor e acesso

Uma operação pede direitos específicos sobre um objeto. O sistema considera
token, descritor de segurança, ACEs, owner, integridade e políticas aplicáveis.
Privilégios tratam capacidades especiais e não substituem genericamente ACL.

Ser membro de Administrators não garante que o processo atual tem token elevado.
UAC normalmente cria contexto filtrado e elevação separada. `SeBackupPrivilege`
presente/desabilitado não significa que qualquer arquivo será lido automaticamente.
Evite explicações como “admin pode tudo”.

## Mandatory Integrity Control

Níveis de integridade, como low, medium, high e system, participam de uma política
obrigatória que restringe escrita de sujeitos de menor integridade em objetos de
maior integridade. Não substituem ACL: são uma verificação adicional.

Aplicações comuns normalmente operam em medium; processo elevado em high.
Ambientes isolados podem usar low/AppContainer e capabilities. AppContainer
restringe recursos e concede capacidades declaradas; não é simplesmente uma
conta local diferente.

Protected Process Light adiciona regras sobre quem pode abrir certos processos.
Ao encontrar acesso negado, registre a fronteira. Este módulo não desativa PPL
nem inspeciona processos de segurança.

## Sessões, desktops e Session 0

Session ID separa contextos logon/interativos. Serviços ficam normalmente na
Session 0, isolada das sessões interativas. Window station e desktop controlam
objetos gráficos dentro de uma sessão. Esses eixos não equivalem à identidade:
processos de contas diferentes podem estar numa sessão, e a mesma conta pode ter
múltiplas sessões.

Evite serviços que tentem apresentar UI diretamente ao usuário. Comunicação
segura entre componentes exige arquitetura própria, abordada no módulo empresarial
quando houver necessidade; aqui apenas analisamos processos locais.

## Comparação segura de elevação

Colete `whoami /all` nas duas janelas e transforme em uma tabela:

- SID da conta: deve permanecer o mesmo no cenário de consentimento;
- grupos e atributos: identifique entradas habilitadas/diferentes;
- privilégios: presença e estado;
- integrity level: medium versus high esperado;
- PID/session: processos distintos, mesma ou outra sessão conforme ambiente.

Não salve nomes reais. Rotule a conta `lab-user`. Feche a janela elevada após a
coleta. O objetivo é explicar diferença, não manter sessão privilegiada.

## Falhas comuns

- tratar privilégio como permissão de arquivo;
- assumir que grupo presente está habilitado;
- confundir token elevado com outra identidade;
- chamar integrity level de “nível de usuário”;
- inferir conta pela Session ID;
- tentar contornar PPL ou acesso negado.

## Exercícios

1. Desenhe token → direito solicitado → descritor → integridade → decisão.
2. Compare duas sessões próprias e destaque apenas diferenças relevantes.
3. Explique token primário versus contexto temporário de thread sem demonstrar manipulação.
4. Modele uma ACL que permite, mas integridade que restringe escrita.
5. Classifique grupo, privilégio, capability, SID e integrity level.

## Checklist de domínio

- [ ] Token não é reduzido a conta ou lista de permissões.
- [ ] Distingo SID, grupo, privilégio, ACL e integrity level.
- [ ] Elevação é outro processo/contexto e permanece pontual.
- [ ] Session ID não identifica conta nem privilégio.
- [ ] AppContainer e PPL são fronteiras respeitadas.
- [ ] Comparações usam apenas processos e sessões próprios.
- [ ] Nenhum privilégio é habilitado ou token é duplicado no laboratório.
