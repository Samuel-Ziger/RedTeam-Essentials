# 13 — Backup, restauração e recuperação do Windows

Backup é uma cópia planejada; restauração é o ato de recuperar dados; recuperação
restabelece a capacidade de trabalhar. A existência de arquivos copiados não
prova que o objetivo será atendido. O teste de restore é a evidência central.

## Objetivos

- classificar dados, sistema, configuração e credenciais de recuperação;
- definir RPO e RTO para um cenário doméstico;
- aplicar 3-2-1 sem confundir sincronização com backup;
- interpretar códigos do `robocopy` e manifests de hash;
- escolher a opção menos destrutiva no Windows Recovery Environment.

## O que precisa sobreviver

Comece pelo inventário: documentos, fotos, projetos, configurações exportáveis,
instaladores/licenças recuperáveis e chaves de recuperação. Sistema operacional e
aplicativos podem ser reinstalados; um arquivo pessoal único talvez não. Segredos
devem ter proteção e localização próprias, não ser incluídos em evidência comum.

RPO é a quantidade de dados que se aceita perder, expressa em tempo ou versão.
RTO é quanto tempo o serviço pode ficar indisponível. “Faço backup todo domingo”
pode atender RPO de sete dias, mas não um projeto que muda a cada hora. A escolha
de ferramenta vem depois desses objetivos.

## Estratégia 3-2-1 adaptada

Mantenha três cópias dos dados importantes, em duas formas ou mídias independentes,
com uma cópia fora do equipamento ou desconectada. Independência importa: duas
pastas no mesmo SSD não sobrevivem à falha do SSD. Um snapshot no mesmo host não
sobrevive à perda do host.

Sincronização mantém disponibilidade entre locais, mas também pode propagar
exclusão, sobrescrita ou corrupção. Histórico de versões melhora a proteção,
porém ainda precisa ser testado e governado. Backup deve ter retenção, verificação
e procedimento de restauração.

## Cópia verificável de fixture

```powershell
$source = 'C:\RTE-Lab\fixture'
$destination = 'R:\RTE-Backup\fixture-001'
robocopy $source $destination /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ
$exitCode = $LASTEXITCODE
if ($exitCode -ge 8) {
    throw "Robocopy falhou com código $exitCode"
}
```

Para `robocopy`, códigos de 0 a 7 representam combinações de sucesso, cópia e
diferenças; 8 ou mais indicam ao menos uma falha. Não trate todo código diferente
de zero como erro, nem todo código abaixo de 8 como prova de conteúdo correto.

Gere manifesto com caminho relativo, tamanho e SHA-256 na origem. Restaure em
uma terceira pasta vazia, gere outro manifesto e compare. Abra amostras com o
aplicativo correto. Hash igual demonstra igualdade de bytes, não que a estratégia
cobre todos os documentos reais.

O script `Backup-RteFixture.ps1` recusa sobrescrever o destino, evita destino
dentro da origem, suporta `-WhatIf` e grava manifesto. Leia-o antes de executar.
Como o manifesto é criado depois da enumeração, ele descreve os arquivos copiados,
não a si próprio — isso evita uma referência circular.

## Restauração como ensaio

Um teste deve medir tempo, registrar erros e evitar sobrescrever a única cópia.
Escolha aleatoriamente alguns arquivos e um diretório completo. Compare conteúdo,
permissões relevantes e uso pelo aplicativo. Documente quem pode autorizar uma
restauração e onde o runbook fica quando o computador não inicia.

Teste também uma falha: altere um byte na cópia restaurada e confirme que o
manifesto detecta divergência. Depois descarte apenas a fixture.

## Opções de recuperação

Ponto de restauração reverte parte de estado de sistema e Registro; não é backup
de documentos. File History ou solução escolhida trata versões de dados. Startup
Repair tenta corrigir certas falhas de boot. Safe Mode inicia conjunto reduzido
para diagnóstico. Uninstall Updates, System Restore, Reset this PC e reinstalação
têm impactos crescentes e pré-condições diferentes.

No Windows Recovery Environment, letras podem diferir das vistas no sistema
normal. Identifique volumes por conteúdo, tamanho e estrutura. Se houver
BitLocker, a recovery key pode ser necessária. Não experimente no computador
principal sem backup e runbook.

Escolha a intervenção menos destrutiva compatível com a hipótese: salvar dados e
coletar evidência precede reset ou reinstalação. Uma recuperação bem-sucedida
termina com atualização, validação de dados, proteção e causa registrada.

## Exercícios

1. Defina RPO/RTO para estudante e profissional com documentos locais.
2. Desenhe uma estratégia 3-2-1 e identifique falhas compartilhadas.
3. Execute backup e restore de fixture em caminho novo e compare manifests.
4. Interprete códigos 0, 1, 3 e 8 do `robocopy` usando a documentação.
5. Ordene Safe Mode, Startup Repair, System Restore, Reset e reinstalação para
   três sintomas, justificando o menor impacto.

## Checklist de domínio

- [ ] Dados e objetivos são definidos antes da ferramenta.
- [ ] RPO/RTO têm valores mensuráveis.
- [ ] As cópias não dependem todas do mesmo disco ou host.
- [ ] Sincronização e snapshot não são chamados de backup completo.
- [ ] Restauração ocorre em caminho separado e é validada por hash e uso.
- [ ] Sei interpretar códigos do `robocopy`.
- [ ] Escolho recuperação por hipótese, evidência e menor impacto.
