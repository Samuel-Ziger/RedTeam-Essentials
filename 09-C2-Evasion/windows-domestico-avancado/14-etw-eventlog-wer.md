# 14 — ETW, Event Log e Windows Error Reporting

Observabilidade no Windows não é uma única caixa de logs. O Event Tracing for Windows (ETW) transporta eventos estruturados e de alto volume; Windows Event Log persiste eventos em canais administráveis; Windows Error Reporting (WER) registra falhas e pode produzir dumps. Saber escolher e correlacionar essas fontes reduz capturas enormes e conclusões frágeis.

## Objetivos

Ao concluir, você deverá conseguir:

- distinguir provider, controller, session e consumer em ETW;
- explicar canais e registros do Windows Event Log;
- planejar uma captura mínima com início, fim e hipótese;
- reconhecer perda de eventos e limites de interpretação;
- coletar somente um mini dump de uma fixture própria;
- tratar traces, logs e dumps como dados potencialmente sensíveis.

## Modelo do ETW

Um **provider** publica eventos com identificador, nível, palavras-chave e payload. Uma **session** mantém buffers e providers habilitados. Um **controller** inicia, configura e encerra a sessão. Um **consumer** lê eventos em tempo real ou de um arquivo ETL e interpreta o esquema.

Esse desacoplamento permite coleta eficiente, mas cria escolhas importantes. Habilitar todos os providers e todas as palavras-chave aumenta volume, custo e exposição de dados. Antes de capturar, escreva a pergunta: “por que a fixture demora mais na segunda etapa?” é melhor do que “gravar tudo”. Escolha providers ligados à hipótese, estabeleça uma janela curta e registre configuração e relógio.

Buffers finitos podem perder eventos quando o produtor supera o consumidor ou a gravação. Um trace sem evento esperado pode significar ausência real, provider incorreto, keyword desabilitada ou perda. Verifique estatísticas da sessão antes de concluir.

O arquivo ETL contém eventos, não uma narrativa pronta. Correlação temporal ajuda, mas proximidade no tempo não prova causalidade. Compare uma linha de base, repita a carga e procure uma cadeia coerente entre início, atividade e resultado.

## Windows Event Log

O Event Log organiza registros em canais, como `System`, `Application` e canais `Operational` específicos. Cada evento possui provedor, ID, nível, horário, record ID e payload. O mesmo ID só faz sentido junto ao provedor e à versão do esquema; memorizar “ID X significa Y” sem contexto é um erro comum.

```powershell
Get-WinEvent -ListProvider *PowerShell* |
    Select-Object Name, LogLinks

$start = (Get-Date).AddMinutes(-15)
Get-WinEvent -FilterHashtable @{
    LogName   = 'System'
    StartTime = $start
    Level     = 2,3
} -ErrorAction SilentlyContinue |
    Select-Object TimeCreated, ProviderName, Id, LevelDisplayName, Message
```

`FilterHashtable` filtra na origem e é preferível a carregar um canal inteiro para depois usar `Where-Object`. Uma consulta vazia não prova saúde; confirme se o canal está habilitado, se a retenção cobriu o período e se a fonte realmente registra ali.

Ao exportar, preserve horário em UTC, nome do computador, consulta e intervalo. A mensagem localizada é útil para humanos, mas automação deve priorizar campos estruturados.

## Windows Error Reporting e dumps

WER coleta metadados de falhas e pode coordenar relatórios ou dumps conforme configuração. Um **mini dump** contém subconjuntos necessários para triagem; um **full dump** pode conter grande parte da memória do processo. Mesmo um mini dump pode revelar caminhos, argumentos e fragmentos de dados.

Neste curso, capture somente uma aplicação fixture criada por você, sem credenciais e sem documentos reais. Nunca gere dumps de navegador, gerenciador de senhas, autenticação, sistema de segurança ou processo de terceiros. Defina antes: caminho restrito, tamanho máximo, período de retenção e exclusão ao final.

Os quatro dados mínimos de uma falha são:

1. versão exata do binário e símbolos;
2. horário e ação que disparou a fixture;
3. exception code e thread em falha;
4. stack e primeiro frame pertencente ao seu código.

Um dump é uma fotografia: ele não preserva toda a sequência anterior. Combine-o com logs de aplicação e, quando necessário, trace curto.

## Um plano de captura reproduzível

Escreva uma ficha com hipótese, versão, relógio, comandos, início, ação de reprodução, término, indicadores de perda e hashes dos artefatos. Faça primeiro uma execução sem falha para obter linha de base. Depois execute exatamente uma alteração. Se a coleta muda o comportamento, registre esse efeito; observabilidade também introduz custo.

Não compartilhe ETL, EVTX ou dump bruto em serviço público. Faça triagem local e produza um relatório minimizado com os campos indispensáveis.

## Exercícios

1. Liste providers ligados a uma fixture e justifique por que dois seriam suficientes.
2. Consulte uma janela de quinze minutos com `FilterHashtable` e exporte os campos estruturados.
3. Compare ETW e Event Log para volume, retenção, esquema e caso de uso.
4. Planeje a coleta de mini dump da fixture do capítulo 19, incluindo descarte, mas não colete processo externo.

## Checklist

- [ ] Distingo transporte ETW, persistência em canais e relato de falha.
- [ ] Toda captura começa com hipótese e janela delimitada.
- [ ] Verifico perda de eventos antes de interpretar ausência.
- [ ] Dumps são restritos à fixture própria e tratados como sensíveis.
- [ ] Correlaciono fontes sem confundir simultaneidade com causa.

