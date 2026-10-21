# 15 — Sysinternals para diagnóstico local

Sysinternals é uma suíte oficial de utilitários para compreender processos, inicialização, arquivos, Registro e memória no Windows. A força dessas ferramentas também exige disciplina: uma captura ampla pode conter nomes de documentos, comandos, caminhos e dados de outros usuários. Aqui elas serão usadas somente no computador de laboratório e em processos fixture próprios.

## Objetivos

Ao final, você deverá conseguir:

- escolher a ferramenta de acordo com uma pergunta observável;
- confirmar procedência, assinatura e versão antes da execução;
- construir filtros mínimos no Process Monitor;
- correlacionar processo, módulo, handle, assinatura e memória;
- interpretar resultados comuns sem transformar todo evento em incidente;
- exportar evidência minimizada e limpar os artefatos do exercício.

## Aquisição e confiança

Obtenha a suíte somente da página oficial Microsoft Sysinternals ou de um repositório interno previamente validado. Registre versão ou hash, confira a assinatura digital e leia os termos da ferramenta. Não copie executáveis de coleções desconhecidas, mesmo que o nome pareça correto.

Assinatura válida ajuda a confirmar origem e integridade, mas a autorização para executar continua dependendo do ambiente. Faça download no host confiável, transfira para a VM conforme a política do laboratório e mantenha uma cópia versionada para reproduzir resultados.

## Ferramenta certa para a pergunta

| Ferramenta | Pergunta principal | Evidência útil |
|---|---|---|
| Process Explorer | Quem executa e quais recursos carregou? | árvore, token, threads, handles, DLLs |
| Process Monitor | Que operações de arquivo, Registro e processo ocorreram? | sequência, resultado, caminho, duração |
| Autoruns | O que está configurado para iniciar automaticamente? | local, publisher, assinatura, comando |
| Sigcheck | Qual é a identidade técnica de um arquivo? | hash, versão, assinatura, cadeia |
| Handle | Qual processo mantém um objeto aberto? | tipo, nome e owner do handle |
| VMMap | Como o espaço virtual deste processo se distribui? | private data, image, mapped file, heap |
| RAMMap | Como a memória física está classificada? | active, standby, modified, file pages |
| ProcDump | Como obter um dump limitado de uma fixture? | dump associado a condição documentada |

Não comece pela ferramenta favorita. Comece por uma pergunta. “Por que `rte_consumer.exe` não encontra sua DLL?” aponta para Process Monitor e Process Explorer; “por que o processo cresce a cada lote?” aponta para VMMap, counters e repetição controlada.

## Process Explorer

A árvore revela relação de criação, não necessariamente controle atual. Confira caminho completo, linha de comando, usuário, nível de integridade, assinatura e início. Na guia de DLLs, observe somente sua fixture. Um módulo carregado não prova que uma função específica foi executada.

Handles representam referências a objetos. Contagem crescente pode sugerir vazamento, mas também cache intencional. Meça ao longo de um cenário repetível e confirme se a contagem estabiliza. Não feche handles de processos alheios; isso pode corromper estado.

## Process Monitor com pouco ruído

Uma captura útil é curta e preparada:

1. inicie a ferramenta e pare a captura imediatamente;
2. limpe eventos antigos;
3. adicione filtro `Process Name is rte_consumer.exe Include`;
4. se necessário, limite categoria ou caminho da fixture;
5. inicie a captura, reproduza uma vez e pare;
6. anote horários e salve o PML bruto em local restrito;
7. produza CSV minimizado somente com linhas relevantes.

`NAME NOT FOUND` aparece durante sondagens normais por configuração, DLLs e arquivos opcionais. `ACCESS DENIED` pode ser tentativa esperada seguida por alternativa válida. Interprete a sequência: operação, resultado, próxima tentativa e resultado final.

O stack de uma operação pode ajudar a identificar qual módulo iniciou a chamada quando símbolos adequados estão disponíveis. Ainda assim, um frame na stack é contexto, não sentença de culpa.

## Assinaturas, hashes e inicialização

Sigcheck fornece metadados e hashes. Compare com uma linha de base que você controla; não envie automaticamente arquivos privados a serviços externos. Autoruns reúne muitos pontos de extensão. Antes de desabilitar uma entrada, valide instalação associada, publisher, caminho, data e impacto. Neste curso, qualquer alteração é limitada à tarefa fixture criada no capítulo 11.

## Memória e dumps

VMMap mostra composição do espaço virtual de um processo; RAMMap descreve uso de memória física do sistema. Compare snapshots sob a mesma carga. “Private Bytes alto” e “Working Set alto” são conceitos diferentes e pedem hipóteses diferentes.

ProcDump será usado somente para a fixture desenvolvida no curso. Prefira mini dump, caminho protegido e retenção curta. Não capture navegador, autenticação, antivírus ou processo de terceiro. A ferramenta não remove a obrigação de minimizar dados.

## Exercícios

1. Verifique assinatura e versão de duas ferramentas e registre como a origem foi comprovada.
2. Renomeie a DLL da fixture, capture apenas uma execução no ProcMon e identifique a primeira falha relevante; restaure o nome.
3. Compare módulos vistos pelo Process Explorer com imports estáticos do capítulo de PE e explique por que as listas podem divergir.
4. Observe a memória da fixture antes e depois de um lote controlado e diferencie reserva, commit e working set.

## Checklist

- [ ] Cada coleta responde a uma pergunta escrita.
- [ ] Ferramentas foram obtidas de fonte oficial e validadas.
- [ ] Filtros evitam captura indiscriminada.
- [ ] Um resultado isolado não é tratado como causa.
- [ ] Evidência sensível possui acesso, retenção e limpeza definidos.

