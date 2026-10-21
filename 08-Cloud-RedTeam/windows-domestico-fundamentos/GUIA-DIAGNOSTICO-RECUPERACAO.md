# Guia transversal de diagnóstico e recuperação

Este guia conecta os capítulos. Use-o quando um sintoma atravessar aplicativo,
conta, armazenamento, atualização ou proteção. Ele não substitui documentação
do componente; oferece um processo para escolher e validar o próximo passo.

## 1. Proteja o cenário

Antes de investigar, determine se há risco imediato a pessoas, dados ou
equipamento. Se houver cheiro, calor, ruído físico anormal, líquido ou bateria
deformada, desligue conforme orientação do fabricante e procure assistência.
Software não repara falha física.

Em sintomas lógicos, preserve documentos e não use o único computador como
laboratório. Registre conta, privilégio, edição/build, horário, timezone, volume,
snapshot e última condição conhecida como boa. Se BitLocker estiver presente,
confirme que a recovery key está disponível fora do dispositivo, sem copiá-la
para o relatório.

Critérios de parada são parte da solução: alvo ambíguo, dados reais sem backup,
comando não compreendido, prompt inesperado, mudança fora de fixture ou evidência
de incidente real exigem pausa e reavaliação.

## 2. Defina o sintoma operacionalmente

Troque adjetivos por observações mensuráveis. “Travando” pode significar janela
sem resposta, entrada atrasada, reboot, tela azul ou aplicativo encerrando. Cada
caso leva a fontes diferentes.

Registre:

- ação exata e resultado esperado;
- resultado observado e mensagem completa;
- início, duração, frequência e impacto;
- todas as contas, arquivos ou aplicativos afetados;
- mudanças anteriores, mesmo que pareçam não relacionadas;
- forma segura de reproduzir com fixture.

Separe quatro categorias no diário: fato coletado, relato de pessoa, inferência e
lacuna. Não promova relato ou proximidade temporal a fato técnico.

## 3. Construa hipóteses refutáveis

Uma hipótese útil prevê evidência a favor e contra. Para “espaço insuficiente”,
uma consulta de volume no momento do sintoma é barata. Para “arquivo corrompido”,
abrir outra fixture conhecida e comparar hash separa arquivo de aplicativo.

Monte uma tabela:

| Hipótese | A favor | Contra | Teste | Risco/custo |
|---|---|---|---|---|
| entrada inválida | só uma fixture falha | todas falham | abrir cópia conhecida | baixo |
| permissão | uma conta falha | mesma conta cria arquivo | consultar ACL/testar conta | baixo |
| espaço | volume perto do limite | espaço amplo e estável | medir antes/durante | baixo |
| componente | várias entradas falham | outro usuário funciona | eventos/versão/conta | médio |

Priorize o teste que divide mais hipóteses com menor risco. Atualize a tabela sem
apagar previsões erradas; elas demonstram como a evidência mudou o modelo.

## 4. Colete uma baseline mínima

Não rode “coletores gigantes”. Selecione fontes conforme o sintoma:

```powershell
Get-ComputerInfo |
  Select-Object WindowsProductName, WindowsVersion, OsBuildNumber,
    OsArchitecture

Get-Volume |
  Select-Object DriveLetter, FileSystem, HealthStatus, Size, SizeRemaining

Get-Process | Sort-Object CPU -Descending |
  Select-Object -First 10 Name, Id, CPU, WorkingSet64

Get-WinEvent -FilterHashtable @{
  LogName = 'Application'
  StartTime = (Get-Date).AddMinutes(-15)
} | Select-Object -First 50 TimeCreated, ProviderName, Id,
    LevelDisplayName, RecordId
```

CPU do objeto é acumulada; espaço é uma amostra; evento exige provider e canal.
Registre essas limitações. Uma saída sem linhas significa somente que o filtro
não retornou registros acessíveis.

## 5. Isole uma dimensão

Use uma fixture conhecida, outra conta comum ou uma cópia em caminho novo para
separar dado, identidade e aplicativo. Não crie conta administrativa para ver se
“resolve”: isso muda permissões e invalida o teste. Não mova documento real sem
backup.

Mude uma variável. Se testar uma atualização de aplicativo, mantenha o arquivo e
a conta. Se testar uma ACL, mantenha conteúdo e programa. Compare antes/depois e
reverta. Quando dois fatores mudam, a conclusão deve admitir ambiguidade.

## 6. Correlacione tempo e mecanismo

Construa linha do tempo em UTC: ação, sintoma, evento da aplicação, evento do
sistema, atualização e recuperação. Monitor de Confiabilidade ajuda a localizar
o período. Proximidade é pista; causalidade requer mecanismo e, quando possível,
reprodução controlada ou desaparecimento após reversão específica.

Um erro anterior pode ser ruído. Um evento informativo pode registrar a mudança
causal. Não selecione apenas níveis vermelhos. Preserve record ID e comando de
coleta para reproduzir a evidência.

## 7. Escolha a intervenção mínima

Uma ordem razoável é:

1. corrigir entrada ou configuração documentada da fixture;
2. liberar espaço criado pelo próprio laboratório;
3. reparar/reinstalar o aplicativo por fonte oficial;
4. reverter mudança recente confirmada;
5. usar verificação de integridade compatível com a hipótese;
6. iniciar Safe Mode para isolamento;
7. usar Startup Repair/System Restore quando o mecanismo indicar;
8. restaurar dados e sistema;
9. resetar ou reinstalar depois de preservar dados.

Essa lista não é receita fixa. Se o disco apresenta falha física, insistir em
scans pode piorar recuperação. Se há alerta real de segurança, não restaure item
nem apague evidência. Saia do exercício e procure processo apropriado.

## 8. Entenda ferramentas de integridade

DISM `/CheckHealth` consulta marcação de corrupção; `/ScanHealth` examina o
Component Store; `/RestoreHealth` altera estado tentando reparar. SFC
`/verifyonly` verifica arquivos protegidos, enquanto `/scannow` pode reparar.
CHKDSK `/scan` faz verificação online do NTFS; opções de correção têm mais impacto.

Leia ajuda, faça backup, use elevação apenas no comando necessário, guarde logs e
código de saída. Execute uma ferramenta porque a hipótese envolve seu objeto,
não porque uma lista genérica a incluiu. Depois, repita o teste original; saída
“sucesso” da ferramenta não é critério funcional.

## 9. Recuperação e letras de volume

No WinRE, a letra vista no Windows normal pode mudar. Identifique o volume por
estrutura, tamanho, conteúdo e status de cifra. Não formate ou atribua letras por
tentativa. Tenha a recovery key antes de entrar em um procedimento que possa
solicitá-la.

Startup Repair, Safe Mode, System Restore, remoção de atualização, Reset this PC
e reinstalação têm escopos diferentes. Documente dados preservados, aplicativos
afetados, dependência de credencial e rollback disponível. Escolha o mecanismo
mais estreito que atende à hipótese.

## 10. Valide em duas dimensões

Validação funcional responde “a pessoa consegue realizar a tarefa?”. Validação
técnica responde “estado, integridade e proteção estão corretos?”. Use ambas.

Após uma restauração: abra amostras, compare manifestos, meça RTO, confira conta
e ACL e confirme que Update/Defender não foram reduzidos. Após reparo de boot:
reinicie novamente, verifique build, volumes e eventos do intervalo. Após remover
fixture de espaço: compare espaço e manifesto.

Peça validação independente quando o impacto for relevante. O autor do runbook
costuma preencher lacunas mentalmente que outro operador revela.

## 11. Faça rollback e cleanup

Rollback também precisa de verificação. Remover a ACE criada não garante que a
ACL voltou ao estado anterior; compare entradas. Excluir conta não decide o
destino seguro do perfil. Restaurar snapshot errado cria um sistema coerente,
mas não o estado esperado. Compare inventários.

Liste recursos temporários: contas, pastas, volumes, chaves, tarefas, snapshots
e exports. Para cada um, registre mantido/removido, responsável e evidência.

## 12. Escreva a conclusão certa

Uma conclusão forte pode dizer:

> A causa foi confirmada como ACL da fixture porque a conta lia outros arquivos,
> a ACE divergente apareceu na baseline e restaurar apenas essa entrada recuperou
> escrita sem outra mudança.

Ou pode dizer:

> A causa não foi confirmada. Eventos do intervalo não cobrem o componente; os
> testes descartaram falta de espaço e entrada inválida. O próximo teste será
> reproduzir com outra conta comum em snapshot.

Incerteza explícita é técnica. Narrativa confiante sem evidência não é.

## Checklist de uso rápido

- [ ] risco imediato e critérios de parada avaliados;
- [ ] sintoma mensurável, intervalo e impacto registrados;
- [ ] hipóteses possuem evidência contra e teste discriminador;
- [ ] baseline é mínima, relevante e sanitizada;
- [ ] apenas uma variável muda por vez;
- [ ] intervenção corresponde ao objeto diagnosticado;
- [ ] função e estado técnico são validados;
- [ ] rollback/cleanup foram comparados à baseline;
- [ ] conclusão separa fato, inferência, limitação e próximo passo.
