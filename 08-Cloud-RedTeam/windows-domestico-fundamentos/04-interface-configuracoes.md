# 04 — Interface, Settings e ferramentas administrativas

O Windows combina interfaces de gerações diferentes. Aprender apenas a posição
de um botão produz conhecimento frágil; aprender o objeto administrado permite
encontrá-lo em Settings, console clássico, linha de comando ou documentação.

## Objetivos

- mapear tarefas às ferramentas corretas;
- distinguir shell gráfico, console administrativo e shell de comandos;
- obter a mesma evidência por interface gráfica e objeto estruturado;
- usar acessibilidade e ergonomia como requisitos funcionais;
- reconhecer quando uma tela consulta, altera ou apenas apresenta estado.

## Um mapa conceitual

Explorer é o shell e o gerenciador de arquivos usado na sessão. Settings é a
experiência moderna de configuração. Painel de Controle e consoles MMC expõem
áreas clássicas que ainda existem por compatibilidade ou profundidade. Windows
Terminal hospeda shells; PowerShell e CMD interpretam comandos. Task Manager é
uma ferramenta de observação e controle, não “o sistema de processos”.

| Necessidade | Ferramenta inicial | Alternativa de evidência |
|---|---|---|
| edição, build e hardware | Settings / `msinfo32` | `Get-ComputerInfo` |
| discos e volumes | `diskmgmt.msc` | `Get-Disk`, `Get-Volume` |
| dispositivos e drivers | `devmgmt.msc` | CIM de PnP/drivers |
| eventos | `eventvwr.msc` | `Get-WinEvent` |
| serviços | `services.msc` | `Get-Service` e CIM |
| tarefas agendadas | `taskschd.msc` | cmdlets `ScheduledTask` |
| confiabilidade | `perfmon /rel` | eventos correlacionados |
| inicialização de apps | Task Manager | propriedades registradas |

O atalho `Win+R` inicia nomes conhecidos e URIs como `ms-settings:`. Não cole
comandos desconhecidos nele: a ausência de terminal não reduz o impacto.

## Da tela ao objeto

Uma tela pode arredondar valores, traduzir estados, ocultar propriedades ou
agrupar dados de várias APIs. Uma consulta programática pode exigir privilégio
ou retornar um tipo que precisa de unidade. Compare sem presumir que textos
visualmente diferentes significam estados diferentes.

Exemplo de coleta somente leitura:

```powershell
$os = Get-CimInstance Win32_OperatingSystem
$volume = Get-Volume -DriveLetter ($env:SystemDrive.TrimEnd(':'))
[pscustomobject]@{
    Caption = $os.Caption
    Build = $os.BuildNumber
    FreeGiB = [math]::Round($volume.SizeRemaining / 1GB, 2)
    VolumeHealth = [string]$volume.HealthStatus
}
```

Anote em qual tela encontrou cada campo e se a unidade ou o momento da coleta
explica alguma diferença. Isso ensina a validar interfaces, não a escolher uma
como “verdadeira” por preferência.

## Settings, MMC e contexto

Uma console MMC pode carregar snap-ins e conectar-se a alvos diferentes, mas
este módulo opera apenas a máquina local. Antes de alterar algo, confira título,
alvo e privilégio. Interfaces elevadas podem parecer idênticas às comuns.

Settings muda entre versões. Pesquise pelo conceito (“aplicativos de
inicialização”, “histórico de atualização”) e confirme na página final o efeito
da ação. Botões como redefinir, remover ou interromper não têm a mesma semântica.
Fechar uma janela também não garante que a operação em segundo plano terminou.

## Acessibilidade e ergonomia

Escala, contraste, tamanho do texto, legendas, teclado, narrador, ponteiro e
configurações de energia fazem parte de uma entrega correta. O padrão “funciona
para mim” exclui o usuário real. Registre preferência e necessidade separadas:
alto contraste pode ser uma necessidade, enquanto posição da barra pode ser
preferência.

Alterações de acessibilidade devem ser testadas na conta correspondente, pois
várias são por usuário. Evite alterar a conta de outra pessoa ou transformar o
laboratório em recomendação médica. O objetivo é garantir operação independente
e reversível.

## Navegação orientada a tarefas

Realize uma “caça ao estado” sem modificar nada: encontre edição/build, firmware,
espaço livre, quatro aplicativos instalados, itens de inicialização, último
evento de confiabilidade e estado do Defender. Para cada item, registre:

1. conceito procurado;
2. caminho gráfico encontrado na sua build;
3. consulta equivalente, quando houver;
4. propriedade usada como evidência;
5. limitação da observação.

Não force correspondência quando a ferramenta gráfica calcula uma agregação.
Documente a diferença.

## Falhas comuns

- decorar cliques e ficar bloqueado após uma atualização visual;
- confundir aplicativo Terminal com PowerShell;
- elevar toda a sessão por conveniência;
- usar Task Manager para encerrar antes de coletar evidência;
- alterar energia, inicialização ou privacidade sem baseline;
- ignorar acessibilidade porque “não é administração”.

## Exercícios

1. Construa seu mapa `necessidade → ferramenta → propriedade → risco`.
2. Encontre cinco estados pela GUI e pelo PowerShell e explique diferenças.
3. Abra uma ferramenta via pesquisa, `Win+R` e Terminal; identifique qual
   componente realmente executou.
4. Configure uma preferência de acessibilidade na conta de laboratório, valide
   com a pessoa fictícia do cenário e reverta.
5. Explique por que um caminho de menu não é documentação suficiente.

## Checklist de domínio

- [ ] Escolho ferramenta pelo objeto administrado, não pela familiaridade.
- [ ] Diferencio Terminal, shell, Explorer, Settings e MMC.
- [ ] Consigo obter evidência gráfica e estruturada do mesmo conceito.
- [ ] Confirmo alvo e privilégio antes de qualquer alteração.
- [ ] Registro diferenças de versão sem inventar equivalência.
- [ ] Trato acessibilidade como requisito funcional.
- [ ] Minha documentação sobrevive a mudanças de posição de menus.
