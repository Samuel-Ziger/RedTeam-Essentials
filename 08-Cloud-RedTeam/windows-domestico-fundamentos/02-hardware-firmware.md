# 02 — Hardware, firmware, UEFI, Secure Boot e TPM

O Windows depende de uma cadeia que começa antes do kernel. Firmware configura
o hardware, seleciona a entrada de boot e transfere controle para componentes
assinados. Compreender essa sequência ajuda a diagnosticar incompatibilidade
sem recorrer a alterações aleatórias na UEFI.

## Objetivos

- desenhar o caminho do botão de energia ao kernel;
- distinguir UEFI, GPT, Secure Boot, TPM e BitLocker;
- verificar requisitos e drivers sem expor identificadores;
- explicar medição, validação, armazenamento de segredo e criptografia;
- planejar atualização de firmware com recuperação e energia estável.

## A cadeia de inicialização

Em uma instalação moderna, o firmware UEFI inicializa dispositivos, lê entradas
de boot persistidas e encontra o Windows Boot Manager na EFI System Partition.
O Boot Manager seleciona uma configuração; o loader prepara kernel, HAL e
drivers necessários ao boot; só depois o Windows assume o sistema.

GPT é a tabela que descreve partições. UEFI é a interface de firmware. Eles são
comumente usados juntos, mas não são sinônimos. A EFI System Partition contém
arquivos de inicialização; não é um local para documentos e não deve receber
uma letra por conveniência.

Secure Boot valida assinaturas na cadeia antes do sistema operacional. TPM é um
componente que oferece chaves protegidas, medições e operações criptográficas.
BitLocker cifra volumes e pode usar o TPM para liberar material de chave quando
o estado medido é esperado. Assim:

- Secure Boot valida componentes permitidos;
- TPM mede/protege segredos e não “escaneia vírus”;
- BitLocker protege dados em repouso;
- backup protege disponibilidade, algo que os três anteriores não garantem.

## Inventário seguro

```powershell
Get-ComputerInfo -Property BiosFirmwareType, CsSystemType,
  CsNumberOfLogicalProcessors, CsTotalPhysicalMemory, HyperVisorPresent

Get-Tpm

try {
    Confirm-SecureBootUEFI
} catch {
    "Secure Boot não pôde ser consultado neste contexto: $($_.Exception.Message)"
}

Get-CimInstance Win32_PnPSignedDriver |
  Select-Object DeviceName, DriverVersion, Manufacturer, IsSigned
```

Algumas consultas exigem elevação, hardware compatível ou execução fora de uma
VM. `False`, `$null`, erro de permissão e “não suportado” são resultados
diferentes. Preserve essa distinção no inventário; não converta todo erro em
“desativado”. Evite serial de BIOS, UUID e identificadores físicos na evidência.

## Requisitos e dimensionamento

Requisito mínimo significa possibilidade de instalação suportada, não boa
experiência para qualquer carga. CPU, RAM, armazenamento, GPU, firmware, TPM e
drivers formam um conjunto. Verifique a lista oficial atual e o suporte do
fabricante antes de comprar ou atualizar. Uma VM também precisa expor o modelo
correto de firmware e, quando usado, TPM virtual persistente.

Capacidade e pressão são diferentes. Ter 8 GiB não prova que há memória
disponível; possuir 80 GiB de disco não prova espaço livre ou saúde. Colete o
estado durante a carga relevante, não apenas em repouso.

## Drivers e confiança

Driver executa em posição privilegiada e incompatibilidade pode causar falha de
boot ou instabilidade. Prefira Windows Update ou o fabricante do equipamento,
confirme modelo e sistema, verifique assinatura e registre versão anterior.
Sites que distribuem “driver packs” ou DLLs avulsas removem procedência e podem
introduzir software indesejado.

Assinatura válida confirma identidade do signatário e integridade desde a
assinatura; não garante ausência de bug. `IsSigned` também não substitui a
análise da cadeia e do status da assinatura quando uma decisão real for tomada.

## Firmware sem improviso

Atualização de UEFI pode corrigir compatibilidade e segurança, mas uma interrupção
é de alto impacto. Antes dela: conecte energia confiável, leia as instruções do
fabricante, registre configurações, suspenda/proceda com BitLocker conforme a
documentação, garanta recovery key e conheça o método de recuperação da placa.
Não altere Secure Boot, modo de armazenamento ou TPM tentando “ver se funciona”.
Uma mudança por vez mantém o diagnóstico possível.

Em laboratório virtual, compare duas VMs idênticas, uma com firmware UEFI/TPM
virtual e outra conforme uma configuração alternativa suportada pelo hipervisor.
Não aplique a comparação ao equipamento principal.

## Exercícios

1. Desenhe firmware → entrada de boot → Boot Manager → loader → kernel e marque
   onde GPT, Secure Boot e TPM participam.
2. Para cada comando de inventário, documente resultado, ausência, erro de
   acesso e não suportado como estados separados.
3. Explique por que TPM presente não implica BitLocker habilitado.
4. Crie um checklist de atualização de firmware com prevenção e recuperação.
5. Escolha um driver da VM, registre fornecedor, versão e assinatura sem
   atualizá-lo. Explique qual fonte seria aceitável para uma nova versão.

## Checklist de domínio

- [ ] Diferencio firmware UEFI, GPT e EFI System Partition.
- [ ] Diferencio validação do Secure Boot, medição do TPM e cifra do BitLocker.
- [ ] Não interpreto falha de consulta como recurso desativado.
- [ ] Inventário de hardware não publica seriais ou UUIDs.
- [ ] Sei por que driver e firmware exigem fonte oficial e rollback.
- [ ] Não contorno requisitos de hardware em um sistema de produção.
- [ ] Consigo explicar toda a cadeia de inicialização em linguagem simples.
