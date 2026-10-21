# Referências

O curso é autocontido. Estas fontes servem para confirmar contratos da plataforma,
acompanhar evoluções e aprofundar decisões. Prefira especificação e documentação
oficial; valide a versão usada pelo seu projeto.

## Arquivos, processos e linguagens

- [Python pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python tempfile](https://docs.python.org/3/library/tempfile.html)
- [Python subprocess](https://docs.python.org/3/library/subprocess.html)
- [Java NIO Files](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/nio/file/Files.html)
- [.NET System.IO](https://learn.microsoft.com/dotnet/api/system.io)
- [Node.js File system](https://nodejs.org/api/fs.html)
- [C17 draft N2176](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2176.pdf)

## HTTP, webhooks e resiliência

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [GitHub — validating webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)
- [AWS Architecture Blog — exponential backoff and jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Google Cloud — retry strategy](https://cloud.google.com/storage/docs/retry-strategy)

## Jobs e orquestração

- [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [Kubernetes CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
- [IANA Time Zone Database](https://www.iana.org/time-zones)
- [RFC 3339 — timestamps](https://www.rfc-editor.org/rfc/rfc3339.html)

## Navegador e documentos

- [Playwright locators](https://playwright.dev/docs/locators)
- [Playwright auto-waiting](https://playwright.dev/docs/actionability)
- [W3C WAI forms](https://www.w3.org/WAI/tutorials/forms/)
- [OWASP CSV Injection](https://owasp.org/www-community/attacks/CSV_Injection)
- [Python csv](https://docs.python.org/3/library/csv.html)

## Observabilidade

- [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [Google SRE Workbook — alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)

## CI/CD e supply chain

- [GitHub Actions security](https://docs.github.com/en/actions/concepts/security)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/reference/security/oidc)
- [GitHub artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations)
- [SLSA specification](https://slsa.dev/spec/)
- [CycloneDX specification](https://cyclonedx.org/specification/overview/)
- [SPDX specification](https://spdx.dev/specifications/)
- [Semantic Versioning](https://semver.org/)
- [Reproducible Builds](https://reproducible-builds.org/docs/)

## Testes

- [Python unittest](https://docs.python.org/3/library/unittest.html)
- [Node test runner](https://nodejs.org/api/test.html)
- [JUnit 5 user guide](https://docs.junit.org/current/user-guide/)
- [.NET testing](https://learn.microsoft.com/dotnet/core/testing/)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/)

## Livros e artigos clássicos

- Martin Kleppmann, *Designing Data-Intensive Applications*.
- Michael T. Nygard, *Release It!*.
- Betsy Beyer et al., *Site Reliability Engineering*.
- Jez Humble e David Farley, *Continuous Delivery*.
- John Allspaw e Paul Hammond, *10+ Deploys Per Day*.

## Vídeos e cursos complementares

- [Full Cycle — Observabilidade com OpenTelemetry](https://www.youtube.com/watch?v=Y0gNpjHwx2M)
- [Full Cycle — CI/CD](https://www.youtube.com/watch?v=sc3LVX3E7RI)
- [GitHub Skills — Actions](https://skills.github.com/)
- [Playwright YouTube](https://www.youtube.com/@Playwrightdev)

Conteúdo em vídeo complementa; não substitui a leitura do contrato oficial nem
os testes na versão instalada.

## Comunidades

- [Stack Overflow](https://stackoverflow.com/)
- [Software Engineering Stack Exchange](https://softwareengineering.stackexchange.com/)
- [SRE Weekly](https://sreweekly.com/)
- [OpenTelemetry community](https://opentelemetry.io/community/)

Ao perguntar, use exemplo mínimo, remova segredos e descreva o que já mediu.

## Avaliação de fonte

Antes de adotar recomendação:

1. confirme autor, versão e data;
2. compare com especificação/documentação oficial;
3. separe propriedade garantida de detalhe de implementação;
4. reproduza com fixture controlada;
5. registre trade-off e limitação;
6. não copie comando destrutivo sem resolver alvos.

