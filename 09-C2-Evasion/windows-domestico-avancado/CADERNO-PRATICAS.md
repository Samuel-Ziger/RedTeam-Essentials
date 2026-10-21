# Caderno de 56 práticas

Execute em ordem na VM e registre previsão, ação, evidência, interpretação, risco e cleanup. Cada prática só termina quando o critério de aceite é demonstrado.

## Arquitetura, método e objetos

### P01 — Contrato avançado

Classifique seis ações nas classes A–D e defina parada. **Aceite:** alvo, dado, privilégio, reversão e proibição estão explícitos.

### P02 — Build identificável

Registre versão, arquitetura, hash, símbolos e UTC de uma fixture. **Aceite:** outro estudante seleciona exatamente o mesmo build.

### P03 — Mapa NT

Desenhe aplicação, subsistemas, Executive, kernel, HAL e driver. **Aceite:** fronteiras documentadas não são confundidas com chamadas internas.

### P04 — API, ABI e syscall

Escolha uma API e descreva contrato, biblioteca, transições possíveis e erros. **Aceite:** não afirma uma syscall única sem evidência.

### P05 — Objeto e handle

Observe arquivo próprio aberto e fechado. **Aceite:** objeto, nome, handle, tabela e ciclo de vida permanecem distintos.

### P06 — Processo e thread

Compare duas execuções da fixture. **Aceite:** identidade estável e valores efêmeros, como PID, são separados.

### P07 — Job e sincronização

Modele limite de processo e dois mecanismos de sincronização. **Aceite:** ownership, espera, timeout e falha são explicados.

## Identidade e memória

### P08 — Token observado

Registre SID, grupos, privilégios e integrity level do próprio terminal. **Aceite:** presente, habilitado e efetivo não são sinônimos.

### P09 — Sessão comparada

Compare IDs de sessão de duas execuções controladas. **Aceite:** sessão, usuário e desktop não são tratados como um único objeto.

### P10 — MIC previsto

Preveja uma decisão de escrita entre níveis na fixture e valide sem relaxar ACL. **Aceite:** MIC e DACL têm papéis separados.

### P11 — Reserva e commit

Desenhe regiões de memória da fixture. **Aceite:** reservar endereço não é descrito como consumir RAM equivalente.

### P12 — Working set amostrado

Colete dez amostras sob carga repetida. **Aceite:** crescimento inicial não é chamado de vazamento.

### P13 — Page fault explicado

Compare soft e hard fault conceitualmente. **Aceite:** page fault não é traduzido automaticamente como acesso a disco.

### P14 — Memória no VMMap

Classifique image, mapped file, heap e private data. **Aceite:** categorias e unidades aparecem no relatório.

## PE, DLL e arquivos

### P15 — DOS e assinatura PE

Leia `MZ`, `e_lfanew` e `PE\0\0` de binário próprio. **Aceite:** todo offset é validado contra tamanho.

### P16 — COFF e optional header

Registre machine, seções, magic e subsystem. **Aceite:** PE32 e PE32+ não são confundidos com arquitetura isoladamente.

### P17 — RVA e offset

Converta uma posição de seção em papel. **Aceite:** alinhamento e limites fazem parte do cálculo.

### P18 — Imports e exports

Compare `dumpbin` com o parser didático. **Aceite:** import estático e resolução dinâmica permanecem distintos.

### P19 — Build da DLL

Compile e execute o consumidor. **Aceite:** saída, toolchain e hashes são reproduzíveis.

### P20 — Busca segura

Revise a composição do caminho absoluto. **Aceite:** nenhuma dependência usa diretório atual ou `PATH` global.

### P21 — ABI incompatível

Altere a versão para 2 e restaure. **Aceite:** incompatibilidade é detectada antes da operação e o código volta à versão 1.

## Registro, NTFS e I/O

### P22 — Hive e identidade

Compare chave fixture HKCU em duas contas de laboratório. **Aceite:** diferenças são explicadas sem copiar dados entre perfis.

### P23 — Tipos do Registro

Armazene texto `1` e DWORD `1`. **Aceite:** tipo e representação são preservados no contrato.

### P24 — Visões do Registro

Explique redirecionamento 32/64 bits na arquitetura usada. **Aceite:** nenhuma conclusão é generalizada para outra arquitetura.

### P25 — MFT e atributos

Modele registro e atributos de um arquivo fixture. **Aceite:** nome visível não é tratado como toda a identidade.

### P26 — Links e reparse points

Inspecione um link criado no lab sem atravessá-lo em cleanup recursivo. **Aceite:** alvo e link são removidos deliberadamente.

### P27 — Timestamps

Copie, mova e edite fixtures; registre UTC. **Aceite:** resultados são observações do filesystem testado, não regras universais.

### P28 — I/O síncrono e assíncrono

Desenhe buffers, espera e conclusão. **Aceite:** assíncrono não é declarado mais rápido por definição.

## Drivers, serviços e PowerShell

### P29 — Inventário de driver

Registre provider, versão, data, INF e assinatura de dispositivo virtual. **Aceite:** nenhuma atualização ou desativação é feita.

### P30 — Pilha de dispositivo

Modele barramento, função e filtros. **Aceite:** presença de filtro não é classificada automaticamente como ameaça.

### P31 — Serviço observado

Compare estado, StartMode, conta e caminho de três serviços. **Aceite:** serviço parado não significa falha.

### P32 — Tarefa fixture

Crie, valide e remova `RTE-Fixture-Timestamp`. **Aceite:** conta comum, histórico e cleanup são comprovados.

### P33 — Pipeline tipado

Passe `FileInfo` para função avançada. **Aceite:** objetos chegam ao fim antes de qualquer formatação.

### P34 — Streams separados

Produza sucesso, verbose e erro controlado. **Aceite:** resultado principal pode ser serializado sem mensagens misturadas.

### P35 — ShouldProcess

Implemente mutação restrita ao lab. **Aceite:** `-WhatIf`, raiz permitida, idempotência e reversão funcionam.

## Módulos e observabilidade

### P36 — Manifesto de módulo

Crie `.psd1` com export explícito. **Aceite:** helper privado não aparece em `Get-Command -Module`.

### P37 — Teste de contrato

Escreva Pester para schema, limite e erro. **Aceite:** introduzir uma regressão faz o teste falhar.

### P38 — Análise estática

Execute PSScriptAnalyzer e avalie alertas. **Aceite:** qualquer supressão é estreita e justificada.

### P39 — Authenticode lido

Inspecione assinatura de arquivo conhecido. **Aceite:** hash, assinatura, confiança e segurança comportamental são diferenciados.

### P40 — Evento completo

Registre canal, provider, ID, versão, record ID e UTC. **Aceite:** significado não depende apenas do número do evento.

### P41 — Sessão ETW modelada

Desenhe provider, controller, session, buffers e consumer. **Aceite:** perda de eventos aparece como possibilidade verificável.

### P42 — ProcMon mínimo

Capture uma leitura de Registro saudável e ausente. **Aceite:** filtro, janela e sequência causal estão preservados.

## Desempenho e defesa

### P43 — Orçamento de desempenho

Defina carga, métrica, aquecimento e limite. **Aceite:** orçamento é escrito antes das amostras.

### P44 — Mediana e p95

Meça vinte execuções. **Aceite:** dados brutos, mínimo, mediana, p95 e máximo são apresentados.

### P45 — WPR/WPA

Capture uma execução e delimite a região. **Aceite:** processo, unidade, símbolo e overhead são verificados.

### P46 — Mudança única

Otimize uma decisão derivada da evidência. **Aceite:** função permanece correta e a mesma carga é repetida.

### P47 — Baseline Defender

Colete campos mínimos e redigidos. **Aceite:** indisponível, desabilitado e desconhecido não são misturados.

### P48 — Mitigações explicadas

Relacione DEP, ASLR e CFG a seus limites. **Aceite:** nenhuma é apresentada como correção de vulnerabilidade.

### P49 — Piloto auditável

Desenhe audit → pilot → enforce para uma regra. **Aceite:** compatibilidade, métrica, parada e rollback existem.

## VBS, debugging e capstone

### P50 — Estado Device Guard

Separe available, configured e running. **Aceite:** arrays são interpretados pela documentação da versão.

### P51 — Cadeia de confiança

Desenhe Secure Boot, TPM, BitLocker, VBS e HVCI. **Aceite:** objetivo e limite de cada camada estão escritos.

### P52 — Compatibilidade HVCI

Modele piloto para driver fictício. **Aceite:** atualização/substituição precede qualquer redução de proteção.

### P53 — Símbolos correspondentes

Abra dump da fixture com PDB correto e incorreto. **Aceite:** o relatório demonstra por que identidade do build importa.

### P54 — Triagem de exceção

Localize exception code, contexto e primeiro frame próprio. **Aceite:** `!analyze` é evidência auxiliar, não veredito.

### P55 — Correção e regressão

Corrija a falha benigna e adicione teste. **Aceite:** o teste falha antes, passa depois e o orçamento é reavaliado.

### P56 — Handoff e limpeza

Entregue o projeto a revisor sem orientação oral. **Aceite:** build, reprodução, decisão e cleanup são concluídos sem dados sensíveis.

## Registro de conclusão

Mantenha tabela com prática, data, snapshot, classe, evidência, revisor e resultado. Leitura não marca prática como concluída. Os seis laboratórios são os gates integradores; este caderno desenvolve as competências atômicas usadas neles.

