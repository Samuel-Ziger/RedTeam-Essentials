# Desenvolvimento de aplicações profissionais

Esta é a quarta etapa da formação em programação. Os módulos 00–02 construíram
fundamentos, dados/APIs, algoritmos e engenharia de software. Aqui o foco passa
para aquilo que a pessoa instala, executa e percebe: **contrato de produto,
interfaces, estado, acessibilidade, diagnóstico, distribuição e suporte**.

O curso não antecipa Sistemas Operacionais ou Redes. Processos, memória virtual,
kernel, drivers, administração, roteamento e protocolos terão módulos próprios.
Quando aparecem, são limites externos acessados por APIs de alto nível.

O material é autocontido. As [referências](REFERENCIAS.md) oferecem documentação
oficial, vídeos, fóruns e aprofundamentos, mas os capítulos, exemplos, práticas e
laboratórios bastam para executar o percurso.

## Contrato de aprendizagem

| Campo | Definição |
|---|---|
| Público | Quem concluiu os módulos 00, 01 e 02 |
| Carga estimada | 240–360 horas, incluindo 32 práticas, cinco labs e capstone |
| Linguagens | Python, Java, C17, C# e JavaScript |
| Interfaces | CLI, GUI desktop, web local-first e fronteiras de clientes de API |
| Ambiente | Toolchains locais, Git, navegador moderno e editor de texto |
| Evidência final | Aplicação instalável, acessível, testada, diagnosticável e documentada |
| Conclusão | Cinco labs, pelo menos 75% na rubrica e nenhum requisito essencial ausente |

## Competências finais

Ao concluir, você será capaz de:

- transformar necessidade vaga em contrato, estados e critérios de aceite;
- desenhar CLIs previsíveis, automatizáveis e compatíveis;
- combinar padrão, arquivo, ambiente e argumento sem esconder a origem;
- validar entrada, classificar falhas e preservar o que pode ser corrigido;
- evoluir documentos locais com schema, migração e commit seguro;
- modelar estado/eventos e conter concorrência sem espalhar mutação pela UI;
- avaliar toolkits de GUI e separar presenter de widgets;
- construir interfaces web semânticas, responsivas, acessíveis e testáveis;
- representar primeira carga, refresh, offline, retry, conflito e cancelamento;
- tratar texto, plural, datas, zonas, números e dinheiro por locale;
- gerar diagnóstico útil sem transformar segredo ou dado pessoal em log;
- projetar extensões com compatibilidade, capacidade e contenção de falha;
- empacotar, inventariar, atualizar, remover e recuperar uma aplicação;
- definir orçamento, medir com profiler e evitar otimização por intuição;
- preparar release, rollout, rollback e suporte com critérios objetivos.

O objetivo não é decorar opções de framework. É reconhecer as garantias que
precisam sobreviver quando framework, toolkit, armazenamento ou linguagem mudam.

## Pré-requisitos verificáveis

Antes de iniciar, confirme que consegue:

- decompor um problema e testar funções em pelo menos duas linguagens;
- usar tipos, módulos, coleções, arquivos, erros e dependências;
- modelar dados e consumir uma API usando contratos dos módulos anteriores;
- trabalhar em branch, interpretar diff e executar uma suíte local;
- explicar separação entre domínio, caso de uso e adapter;
- usar somente fixtures sintéticas e manter segredo fora do repositório.

Se esses itens ainda dependem de tentativa aleatória, retome o ponto equivalente
dos módulos 00–02. Este curso ensina os novos conceitos desde a base, mas assume
a fluência construída nas etapas anteriores.

## Rota em cinco etapas

| Etapa | Conteúdo | Gate prático |
|---|---|---|
| 1. Entrada do produto | 00–03 + exemplos | Lab 01: contrato, CLI, configuração e erros |
| 2. Dados e estado | 04–06 + Study Desk | Lab 02: schema, commit, reducer e fronteira GUI |
| 3. Experiência | 07–10 + Study Desk | Lab 03: web, acessibilidade, offline e i18n |
| 4. Entrega | 11–15 + diagnóstico | Lab 04: logs, extensão, pacote, perfil e release |
| 5. Síntese | caderno + 16 | Lab 05: aplicação profissional completa |

Na primeira passagem, siga esta ordem:

1. [Do código ao produto](00-do-codigo-ao-produto.md)
2. [CLI profissional](01-cli-profissional.md)
3. [Configuração, ambientes e segredos](02-configuracao-ambientes-segredos.md)
4. [Exemplos comparados nas cinco linguagens](exemplos/README.md)
5. [Validação, erros e feedback](03-validacao-erros-feedback.md)
6. [Lab 01 — contrato, CLI e configuração](laboratorios/lab-01-contrato-cli-configuracao.md)
7. [Arquivos, serialização e dados locais](04-arquivos-serializacao-dados-locais.md)
8. [Estado, eventos e fluxo de dados](05-estado-eventos.md)
9. [GUI desktop](06-gui-desktop.md)
10. [Projeto de referência Study Desk](projetos/study-desk/README.md)
11. [Lab 02 — dados, estado e GUI](laboratorios/lab-02-dados-estado-gui.md)
12. [Interfaces web](07-interfaces-web.md)
13. [Acessibilidade e responsividade](08-acessibilidade-responsividade.md)
14. [Clientes de API e experiência offline](09-clientes-api-offline.md)
15. [Internacionalização, tempo e dinheiro](10-internacionalizacao-tempo-dinheiro.md)
16. [Lab 03 — web acessível, offline e i18n](laboratorios/lab-03-web-acessivel-offline-i18n.md)
17. [Logs, diagnóstico e observabilidade](11-logs-diagnostico.md)
18. [Plugins e extensibilidade](12-plugins-extensibilidade.md)
19. [Empacotamento, distribuição e atualização](13-empacotamento-distribuicao.md)
20. [Desempenho percebido e profiling](14-desempenho-profiling.md)
21. [Qualidade, release e suporte](15-qualidade-release-suporte.md)
22. [Guia de diagnóstico](GUIA-DIAGNOSTICO.md)
23. [Lab 04 — diagnóstico, distribuição e desempenho](laboratorios/lab-04-diagnostico-distribuicao-desempenho.md)
24. [Caderno com 32 práticas](CADERNO-PRATICAS.md)
25. [Projetos e avaliação](16-projetos-avaliacao.md)
26. [Lab 05 — capstone de aplicação profissional](laboratorios/lab-05-capstone-aplicacao-profissional.md)

Use também o [índice dos laboratórios](laboratorios/README.md), as
[respostas orientativas](RESPOSTAS.md), o [glossário](GLOSSARIO.md) e as
[referências](REFERENCIAS.md). Respostas descrevem propriedades e evidências,
não código para copiar.

## Código executável nas cinco linguagens

Em [exemplos](exemplos/), as cinco linguagens implementam o mesmo contrato:

```text
--profile > APP_PROFILE > development
```

As implementações tornam visíveis ajuda, validação, origem da configuração,
saída humana/JSON, `stdout`/`stderr` e código `0/2`. O runner compila com avisos
como erro, executa testes e também verifica o caminho negativo como subprocesso.

```bash
bash 03-AD-Notes/desenvolvimento-aplicacoes/testar-curso.sh
```

Toolchain ausente é informada como `SKIP`; ferramenta instalada que falha torna
a validação inválida. A CI instala as versões previstas.

## Projeto de referência: Study Desk

O [Study Desk](projetos/study-desk/README.md) é uma aplicação web local-first sem
framework e sem dependências de runtime. Ele inclui:

- HTML semântico, CSS responsivo e JavaScript modular;
- domínio/reducer separado de DOM e Storage;
- documento versionado, limites, datas canônicas e IDs únicos;
- importação integral antes do commit e rollback de falha de persistência;
- renderização textual, CSP local e tratamento de preferências;
- arquitetura, dois ADRs, runbook e fixture;
- 35 testes automatizados mais roteiro manual de acessibilidade.

```bash
cd 03-AD-Notes/desenvolvimento-aplicacoes/projetos/study-desk
npm test
python3 -m http.server 8000
```

O projeto é uma referência para leitura e evolução. O capstone precisa resolver
outro problema ou apresentar uma evolução arquitetural substancial defendida por
novos requisitos e testes.

## Ciclo de aprendizagem e evidência

Para cada conceito, percorra quatro níveis:

1. **explicar:** declare contrato, invariante e vocabulário;
2. **prever:** antecipe estado, saída e falha para um cenário novo;
3. **construir:** implemente e teste uma fatia vertical;
4. **operar:** empacote, provoque falha, diagnostique e recupere.

Guarde comando, fixture, resultado esperado, resultado observado e conclusão.
Uma captura de tela sem ambiente ou critério não permite reprodução.

## Método para cada capítulo

1. Leia os objetivos e marque o que já consegue demonstrar.
2. Reescreva contratos e invariantes com suas palavras.
3. Execute o exemplo antes de modificá-lo.
4. Faça exercícios sem consultar a resposta.
5. Provoque pelo menos uma falha de fronteira e preserve o estado anterior.
6. Registre a decisão, o trade-off e a evidência.
7. Explique como o conceito aparece no Study Desk.
8. Só avance quando o checklist de domínio for verificável.

## Gates de progressão

Não avance apenas porque terminou a leitura:

- **após 03:** ajuda, precedência, canais e erros são contratos testados;
- **após 06:** dado local, commit e estado funcionam sem UI concreta;
- **após 10:** teclado, reflow, concorrência, offline e locale têm evidência;
- **após 15:** diagnóstico, artefato, orçamento e rollback são reproduzíveis;
- **após 16:** uma pessoa nova instala, usa, falha e recupera pelo README.

O aplicativo de estudos marca leitura; conclusão de laboratório exige a entrega
descrita nele. Os pré-requisitos semânticos impedem desbloquear o capstone apenas
por abrir documentos fora de ordem.

## Limites e política de uso

Frameworks mudam rapidamente. React, Angular, JavaFX, .NET MAUI, Qt, Electron ou
outra tecnologia podem ser estudados depois usando os critérios duráveis deste
módulo: contrato, acessibilidade, manutenção, observabilidade e distribuição.

Use dados sintéticos. Não inclua credenciais, dados pessoais ou artefatos de
terceiros sem licença em código, logs, fixtures ou pacotes. Ao combinar este
conhecimento com trilhas de segurança, trabalhe somente em sistemas próprios ou
formalmente autorizados e siga [ETHICAL-USE.md](../../ETHICAL-USE.md).
