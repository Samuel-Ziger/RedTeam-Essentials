# 09 — NTFS internals: MFT, atributos, links e journaling

NTFS representa cada arquivo por um registro com atributos. Nome e bytes são
apenas parte do objeto. Entender identidade, links, streams e logs evita conclusões
forenses precipitadas e automações recursivas inseguras.

## Objetivos

- explicar MFT, atributos residentes e não residentes;
- distinguir nome, file ID, hard link e reparse point;
- interpretar journaling como consistência, não backup;
- comparar múltiplos timestamps com contexto;
- criar links e streams somente numa árvore descartável.

## MFT e atributos

Master File Table contém registros para arquivos e diretórios. Um registro possui
atributos como nomes, informação padrão, descritor de segurança e dados. Conteúdo
pequeno pode ser residente no registro; conteúdo maior referencia runs de clusters.
Isso é detalhe de alocação, não garantia de desempenho nem API de aplicação.

Um arquivo pode ter múltiplos nomes por hard links. O registro/file ID representa
identidade mais estável no volume; caminho é entrada de namespace. Excluir um nome
reduz links; dados permanecem enquanto links/handles e semântica do sistema os
mantiverem.

```powershell
fsutil.exe file queryfileid .\fixture.txt
fsutil.exe hardlink list .\fixture.txt
```

`fsutil` pode exigir elevação conforme operação. Consulte somente volume/fixture.

## Journals diferentes

`$LogFile` registra operações de metadados para recuperação de consistência após
falha. USN Change Journal registra mudanças para consumidores como indexadores e
backup. Nenhum preserva necessariamente conteúdo histórico e nenhum substitui
backup. Retenção é limitada e registros podem ser removidos.

O curso não analisa metarquivos diretamente nem altera o journal. Observe apenas
com APIs/comandos documentados quando disponível.

## Hard links e reparse points

Hard links são nomes no mesmo volume apontando ao mesmo registro. Editar conteúdo
por um nome aparece pelo outro. Symlink/junction são reparse points: resolução é
interceptada e pode apontar a outro destino. Uma rotina recursiva pode sair da
raiz se seguir junction sem política.

```powershell
New-Item -ItemType HardLink -Path .\fixture-hard.txt -Target .\fixture.txt
New-Item -ItemType SymbolicLink -Path .\fixture-link.txt -Target .\fixture.txt
Get-Item .\fixture*.txt -Force |
  Select-Object Name, Length, LinkType, Target, LastWriteTimeUtc
```

Criação de symlink depende de configuração/privilégio. Se indisponível, registre
e não eleve apenas para cumprir. Remova o link, não o alvo.

## Alternate Data Streams

NTFS permite streams nomeados. PowerShell os lista com `-Stream *`. Eles são parte
do arquivo no NTFS e podem ser perdidos ao copiar para filesystem sem suporte.
Não os use para ocultar dados ou segredos. A prática cria apenas stream textual
`rte.note`, lista, lê e remove.

```powershell
Set-Content -LiteralPath .\fixture.txt -Stream rte.note -Value 'metadado didático'
Get-Item -LiteralPath .\fixture.txt -Stream *
Remove-Item -LiteralPath .\fixture.txt -Stream rte.note
```

## Timestamps e linhas do tempo

NTFS/Win32 expõem tempos de criação, modificação, acesso e mudança de metadados em
camadas/ferramentas diferentes. Cópia, rename, restore, cache e aplicação afetam
campos de modos distintos. Resolução e atualização variam.

Nunca conclua autoria ou ação humana por um timestamp. Correlacione journal,
eventos, ação controlada e hashes. Use UTC e registre ferramenta/API.

## Segurança, EFS e compressão

Descritores de segurança podem ser compartilhados internamente; a API apresenta
ACL do objeto. EFS cifra arquivos por identidade/certificado e não é BitLocker.
Compressão NTFS e EFS têm interações/restrições. O laboratório não habilita EFS
porque perda do certificado pode tornar fixture inacessível; estude apenas o
modelo.

## Experimento controlado

Em segundo volume NTFS, crie arquivo e manifesto. Adicione hard link, symlink se
suportado e stream didático. Modifique pelo hard link, observe hash pelos dois
nomes e compare file ID. Copie para pasta no mesmo volume e, opcionalmente, para
exFAT descartável; registre quais metadados/streams sobrevivem. Limpe links em
ordem e valide o alvo.

## Exercícios

1. Desenhe registro MFT com nomes, dados e descritor.
2. Explique por que hard link não é cópia.
3. Escreva regra para impedir backup de atravessar reparse point.
4. Compare `$LogFile`, USN Journal e backup.
5. Produza timeline da própria fixture com quatro timestamps e limitações.

## Checklist de domínio

- [ ] MFT e atributos são explicados sem tratar formato interno como API pública.
- [ ] Caminho, nome, file ID e conteúdo são distintos.
- [ ] Hard link, symlink e junction não são confundidos.
- [ ] Journaling não é chamado de histórico de conteúdo ou backup.
- [ ] Streams nunca são usados para ocultação.
- [ ] Timestamps são correlacionados e não provam autoria.
- [ ] Toda prática ocorre em árvore/volume descartável com cleanup verificado.
