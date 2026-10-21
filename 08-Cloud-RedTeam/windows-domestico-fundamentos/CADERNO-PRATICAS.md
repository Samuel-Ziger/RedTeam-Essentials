# Caderno de 48 práticas

Faça as práticas na VM, em ordem, e registre previsão, comando/ação, evidência,
interpretação e cleanup. “Concluído” significa que o critério de aceite foi
demonstrado, não apenas que o comando executou.

## Método, versão e instalação

### P01 — Contrato do laboratório

Desenhe VM, firmware, dois discos, snapshots e limites. Classifique quatro ações
nas classes A–D. **Aceite:** cada ação possui alvo, risco, parada e rollback.

### P02 — Diário reproduzível

Execute uma consulta simples, registre hipótese e peça a outra pessoa para
repetir sem ajuda. **Aceite:** resultados equivalentes e dados sanitizados.

### P03 — Identidade do Windows

Compare `winver`, `Get-ComputerInfo` e CIM para edição, versão, build e arquitetura.
**Aceite:** diferenças de apresentação e cobertura estão explicadas.

### P04 — Ciclo de suporte

Consulte a fonte oficial atual e registre versão/edição, fim de suporte, URL e
data. **Aceite:** informação local e informação externa estão separadas.

### P05 — Cadeia de boot

Desenhe UEFI, GPT, ESP, Boot Manager, loader e kernel; marque Secure Boot e TPM.
**Aceite:** validação, medição, proteção de chave e cifra não são confundidas.

### P06 — Plano de instalação

Crie checklist de mídia, licença, backup, discos, OOBE e baseline. **Aceite:** o
plano impede selecionar disco por letra/posição e não usa bypass.

## Interface e arquivos

### P07 — Mapa de ferramentas

Relacione dez necessidades a Settings, MMC, utilitário e consulta PowerShell.
**Aceite:** a escolha é explicada pelo objeto administrado.

### P08 — GUI versus objeto

Colete build e espaço livre por interface e PowerShell. **Aceite:** unidades,
arredondamento e momento da coleta explicam diferenças.

### P09 — Preferência acessível

Aplique uma configuração de acessibilidade ao usuário fictício e reverta.
**Aceite:** necessidade, teste com a conta e rollback estão documentados.

### P10 — Caminhos literais

Crie fixtures com espaço, acento e `[01]`; consulte usando `-LiteralPath`.
**Aceite:** nenhum curinga expande e todos os caminhos são resolvidos.

### P11 — Nome, bytes e origem

Altere extensão, depois conteúdo, e compare hash e associação. **Aceite:** a
conclusão distingue nome, formato, bytes, assinatura e procedência.

### P12 — Metadados em operações

Copie, mova e renomeie fixtures entre pastas; compare timestamps UTC e hashes.
**Aceite:** observações não são generalizadas além do experimento.

## Armazenamento e identidade

### P13 — Mapa de armazenamento

Associe `Get-Disk`, `Get-Partition` e `Get-Volume` num diagrama. **Aceite:** disco,
partição, volume, filesystem e ponto de montagem são distintos.

### P14 — Decisão de filesystem

Compare NTFS e exFAT para SSD interno e mídia intercambiável. **Aceite:** a
escolha usa ACL, journaling, tamanho e compatibilidade como requisitos.

### P15 — Estado do BitLocker

Consulte conversão, porcentagem, proteção e protetores sem exportar segredo.
**Aceite:** indisponível, não consultável e desativado permanecem separados.

### P16 — Fluxo de autorização

Desenhe conta, SID, grupos, token, ACE e decisão de acesso. **Aceite:** autenticação
e autorização são explicadas com exemplos diferentes.

### P17 — Herança prevista

Antes de alterar a fixture, preveja ACEs herdadas em três arquivos e consulte.
**Aceite:** divergências são investigadas sem usar `FullControl` ou `Deny`.

### P18 — UAC em contexto

Compare conta comum, administrador não elevado e processo elevado em uma tabela.
**Aceite:** o texto explica por que UAC não substitui privilégio mínimo.

## Execução e aplicativos

### P19 — Processo e instância

Abra duas instâncias de aplicativo nativo; registre PID, caminho e início.
**Aceite:** PID é tratado como temporário e nome não é usado como identidade única.

### P20 — Amostragem de recursos

Colete cinco amostras de CPU acumulada e working set de uma fixture. **Aceite:**
contador, taxa, memória física e vazamento não são confundidos.

### P21 — Serviços sem alteração

Compare estado, StartMode, conta e dependências de três serviços. **Aceite:** um
serviço parado não é classificado automaticamente como falha.

### P22 — Mecanismos de início

Classifique itens observados como aplicativo de inicialização, tarefa ou serviço.
**Aceite:** cobertura e limitações da ferramenta estão descritas.

### P23 — Procedência de pacote

Para um instalador não executado, registre fonte, hash, assinatura, arquitetura e
licença. **Aceite:** formato e confiança não são tratados como sinônimos.

### P24 — Ciclo de aplicativo

Em snapshot, instale/repare um pacote oficial pequeno, valide e remova. **Aceite:**
dados, integrações, versão, reboot e resíduos têm decisão documentada.

## Servicing, Registro e eventos

### P25 — Linha do tempo de update

Relacione build, histórico, KB/pacotes e reinicializações. **Aceite:** nenhuma
fonte é apresentada como cobertura total do servicing.

### P26 — Diagnóstico por fase

Crie uma árvore para falha em detecção, download, instalação e boot. **Aceite:**
cada ramo tem evidência e ação de menor impacto distintas.

### P27 — Component Store explicado

Explique por que tamanho de `WinSxS` no Explorer pode enganar e qual mecanismo
oficial gerencia componentes. **Aceite:** nenhuma remoção manual é proposta.

### P28 — Tipos do Registro

Na chave RTECourse, crie String e DWORD representando “1” e compare. **Aceite:**
tipo e dado são registrados e a chave é removida.

### P29 — Contexto de HKCU

Consulte a chave de laboratório em duas contas comuns. **Aceite:** diferenças são
explicadas pela identidade, sem copiar valor entre perfis.

### P30 — Evento completo

Escolha um evento e registre canal, provider, ID, nível, record ID e UTC.
**Aceite:** nenhuma conclusão depende apenas de ID ou cor.

## Backup e proteção

### P31 — Objetivos de continuidade

Defina RPO/RTO para documentos do usuário fictício. **Aceite:** frequência,
retenção e tempo de restore derivam dos objetivos.

### P32 — Falhas compartilhadas

Desenhe estratégia 3-2-1 virtual e marque host, disco e credencial compartilhados.
**Aceite:** três pastas no mesmo volume não contam como independência.

### P33 — Restore por manifesto

Faça backup da fixture, restaure em caminho novo e compare SHA-256. **Aceite:**
conteúdo é aberto e o tempo real é comparado ao RTO.

### P34 — Corrupção detectável

Altere um byte numa cópia de teste e execute a comparação. **Aceite:** a prática
reprova a divergência e preserva o backup original.

### P35 — Baseline do Defender

Colete engine/serviço, inteligência, tempo real e idades de scan. **Aceite:** erro,
ausência, produto terceiro e estado falso são tratados separadamente.

### P36 — Integridade de binário conhecido

Registre versão, hash e assinatura de componente nativo. **Aceite:** o relatório
explica exatamente o que cada evidência demonstra e não demonstra.

## PowerShell e automação

### P37 — Descoberta de comandos

Use `Get-Command`, `Get-Help` e `Get-Member` para uma consulta. **Aceite:** origem,
tipo do comando, propriedades e exemplos úteis estão anotados.

### P38 — Objetos antes de formato

Exporte processos selecionados antes e depois de `Format-Table` para comparar.
**Aceite:** explica por que formatação deve ficar no fim.

### P39 — Função validada

Implemente resumo de volume com parâmetro obrigatório e validação de letra.
**Aceite:** entrada inválida falha antes de consultar ou alterar estado.

### P40 — Erro explícito

Consulte fixture ausente com `-ErrorAction Stop` e `try/catch` específico.
**Aceite:** o erro não é ocultado e nenhuma saída falsa de sucesso é produzida.

### P41 — Saída determinística

Produza JSON com schema, UTC, propriedades mínimas e ordem estável. **Aceite:**
`ConvertFrom-Json` reabre e nenhum identificador proibido aparece.

### P42 — Revisão de script

Revise os dois exemplos linha a linha e identifique validação, falhas e rollback.
**Aceite:** nenhuma execução ocorre antes da revisão e de `-WhatIf` aplicável.

## Diagnóstico e capstone

### P43 — Sintoma mensurável

Reescreva “está lento”, “não abre” e “travou” como problemas operacionais.
**Aceite:** ação, tempo, escopo, frequência e impacto aparecem.

### P44 — Matriz de hipóteses

Para fixture que não abre, escreva quatro hipóteses, evidências contra e testes.
**Aceite:** o primeiro teste divide hipóteses com baixo risco.

### P45 — Integridade sem ritual

Associe DISM, SFC e CHKDSK aos objetos que verificam. **Aceite:** nenhum comando
de reparo é recomendado sem hipótese, backup e validação posterior.

### P46 — Linha do tempo correlacionada

Junte ação, sintoma, eventos e mudança em UTC. **Aceite:** fato, relato,
inferência e lacuna estão rotulados.

### P47 — Runbook sem fala

Entregue a outra pessoa um procedimento de restauração e permaneça em silêncio.
**Aceite:** ambiguidades observadas são corrigidas e o teste é repetido.

### P48 — Defesa final

Apresente baseline, falha cega, diagnóstico, restore e cleanup em dez minutos.
**Aceite:** cada afirmação aponta para evidência e incertezas são explícitas.

## Registro de conclusão

Use uma tabela com prática, data, snapshot, evidência, revisor e resultado. Não
marque práticas por leitura. Os seis gates da trilha são a validação integrada;
este caderno prepara as habilidades atômicas.
