# 10 — I/O, dispositivos e drivers

O subsistema de entrada e saída conecta uma chamada aparentemente simples — ler um arquivo, reproduzir áudio ou consultar um sensor — a uma cadeia de componentes no modo usuário e no kernel. O objetivo deste capítulo não é desenvolver drivers: é construir um modelo mental que permita diagnosticar dispositivos e operações de I/O sem alterar componentes sensíveis do sistema.

## Objetivos

Ao terminar, você deverá conseguir:

- descrever o caminho entre uma API, um handle, o I/O Manager e uma pilha de dispositivos;
- diferenciar I/O síncrono, assíncrono, em buffer e mapeado em memória;
- explicar o papel conceitual de IRPs, drivers de barramento, função e filtro;
- relacionar Plug and Play, energia, assinatura e compatibilidade de driver;
- produzir um inventário somente leitura e uma hipótese de diagnóstico reproduzível.

## Da chamada à conclusão

Um programa normalmente não conversa diretamente com o hardware. Ele chama uma API, recebe ou usa um *handle* e solicita uma operação. Depois da validação de parâmetros e permissões, o I/O Manager representa o pedido internamente e o encaminha à pilha associada ao dispositivo. Nessa pilha, um driver pode transformar, encaminhar ou concluir o pedido.

Uma **IRP** (*I/O Request Packet*) é uma estrutura do kernel usada para representar muitas dessas solicitações. Ela carrega o tipo da operação, parâmetros, estado e locais de pilha destinados aos drivers participantes. É importante não reduzir o modelo a “um pacote que sempre chega ao hardware”: uma operação pode ser atendida por cache, por um driver virtual ou falhar antes de qualquer acesso físico.

Uma pilha típica pode conter:

- **driver de barramento**, responsável por enumerar dispositivos e representar a conexão física ou lógica;
- **driver de função**, que implementa o comportamento principal do dispositivo;
- **drivers de filtro**, que observam ou complementam o fluxo acima ou abaixo do driver de função.

Filtros legítimos aparecem em antivírus, criptografia, backup e monitoramento. A presença de um filtro, isoladamente, não prova falha nem ameaça.

## Sincronia, buffers e conclusão

Em I/O síncrono, a thread pode aguardar a conclusão da operação. Em I/O assíncrono ou *overlapped*, ela inicia a solicitação e continua o trabalho; a conclusão é observada depois por evento, callback ou mecanismo como I/O Completion Ports. Isso permite atender muitas operações sem reservar uma thread bloqueada para cada uma, mas exige controlar ciclo de vida do buffer, cancelamento e erros parciais.

“Assíncrono” não significa automaticamente “mais rápido”. Para uma única leitura pequena, a coordenação pode custar mais do que economiza. Ele é valioso quando há concorrência, latência externa ou trabalho útil durante a espera.

O modo de transferência também importa. O Windows pode copiar dados por buffers do sistema, descrever páginas já existentes ou mapear arquivos em memória. Cada escolha envolve segurança, pressão de memória e custo de cópia. No diagnóstico, não conclua que toda leitura vista em uma ferramenta equivale a uma ida ao disco: cache do sistema de arquivos e memória mapeada mudam esse caminho.

## Plug and Play e energia

O Plug and Play coordena descoberta, identificação, instalação e remoção. IDs de hardware e compatibilidade ajudam o Windows a escolher um pacote de driver. O Power Manager coordena transições de energia; por isso, uma falha que aparece ao suspender ou retomar pode estar ligada à sequência de energia, não à carga normal.

Drivers operam com privilégios elevados e uma falha pode comprometer estabilidade e confidencialidade. Avalie origem, assinatura, versão, data, modelo do dispositivo e compatibilidade com a versão do Windows. Assinatura válida responde quem assinou e se o conteúdo permaneceu íntegro; não garante qualidade ou ausência de vulnerabilidades.

```powershell
$drivers = Get-CimInstance Win32_PnPSignedDriver |
    Select-Object DeviceName, DeviceClass, DriverProviderName,
                  DriverVersion, DriverDate, IsSigned, InfName

$drivers |
    Sort-Object DeviceClass, DeviceName |
    Export-Csv -NoTypeInformation -Encoding utf8 .\drivers-inventario.csv
```

Esse comando apenas inventaria. Não remova, desative ou atualize drivers durante a coleta. Guarde também a versão do sistema e o horário para que a comparação futura tenha contexto.

## Método seguro de diagnóstico

Comece pelo sintoma observável: horário, dispositivo, ação e resultado. Depois correlacione o código exibido no Gerenciador de Dispositivos, eventos do provedor relevante, mudanças recentes e versão do pacote. Formule uma hipótese testável, altere uma variável por vez e registre o resultado. Um *rollback* direcionado pode ser válido quando existe evidência temporal, mas “atualizar todos os drivers” mistura variáveis e destrói a linha de base.

No laboratório, use um dispositivo virtual ou um periférico não essencial. Nunca desative controladores de armazenamento, entrada necessária, vídeo principal ou componentes dos quais a VM depende.

## Exercícios

1. Gere dois inventários com dez minutos de intervalo e escreva um script que compare `DriverVersion`, `IsSigned` e `InfName` por dispositivo.
2. Escolha um dispositivo virtual e desenhe a sequência API → handle → I/O Manager → pilha → conclusão. Marque o que foi observado e o que é inferência.
3. Explique por que duração alta de uma leitura não prova defeito físico e liste três causas alternativas.
4. Identifique nos logs apenas os eventos do dispositivo escolhido, exporte o intervalo mínimo e registre a consulta usada.

## Checklist

- [ ] Distingo solicitação de I/O, IRP e operação física.
- [ ] Sei explicar drivers de barramento, função e filtro.
- [ ] Entendo os custos e responsabilidades do I/O assíncrono.
- [ ] Não interpreto assinatura válida como garantia de segurança.
- [ ] Meu diagnóstico preserva estado, evidência e possibilidade de reversão.

