# Referências e materiais complementares

O curso é autocontido. Estas fontes servem para consultar contratos oficiais,
acompanhar ferramentas e ouvir explicações alternativas.

## Interface web e acessibilidade

- [MDN Web Docs](https://developer.mozilla.org/pt-BR/) — HTML, CSS, DOM,
  JavaScript, formulários, armazenamento e APIs do navegador.
- [Validação de formulários no cliente — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Form_validation) —
  validação nativa e JavaScript, sem substituir o servidor.
- [WCAG 2.2 — W3C](https://www.w3.org/TR/WCAG22/) e
  [visão geral](https://www.w3.org/WAI/standards-guidelines/wcag/) — padrão e
  materiais de apoio.
- [Tutorial de formulários acessíveis — W3C WAI](https://www.w3.org/WAI/tutorials/forms/) —
  rótulos, agrupamento, instruções e feedback.
- [Learn Forms — web.dev](https://web.dev/learn/forms/) — curso prático de
  formulários e acessibilidade.
- [Web Storage API — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API) —
  contrato síncrono de `localStorage` e `sessionStorage`.
- [Quotas e critérios de remoção — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria) —
  limites e condições nas quais armazenamento do navegador pode falhar ou ser
  removido.
- [`Intl.DateTimeFormat` — MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) —
  formatação de datas por locale e zona de tempo.
- [Interaction to Next Paint — web.dev](https://web.dev/articles/inp) — métrica
  de responsividade de interação e orientação de medição.

## Linguagens, testes e interfaces de processo

- [`argparse` — Python](https://docs.python.org/3/library/argparse.html) e
  [`unittest`](https://docs.python.org/3/library/unittest.html) — parser e testes
  usados no exemplo Python.
- [`System.getenv` — Java](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/System.html#getenv()) —
  leitura do ambiente e ressalvas de portabilidade.
- [`getenv` — C](https://en.cppreference.com/w/c/program/getenv) — acesso ao
  ambiente no contrato da biblioteca padrão C.
- [Environment.GetEnvironmentVariable — .NET](https://learn.microsoft.com/dotnet/api/system.environment.getenvironmentvariable) —
  acesso explícito a variáveis de ambiente.
- [`util.parseArgs` — Node.js](https://nodejs.org/api/util.html#utilparseargsconfig) e
  [test runner](https://nodejs.org/api/test.html) — parser e testes nativos do
  exemplo JavaScript.

## Empacotamento oficial

- [Python Packaging User Guide](https://packaging.python.org/en/latest/) —
  `pyproject.toml`, wheel, sdist e fluxo de publicação.
- [jpackage — Oracle](https://docs.oracle.com/en/java/javase/26/jpackage/packaging-overview.html) —
  imagens de aplicação e pacotes Java por plataforma.
- [.NET application publishing](https://learn.microsoft.com/dotnet/core/deploying/) —
  framework-dependent, self-contained, single-file e AOT.
- [npm documentation](https://docs.npmjs.com/) — pacotes e publicação no
  ecossistema JavaScript.
- [GNU Coding Standards: releases](https://www.gnu.org/prep/standards/) —
  convenções úteis para software C portátil.

## Configuração, interface e qualidade

- [Node.js: environment variables](https://nodejs.org/api/environment_variables.html) —
  `process.env` e arquivos `.env` no runtime atual.
- [Command Line Interface Guidelines](https://clig.dev/) — princípios de UX para
  CLIs; compare com convenções da sua plataforma.
- [SemVer em português](https://semver.org/lang/pt-BR/) e
  [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) —
  eventos, proteção e dados que não devem ser registrados.
- [GitHub artifact attestations](https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds) —
  proveniência verificável de artefatos.
- [OpenTelemetry — convenções gerais](https://opentelemetry.io/docs/specs/semconv/general/) e
  [modelo de dados de logs](https://opentelemetry.io/docs/specs/otel/logs/data-model/) —
  referência para atributos, correlação e estrutura de eventos; adotar o padrão
  completo não é requisito do curso.
- [Reproducible Builds](https://reproducible-builds.org/docs/) — fontes comuns de
  não determinismo e técnicas para artefatos reproduzíveis.
- [CycloneDX](https://cyclonedx.org/docs/1.6/json/) — formato de SBOM; compare com
  os recursos nativos da toolchain escolhida.

## GUI desktop e arquitetura

- [Tkinter — Python](https://docs.python.org/3/library/tkinter.html),
  [JavaFX](https://openjfx.io/openjfx-docs/),
  [Windows Presentation Foundation](https://learn.microsoft.com/dotnet/desktop/wpf/overview/),
  [GTK](https://docs.gtk.org/) e
  [Electron](https://www.electronjs.org/docs/latest/) — documentação primária
  para comparar plataforma, acessibilidade, thread de UI e distribuição.
- [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/) —
  use critérios aplicáveis também ao avaliar uma interface híbrida; não trate
  conformidade como resultado de uma ferramenta única.

## Vídeos em português

- [JavaScript Web e DOM na prática](https://www.youtube.com/watch?v=DcN49TD7it0) —
  interação com DOM e eventos.
- [Observabilidade e OpenTelemetry na prática — Full Cycle](https://www.youtube.com/watch?v=Y0gNpjHwx2M) —
  sinais e instrumentação.
- [Observabilidade de APIs na prática — Full Cycle](https://www.youtube.com/watch?v=bSU_O9JAibs) —
  experiência de diagnóstico entre cliente e serviço.
- [Fundamentos da arquitetura de software — Full Cycle](https://www.youtube.com/watch?v=Xt66rPTAWMs) —
  limites que também sustentam aplicações cliente.
- [Design Patterns — Filipe Deschamps](https://www.youtube.com/watch?v=arAz2Ff8s88) —
  abstrações e extensibilidade com contexto.

## Comunidade e blogs

- [Stack Overflow](https://stackoverflow.com/) e
  [Software Engineering Stack Exchange](https://softwareengineering.stackexchange.com/) —
  fóruns; verifique versão, contexto e documentação primária.
- [web.dev](https://web.dev/) — artigos técnicos sobre UX, acessibilidade e
  desempenho web.
- [Martin Fowler](https://martinfowler.com/) — arquitetura, entrega e padrões;
  trate artigos como orientação contextual, não especificação.

## Como usar referências

1. Use documentação oficial para comportamento exato.
2. Confirme versão, plataforma e data.
3. Reproduza um exemplo mínimo.
4. Compare respostas comunitárias com o contrato oficial.
5. Verifique licença antes de copiar código ou recursos visuais.
