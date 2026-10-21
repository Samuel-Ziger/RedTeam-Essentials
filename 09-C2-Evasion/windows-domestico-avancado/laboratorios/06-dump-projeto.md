# Lab 06 — Dump, WinDbg e projeto integrador

**Classe:** C — mini dump exclusivamente da fixture própria, com retenção curta e acesso limitado.

## Propósito

Demonstrar o ciclo completo de engenharia diagnóstica: contrato, build, linha de base, falha benigna, coleta mínima, análise causal, correção, regressão e limpeza. Este gate usa o projeto `Diagnostic Workbench`; não analisa processos sensíveis ou de terceiros.

## Pré-condições

- Labs 01–05, capítulo 19, guia transversal e caderno de práticas concluídos;
- projeto de referência lido e implementação própria revisada;
- executável, DLL e PDBs do mesmo build preservados com hashes;
- dados artificiais, conta comum, VM em snapshot e rede desnecessária desligada;
- diretório de dump com ACL limitada e prazo de exclusão definido.

Se os símbolos não correspondem ao binário, pare e refaça o build. Se a ferramenta apontar outro processo, cancele. Dump completo, dump de kernel e dump de navegador, autenticação ou antivírus estão fora do curso.

## Linha de base saudável

Execute o projeto com um conjunto fixture conhecido. Valide schema do JSON, correlation ID, resultado da DLL e códigos de saída. Rode testes Pester, análise estática e benchmark. Registre versão da toolchain, commit, comandos, hashes, mediana e p95.

Confirme no Process Explorer que o módulo carregado é a DLL ao lado do consumidor. Use ProcMon apenas se necessário, com filtro pelo executável. A linha de base deve funcionar com Defender e mitigações normais.

## Falha controlada

Escolha uma única falha permitida: DLL ausente, versão de ABI rejeitada, entrada inválida ou exceção explicitamente compilada para laboratório. As três primeiras podem ser resolvidas sem dump. Para cumprir a parte WinDbg, use apenas a exceção controlada e documente o flag que a habilita.

Reproduza uma vez. Capture mini dump da fixture com WER, ProcDump ou mecanismo documentado. Registre comando, versão da ferramenta, horário, tamanho e SHA-256. Pare qualquer coleta depois da falha.

## Triagem no WinDbg

Abra o dump localmente. Revise `.sympath`, execute `.reload /f` e confirme pelo log que executável e DLL próprios resolveram os PDBs corretos. Liste módulos com `lm`, registre exception code e selecione o contexto da exceção quando aplicável. Use stack para localizar a primeira frame de código próprio.

Execute `!analyze -v`, mas trate sua saída como ponto de partida. Compare a hipótese com fonte, argumentos sintéticos, log estruturado e trace. Marque no relatório fatos, inferências e dados ausentes. Não inclua dump bruto ou valores de memória na entrega pública.

## Correção e regressão

Faça a menor correção coerente com a causa. Acrescente um teste que falhava antes e passa depois. Recompile, gere novos hashes, execute o cenário saudável e repita o orçamento de desempenho. Uma correção que apenas suprime a exceção sem validar o resultado não passa.

Peça a outra pessoa para seguir o runbook a partir de checkout limpo, sem explicação oral. Registre ambiguidades e revise instruções. O revisor deve conseguir reproduzir build e teste sem receber o dump.

## Entrega

O pacote contém fonte, manifesto de build, hashes, contrato, testes, relatório causal, comparação de desempenho, baseline defensiva redigida e cleanup. Separe artefatos reconstruíveis de evidência sensível. A rubrica detalhada está no capítulo 19 e no projeto de referência.

## Critérios de aceite

- binário e símbolos são do mesmo build, comprovados por registro e hash;
- mini dump pertence apenas à fixture e foi analisado localmente;
- a causa combina stack, fonte e evidência externa, não apenas `!analyze`;
- teste de regressão falha antes e passa depois da correção;
- terceiro reproduz o fluxo e a limpeza remove artefatos sensíveis.

## Cleanup e defesa

Apague dump, ETL, PML, binários gerados e arquivos temporários conforme a retenção. Confirme encerramento dos processos e ausência de sessão ETW. Restaure snapshot ou compare com a baseline. Preserve somente relatório sanitizado e hashes não sensíveis.

Na defesa final, responda: qual foi a causa e que evidência poderia refutá-la? O que o mini dump não continha? Como a correção preservou ABI e mitigações? Que informação permitiria reproduzir o resultado daqui a seis meses? Se uma afirmação não aponta para evidência, trate-a como hipótese.

