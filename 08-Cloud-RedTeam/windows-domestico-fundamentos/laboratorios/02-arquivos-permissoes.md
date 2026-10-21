# Lab 02 — Arquivos, caminhos e permissões efetivas

**Classe: B/C — fixture local e alteração reversível de ACL.**

Este gate demonstra que nome, atributo e permissão são conceitos diferentes. A
prática usa somente `C:\RTE-Lab\dados` e uma conta temporária. Diretórios de
sistema, perfis reais e o disco principal fora da VM estão proibidos.

## Pré-requisitos e hipótese

Conclua o Lab 01 e os capítulos 05–07. Confirme snapshot, conta administrativa
de recuperação e sessão cotidiana comum. Escreva uma matriz prevista com as
operações listar, ler, criar, alterar e excluir para cada identidade.

Pare se o caminho resolvido não estiver sob `C:\RTE-Lab`, se houver reparse point,
se a ACL original não puder ser exportada ou se a conta temporária coincidir com
uma identidade preexistente.

## Preparação da fixture

```powershell
$root = 'C:\RTE-Lab\dados'
New-Item -ItemType Directory -Path $root -Force | Out-Null
'alpha' | Set-Content -LiteralPath (Join-Path $root 'relatório [01].txt')
'beta'  | Set-Content -LiteralPath (Join-Path $root 'dados com espaço.csv')
'gamma' | Set-Content -LiteralPath (Join-Path $root 'leia-me.md')

Get-ChildItem -LiteralPath $root -File |
  Sort-Object Name |
  ForEach-Object {
    [pscustomobject]@{
      Name = $_.Name
      Length = $_.Length
      Sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    }
  } | Export-Csv 'C:\RTE-Lab\evidencias\lab-02\manifesto-inicial.csv' `
      -NoTypeInformation -Encoding UTF8
```

Exporte a ACL original de forma legível e registre proprietário, proteção de
herança e entradas. Não reutilize comandos com nome de grupo localizado sem
verificar a identidade.

## Procedimento de acesso

1. Crie uma conta local comum exclusiva do laboratório por interface suportada.
2. Registre seu SID; o segredo não entra no relatório.
3. Adicione uma ACE que conceda somente leitura à pasta e conteúdo.
4. Não use `Deny`, `Everyone` ou `FullControl`.
5. Abra uma sessão da conta temporária e execute cada operação da matriz.
6. Registre resultado e mensagem exata, sem alterar ACL no meio do teste.
7. Aplique atributo ReadOnly a uma fixture e repita apenas testes necessários.
8. Compare atributo e decisão de acesso; remova o atributo.
9. Retorne à conta autorizada, remova somente a ACE adicionada e compare ACL.
10. Recalcule hashes para provar que o conteúdo original permaneceu igual.

Se usar PowerShell para modificar ACL, construa e revise o objeto antes de
`Set-Acl`. A implementação é parte do exercício; não cole uma linha opaca.

## Evidências

- caminho resolvido, ausência de reparse point e snapshot;
- manifesto de hash antes e depois;
- ACL original e final, além da ACE intermediária;
- SID sanitizado/rotulado da conta de fixture;
- matriz prevista e matriz observada com cinco operações;
- explicação de herança, ReadOnly e permissão efetiva;
- prova de remoção da ACE e da conta.

## Validação e cleanup

Confirme que a conta temporária não aparece mais, a ACL final equivale à baseline,
nenhuma fixture foi alterada e outro caminho não recebeu permissões. Restaure o
snapshot e repita apenas a coleta para confirmar o estado original.

Não compare ACL como texto ingênuo quando a ordem de apresentação variar;
compare identidades, tipos, direitos e herança. Registre diferenças justificadas.

## Aprovação

O gate passa com matriz completa, leitura permitida, escrita negada conforme a
previsão, conteúdo íntegro e rollback exato. Falha se usar diretório real,
conceder privilégio amplo, depender do nome inglês de grupo sem descoberta,
confundir ReadOnly com ACL ou deixar conta/ACE temporária.

## Questões de defesa

1. Por que o SID é mais estável que o nome?
2. Qual é a diferença entre autenticação e autorização?
3. Como herança afetou os três arquivos?
4. Por que `Deny` explícito dificultaria o modelo?
5. O que aconteceria se a conta fosse excluída antes do perfil ser avaliado?
