# Guia transversal de tracing e debugging

Este guia conecta Event Log, ETW, ProcMon, counters, dumps e depuração. Ele existe para responder a uma pergunta difícil: diante de um sintoma, qual evidência coletar primeiro? Ferramentas produzem muitos dados; diagnóstico produz uma explicação testável com o menor volume necessário.

## 1. Defina o sintoma antes da ferramenta

Transforme “travou” em uma observação: a interface deixou de responder por oito segundos depois de abrir uma fixture de 500 arquivos; o processo permaneceu ativo; a operação terminou; ocorreu em quatro de cinco tentativas. Registre esperado, observado, início, duração, frequência, impacto e versão.

Uma pergunta operacional determina a fonte. Falha ao abrir dependência aponta para sequência de File I/O; uso crescente sob repetição aponta para counters e VMMap; exceção determinística aponta para logs e mini dump. “Vamos capturar tudo” não é uma pergunta.

Separe no diário:

- **fato:** campo observado e sua fonte;
- **inferência:** interpretação apoiada no modelo;
- **relato:** descrição recebida, ainda não reproduzida;
- **lacuna:** dado necessário que não está disponível.

Essa separação evita que a narrativa fique mais confiante do que a evidência.

## 2. Preserve identidade e tempo

Registre versão do Windows, arquitetura, timezone, relógio, versão e hash do binário, PDB correspondente, argumentos sintéticos e commit. PID é reutilizável; associe-o ao horário de início e caminho. Para comparação entre fontes, normalize o relatório em UTC e preserve o valor original quando a ferramenta usa horário local.

Não altere binário depois da captura. Se recompilar, gere um novo conjunto de hashes e PDBs. Símbolos incompatíveis podem gerar nomes plausíveis em endereços errados.

## 3. Construa hipóteses que possam falhar

Para cada hipótese, escreva evidência esperada e evidência contra. Exemplo:

| Hipótese | A favor | Contra | Próximo teste |
|---|---|---|---|
| DLL ausente | tentativa no diretório permitido termina `NAME NOT FOUND` | módulo aparece carregado | ProcMon curto + lista de módulos |
| ABI incompatível | DLL carrega, versão retornada difere | versões iguais | log do contrato antes da chamada |
| I/O domina latência | duração concentrada em File I/O | CPU domina com pouco I/O | WPR CPU/File I/O |
| exceção em entrada | mesmo dado falha no mesmo frame | entradas variadas falham antes | mini dump da fixture + teste mínimo |

Escolha primeiro o teste que divide hipóteses com menor risco e custo. Não apague previsões erradas; elas mostram como o conhecimento evoluiu.

## 4. Escada de evidência

Comece pelo menos intrusivo:

1. mensagem, código de saída e log da aplicação;
2. versão, assinatura, hash e configuração efetiva;
3. Event Log filtrado pelo intervalo e provider;
4. counters amostrados durante cenário reproduzível;
5. ProcMon filtrado por processo e categoria;
6. ETW/WPR com providers mínimos e janela curta;
7. mini dump somente da fixture própria;
8. depuração ao vivo apenas quando o estado não puder ser preservado de outra forma.

A ordem não é absoluta. Exceção que encerra imediatamente pode justificar mini dump cedo. O princípio é coletar o mínimo que discrimina as hipóteses.

## 5. Process Monitor

Pare, limpe, filtre, capture, reproduza uma vez e pare. Inclua nome de processo e, quando possível, caminho ou categoria. Salve PML bruto em local restrito; derive um CSV sanitizado.

Leia sequências, não cores. `NAME NOT FOUND` pode ser busca opcional; `ACCESS DENIED` pode ser seguido por fallback esperado; `BUFFER OVERFLOW` pode indicar negociação normal de tamanho. Para ser causal, o evento deve corresponder ao recurso exigido, alinhar-se ao fluxo do código e explicar o resultado. A recuperação após restaurar uma única variável fortalece a conclusão.

## 6. Event Log e ETW

No Event Log, preserve canal, provider, ID, versão, record ID, nível e UTC. O mesmo ID em providers diferentes não tem significado comum. Filtre na origem com `FilterHashtable` e limite o intervalo. Canal vazio pode estar desabilitado, ter retenção curta ou não cobrir o componente.

No ETW, documente provider, keywords, level, session, buffers, horário e indicadores de perda. Um ETL é uma sequência estruturada, não uma explicação. Use WPA para delimitar o intervalo do sintoma, filtrar processo/thread e verificar unidades. Se símbolos não resolverem, declare essa limitação.

Capturar stacks, disco e vários providers aumenta custo. Faça uma execução de linha de base sem tracing e compare duração com a execução capturada para estimar efeito do observador.

## 7. Counters e desempenho

Counters são amostras. `CPU` em `Get-Process` é tempo acumulado; `% Processor Time` é taxa no intervalo; Working Set é residência; Private Bytes é compromisso privado. Nomear corretamente o indicador evita diagnósticos falsos.

Defina carga fixa, duas rodadas de aquecimento e pelo menos vinte amostras no laboratório. Preserve valores brutos; informe mediana, p95 e máximo. Não exclua outlier sem causa externa documentada e regra definida antes. Compare antes/depois alterando uma variável.

Uma associação temporal não prova mecanismo. Se CPU sobe quando a latência sobe, use stacks ou código para explicar o trabalho. Se File I/O domina, identifique caminho e padrão sem incluir arquivos reais no relatório.

## 8. Dumps e WinDbg

Dump é dado sensível. Capture apenas a fixture, com dados artificiais, conta comum, diretório restrito e retenção curta. Prefira mini dump. Preserve binário e PDB exatos, ferramenta de captura, comando, horário, tamanho e hash.

No WinDbg:

1. confira arquitetura e tipo do dump;
2. revise `.sympath` e carregue com `.reload /f`;
3. liste módulos com `lm` e valide versões;
4. obtenha resumo com `!analyze -v`;
5. selecione o contexto de exceção quando aplicável;
6. leia stack e encontre o primeiro frame próprio confiável;
7. correlacione parâmetros disponíveis, fonte, logs e trace.

Não trate `!analyze` como veredito. Uma função do sistema pode receber entrada inválida da aplicação; o primeiro frame próprio pode ser apenas tratamento. Um mini dump pode omitir memória necessária; registre “desconhecido” em vez de preencher a lacuna.

## 9. Causalidade e correção

Uma conclusão forte conecta mecanismo e intervenção: a aplicação calculou diretório incorreto, ProcMon mostrou busca somente nesse caminho, o código confirmou a composição, corrigir essa função fez o mesmo build de teste localizar a DLL, e um teste de regressão agora cobre o caminho.

Uma conclusão fraca diz “depois de reinstalar, funcionou”. Muitas variáveis mudaram. Prefira a menor correção compatível com a hipótese. Acrescente teste que falhava antes, repita cenário e verifique efeitos colaterais de desempenho e segurança.

Se a causa não foi demonstrada, entregue o que foi descartado e o próximo teste. Incerteza explícita é mais útil do que precisão inventada.

## 10. Privacidade, segurança e parada

ETL, PML, EVTX e dump podem conter nomes, caminhos, linhas de comando e conteúdo. Não os publique. Redija relatório com IDs sintéticos, agregados e trechos mínimos. Não colete navegador, autenticação, antivírus, processo protegido ou software de terceiro.

Pare quando:

- o PID/caminho não corresponde à fixture;
- a captura inclui dados reais ou outra conta;
- o tamanho excede o orçamento;
- símbolos não correspondem ao build;
- uma instrução pede desabilitar proteção;
- a alteração sai da pasta/chave prevista;
- ocorre incidente real ou comportamento inesperado.

Parar preserva o laboratório e a validade do experimento.

## 11. Modelo de relatório

Use uma estrutura estável:

1. escopo, autorização e classe de risco;
2. ambiente, versões, hashes e tempo;
3. sintoma operacional e impacto;
4. hipóteses iniciais e previsões;
5. fontes, filtros, comandos e limitações;
6. linha do tempo dos fatos;
7. análise causal e alternativas descartadas;
8. correção, teste de regressão e comparação;
9. dados minimizados, retenção e cleanup;
10. incertezas e próximo passo.

Outra pessoa deve conseguir reproduzir a investigação sem uma explicação oral. Se um comando depende de estado implícito, documente-o.

## 12. Checklist rápido

- [ ] sintoma e orçamento estão definidos antes da coleta;
- [ ] binário, PDB, versão e relógio estão identificados;
- [ ] hipóteses possuem evidência a favor e contra;
- [ ] a fonte escolhida é a menos intrusiva que responde à pergunta;
- [ ] filtros, janela e indicadores de perda foram registrados;
- [ ] fatos, inferências, relatos e lacunas estão separados;
- [ ] correção muda uma variável e possui teste de regressão;
- [ ] proteção não foi reduzida para facilitar diagnóstico;
- [ ] artefatos brutos têm acesso, retenção e cleanup;
- [ ] relatório sanitizado permite reprodução independente.

