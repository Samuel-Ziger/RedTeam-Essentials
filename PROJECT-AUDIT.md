# Auditoria editorial e tecnica do projeto

> Revisao interna do estado atual do RedTeam Essentials, atualizada em 3 de
> outubro de 2026. Este documento transforma a analise do repositorio em um
> backlog pratico; nao substitui uma revisao juridica nem um teste de seguranca.

## Resumo executivo

### Estado de implementação

Esta auditoria também funciona como registro de progresso. A rodada de
estabilização entregou:

- [x] configuração central de Ruff/pytest e testes Python totalmente offline;
- [x] correções descobertas pelos testes em lotes e faixas de portas;
- [x] matriz Python unificada em 3.10+;
- [x] módulo 00 aprofundado com raciocínio, contratos, invariantes, depuração,
  ambiente local seguro, prática progressiva e autoavaliação;
- [x] curso autocontido de programação no módulo 00, com cinco linguagens,
  exemplos e testes executáveis, cinco laboratórios, CI e projeto full stack;
- [x] continuação avançada no módulo 01, com SQL/PostgreSQL, NoSQL/MongoDB,
  engenharia de APIs, clientes nas cinco linguagens, laboratórios, CI e projeto
  de persistência poliglota;
- [x] fechamento da formação de programação no módulo 02, com algoritmos,
  estruturas de dados, design, arquitetura, refatoração, testes, cinco
  linguagens e projeto integrado validado em CI;
- [x] trilha de desenvolvimento de aplicações no módulo 03, com CLI, GUI, web,
  acessibilidade, configuração, distribuição, cinco linguagens e projeto
  local-first, mantendo Active Directory como conteúdo complementar;
- [x] trilha de automação profissional no módulo 04, com idempotência, dry-run,
  pipelines, jobs, testes, CI e projeto FileFlow nas cinco linguagens;
- [x] especialização de APIs no módulo 05, com contrato, segurança, estilos,
  operação, clientes multilíngue, projeto executável e CI dedicada;
- [x] formação Linux do zero ao kernel no módulo 06, com laboratórios
  reversíveis, exemplos em Bash/C, administração, memória, boot, hardening,
  drivers e validação dedicada;
- [x] especialização Linux avançada no módulo 07, com fonte/ABI do kernel,
  scheduler, concorrência, MM/NUMA, VFS/bloco, boot confiável, tracing/eBPF
  local, KVM, integridade, distribuição, 35 capítulos, laboratórios e CI;
- [x] formação Windows doméstica nos módulos 08–09, da instalação e
  administração local a NT internals, PE/DLL, PowerShell, tracing e debugging;
- [x] formação Windows empresarial nos módulos 10–11, com Windows Server,
  Server Core, imagens/deployment, AD/GPO, PKI, Defender, App Control,
  compliance, recuperação e validação offline dedicada;
- [x] especialização Purple Team no módulo 26, com firewalls, WAF, bots,
  identidade, testes Red/Blue pareados, ferramentas offline e CI;
- [x] contrato reutilizável para novos módulos;
- [x] `lab-doctor` para validar Compose, serviços e endpoints;
- [x] trilhas de aprendizagem por objetivo no README;
- [x] healthchecks, limites e profiles internos no Compose;
- [x] imagens Docker imutáveis, com inventário de digests e processo de atualização;
- [x] gateway HTTP local testado, sem publicação direta ou egress nos alvos;
- [x] testes Pester/Bash/Java e validação estrutural do layer ATT&CK JSON;
- [x] aplicação e validação do contrato editorial aos 41 módulos (00–40);
- [x] fixtures/respostas explicadas para cinco labs (três Web, DFIR e Kubernetes);
- [x] acervos iniciais de identidade híbrida, APIs modernas e CI/CD supply chain;
- [x] formação macOS autocontida nos módulos 12–13 e acervo wireless preservado;
- [x] formação de redes autocontida nos módulos 14–18, dos fundamentos à
  infraestrutura empresarial e engenharia de protocolos;
- [x] formação de criptografia autocontida nos módulos 19–22, da matemática à
  PKI/TLS, engenharia de chaves e transição pós-quântica;
- [x] formação de privacidade autocontida nos módulos 23–25, dos modelos de
  ameaça à VPN própria e atribuição defensiva com evidências sintéticas;
- [x] formação final de borda autocontida no módulo 26, unindo avaliação
  ofensiva autorizada, prevenção, detecção, resposta, tuning e reteste;
- [x] especialização em segurança nos módulos 27–40, com governança,
  ferramentas, recon/OSINT, AppSec, identidade, cloud, containers, plataformas,
  operações, DFIR, threat intelligence e capstone Purple Team;
- [x] aplicacao visual local em React para navegar pelas trilhas, ler Markdown,
  continuar do ultimo ponto e acompanhar leituras e laboratorios desbloqueados;
- [x] Biblioteca Completa com base e especialização nomeadas, laboratorios/projetos,
  codigo/ferramentas, documentacao global e cobertura elegivel sem lacunas;
- [x] catalogo visual reproduzivel gerado dos arquivos fonte, com testes de
  seguranca de caminhos, launcher restrito ao loopback e CI dedicada;
- [ ] aprofundamentos e adversary emulation adicionais por cenário.

Itens desmarcados continuam no backlog e não devem ser descritos como prontos.

O estado canônico possui 41 módulos em sete áreas. Os módulos 00–26 formam
a base obrigatória; os 14 módulos 27–40 compõem a especialização avançada e
dependem dessa base. O manifesto usa `contentPaths` para adotar curricularmente
os artefatos já existentes sem copiá-los ou mudar seus caminhos, preservando
links e histórico do repositório.

O RedTeam Essentials e uma base educacional em portugues sobre o ciclo de uma
operacao de Red Team. O projeto combina teoria, cheatsheets, laboratorios web,
automacoes, ferramentas pequenas e materiais defensivos/DFIR. Seu diferencial
e ligar ofensiva, deteccao, etica, MITRE ATT&CK e reporting no mesmo lugar.

A base ja e ampla e navegavel, mas a profundidade varia bastante entre os
modulos. Programação, Linux, Windows, Recon, Active Directory e Web AppSec
possuem mais material, enquanto C2/evasion, initial access e post-exploitation
sao intencionalmente introdutorios. A principal oportunidade nao e simplesmente
adicionar mais comandos: e tornar cada modulo uma unidade de aprendizagem
mensuravel, com pre-requisitos, pratica reproduzivel, evidencias esperadas,
deteccoes, mitigacoes e criterios de conclusao.

As prioridades originais foram convertidas nas seguintes entregas:

1. testes automatizados, cobertura e fixtures offline para as ferramentas;
2. laboratório observável, com perfis, recursos limitados e rede interna;
3. catálogo canônico e contrato validado em todos os módulos;
4. validadores para ATT&CK, Compose, vídeos, metadados, SBOM e segredos;
5. fundamentos, governança e uma CLI única para as operações do projeto.

## Como a revisao foi feita

A revisao cobriu todos os arquivos versionados e considerou:

- estrutura e navegacao entre os 41 modulos (00–40);
- o corpus Markdown fonte e seus links locais;
- scripts PowerShell, Bash e Python, a ferramenta Java e as bibliotecas comuns;
- arquivos de teste, workflows de CI, laboratorio Docker, templates de
  relatorio e governanca;
- consistencia entre README, ROADMAP, CHANGELOG e conteudo implementado;
- presenca de objetivos, pratica, defesa, etica, referencias e validacao.

Esta e uma avaliacao de repositorio. Os laboratorios externos e cada comando
ofensivo nao foram executados contra alvos reais.

## O que o projeto e hoje

O conteudo se organiza em capacidades complementares:

| Capacidade | Modulos e artefatos | Papel no projeto |
|------------|---------------------|------------------|
| Programação e engenharia de aplicações | 00–05 | Evoluir dos fundamentos a dados, software, aplicações, automação e APIs especializadas. |
| Sistemas e infraestrutura | 06–07 Linux, 08–11 Windows, 12–13 macOS, 14–18 Redes | Construir e operar a base técnica anterior aos estudos integrados de segurança. |
| Criptografia | 19–22, OpenSSL, Python e padrões NIST/IETF | Projetar, implantar, operar, revisar e migrar proteção criptográfica. |
| Privacidade e atribuição | 23–25, WireGuard, telemetria e evidência sintética | Modelar exposição, operar VPN própria e investigar rastros com limites éticos. |
| Purple Team de borda | 26, firewalls, WAF, Cloudflare, BunkerWeb, bots e identidade | Testar controles autorizados, observar, ajustar, responder e retestar. |
| Especialização em segurança | 27–40 | Integrar governança, automação, reconhecimento, AppSec, identidade, cloud, plataformas, operações e defesa. |
| Acesso e exploracao | 30–37 | Estudar Web/API, AD, cloud, containers, acesso inicial, elevação e movimento lateral dentro de escopo autorizado. |
| Operacao | 35–37 e capstone 40 | Aplicar OPSEC, pós-exploração e movimentação lateral com evidência e critérios de parada. |
| Defesa e entrega | 38–40, atribuição no 25, templates e ATT&CK | Mostrar rastros, resposta, emulação e comunicação do risco. |
| Ferramental e ambiente | 27–30, `lib/`, `30-Web-API-AppSec/docker-lab/` | Reproduzir tarefas e sustentar os exercicios. |
| Experiencia de estudo | `estudo.sh`, React/Vite, Formacao e Biblioteca Completa | Navegar pelo curriculo e por todo o acervo, persistir progresso local e orientar a liberacao dos labs. |

O publico mais bem atendido e o estudante iniciante/intermediario. O módulo 00
cobre a base exigida e o repositorio tambem funciona como referencia rapida
para profissionais, mas ainda não é um curso totalmente autocontido: a
profundidade, as avaliações e a telemetria ainda variam nos acervos que não
integram as formações autocontidas de programação, Linux, Windows, macOS, redes,
criptografia e privacidade.

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
- A interface de estudos deriva seu catalogo do conteudo versionado, sem banco,
  conta ou telemetria, e nao duplica manualmente o curriculo. O manifesto
  separa a base da especialização, adota arquivos existentes por
  `contentPaths` e exige que todo material didatico elegivel pertença a uma
  colecao visivel.
- As ferramentas Python usam apenas a biblioteca padrao, facilitando o primeiro
  uso e a auditoria do codigo.
- O laboratorio publica somente um gateway em `127.0.0.1`; os alvos permanecem
  sem portas no host e sem egress.

## Lacunas e melhorias do conteudo atual

### Prioridade P0: confiabilidade e seguranca do aprendizado

| Lacuna | Impacto | Melhoria proposta | Criterio de aceite |
|--------|---------|-------------------|--------------------|
| Suite e cobertura implementadas; novos fluxos ainda exigem testes. | Regressões podem reaparecer quando uma ferramenta cresce sem fixture. | Exigir caso de sucesso e erro em toda mudança funcional. | CI verde e cobertura das bibliotecas comuns de pelo menos 70%. |
| As imagens estão fixadas, mas os digests envelhecem. | Sem revisão, correções de compatibilidade não chegam ao lab. | Revisar mensalmente `30-Web-API-AppSec/docker-lab/IMAGE-PINS.md` em branch e executar smoke test. | `docker compose config`, build e endpoints passam antes de atualizar cada digest. |
| Exemplos dependem de servicos publicos e respostas variaveis. | Exercicios podem falhar por rede, rate limit ou mudanca externa. | Criar fixtures DNS/HTTP/JWT e modos offline para exemplos e testes. | Quick start basico funciona sem atacar ou consultar terceiros. |
| Versoes suportadas podem divergir em mudanças futuras. | Documentação ou CI desatualizados confundem contribuidores. | Manter o núcleo de ferramentas em Python 3.10+, o curso 00 em Python 3.12+, Java 17+ e runtimes de frontend ainda suportados; revisar alterações no CI. | README, módulos, `pyproject.toml` e matrizes de CI continuam coerentes e distinguem requisito global do requisito didático. |

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

- Manter `pyproject.toml` como fonte da versão Python, Ruff, pytest e cobertura.
- Adicionar empacotamento reproduzivel e, se a ferramenta crescer, testes JUnit.
  A suite atual já compila com `-Werror` e testa os comportamentos da CLI.
- Validar schemas do JSON exportado pelas ferramentas e do layer ATT&CK.
- Manter scanner de segredos, SBOM, Actions fixadas por SHA, Dependabot e o
  inventário verificável de digests do lab.
- Fazer o CI de Markdown ignorar exemplos deliberadamente ficticios de forma
  explicita, em vez de enfraquecer regras globais.
- Criar uma politica de manutencao para ferramentas descontinuadas e exemplos
  legados; marcar conteudo como atual, legado ou historico.

## Novos conteudos recomendados

### Fundamentos antes de novas tecnicas

1. **Modulo 00 - Fundamentos, programação e seguranca do laboratorio (entregue)**
   - lógica, algoritmos, estruturas de dados, Python, Java, C, C#,
     JavaScript, terminal e Git;
   - engenharia de software, testes, depuração, HTTP, SQLite, APIs,
     concorrência, Docker e Nginx;
   - cinco laboratórios progressivos, exemplos executáveis nas cinco
     linguagens e TaskBoard full stack;
   - segurança local mínima: loopback, dados sintéticos, menor privilégio,
     proteção de segredos e cleanup;
   - redes, sistemas operacionais, criptografia e governança/RoE aprofundados
     permanecem nos módulos próprios.
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
| macOS distribuído | Conectar a formação 12–13 aos fundamentos de DNS, PKI, identidade e transporte dos módulos 14–18. | Lab MDM autorizado com teardown e dados sintéticos. |
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
- **07:** manter o curso Linux avançado sincronizado com ABIs e documentação
  do kernel; o material Web mantido nesse caminho integra curricularmente o
  módulo 30 sem quebrar links históricos.
- **08/09:** manter as trilhas Windows domesticas sincronizadas com o ciclo de
  vida do cliente, PowerShell, Defender, Sysinternals e a documentacao do SDK;
  os materiais de cloud e C2 nesses caminhos integram os módulos 32 e 35.
- **10/11:** manter Windows Server, implantacao, identidade e baselines
  sincronizados; depois do modulo de redes, acrescentar laboratorios
  distribuidos. Os materiais de containers e Python integram os módulos 33 e
  28, respectivamente.
- **12/13:** manter as trilhas macOS sincronizadas com hardware suportado,
  XNU, Platform Security, Deployment, MDM/DDM e SDKs; depois de redes, incluir
  um lab distribuído sem dados pessoais. Java e Initial Access integram os
  módulos 28 e 35.
- **14–18:** manter RFCs, recomendações Wi-Fi/VPN e exemplos de protocolo
  sincronizados; ampliar interoperabilidade sem exigir acesso a redes externas.
- **19–22:** manter padrões NIST/IETF, perfis TLS, bibliotecas e status PQC
  sincronizados; ampliar vetores oficiais e interoperabilidade sem chaves reais.
- **Pós-exploração no 37:** ampliar simulação com canários, aprovação do
  cliente, kill list, rollback, métricas de campanha e debrief purple team.

## Roadmap de implementacao sugerido

### 0-30 dias: estabilizar

- [x] corrigir a matriz de versoes Python e o README;
- [x] criar testes para `rte_common.py` e para os parsers sem rede;
- [x] adicionar healthchecks, limites de recursos e profiles ao Compose;
- [x] fixar imagens por digest após resolução dos manifests públicos;
- [x] publicar o contrato de modulo;
- [x] aplicar o contrato aos modulos 01, 07 e 11;
- [x] validar estrutura e invariantes do layer ATT&CK no CI;
- [x] revisar IDs e táticas do layer contra o snapshot oficial ATT&CK 19.2.

### 31-90 dias: tornar ensinavel

- [x] criar o modulo 00 com fundamentos de identidade e terminologia essencial;
- [x] adicionar fixtures, datasets e respostas explicadas para cinco labs;
- [x] criar `lab-doctor` e smoke tests locais;
- [x] criar profiles Compose `api`, `extended` e `full`, mantendo um default básico;
- [x] documentar unidades verificáveis de detecção em AD, Web, cloud e containers;
- [x] adicionar fixtures executáveis para AWS, Azure e GCP;
- [x] reorganizar a navegação com catálogo canônico e CLI.
- [x] oferecer uma interface visual local com progresso e desbloqueio de labs.

### 91-180 dias: ampliar com profundidade

- [x] entregar trilhas iniciais de identidade hibrida e APIs modernas;
- [x] criar conteúdo de auditoria CI/CD e supply chain;
- [x] entregar cinco módulos de redes com 91 capítulos, 26 labs, código e CI;
- [x] entregar o módulo 26 Purple Team com 22 capítulos, sete labs e CI;
- adicionar telemetria centralizada opcional ao lab;
- [x] publicar microemulacao purple team offline, do RoE ao debrief;
- medir conclusao, reproducibilidade e manutencao, nao apenas quantidade de
  arquivos ou tecnicas ATT&CK.

## Indicadores de qualidade

| Indicador | Meta inicial |
|-----------|--------------|
| Modulos com contrato editorial mínimo | 100% dos 41 módulos; validado por `validate_module_catalog.py` |
| Labs com setup, resultado esperado e cleanup testados | 100% |
| Ferramentas com testes offline | 100% |
| Bibliotecas comuns cobertas por testes | >= 70% |
| Imagens e Actions com versao imutavel | 100% |
| Documentos tecnicos revisados nos ultimos 12 meses | >= 90% |
| Tecnicas praticas ligadas a uma fonte de telemetria | >= 80% |
| Links locais validos no CI | 100% |
| Catalogo da aplicacao reproduzivel e sem artefatos versionados | 100% |

## Ordem recomendada para contribuicoes

Uma contribuicao deve preferir, nesta ordem:

1. corrigir material inseguro, quebrado ou irreproduzivel;
2. adicionar teste e evidencia ao que ja existe;
3. preencher fundamentos e defesa de um tema existente;
4. criar um lab pequeno, isolado e com cleanup;
5. somente entao adicionar uma nova tecnica ou ferramenta.

Essa ordem preserva o principal valor do projeto: ensinar seguranca ofensiva de
forma etica, verificavel e util tambem para quem precisa detectar e corrigir.
