# 16 — Desempenho, WPR e WPA

Otimização começa por uma meta mensurável, não por uma lista de ajustes. Tempo de resposta, throughput, uso de recursos e energia podem apontar em direções diferentes. Windows Performance Recorder (WPR) e Windows Performance Analyzer (WPA) ajudam a correlacionar eventos e stacks, desde que a carga, a linha de base e a pergunta sejam controladas.

## Objetivos

Ao terminar, você deverá conseguir:

- definir uma métrica ligada à experiência do usuário;
- diferenciar utilização, saturação, latência e throughput;
- montar experimento com aquecimento, repetições e percentis;
- escolher entre counters, amostragem e tracing;
- capturar uma janela curta com WPR e explorá-la no WPA;
- propor mudança baseada em evidência e medir regressão.

## Do sintoma à métrica

“O programa está lento” precisa virar cenário: entrada, ação, hardware, versão e limite esperado. Por exemplo: “processar 500 arquivos fixture de 4 KiB deve terminar em até 800 ms no p95 após duas execuções de aquecimento”. Essa definição separa latência de uma execução do throughput ao longo de várias.

**Utilização** indica quanto um recurso esteve ocupado. **Saturação** indica trabalho aguardando o recurso. **Erros** mostram falhas ou retries. Esse modelo é útil para CPU, disco, memória e filas, mas counters precisam de contexto. CPU a 100% pode ser ótimo se o objetivo for concluir trabalho paralelo; CPU baixa com latência alta pode indicar espera por I/O ou contenção.

Memória exige termos precisos. Working set é memória residente observada para o processo; private bytes medem memória comprometida que não pode ser compartilhada dessa forma; commit do sistema é outra fronteira. Uma redução de working set causada por trim não significa que o programa passou a exigir menos memória.

## Experimento reproduzível

Controle versão do binário, conjunto de entrada, energia, concorrência e estado da VM. Faça aquecimento para reduzir efeitos de carregamento, JIT e cache. Meça várias vezes, preserve dados brutos e informe mediana e p95. Média sozinha esconde caudas.

Com vinte amostras, p95 ainda é uma estimativa grosseira; ela serve ao laboratório, não a uma conclusão estatística universal. Apresente mínimo, mediana, p95, máximo e dispersão visível. Alterar uma variável por rodada facilita atribuir o efeito.

```powershell
$samples = 1..20 | ForEach-Object {
    $elapsed = Measure-Command {
        Get-ChildItem -LiteralPath .\fixture -File | Get-FileHash | Out-Null
    }
    [pscustomobject]@{ Run = $_; Milliseconds = $elapsed.TotalMilliseconds }
}

$ordered = @($samples.Milliseconds | Sort-Object)
$p95Index = [math]::Ceiling($ordered.Count * 0.95) - 1
[pscustomobject]@{
    MedianMs = ($ordered[[math]::Floor(($ordered.Count - 1) / 2)])
    P95Ms    = $ordered[$p95Index]
    MaximumMs = $ordered[-1]
}
```

Para trabalho sério, trate mediana par/ímpar adequadamente e registre o ambiente. O exemplo enfatiza o método.

## Counters, sampling e tracing

Performance Monitor e `Get-Counter` observam séries de counters com baixo custo relativo:

```powershell
Get-Counter '\Processor(_Total)\% Processor Time',
            '\Memory\Available MBytes' `
            -SampleInterval 1 -MaxSamples 10
```

Um profiler por amostragem observa periodicamente onde threads executam; é eficiente para localizar consumo de CPU, mas pode perder operações raras. Tracing registra eventos selecionados e é mais adequado para sequência, I/O e agendamento, com custo dependente dos providers e stacks habilitados.

WPR oferece perfis de gravação; WPA analisa o ETL em gráficos e tabelas. Selecione o perfil mínimo, inicie imediatamente antes do cenário e pare logo depois. No WPA, alinhe a região temporal do sintoma, agrupe por processo e thread, confira unidade e ordene pelo custo relevante. Só então desça para stack.

Símbolos corretos transformam endereços em módulos e funções. Frames não resolvidos limitam a conclusão; não invente nomes. Um hotspot mostra onde amostras ou tempo se acumularam, mas a correção pode estar no chamador, na estrutura de dados ou em I/O anterior.

## Orçamento e regressão

Defina um orçamento como contrato testável, por exemplo p95 abaixo de um limite e memória privada abaixo de outro. Compare antes/depois com a mesma carga. Uma melhoria de tempo que dobra memória ou piora estabilidade precisa ser explicitada. Mantenha também um teste funcional: resultado rápido, porém incorreto, não é otimização.

Evite “otimizadores” que desabilitam serviços ou proteções em massa. Se uma mitigação introduz custo mensurável, documente o trade-off e corrija desenho ou compatibilidade; não transforme desempenho em justificativa automática para reduzir segurança.

## Exercícios

1. Escreva um cenário de benchmark com entrada, aquecimento, repetições e orçamento.
2. Calcule mediana e p95 sem descartar amostras inconvenientes.
3. Capture a execução da fixture com um perfil WPR mínimo e localize CPU ou File I/O no WPA.
4. Proponha uma única mudança, repita exatamente a carga e relate benefício e custo.

## Checklist

- [ ] O sintoma foi convertido em métrica e orçamento.
- [ ] A carga e o ambiente são reproduzíveis.
- [ ] Sei quando usar counter, sampling ou tracing.
- [ ] Percentis acompanham dados brutos e número de amostras.
- [ ] Otimização preserva correção, segurança e comparação justa.

