# Auditoria editorial e tecnica do projeto

> Revisao interna do estado atual do RedTeam Essentials, realizada em 12 de
> agosto de 2026. Este documento transforma a analise do repositorio em um
> backlog pratico; nao substitui uma revisao juridica nem um teste de seguranca.

## Resumo executivo

### Estado de implementação

Esta auditoria agora também funciona como registro de progresso. O primeiro
incremento de implementação entregou:

- [x] configuração central de Ruff/pytest e testes Python totalmente offline;
- [x] correções descobertas pelos testes em lotes e faixas de portas;
- [x] matriz Python unificada em 3.10+;
- [x] módulo 00 com fundamentos, RoE, laboratório e autoavaliação;
- [x] contrato reutilizável para novos módulos;
- [x] `lab-doctor` para validar Compose, serviços e endpoints;
- [x] trilhas de aprendizagem por objetivo no README;
- [x] healthchecks, limites e profiles internos no Compose;
- [ ] imagens Docker imutáveis (bloqueadas até resolver/testar digests oficiais);
- [x] testes Pester/Bash/Java e validação estrutural do layer ATT&CK JSON;
- [x] aplicação do contrato editorial aos 25 módulos existentes (00–24);
- [x] fixtures/respostas explicadas para cinco labs (três Web, DFIR e Kubernetes);
- [x] conteúdos iniciais de identidade híbrida, APIs modernas e CI/CD supply chain;
- [x] trilhas iniciais macOS, mobile e wireless;
- [ ] aprofundamentos e adversary emulation adicionais por cenário.

Itens desmarcados continuam no backlog e não devem ser descritos como prontos.

O RedTeam Essentials e uma base educacional em portugues sobre o ciclo de uma
operacao de Red Team. O projeto combina teoria, cheatsheets, laboratorios web,
automacoes, ferramentas pequenas e materiais defensivos/DFIR. Seu diferencial
e ligar ofensiva, deteccao, etica, MITRE ATT&CK e reporting no mesmo lugar.

A base ja e ampla e navegavel, mas a profundidade varia bastante entre os
modulos. Recon, Active Directory, Web AppSec e privilege escalation possuem
mais material, enquanto C2/evasion, initial access e post-exploitation sao
intencionalmente introdutorios. A principal oportunidade nao e simplesmente
adicionar mais comandos: e tornar cada modulo uma unidade de aprendizagem
mensuravel, com pre-requisitos, pratica reproduzivel, evidencias esperadas,
deteccoes, mitigacoes e criterios de conclusao.

As prioridades recomendadas sao:

1. criar testes automatizados e fixtures offline para as ferramentas;
2. tornar o laboratorio reproduzivel, versionado e observavel;
3. padronizar todos os modulos com objetivos e criterios de conclusao;
4. atualizar referencias, versoes declaradas e mapeamento ATT&CK;
5. adicionar fundamentos ausentes antes de ampliar tecnicas ofensivas.

## Como a revisao foi feita

A revisao cobriu todos os arquivos versionados e considerou:

- estrutura e navegacao entre os 25 modulos (00–24);
- aproximadamente 20 mil linhas distribuidas em 72 documentos Markdown;
- scripts PowerShell, Bash e Python, a ferramenta Java e as bibliotecas comuns;
- workflows de CI, laboratorio Docker, templates de relatorio e governanca;
- consistencia entre README, ROADMAP, CHANGELOG e conteudo implementado;
- presenca de objetivos, pratica, defesa, etica, referencias e validacao.

Esta e uma avaliacao de repositorio. Os laboratorios externos e cada comando
ofensivo nao foram executados contra alvos reais.

## O que o projeto e hoje

O conteudo se organiza em cinco capacidades:

| Capacidade | Modulos e artefatos | Papel no projeto |
|------------|---------------------|------------------|
| Descoberta | 01 Recon, 02 OSINT | Identificar superficie e contexto do alvo. |
| Acesso e exploracao | 03 AD, 06 Cheatsheets, 07 Web, 08 Cloud, 10 Containers, 13 Initial Access | Ensinar caminhos de ataque em ambiente autorizado. |
| Operacao | 09 C2/Evasion, 14 Post-Exploitation | Explicar OPSEC, persistencia, coleta e exfiltracao controlada. |
| Defesa e entrega | 05 DFIR, templates de report, ATT&CK mapping | Mostrar rastros, resposta e comunicacao do risco. |
| Ferramental e ambiente | 04 Automation, 11 Python, 12 Java, `lib/`, `docker-lab/` | Reproduzir tarefas e sustentar os exercicios. |

O publico mais bem atendido e o estudante iniciante/intermediario que ja possui
fundamentos de redes e sistemas. O repositorio tambem funciona como referencia
rapida para profissionais, mas ainda nao como curso autocontido: faltam aulas
basicas, avaliacoes, respostas esperadas e telemetria de laboratorio.

## Pontos fortes

### Conteudo e pedagogia

- A jornada cobre recon, acesso inicial, exploracao, pos-exploracao, defesa e
  relatorio, em vez de apresentar tecnicas isoladas.
- Os avisos de autorizacao, RoE, minimizacao de dados e cleanup aparecem nos
  temas de maior risco.
- A perspectiva purple team esta presente em AD, Web, cloud, containers, C2 e
  DFIR, o que melhora o valor educacional e reduz o foco em simples receitas.
- Ha labs guiados para SQLi, XSS e API, alem de exercicios em varios documentos.
- O template de relatorio, o playbook de ransomware e o layer ATT&CK aproximam
  o estudo de entregaveis profissionais.

### Engenharia

- A biblioteca comum por linguagem reduz duplicacao de logging, validacao e
  exportacao.
- O CI cobre sintaxe/lint de PowerShell, Bash, Python, Java e Markdown.
- As ferramentas Python usam apenas a biblioteca padrao, facilitando o primeiro
  uso e a auditoria do codigo.
- O laboratorio publica os alvos apenas em `127.0.0.1`, uma escolha segura para
  o caso local padrao.

## Lacunas e melhorias do conteudo atual

### Prioridade P0: confiabilidade e seguranca do aprendizado

| Lacuna | Impacto | Melhoria proposta | Criterio de aceite |
|--------|---------|-------------------|--------------------|
| Suite inicial implementada; cobertura ainda não é medida no CI. | Fluxos não exercitados ainda podem quebrar apesar dos testes verdes. | Expandir pytest/Pester/testes shell e publicar cobertura das bibliotecas comuns. | Fixtures offline, testes de sucesso/erro e cobertura inicial de pelo menos 70% das bibliotecas comuns. |
| O Compose usa imagens `latest`. | Um lab pode mudar ou parar de funcionar sem alteracao no repositorio. | Fixar tags ou digests, registrar data de atualizacao e automatizar revisao mensal. | `docker compose config` e um smoke test HTTP reproduzem a mesma versao dos sete alvos. |
| O lab nao declara healthchecks nem limites de recursos. | O aluno nao sabe quando um alvo esta pronto e pode consumir recursos excessivos. | Adicionar healthchecks, perfis (`web-basic`, `api`, `full`) e limites documentados. | Um script `lab-doctor` informa dependencias, estado, URLs e falhas acionaveis. |
| Exemplos dependem de servicos publicos e respostas variaveis. | Exercicios podem falhar por rede, rate limit ou mudanca externa. | Criar fixtures DNS/HTTP/JWT e modos offline para exemplos e testes. | Quick start basico funciona sem atacar ou consultar terceiros. |
| Versoes declaradas divergem. | O README principal exige Python 3.10+, mas o modulo Python informa 3.9+. | Escolher uma matriz oficial e aplica-la em README, CI e modulos. | Uma unica tabela de compatibilidade e CI cobrindo exatamente as versoes suportadas. |

### Prioridade P1: consistencia editorial e progressao

1. **Criar um contrato de modulo.** Todo README de modulo deve conter publico,
   pre-requisitos, objetivos observaveis, tempo, ordem de leitura, ambiente,
   exercicios, resultado esperado, cleanup, deteccao, mitigacao e referencias.
2. **Trocar checklists pre-marcados por criterios reais.** Algumas tarefas do
   ROADMAP aparecem com `✅`, embora sejam atividades que o leitor ainda deve
   realizar. Usar `[ ]` para o aluno e uma coluna separada para conteudo ja
   implementado evita ambiguidade.
3. **Definir trilhas por persona.** Manter a trilha Red Team, mas adicionar
   caminhos curtos para AppSec, AD, cloud/container e purple/DFIR, indicando
   onde as leituras se cruzam.
4. **Adicionar glossario e fundamentos.** Termos como SPN, RoE, IAM, SSRF, C2,
   staging e evidencias aparecem antes de uma base comum. Um modulo 00 deve
   ensinar redes, DNS/HTTP, Linux/Windows, Git, terminal, identidade, etica e
   montagem segura do lab.
5. **Padronizar portugues e encoding.** Parte do acervo usa acentos e outra
   parte usa texto sem acentuacao. Adotar UTF-8 e um guia editorial melhora a
   leitura e a busca.
6. **Revisar fontes periodicamente.** Links, nomes de ferramentas, matrizes
   ATT&CK e recomendações envelhecem. Cada documento deve declarar
   `Revisado em`, fontes primarias e responsavel pela proxima revisao.
7. **Separar historico de estado atual.** `IMPLEMENTATION_SUMMARY.md` descreve
   a v1.1, enquanto a pagina inicial apresenta v2.1. Move-lo para `docs/history/`
   ou identifica-lo claramente no indice principal.

### Prioridade P1: qualidade tecnica

- Adicionar `pyproject.toml` para centralizar versao Python, Ruff, pytest e
  configuracao de cobertura.
- Adicionar build reproduzivel e testes JUnit para Java. O `javac` direto e bom
  para ensino, mas nao testa comportamento nem empacota releases.
- Validar schemas do JSON exportado pelas ferramentas e do layer ATT&CK.
- Adicionar analise de segredos, SBOM, pinning de GitHub Actions por SHA e
  verificacao das imagens do lab.
- Fazer o CI de Markdown ignorar exemplos deliberadamente ficticios de forma
  explicita, em vez de enfraquecer regras globais.
- Criar uma politica de manutencao para ferramentas descontinuadas e exemplos
  legados; marcar conteudo como atual, legado ou historico.

## Novos conteudos recomendados

### Fundamentos antes de novas tecnicas

1. **Modulo 00 - Fundamentos e seguranca do laboratorio**
   - redes, subnetting, DNS, HTTP/TLS e proxies;
   - Linux, Windows, PowerShell, Bash, Python e Git essenciais;
   - escopo, RoE, cadeia de custodia, LGPD e classificacao de dados;
   - snapshots, redes host-only, canarios e procedimento de cleanup.
2. **Threat modeling e planejamento de engagement**
   - objetivos, hipoteses, crown jewels, attack surface e plano de comunicacao;
   - modelos de RoE, matriz de riscos operacionais e criterios de parada;
   - traducao de ATT&CK para objetivos do negocio, sem tratar cobertura como
     uma simples contagem de tecnicas.
3. **Fundamentos de deteccao**
   - Windows Event Logs/Sysmon, auditd, CloudTrail, Entra sign-in logs e K8s
     audit logs;
   - exemplos Sigma e consultas basicas em KQL/Splunk;
   - para cada lab: acao, telemetria, hipotese de deteccao e falso positivo.

### Expansoes por dominio

| Tema novo | Escopo inicial recomendado | Entregavel pratico |
|-----------|----------------------------|--------------------|
| Identidade hibrida | Entra ID, federacao, conditional access, workload identities e relacao AD-cloud. | Lab de tenant sandbox com grafo de ataque e deteccoes. |
| Seguranca de APIs moderna | OWASP API, GraphQL, gRPC, OAuth 2.0/OIDC, BOLA e mass assignment. | Dois labs locais com testes e remediacao. |
| Supply chain e CI/CD | GitHub Actions, secrets, OIDC, artefatos, dependencias e runners. | Pipeline vulneravel local + pipeline corrigido. |
| macOS e endpoints modernos | TCC, LaunchAgents, keychain, unified logs e MDM, com foco defensivo. | Checklist de auditoria e coleta de artefatos. |
| Mobile | Android/iOS basico, armazenamento, trafego e MASVS. | App deliberadamente vulneravel e roteiro de analise. |
| Wireless | WPA2/3, evil twin apenas conceitual, deteccao e desenho seguro de lab RF. | Analise de captura fornecida, sem transmissao ofensiva. |
| Engenharia de deteccao | Sigma, YARA, KQL, SPL e validacao com eventos sinteticos. | Regra, fixture, teste e explicacao de tuning por tecnica. |
| Adversary emulation | Planos baseados em inteligencia, controles de seguranca e purple-team debrief. | Microemulacao segura com canarios e success criteria. |

### Expansoes nos modulos existentes

- **01/02:** normalizacao e correlacao de resultados, passive DNS, ASN, limites de
  privacidade e um relatorio OSINT com dados sinteticos.
- **03:** hardening de ADCS, LAPS/Windows LAPS, gMSA, tiering, Protected Users e
  deteccoes verificaveis para os caminhos ja descritos.
- **05:** Linux e cloud forensics, Velociraptor, timeline com Plaso, aquisicao e
  cadeia de custodia; incluir datasets pequenos e respostas dos exercicios.
- **06:** transformar cheatsheets em arvores de decisao, sempre ligando comando,
  pre-condicao, evidencia, risco operacional, deteccao e remediacao.
- **07:** adicionar CSRF, deserializacao, template injection, request smuggling,
  WebSockets e OAuth/OIDC; atualizar o Top 10 por meio de uma politica versionada.
- **08:** identidade e logging devem ganhar a mesma profundidade nos tres clouds;
  incluir custos, teardown automatico e protecoes contra gasto inesperado.
- **09:** adicionar arquitetura segura de infraestrutura, redirectors em nivel
  conceitual, logging do operador e exercicios de deteccao com trafego sintetico.
- **10:** image supply chain, admission control, runtime security, secrets e
  ambientes serverless; fornecer manifests vulneravel/corrigido lado a lado.
- **11/12:** adicionar testes, formatos de saida comuns, exemplos offline e uma
  tabela explicando quando usar cada ferramenta em vez de utilitarios maduros.
- **13/14:** ampliar simulacao com canarios, aprovacao do cliente, kill list,
  rollback, metricas de campanha e debrief purple team.

## Roadmap de implementacao sugerido

### 0-30 dias: estabilizar

- [x] corrigir a matriz de versoes Python e o README;
- [x] criar testes para `rte_common.py` e para os parsers sem rede;
- [x] adicionar healthchecks, limites de recursos e profiles ao Compose;
- [ ] fixar imagens por digest após resolução e smoke test em ambiente com Docker/registry;
- [x] publicar o contrato de modulo;
- [x] aplicar o contrato aos modulos 01, 07 e 11;
- [x] validar estrutura e invariantes do layer ATT&CK no CI;
- [ ] revisar a atualidade de cada técnica do layer contra fontes primárias.

### 31-90 dias: tornar ensinavel

- [x] criar o modulo 00 com fundamentos de identidade e terminologia essencial;
- [x] adicionar fixtures, datasets e respostas explicadas para cinco labs;
- [x] criar `lab-doctor` e smoke tests locais;
- [x] criar profiles Compose `api`, `extended` e `full`, mantendo um default básico;
- [x] documentar unidades verificáveis de detecção em AD, Web, cloud e containers;
- [x] adicionar fixtures executáveis para AWS, Azure e GCP;
- reorganizar a navegacao por personas e dificuldade.

### 91-180 dias: ampliar com profundidade

- [x] entregar trilhas iniciais de identidade hibrida e APIs modernas;
- [x] criar conteúdo de auditoria CI/CD e supply chain;
- adicionar telemetria centralizada opcional ao lab;
- [x] publicar microemulacao purple team offline, do RoE ao debrief;
- medir conclusao, reproducibilidade e manutencao, nao apenas quantidade de
  arquivos ou tecnicas ATT&CK.

## Indicadores de qualidade

| Indicador | Meta inicial |
|-----------|--------------|
| Modulos com contrato editorial mínimo | 100% dos 25 módulos; validado por `project_metrics.py` |
| Labs com setup, resultado esperado e cleanup testados | 100% |
| Ferramentas com testes offline | 100% |
| Bibliotecas comuns cobertas por testes | >= 70% |
| Imagens e Actions com versao imutavel | 100% |
| Documentos tecnicos revisados nos ultimos 12 meses | >= 90% |
| Tecnicas praticas ligadas a uma fonte de telemetria | >= 80% |
| Links locais validos no CI | 100% |

## Ordem recomendada para contribuicoes

Uma contribuicao deve preferir, nesta ordem:

1. corrigir material inseguro, quebrado ou irreproduzivel;
2. adicionar teste e evidencia ao que ja existe;
3. preencher fundamentos e defesa de um tema existente;
4. criar um lab pequeno, isolado e com cleanup;
5. somente entao adicionar uma nova tecnica ou ferramenta.

Essa ordem preserva o principal valor do projeto: ensinar seguranca ofensiva de
forma etica, verificavel e util tambem para quem precisa detectar e corrigir.
