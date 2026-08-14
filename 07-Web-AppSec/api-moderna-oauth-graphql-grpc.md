# APIs modernas: OAuth/OIDC, GraphQL e gRPC

## OAuth 2.0 e OpenID Connect

OAuth delega autorização; OIDC adiciona identidade. Valide `issuer`, `audience`,
assinatura, expiração, nonce/state e redirect URI exata. PKCE reduz interceptação
de authorization code em clientes públicos. Não aceite token destinado a outra
API e não trate ID token como access token.

### Checklist seguro

- authorization code + PKCE para clientes públicos;
- redirect URIs exatas, sem wildcard amplo;
- scopes mínimos e consentimento revisável;
- refresh token rotacionado e revogável;
- chaves JWKS com rotação/cache seguro;
- logs sem token completo.

## GraphQL

GraphQL concentra tipos e resolvers em um endpoint. Profundidade, aliases e
batching podem aumentar custo; autorização deve ocorrer por objeto/resolver, não
apenas na entrada. Introspection não é vulnerabilidade isolada, mas exposição em
produção precisa ser decisão consciente.

Teste em lab: limite depth/complexity, paginação, tamanho de batch, erros,
field-level authorization e BOLA em nodes. Registre operação e variáveis
redatadas, nunca secrets.

## gRPC

gRPC usa contratos protobuf e HTTP/2. Avalie TLS/mTLS, reflection, interceptors,
metadata, deadlines, tamanho de mensagem e autorização por método/objeto.
Streaming requer limites e cancelamento para evitar consumo não controlado.

## Evidência, detecção e mitigação

Uma evidência mínima contém principal, audience/scope, operação/método, objeto,
decisão de autorização, status e correlation ID. Detecção deve correlacionar
gateway e aplicação; retries e clientes móveis são falsos positivos comuns.

Mitigue com validação de token em biblioteca mantida, policy enforcement
centralizado, autorização também no domínio, rate/cost limits e testes negativos
cross-user automatizados.

