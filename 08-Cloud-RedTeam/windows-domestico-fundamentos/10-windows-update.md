# 10 — Windows Update, servicing e rollback

Servicing mantém componentes do Windows em um estado suportado. Atualização não
é evento isolado: há detecção, download, staging, instalação, reinicialização,
validação e eventualmente rollback. Diagnosticar exige saber em qual fase a
falha ocorreu.

## Objetivos

- distinguir atualizações de qualidade, recursos, drivers e opcionais;
- explicar Component Store e reinicialização pendente em nível introdutório;
- construir linha do tempo de build, KB e eventos;
- validar uma atualização sem depender só da lista de histórico;
- escolher rollback apenas para incidente confirmado.

## Tipos e responsabilidades

Atualizações de qualidade corrigem segurança e confiabilidade e normalmente são
cumulativas. Atualizações de recursos movem para outra versão do produto e
renovam componentes em escala maior. Drivers e atualizações opcionais têm
critérios próprios. Inteligência do Defender segue um ciclo mais frequente e
não deve ser confundida com build do sistema.

A Servicing Stack orquestra aplicação de pacotes; o Component Store mantém
componentes e relações necessárias para instalar, habilitar recursos e reparar.
Não exclua manualmente conteúdo de `WinSxS`: o tamanho aparente inclui hard links
e não corresponde diretamente a espaço recuperável.

Uma instalação pode ficar aguardando reinicialização para substituir arquivos
em uso e completar fases. “Baixado” ou “100%” na interface não prova que a nova
build iniciou. A validação ocorre depois do reboot e de uma nova coleta.

## Baseline e histórico

```powershell
Get-ComputerInfo |
  Select-Object WindowsProductName, WindowsVersion, OsBuildNumber

Get-HotFix |
  Sort-Object InstalledOn -Descending |
  Select-Object -First 15 HotFixID, Description, InstalledOn

Get-WindowsPackage -Online |
  Where-Object PackageState -eq Installed |
  Select-Object -First 20 PackageName, ReleaseType, InstallTime
```

`Get-HotFix` não representa todo o servicing moderno. O histórico gráfico também
pode listar tentativas e categorias. Correlacione edição/build, página oficial
de release health, pacotes e eventos. Registre timezone e use intervalo pequeno.

Antes de atualizar: confirme suporte da versão, backup restaurável, chave de
recuperação quando houver, energia, espaço e snapshot da VM. Conecte a VM apenas
no período controlado necessário, se esse for o método autorizado, e não use a
atividade para estudar configuração de conectividade.

## Estratégia de atualização doméstica

1. registre build, proteções e sintomas existentes;
2. verifique problemas conhecidos oficiais da versão;
3. preserve dados e espaço livre;
4. aplique pelo mecanismo suportado;
5. reinicie até o servicing indicar conclusão;
6. recoloque a VM no modo local do curso;
7. valide build, aplicativos, dispositivos, Defender e eventos do intervalo;
8. atualize o diário e mantenha o rollback apenas pelo tempo planejado.

Pausar temporariamente pode fazer parte da resposta a um problema conhecido,
mas desativar permanentemente Windows Update acumula risco. “Nunca atualizo
porque pode quebrar” e “instalo imediatamente sem backup” são extremos ruins.

## Diagnóstico por fase

Registre código de erro completo, KB ou versão, horário, fase observada, espaço
livre, último reboot e mudança recente. Primeiro, repita a verificação suportada,
reinicie quando realmente pendente e consulte o problema conhecido. Preserve
logs antes de limpar cache ou executar reparos.

Uma falha de download, uma falha ao aplicar pacote e um rollback durante boot
têm evidências e soluções diferentes. Não use uma sequência genérica de dezenas
de comandos. Escolha o teste que distingue as hipóteses mais prováveis.

O Event Viewer e `Get-WinEvent` permitem consultar canais do servicing e sistema,
mas provider/IDs variam. Filtre por tempo e provider observado na sua máquina;
não memorize um ID sem o nome do provedor.

## Rollback consciente

Remover atualização ou voltar de versão reduz correções e pode ter janela
limitada. Só faça após demonstrar relação temporal, impacto e incompatibilidade,
consultar documentação e preservar dados. Depois do rollback, valide a build e
planeje a solução sustentada; permanecer indefinidamente vulnerável não é
resolução.

Snapshot da VM é o primeiro rollback do laboratório. Em computador real, use os
mecanismos oficiais e backup. Nunca teste remoção de pacote na máquina principal
para “aprender”.

## Prática guiada

Com snapshot, construa uma linha do tempo das últimas atualizações: data/hora,
categoria, KB quando aplicável, build antes/depois e reinicialização. Se a VM
permanecer offline, analise apenas histórico já presente. Explique quais fontes
não cobrem todo o estado e como você provaria a conclusão do servicing.

## Exercícios

1. Diferencie quality update, feature update, driver e inteligência do Defender.
2. Explique por que tamanho de `WinSxS` no Explorer pode enganar.
3. Produza uma linha do tempo e marque fato, inferência e lacuna.
4. Crie uma árvore de decisão para falha antes, durante e depois do reboot.
5. Defenda quando pausar ou reverter seria justificável e qual é a saída final.

## Checklist de domínio

- [ ] Identifico a categoria e a fase da atualização.
- [ ] Não uso `Get-HotFix` como fonte única.
- [ ] Verifico build após reiniciar para provar conclusão.
- [ ] Backup, espaço, energia e recuperação precedem servicing relevante.
- [ ] Preservo logs antes de limpeza ou reparo.
- [ ] Rollback responde a incidente confirmado e gera plano de retorno.
- [ ] Nunca desativo atualizações permanentemente por conveniência.
