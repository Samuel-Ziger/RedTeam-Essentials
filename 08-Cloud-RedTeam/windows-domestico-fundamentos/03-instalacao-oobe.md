# 03 — Instalação, particionamento, OOBE e primeira inicialização

Instalar é uma operação de ciclo de vida, não apenas avançar por telas. Uma
instalação confiável começa na origem da mídia, passa pela identificação dos
discos e só termina quando atualização, drivers, proteção e recuperação foram
validados.

## Objetivos

- diferenciar instalação limpa, upgrade, reset e reparo;
- explicar as fases do Windows Setup e as partições criadas;
- planejar uma instalação sem apagar o disco errado;
- tomar decisões conscientes no OOBE sem usar contornos;
- construir uma baseline pós-instalação verificável.

## Preparação e decisão

Obtenha ISO ou ferramenta de criação somente da Microsoft ou canal autorizado.
Registre produto, edição, idioma, arquitetura, URL, data e hash quando publicado.
Uma ISO legítima ainda precisa corresponder à licença e ao hardware.

Antes de iniciar:

1. teste a restauração dos dados em outro local;
2. inventarie aplicativos, edição e chaves de recuperação;
3. confirme requisitos oficiais e drivers críticos;
4. identifique fisicamente discos por modelo e capacidade;
5. desconecte mídias que não participam do procedimento;
6. mantenha energia estável e uma segunda forma de consultar o runbook.

Instalação limpa substitui sistema, aplicativos e configurações. Upgrade
in-place preserva mais estado, mas também pode carregar dependências quebradas.
“Reset this PC” reinstala por mecanismo de recuperação com opções específicas;
System Restore reverte parte do estado do sistema; Startup Repair trata certas
falhas de inicialização. Nenhum desses termos é sinônimo de backup de dados.

## O que o Setup faz

A mídia inicializa, carrega Windows PE, coleta opções, prepara armazenamento,
aplica uma imagem WIM/ESD, instala arquivos de boot e inicia a especialização.
Em UEFI/GPT, uma disposição comum contém:

- EFI System Partition, com arquivos de boot;
- Microsoft Reserved Partition, usada pelo gerenciamento GPT;
- volume do Windows, normalmente NTFS;
- partição de recuperação, com Windows Recovery Environment.

Tamanho e disposição podem variar por versão e fabricante. Não memorize números
como regra universal. Liste o que o seu Setup criou e explique a função de cada
entrada. O disco de dados deve ser reconhecido por número, capacidade e estado;
letra ainda pode não existir nessa fase.

## OOBE e contas

O Out-of-Box Experience configura região, teclado, conta, privacidade e serviços
disponíveis na edição/build. As telas mudam. Requisitos atuais publicados pela
Microsoft podem exigir internet e conta Microsoft para Windows 11 Home e para
Windows 11 Pro em uso pessoal durante a configuração inicial. Siga o fluxo
suportado aplicável; o curso não ensina comandos de bypass, imagens modificadas
ou credenciais fictícias.

Leia cada opção de privacidade pelo efeito descrito na versão instalada. Depois
do OOBE, crie uma conta cotidiana sem privilégio administrativo quando o cenário
permitir. Uma conta Microsoft e uma conta local têm propriedades e experiências
diferentes, mas ambas devem usar autenticação forte e método de recuperação
controlado pelo titular. Este módulo não configura identidade empresarial.

## Validação pós-instalação

```powershell
Get-ComputerInfo |
  Select-Object WindowsProductName, WindowsVersion, OsBuildNumber,
    OsArchitecture, BiosFirmwareType

Get-Partition |
  Select-Object DiskNumber, PartitionNumber, DriveLetter, Type, Size

Get-Volume |
  Select-Object DriveLetter, FileSystem, HealthStatus, Size, SizeRemaining

Get-CimInstance Win32_PnPEntity |
  Where-Object ConfigManagerErrorCode -ne 0 |
  Select-Object Name, ConfigManagerErrorCode
```

Interprete ausência de saída da última consulta como “nenhum dispositivo
reportado por esse filtro”, não como prova absoluta de que todo driver é ideal.
Confirme relógio, ativação, Secure Boot/TPM quando aplicável, Update, Defender,
áudio/vídeo e reinicialização. Faça o primeiro inventário e um backup de fixture
antes de declarar a baseline concluída.

## Duas instalações didáticas

Na primeira VM, deixe o Setup preparar um disco virtual vazio. Registre cada
fase e partição. Na segunda tentativa, adicione um volume de dados com fixtures
e demonstre como reconhecê-lo sem formatá-lo. O objetivo não é confiar que “D:”
sempre é dados, mas validar disco, partição, capacidade e conteúdo.

Após cada instalação, reinicie duas vezes e compare inventários. Um snapshot
tirado antes de concluir servicing pode capturar um estado intermediário; nomeie
o checkpoint apenas depois da validação.

## Falhas comuns

- instalar de origem não oficial ou sem registrar a versão;
- escolher disco apenas pela letra ou posição na tela;
- acreditar que “manter arquivos” substitui backup testado;
- aplicar vários drivers genéricos antes de medir o problema;
- contornar OOBE e criar uma instalação impossível de suportar;
- considerar a área de trabalho visível como fim do processo.

## Exercícios

1. Compare instalação limpa, upgrade, reset, restauração e reparo em uma tabela.
2. Desenhe as partições da VM e explique quem consome cada uma.
3. Produza um checklist que impeça escolher o disco errado.
4. Documente as decisões do OOBE sem capturar e-mail ou segredo.
5. Faça inventários antes e depois do primeiro ciclo de atualização e explique
   quais diferenças eram esperadas.

## Checklist de domínio

- [ ] A mídia veio de origem oficial e sua identidade foi registrada.
- [ ] Backup foi restaurado antes de qualquer instalação destrutiva.
- [ ] Identifico discos sem depender de letra ou ordem visual.
- [ ] Explico ESP, MSR, volume do sistema e recuperação.
- [ ] Não usei bypass de OOBE, ativação ou requisito de hardware.
- [ ] A baseline inclui build, drivers, proteção, atualização e reinício.
- [ ] Sei escolher entre instalar, atualizar, redefinir, restaurar e reparar.
