# Lab 05 — Baseline defensiva e piloto de compatibilidade

**Classe:** B para inventário; C apenas para mudança documentada em VM com snapshot e autorização local.

## Propósito

Produzir uma baseline das proteções do Windows e desenhar um piloto auditável. O gate avalia raciocínio de compatibilidade e verificação, não a quantidade de opções habilitadas. Nenhuma exclusão ampla, desativação do Defender ou política de execução `Bypass` é aceita.

## Pré-condições

- Labs 01–04 e capítulos 17–18 concluídos;
- VM própria, snapshot testado e conta administrativa disponível apenas para consulta autorizada;
- versão, edição e estado de gerenciamento documentados;
- fixtures dos gates anteriores funcionando com a postura atual.

Se a máquina for gerenciada por organização, limite-se à observação e não altere políticas. Se um cmdlet estiver indisponível, registre `unknown`, erro e contexto.

## Baseline minimizada

Colete somente campos necessários de `Get-MpComputerStatus`, `Get-MpPreference`, `Get-ProcessMitigation -System`, mitigação da fixture e `Win32_DeviceGuard`. Consulte também TPM e Secure Boot quando suportados. Não exporte exclusões, caminhos privados, identificadores de hardware ou política corporativa para o relatório público.

Modele quatro estados separados: `available`, `configured`, `running` e `unknown`. Um recurso compatível mas não configurado não equivale a um serviço configurado que falhou. Arrays de Device Guard devem ser interpretados com a documentação correspondente à versão.

Produza diagrama de camadas: Secure Boot, TPM/BitLocker quando disponíveis, VBS/HVCI, Defender Antivirus, ASR, Controlled Folder Access, Exploit Protection e Application Control. Para cada uma, registre objetivo e pelo menos um limite.

## Desenho do piloto

Escolha **uma** mitigação aplicável à fixture e consulte a documentação oficial. Prefira um modo de auditoria quando o recurso oferecer. Escreva:

- ameaça e comportamento que a política pretende reduzir;
- pré-requisitos de edição, hardware e reinicialização;
- população piloto e período;
- eventos e métricas esperados;
- testes funcionais da DLL, scripts e benchmark;
- critérios de parada e rollback;
- responsável e prazo para qualquer exceção.

Não aplique a mudança se o modo, o impacto ou o rollback não estiverem compreendidos. Um plano completo e não executado é melhor que enforcement improvisado.

## Execução opcional em snapshot

Se o recurso for suportado, a documentação for inequívoca e o ambiente for exclusivamente seu, exporte estado, confirme snapshot e aplique somente ao piloto. Reinicie quando exigido. Execute as fixtures saudáveis, consulte eventos e compare desempenho pelo mesmo método do Lab 04.

Uma incompatibilidade deve gerar investigação por regra, versão e evento. Procure atualização ou correção da fixture. Não crie exclusão de pasta e não desligue outra camada para fazer o teste passar. Depois restaure a política e confirme estado, ou reverta o snapshot se esse era o procedimento aprovado.

## Evidência e decisão

Entregue baseline redigida, matriz das camadas, plano do piloto, resultado funcional e decisão: promover, corrigir antes de repetir ou não aplicar. A decisão deve citar evidência e risco residual.

Explique por que assinatura válida não prova comportamento seguro; por que Credential Guard não protege todo segredo; e por que Execution Policy não é sandbox. Esses limites evitam um relatório falsamente binário.

## Critérios de aceite

- edição, versão e fonte de gerenciamento contextualizam a coleta;
- indisponível, desabilitado e desconhecido permanecem distintos;
- nenhuma proteção foi reduzida para concluir o gate;
- piloto possui auditabilidade, compatibilidade, rollback e verificação;
- relatório público não contém exclusões ou dados identificáveis.

## Cleanup e revisão

Confirme que a política voltou ao estado definido, que fixtures funcionam e que dumps/traces não foram criados. Apague exports brutos sensíveis e preserve somente baseline redigida.

Responda: que controle cobre execução de código e qual cobre escrita em pastas? Que evidência prova que uma política está rodando, não apenas configurada? Quando a decisão correta é substituir um driver? Qual controle compensatório acompanha uma exceção temporária?

