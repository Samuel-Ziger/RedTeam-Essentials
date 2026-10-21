# 06 — Discos, partições, volumes, sistemas de arquivos e BitLocker

Armazenamento possui camadas. Disco, tabela de partições, partição, volume,
sistema de arquivos e ponto de montagem não são palavras intercambiáveis. Essa
distinção é a proteção mais importante contra formatar o alvo errado.

## Objetivos

- desenhar as camadas entre dispositivo e caminho;
- inventariar discos e volumes por propriedades estáveis;
- escolher NTFS ou exFAT conforme requisito;
- interpretar estados e protetores do BitLocker;
- particionar somente o disco virtual descartável com rollback documentado.

## Modelo em camadas

Um disco físico ou virtual expõe blocos. GPT registra partições e seus tipos.
O Windows pode apresentar uma partição como volume; o volume recebe um sistema
de arquivos, como NTFS, e é montado por letra ou por caminho em outro volume.
Uma letra é uma associação mutável, não identidade do dispositivo.

```text
disco 1 → GPT → partição 1 → volume → NTFS → R:\ ou ponto de montagem
```

O disco do sistema normalmente contém mais de uma partição, inclusive ESP e
recuperação. “C:” identifica o volume montado usado pelo sistema em execução,
não o primeiro disco por definição. Em ambientes de recuperação, letras podem
mudar.

## Inventário antes da mudança

```powershell
Get-Disk |
  Select-Object Number, FriendlyName, PartitionStyle, OperationalStatus,
    HealthStatus, Size, IsBoot, IsSystem

Get-Partition |
  Select-Object DiskNumber, PartitionNumber, DriveLetter, Type, Size

Get-Volume |
  Select-Object DriveLetter, FileSystemLabel, FileSystem, DriveType,
    HealthStatus, Size, SizeRemaining
```

Registre número, tamanho, estilo, flags de boot/sistema e snapshot. O número de
disco pode mudar após reconfigurar a VM; revalide imediatamente antes de cada
comando. Nunca copie um número do runbook e presuma que ainda representa o
mesmo dispositivo.

No exercício de criação, o alvo deve ser um segundo disco virtual vazio. Se
qualquer propriedade divergir do planejamento, pare. Inicializar, limpar ou
formatar é destrutivo e não será automatizado pelo material.

## Sistemas de arquivos

NTFS oferece ACLs, journaling, hard links, reparse points, compressão e recursos
esperados pelo Windows. exFAT prioriza interoperabilidade e mídia removível, mas
não fornece o mesmo modelo de permissões e resiliência. FAT32 possui limitações
adicionais. ReFS atende cenários específicos e sua disponibilidade depende da
edição e do uso; não é uma substituição universal de NTFS.

Escolha a partir de tamanho de arquivos, sistemas que precisam ler a mídia,
controle de acesso, resiliência e suporte. “O mais novo” ou “o que apareceu no
menu” não são requisitos.

O estado `Healthy` é uma observação do subsistema, não garantia de que cada byte
do conteúdo está correto. Integridade do dado exige teste de leitura, manifesto
e backup.

## BitLocker como sistema de recuperação

BitLocker cifra volumes inteiros e protege dados em repouso. TPM pode liberar a
chave quando medições de boot são esperadas; protetores adicionais podem usar
PIN, chave de inicialização ou recovery password conforme cenário e edição. O
algoritmo de cifra, o estado de conversão e a proteção ativa são dimensões
separadas.

```powershell
Get-BitLockerVolume |
  Select-Object MountPoint, VolumeType, VolumeStatus, EncryptionPercentage,
    ProtectionStatus, EncryptionMethod, KeyProtector
```

Não exporte o conteúdo de `RecoveryPassword` para o diário. Registre apenas que
um protetor existe, onde a chave foi guardada e quando a recuperação foi testada.
A recovery key deve ficar separada do único equipamento que ela recupera. Um
snapshot da VM não é o único local aceitável para esse segredo.

Criptografado e protegido também não são sinônimos: um volume pode estar
convertido e temporariamente com protetores suspensos. Interprete
`VolumeStatus`, porcentagem e `ProtectionStatus` em conjunto. Disponibilidade do
cmdlet e do recurso varia por edição.

## Mudanças de firmware e recuperação

Alterar TPM, Secure Boot, firmware ou configuração de boot pode mudar medições e
acionar recuperação. Antes de qualquer alteração compatível, confirme a chave,
procedimento oficial e acesso ao teclado/layout correto. Suspender proteção é
uma operação controlada, não uma correção genérica, e deve ser revertida e
validada.

O teste seguro usa apenas um volume de dados descartável: grave fixtures e
manifesto, desmonte e remonte, valide conteúdo. Habilite BitLocker somente se a
edição permitir, depois de snapshot e armazenamento separado da chave. Nunca
pratique no volume do computador real.

## Capacidade, espaço e descarte

Capacidade total, espaço alocado e espaço livre não respondem à mesma pergunta.
Arquivos temporários, Component Store e pontos de restauração têm gerenciamento
próprio. Evite “limpadores” que removem objetos sem explicar dependências. Use as
ferramentas do Windows e meça antes/depois.

Excluir partição ou formatar remove estruturas de referência e pode tornar dados
inacessíveis; não é método garantido de descarte seguro de mídia. O tema de
sanitização exige política e suporte do dispositivo e fica fora desta prática.

## Exercícios

1. Desenhe disco, GPT, partição, volume, NTFS e letra da VM.
2. Explique por que `Healthy` não substitui manifesto e restauração.
3. Compare NTFS e exFAT para um SSD interno e uma mídia entre sistemas.
4. Registre estados possíveis de BitLocker sem expor protetores.
5. No segundo disco, crie volume, fixture e manifesto; desmonte, remonte e
   confirme hashes. Reverta o snapshot e reconfirme a topologia original.

## Checklist de domínio

- [ ] Diferencio disco, partição, volume, filesystem e montagem.
- [ ] Revalido o alvo imediatamente antes de uma operação destrutiva.
- [ ] Nunca uso letra ou posição como única identidade.
- [ ] Escolho filesystem por requisitos verificáveis.
- [ ] Interpreto conversão, proteção e protetores do BitLocker separadamente.
- [ ] Recovery key não aparece nas evidências e foi guardada separadamente.
- [ ] Toda prática de particionamento ocorre no segundo disco descartável.
