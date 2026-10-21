# 12 — Windows Event Log, confiabilidade e linhas do tempo

Logs registram observações produzidas por componentes; não são uma narrativa
pronta. O mesmo número de evento pode ter significado diferente por provider, e
um erro pode representar tentativa recuperada. A investigação precisa de
contexto, intervalo e correlação.

## Objetivos

- interpretar canal, provider, ID, nível, horário e payload;
- filtrar no mecanismo antes de formatar a saída;
- construir linha do tempo com ações, mudanças e sintomas;
- usar o Monitor de Confiabilidade como índice, não como fonte única;
- exportar evidência pequena, sanitizada e reproduzível.

## Anatomia de um evento

Um provider publica eventos em canais. O registro inclui Event ID, nível,
timestamp, record ID, máquina, usuário quando aplicável e dados estruturados ou
mensagem renderizada. `Event ID 1000` sozinho é ambíguo: provider e canal fazem
parte da identidade semântica.

Nível também não equivale diretamente a impacto. `Error` informa a classificação
do produtor, mas o componente pode ter repetido a operação com sucesso. Um
evento `Information` pode registrar a mudança relevante. A pergunta é “o que
aconteceu no intervalo do sintoma?”, não “quantos vermelhos existem?”.

## Filtragem eficiente

```powershell
$start = (Get-Date).AddHours(-2)
$events = Get-WinEvent -FilterHashtable @{
    LogName = 'System'
    StartTime = $start
} -ErrorAction Stop

$events |
  Select-Object -First 30 TimeCreated, ProviderName, Id,
    LevelDisplayName, RecordId
```

`FilterHashtable` envia critérios ao mecanismo e evita carregar um canal inteiro
para depois usar `Where-Object`. Comece por tempo e canal; refine por provider ou
ID observado. Não filtre pelo texto traduzido quando uma propriedade estruturada
está disponível.

O relógio da interface pode aparecer no timezone local, enquanto exportações
usam representações diferentes. No relatório, registre timezone e normalize a
UTC quando cruzar fontes:

```powershell
$events | Select-Object -First 30 @{ Name = 'TimeUtc'; Expression = {
    $_.TimeCreated.ToUniversalTime().ToString('o')
}}, ProviderName, Id, LevelDisplayName, RecordId |
  ConvertTo-Json -Depth 4
```

Mensagem pode conter caminhos, nomes ou documentos. Revise e sanitize antes de
compartilhar. Não exporte todo o log “por garantia”; minimize dados e preserve o
arquivo original somente quando o cenário realmente exigir.

## Linha do tempo e causalidade

Uma linha do tempo útil combina:

1. ação conhecida do usuário;
2. momento em que o sintoma foi percebido;
3. evento da aplicação;
4. evento do sistema;
5. mudança de aplicativo, driver ou atualização;
6. recuperação e teste posterior.

Ordene tudo numa base de tempo consistente. Marque cada entrada como fato
direto, informação do usuário, inferência ou lacuna. Proximidade temporal aumenta
uma hipótese, mas não demonstra causalidade. Procure mecanismo plausível e um
teste que possa refutar a hipótese.

## Monitor de Confiabilidade

`perfmon /rel` agrega falhas, instalações e mudanças por dia e oferece um bom
ponto de entrada. Seu índice é calculado; não é uma medição universal de “saúde”.
Use-o para localizar o período e retornar aos eventos e ao aplicativo. Uma
queda pode coincidir com falhas já resolvidas.

Compare o item agregado com provider, horário e versão. Se nada aparecer, isso
não prova ausência de falha; talvez o componente não publique naquele mecanismo.

## Ausência e retenção

Logs possuem tamanho e política de retenção. Eventos antigos podem ter sido
sobrescritos. Serviço parado, canal desabilitado, relógio incorreto e falta de
permissão também criam ausência. Registre a limitação em vez de escrever “não
aconteceu”. Não limpe logs durante diagnóstico ou prática.

Exportar `.evtx` preserva mais estrutura, mas JSON selecionado facilita análise
do curso. Guarde comandos de coleta para tornar a seleção reproduzível.

## Prática guiada

Marque início em UTC, abra uma aplicação nativa, crie uma fixture, feche-a
normalmente e marque o fim. Consulte `Application` e `System` apenas nesse
intervalo. Limite a 50 eventos, abra o Monitor de Confiabilidade e escreva uma
linha do tempo. É aceitável não encontrar evento relacionado: documente quais
fontes foram consultadas e por que ausência não é conclusão absoluta.

## Exercícios

1. Explique por que `ID` sem provider e canal é insuficiente.
2. Compare filtragem no mecanismo com `Where-Object` após carregar tudo.
3. Converta horários para UTC e registre o timezone original.
4. Escolha um erro antigo e demonstre por que proximidade não prova causa atual.
5. Produza JSON sanitizado e o comando exato que o gerou.

## Checklist de domínio

- [ ] Toda referência inclui canal, provider, ID e horário.
- [ ] Filtro por intervalo antes de coletar ou formatar.
- [ ] Registro timezone e normalizo quando correlaciono fontes.
- [ ] Diferencio nível do evento e impacto ao usuário.
- [ ] Monitor de Confiabilidade serve como índice, não veredito.
- [ ] Ausência é descrita com limites de retenção e cobertura.
- [ ] Não limpo logs nem exporto dados pessoais desnecessários.
