# 05 — Arquivos, diretórios, caminhos e metadados

O sistema de arquivos apresenta dados por volumes e caminhos. Manipular esses
objetos com segurança exige compreender contexto, caracteres especiais,
metadados e diferença entre nome, conteúdo e identidade.

## Objetivos

- interpretar caminhos absolutos, relativos e baseados em ambiente;
- escolher diretórios de usuário, aplicação e sistema corretamente;
- usar `-LiteralPath`, `Join-Path` e testes de alvo;
- distinguir extensão, tipo, hash, assinatura e procedência;
- observar timestamps, atributos, links e permissões sem confundi-los.

## Namespace e contexto

`C:\` é a raiz de um volume, não a raiz de todo o computador. Outros volumes
podem usar letras ou pontos de montagem. O diretório atual influencia caminhos
relativos; a conta e o processo determinam variáveis de ambiente.

- `%USERPROFILE%` guarda o perfil do usuário atual;
- `%ProgramFiles%` é destinado a programas instalados segundo a arquitetura;
- `%ProgramData%` guarda dados compartilhados por aplicações;
- `%LOCALAPPDATA%` e `%APPDATA%` têm escopos distintos no perfil;
- `%SystemRoot%` aponta para o diretório do Windows;
- `%TEMP%` é temporário, não armazenamento durável.

Não grave dados de aplicação em `System32` ou na raiz porque “é mais fácil”.
Escolha o local conforme proprietário, duração, compartilhamento e backup.

## Caminhos robustos

```powershell
$root = Join-Path $env:TEMP 'RTE-Arquivos'
$report = Join-Path $root 'relatório [01].txt'

New-Item -ItemType Directory -Path $root -Force | Out-Null
'linha segura' | Set-Content -LiteralPath $report -Encoding UTF8

Get-Item -LiteralPath $report |
  Select-Object FullName, Length, Attributes, CreationTimeUtc, LastWriteTimeUtc

Get-FileHash -LiteralPath $report -Algorithm SHA256
```

`-Path` pode interpretar curingas como `*`, `?` e colchetes. `-LiteralPath`
trata o nome recebido literalmente e é a escolha segura quando há entrada ou
caracteres especiais. `Join-Path` expressa intenção e evita concatenar barras.
Antes de remover, resolva o caminho, confirme que ele está dentro da raiz do
laboratório e liste o alvo.

## Nome não é conteúdo

Extensão orienta associação e experiência gráfica, mas não prova formato.
Ative a exibição de extensões e itens ocultos para reduzir ambiguidades como
`relatorio.pdf.exe`. Ícone também pode ser escolhido por associação. Hash prova
que os bytes são iguais aos de uma referência conhecida; assinatura válida
vincula integridade e signatário; origem e reputação completam a decisão.

Um arquivo sem assinatura não é automaticamente perigoso — seu próprio `.txt`
não será assinado. E um arquivo assinado ainda pode ter vulnerabilidade. A
conclusão precisa refletir exatamente a evidência disponível.

## Metadados e identidade

`CreationTime`, `LastWriteTime` e `LastAccessTime` respondem a perguntas
diferentes. Cópia, restauração, ferramenta e configuração do volume podem
alterá-los. Use UTC em linhas do tempo e registre como o artefato foi produzido.

Atributos como Hidden, System e ReadOnly influenciam apresentação ou certas
operações; não são controle de acesso. ACL responde quem pode fazer o quê. O
capítulo 07 detalha permissões.

NTFS suporta hard links e reparse points. Dois nomes podem referir o mesmo
conteúdo, e um diretório pode redirecionar a outro local. Portanto, uma rotina
recursiva precisa evitar atravessar links inesperados. No laboratório, apenas
observe `LinkType` e `Target`; não construa árvores complexas antes de dominar
o alvo.

```powershell
Get-ChildItem -LiteralPath $root -Force |
  Select-Object Name, Length, Attributes, LinkType, Target, LastWriteTimeUtc
```

## Operações e validação

Copiar cria outra entrada e possivelmente novos metadados. Mover no mesmo volume
pode apenas alterar o namespace; entre volumes pode envolver cópia e remoção.
Renomear muda o caminho, não necessariamente os bytes. Excluir pode enviar à
Lixeira pela interface, enquanto `Remove-Item` normalmente não oferece essa
recuperação. Use somente fixtures e valide com hash e contagem.

Uma sequência segura é: criar manifesto, executar operação, reconstruir
manifesto, comparar, testar abertura e então limpar. O manifesto deve usar
caminho relativo para poder comparar raízes distintas.

## Prática guiada

Crie três arquivos contendo espaços, acentos e colchetes. Gere tabela com caminho
relativo, tamanho e SHA-256. Copie para uma segunda pasta, renomeie um arquivo,
altere outro e compare. Você deve concluir corretamente que o renomeado manteve
bytes, o alterado mudou o hash e timestamps dependem da operação. Remova apenas
a raiz temporária depois de imprimir e conferir seu caminho completo.

## Exercícios

1. Explique caminhos absoluto, relativo e baseado em variável com exemplos.
2. Compare extensão, hash, assinatura e origem como evidências.
3. Demonstre por que `-LiteralPath` é necessário com `[01]` no nome.
4. Copie e mova uma fixture; compare timestamps e hashes sem generalizar além
   do experimento.
5. Escreva uma função que rejeite cleanup fora de `C:\RTE-Lab`, use `-WhatIf`
   e não siga reparse points.

## Checklist de domínio

- [ ] Não confundo raiz do volume com raiz do computador.
- [ ] Escolho diretório conforme escopo e ciclo de vida do dado.
- [ ] Uso caminhos literais e resolvo o alvo antes de remover.
- [ ] Extensão, atributo, ACL, hash e assinatura têm significados distintos.
- [ ] Interpreto timestamps com contexto e preferencialmente em UTC.
- [ ] Reconheço o risco de recursão através de links/reparse points.
- [ ] Toda prática usa fixture descartável e manifesto verificável.
