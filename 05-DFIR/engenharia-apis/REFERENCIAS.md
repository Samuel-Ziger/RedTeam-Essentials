# Referências e aprofundamento

O curso é autocontido: referências confirmam detalhes normativos, acompanham
versões e oferecem outras explicações. Quando blog, vídeo ou fórum divergir,
prefira a especificação e registre a versão consultada. Links revisados em
2026-10-05.

## HTTP e mensagens

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html)
- [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [RFC 9333 — RateLimit Fields for HTTP](https://www.rfc-editor.org/rfc/rfc9333.html)
- [RFC 6585 — Additional HTTP Status Codes](https://www.rfc-editor.org/rfc/rfc6585.html)
- [IANA HTTP Field Registry](https://www.iana.org/assignments/http-fields/http-fields.xhtml)
- [WHATWG URL Standard](https://url.spec.whatwg.org/)

## Contratos e schemas

- [OpenAPI — índice oficial de versões](https://spec.openapis.org/oas/)
- [OpenAPI 3.1.0](https://spec.openapis.org/oas/v3.1.0.html)
- [OpenAPI 3.2.1](https://spec.openapis.org/oas/v3.2.1.html)
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12)
- [AsyncAPI 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0)
- [CloudEvents specification](https://github.com/cloudevents/spec)
- [GraphQL — índice de releases](https://spec.graphql.org/)
- [GraphQL September 2025](https://spec.graphql.org/September2025/)
- [Protocol Buffers language guide](https://protobuf.dev/programming-guides/proto3/)

## Identidade e autorização

- [RFC 6749 — OAuth 2.0](https://www.rfc-editor.org/rfc/rfc6749.html)
- [RFC 7636 — PKCE](https://www.rfc-editor.org/rfc/rfc7636.html)
- [RFC 9700 — OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700.html)
- [OAuth 2.1 — Internet-Draft atual](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [OpenID Connect Core 1.0, errata 2](https://openid.net/specs/openid-connect-core-1_0.html)
- [RFC 7519 — JWT](https://www.rfc-editor.org/rfc/rfc7519.html)
- [RFC 8725 — JWT Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725.html)

OAuth 2.1 continua Internet-Draft na data de revisão; não o apresente como RFC.

## Segurança e engenharia

- [OWASP API Security Top 10 — 2023](https://api-security.owasp.org/editions/2023/en/0x00-header/)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [CNCF TAG Security — Cloud Native Security Whitepaper](https://github.com/cncf/tag-security/tree/main/security-whitepaper)

## gRPC, streaming e observabilidade

- [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [gRPC Deadlines](https://grpc.io/docs/guides/deadlines/)
- [gRPC Retry](https://grpc.io/docs/guides/retry/)
- [gRPC Health Checking](https://grpc.io/docs/guides/health-checking/)
- [gRPC Service Config](https://grpc.io/docs/guides/service-config/)
- [RFC 6455 — WebSocket](https://www.rfc-editor.org/rfc/rfc6455.html)
- [HTML Living Standard — Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
- [OpenTelemetry HTTP conventions](https://opentelemetry.io/docs/specs/semconv/http/)

## Implementação nas cinco linguagens

- [FastAPI](https://fastapi.tiangolo.com/)
- [Python urllib.parse](https://docs.python.org/3/library/urllib.parse.html)
- [Java HttpClient](https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/HttpClient.html)
- [C — SEI CERT Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)
- [.NET HttpClient](https://learn.microsoft.com/dotnet/api/system.net.http.httpclient)
- [JavaScript Fetch Standard](https://fetch.spec.whatwg.org/)

## Vídeos, fóruns e blogs complementares

- [CNCF — canal oficial](https://www.youtube.com/@cncf)
- [GraphQL Foundation — canal oficial](https://www.youtube.com/@GraphQLFoundation)
- [OWASP — canal oficial](https://www.youtube.com/@OWASPGLOBAL)
- [OpenAPI Initiative — discussões](https://github.com/OAI/OpenAPI-Specification/discussions)
- [AsyncAPI — discussões](https://github.com/asyncapi/spec/discussions)
- [gRPC — discussões](https://github.com/grpc/grpc/discussions)
- [Stack Overflow — OpenAPI](https://stackoverflow.com/questions/tagged/openapi)
- [Stack Overflow — FastAPI](https://stackoverflow.com/questions/tagged/fastapi)
- [Martin Fowler — artigos de arquitetura](https://martinfowler.com/architecture/)

Fóruns ajudam a encontrar casos reais, não a estabelecer regra normativa. Antes
de aplicar uma resposta, confirme data, versão, contexto, segurança e teste local.

## Roteiro de leitura

1. Capítulos 00–08: RFC 9110, 9111, 9457 e OpenAPI 3.1.
2. Capítulos 09–12: RFC 9700, OIDC Core e OWASP API 2023.
3. Capítulos 13–17: OpenTelemetry e documentação do framework.
4. Capítulos 18–22: CloudEvents, AsyncAPI, GraphQL, gRPC e WebSocket.
5. Capítulos 23–25: documentação das linguagens e discussões dos projetos.

