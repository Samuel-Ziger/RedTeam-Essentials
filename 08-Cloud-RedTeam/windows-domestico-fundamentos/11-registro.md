# 11 — Registro do Windows: modelo, visualizações e mudança segura

O Registro é um banco hierárquico usado por Windows e aplicativos. Ele não é uma
pasta comum, não precisa de “limpeza periódica” e não possui uma configuração
mágica universal. Toda edição deve partir de uma propriedade documentada e de
um rollback específico.

## Objetivos

- distinguir hive, chave, valor, tipo e dado;
- explicar HKLM, HKCU e contexto de usuário;
- reconhecer visualizações 32/64 bits;
- consultar e alterar somente uma chave de laboratório;
- exportar, validar e remover a mudança sem usar limpadores.

## Modelo hierárquico

Hives representam conjuntos persistentes ou projeções de configuração. Chaves
organizam subchaves e valores. Um valor possui nome, tipo e dado; o valor padrão
é apenas um valor especial, não “a configuração que sempre prevalece”. Tipos
como string, string expansível, múltiplas strings, DWORD, QWORD e binário têm
semânticas diferentes.

`HKEY_LOCAL_MACHINE` contém estado de máquina; `HKEY_CURRENT_USER` é uma visão
do hive associado ao usuário do processo. Portanto, executar a mesma automação
com outra conta pode consultar outro HKCU. `HKEY_CLASSES_ROOT` combina partes de
máquina e usuário para associações; não deve ser tratado como uma árvore
independente simples.

No PowerShell, os providers expõem `HKLM:` e `HKCU:` como drives, mas objetos do
Registro continuam diferentes de arquivos.

```powershell
Get-PSDrive -PSProvider Registry
Get-ChildItem -LiteralPath 'HKCU:\Software' |
  Select-Object -First 10 PSChildName, Name
```

## Laboratório isolado

Use exclusivamente `HKCU:\Software\RTECourse`:

```powershell
$path = 'HKCU:\Software\RTECourse'
New-Item -Path $path -Force | Out-Null
New-ItemProperty -Path $path -Name Lesson -PropertyType String `
  -Value 'registry-basics' -Force | Out-Null
New-ItemProperty -Path $path -Name Attempts -PropertyType DWord `
  -Value 1 -Force | Out-Null

Get-ItemProperty -LiteralPath $path |
  Select-Object Lesson, Attempts
```

Observe que o tipo foi declarado. Uma string contendo `1` e um DWORD com valor
1 não são equivalentes para consumidores. Depois da validação, liste o alvo e
remova somente essa chave:

```powershell
Get-Item -LiteralPath $path
Remove-Item -LiteralPath $path -Recurse -Confirm
Test-Path -LiteralPath $path
```

Snapshot protege o estado amplo da VM; exportar a chave registra um rollback
local. Um `.reg` não captura toda dependência externa e pode sobrescrever estado
novo quando importado. Leia o arquivo como texto antes de qualquer importação e
trate-o como código que altera configuração.

## Visualizações e arquitetura

Em Windows x64, processos de 32 e 64 bits podem receber visualizações diferentes
de partes do Registro. Assim, “a chave não existe” pode significar que a
ferramenta observou outra visão. Declare arquitetura do processo e API quando
diagnosticar. Não copie chaves entre visualizações tentando fazer aplicativo
funcionar; reinstale a arquitetura correta ou siga documentação do fornecedor.

HKCU também depende da identidade. Uma tarefa ou processo elevado pode não ter
o contexto que o autor imaginou. Registre `whoami`, arquitetura do processo e
hive antes de concluir que um valor “sumiu”.

## Políticas e preferência

Algumas configurações exibidas pela interface são persistidas no Registro;
outras são compostas, protegidas ou gerenciadas por serviços. Encontrar um valor
não autoriza editá-lo diretamente. Use a interface ou API documentada. Valores
em caminhos de política têm semântica administrativa e serão estudados nos
módulos empresariais; este módulo não simula domínio nem GPO.

Aplicar arquivos `.reg` de fóruns sem compreender cada caminho destrói a relação
entre causa e efeito. “Otimizações” que alteram dezenas de valores também podem
interferir em servicing e segurança. O Registro não fica mais rápido porque uma
ferramenta removeu entradas consideradas órfãs.

## Diagnóstico disciplinado

Antes da edição: reproduza o sintoma, identifique o consumidor, encontre
documentação oficial, registre valor ausente/presente, tipo e dado, exporte a
chave e tire snapshot. Modifique um valor. Reinicie somente o componente que a
documentação exigir. Valide função e reverta.

Se a mudança não surtir efeito, não acrescente outras chaves por tentativa.
Considere visão errada, usuário diferente, cache, política, tipo incorreto ou
hipótese falsa. A ausência de efeito é evidência.

## Exercícios

1. Desenhe hive → chave → valor → tipo → dado usando a fixture.
2. Compare `HKCU` em duas contas temporárias e explique o contexto.
3. Exporte a chave RTECourse, leia o arquivo e marque cada alteração proposta.
4. Demonstre a diferença entre String `1` e DWord `1` sem tocar chave real.
5. Escreva um runbook de edição que inclui baseline, rollback e validação.

## Checklist de domínio

- [ ] Diferencio hive, chave, valor, tipo e dado.
- [ ] Entendo por que HKCU muda conforme a identidade.
- [ ] Registro arquitetura e visualização ao investigar divergências.
- [ ] Edito somente `HKCU:\Software\RTECourse` no laboratório.
- [ ] Leio `.reg` como código e não importo origem desconhecida.
- [ ] Não uso limpadores nem pacotes genéricos de otimização.
- [ ] Uma mudança tem documentação, exportação, validação e rollback.
