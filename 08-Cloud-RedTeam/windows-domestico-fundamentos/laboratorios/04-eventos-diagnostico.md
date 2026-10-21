# Lab 04 — Eventos, linha do tempo e diagnóstico

**Classe: A — observação local e arquivos de fixture.**

Este gate avalia a capacidade de transformar sintoma em hipótese sem limpar logs,
provocar crash ou aplicar reparos. O resultado pode ser “nenhum evento relevante
encontrado”, desde que a cobertura e as limitações estejam demonstradas.

## Pré-requisitos e cenário

Conclua o Lab 03, os capítulos 08–13 e leia o guia transversal de diagnóstico.
Escolha um aplicativo nativo e uma fixture. Outra pessoa define um sintoma
reversível: arquivo com formato inválido, caminho ausente ou aplicativo fechado
antes de salvar. Não altere binário ou arquivo do sistema.

Antes da ação, registre build, timezone, relógio UTC, conta, intervalo máximo de
15 minutos e comportamento esperado. Escreva três hipóteses e a evidência que
refutaria cada uma.

## Procedimento

1. Marque `StartUtc` e anote o record ID mais recente de `Application` e `System`.
2. Execute a ação de fixture uma vez e registre o sintoma em termos mensuráveis.
3. Marque `EndUtc`; não reinicie, encerre à força ou faça reparo.
4. Consulte cada canal usando `FilterHashtable` e o intervalo.
5. Selecione no máximo 50 registros relevantes, incluindo provider, ID, nível,
   record ID e horário UTC.
6. Abra `perfmon /rel` e procure o mesmo período. Trate-o como índice.
7. Monte uma linha do tempo com ação, sintoma, eventos e mudanças conhecidas.
8. Para cada hipótese, marque evidência a favor, contra e desconhecida.
9. Escolha o teste seguinte de menor impacto e execute somente se ainda estiver
   dentro do escopo da fixture.
10. Exporte JSON e reabra com `ConvertFrom-Json` para validar.

Exemplo de coleta inicial:

```powershell
$start = [datetime]'2026-01-01T12:00:00Z'
$end = $start.AddMinutes(15)
Get-WinEvent -FilterHashtable @{
  LogName = 'Application'
  StartTime = $start
  EndTime = $end
} | Select-Object -First 50 TimeCreated, ProviderName, Id,
    LevelDisplayName, RecordId
```

Substitua o horário por variáveis realmente coletadas. Não copie a data de
exemplo. Se a interface usar tempo local, registre a conversão.

## Evidências

- definição operacional do sintoma e critérios de reprodução;
- início/fim UTC e timezone local;
- consulta exata e JSON sanitizado;
- linha do tempo com fato, relato, inferência e lacuna;
- tabela das três hipóteses e teste discriminador;
- comparação com Monitor de Confiabilidade;
- conclusão com grau de confiança e próximo passo.

Mensagem renderizada pode conter caminho ou nome de usuário. Substitua apenas a
cópia do relatório por rótulos consistentes; preserve o significado e explique a
sanitização. Não edite o arquivo bruto de laboratório para esconder evidência.

## Interpretação obrigatória

Escolha dois eventos e explique por que nível não é impacto. Para qualquer ID,
cite provider e canal. Se encontrar erro próximo ao sintoma, proponha um mecanismo
plausível e um teste; não escreva “foi a causa” apenas pela proximidade.

Se não encontrar evento, avalie canal, retenção, provider, permissão e cobertura.
A ausência pode reduzir uma hipótese, nunca provar que a ação não ocorreu.

## Cleanup e aprovação

Feche o aplicativo normalmente, remova somente as fixtures e mantenha os logs
intactos. Restaure snapshot se o cenário alterou associações ou configurações.
Compare o estado final com a baseline.

O gate passa com intervalo pequeno, filtros eficientes, timeline coerente,
hipóteses refutáveis e conclusão proporcional à evidência. Reprova se coletar
todo log sem necessidade, limpar canal, provocar crash, ocultar ausência, usar ID
sem provider ou aplicar uma “correção” antes de diagnosticar.

## Questões de defesa

1. Por que um erro pode ser parte de recuperação normal?
2. O que record ID ajuda a ordenar e o que não garante?
3. Por que `Where-Object` após carregar todo canal foi evitado?
4. Como timezone incorreto mudaria a conclusão?
5. Qual evidência adicional distinguiria suas duas hipóteses principais?
