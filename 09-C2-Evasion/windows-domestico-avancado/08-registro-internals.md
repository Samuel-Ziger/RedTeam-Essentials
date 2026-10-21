# 08 — Registro internals: hives, views, ACL e observação

O módulo 08 ensinou chaves e valores. Agora o Registro é visto como subsistema:
hives persistentes, logs, namespace, contexto de usuário e compatibilidade. O
objetivo é diagnosticar uma fixture, nunca montar ou editar hive real offline.

## Objetivos

- relacionar roots lógicas a hives e identidade;
- explicar persistência, logs e carregamento sem editar arquivos de hive;
- distinguir views 32/64 bits e virtualization legada;
- interpretar ACL de chave e momento de leitura;
- capturar consultas da própria fixture com filtro estreito.

## Hives e namespace

Configuration Manager implementa o Registro no kernel e monta hives num namespace
hierárquico. Hives persistentes usam arquivos e logs para consistência; outros
dados podem ser construídos em memória. HKLM, HKU e demais roots são visões
convenientes, não cada uma necessariamente um arquivo único.

HKCU aponta para o hive do usuário no contexto atual sob HKEY_USERS. Uma tarefa
executada por outra identidade vê outro HKCU. HKCR é uma visão combinada de
classes por máquina e usuário. Diagnóstico sempre registra identidade, arquitetura
do processo, root e caminho completo.

Não copie arquivos de hive enquanto ativos nem os abra como texto. Backup e
restore do Registro usam mecanismos suportados. O laboratório permanece em
`HKCU\Software\RTECourse\Advanced`.

## Chaves, valores e notificações

Handle de chave mantém contexto de acesso. Valor tem nome, tipo e dados. Aplicação
pode abrir chave uma vez, manter handle, armazenar configuração em cache ou usar
notificação de mudança. Portanto editar valor não garante efeito imediato; o
consumidor precisa reler conforme seu design.

Observe quando a fixture lê: startup, primeira operação ou cada chamada. Isso
define se reiniciar somente a fixture é necessário. Não reinicie Windows por
hábito.

## Views 32 e 64 bits

Em x64, partes do Registro oferecem visões distintas para processos de
arquiteturas diferentes. Ferramentas permitem escolher explicitamente:

```powershell
reg.exe query HKCU\Software\RTECourse\Advanced /reg:64
reg.exe query HKCU\Software\RTECourse\Advanced /reg:32
```

Ausência numa view não prova ausência na outra. Redirecionamento e reflexão têm
regras dependentes da área/versão; não generalize `WOW6432Node` para toda chave.
Use APIs/flags documentadas e compare fixtures x86/x64.

## Registry virtualization

Virtualization ajuda certos aplicativos legados sem manifesto quando tentam
gravar locais protegidos, redirecionando parte do estado por usuário. Não é
recurso para novos aplicativos, mecanismo de segurança nem garantia universal.
Aplicações bem projetadas usam local apropriado e manifesto.

Se uma escrita “funciona” para usuário comum, não conclua que alterou HKLM.
Verifique processo, manifesto, caminho real e ProcMon. O curso não depende de
virtualization; apenas aprende a reconhecê-la.

## ACL e privilégio

Chaves têm descritores de segurança. Direito de ler valor, criar subchave ou
alterar ACL são diferentes. Elevação não deve ser usada para superar um design
incorreto. A fixture em HKCU funciona como conta comum.

Exportar chave registra nomes/tipos/dados, mas não captura todos os consumidores,
handles/caches ou dependências. Snapshot permanece rollback amplo.

## ProcMon orientado por hipótese

Prepare o filtro antes de capturar:

1. `Process Name` ou PID igual à fixture;
2. categoria Registry;
3. path começa pela chave do curso;
4. intervalo de uma execução;
5. colunas Operation, Path, Result e Detail.

Pare captura, limpe buffer, inicie, reproduza, pare e exporte cinco a vinte
eventos. `NAME NOT FOUND` pode ser busca opcional seguida de fallback. Só é causa
se a aplicação exige o valor e o comportamento muda quando ele existe.

## Fixture recomendada

Crie String `Mode=baseline`, faça script próprio ler e retornar objeto com
`Present`, `Type` e `Value`. Capture. Remova o valor, capture novamente e faça a
fixture usar default explícito. Restaure o valor e comprove cleanup removendo
somente a chave Advanced.

## Exercícios

1. Desenhe root lógica, hive, chave, handle, valor e consumidor.
2. Compare a chave em processo PowerShell x64 e x86, quando disponível.
3. Demonstre cache versus releitura numa fixture própria.
4. Explique três `NAME NOT FOUND` benignos e um realmente causal.
5. Exporte ACL/dados da chave antes e prove rollback após o trace.

## Checklist de domínio

- [ ] Roots lógicas não são reduzidas a um arquivo cada.
- [ ] HKCU depende da identidade do processo.
- [ ] View 32/64 é registrada em toda comparação.
- [ ] Virtualization legada não é solução de design.
- [ ] ACL, tipo, dado e momento de leitura são analisados separadamente.
- [ ] ProcMon captura apenas fixture, chave e intervalo necessários.
- [ ] Nenhum hive real é montado, copiado ou editado offline.
