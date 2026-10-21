# 09 — Autenticação de consumidores

Autenticação estabelece uma identidade com um nível de confiança. Autorização
decide ações. API key, cookie de sessão, access token, ID token e certificado
têm finalidades distintas; trocar um pelo outro cria vulnerabilidades difíceis
de perceber.

## Objetivos

- selecionar mecanismo por tipo de cliente;
- compreender OAuth 2.0, OpenID Connect e PKCE;
- validar tokens completamente;
- projetar emissão, rotação, revogação e auditoria;
- evitar credenciais em logs, URLs e código.

## 1. Atores e credenciais

- API key identifica aplicação/projeto, raramente pessoa;
- sessão autentica usuário e mantém estado no servidor;
- OAuth delega autorização a um cliente;
- OpenID Connect adiciona autenticação do usuário e ID Token;
- mTLS autentica pares por certificados;
- workload identity usa identidade da plataforma em vez de segredo estático.

Defina subject, actor e client separadamente. Um serviço pode agir em nome de
usuário; auditoria precisa saber ambos. Não use endereço IP como identidade.

## 2. OAuth e OpenID Connect

Authorization Code com PKCE é base para clientes públicos modernos. PKCE liga a
troca do código ao cliente que iniciou o fluxo. Redirect URI deve corresponder à
registrada. state protege correlação/CSRF; nonce liga autenticação OIDC à sessão.

OAuth 2.1 ainda é Internet-Draft em outubro de 2026, portanto não o cite como RFC
publicado. Ele consolida práticas modernas; use especificações finais e o
Security Best Current Practice aplicável ao implementar.

Access token autoriza acesso ao resource server. ID token fala ao client sobre
a autenticação; não deve ser aceito automaticamente como access token.

## 3. Validação de JWT

Decodificar três segmentos não é validar. Verifique:

1. formato e tamanho;
2. algoritmo permitido, sem aceitar escolha insegura do token;
3. assinatura com chave do emissor;
4. issuer exato;
5. audience da API;
6. expiração e not-before com skew limitado;
7. tipo/uso esperado quando disponível;
8. scopes/claims na autorização;
9. política de revogação ou sessão para o risco.

Cache de JWKS precisa de TTL, rotação e comportamento seguro para kid
desconhecido. Não busque URL arbitrária declarada pelo token.

Opaque tokens exigem introspection ou estado local. Isso facilita revogação, mas
adiciona dependência e cache de decisão.

## 4. Tipos de cliente

| Cenário | Base comum |
|---|---|
| aplicação web server-side | sessão segura ou code flow |
| SPA/mobile | code + PKCE, sem client secret embutido |
| serviço para serviço | client credentials/workload identity/mTLS |
| CLI pessoal | device flow ou loopback code flow conforme suporte |
| webhook recebido | assinatura da mensagem e segredo/certificado |

Um segredo compilado em app público não é segredo. Password grant e implicit
grant não devem ser escolhidos para novos sistemas.

## 5. Ciclo de vida

~~~text
emitir -> distribuir -> armazenar -> usar -> observar
       -> rotacionar -> revogar -> expirar -> destruir
~~~

Tokens de acesso devem ser curtos e de menor privilégio. Refresh tokens pedem
armazenamento forte, rotação e detecção de reuso. Chaves/certificados precisam
de overlap durante rotação. Revogação sem propagação e teste é apenas intenção.

Não coloque token em query string: URLs aparecem em histórico, proxy e logs.
Redija Authorization, Cookie e segredos em todos os sinais e bundles de suporte.

## 6. Falha e disponibilidade

Se o IdP está indisponível, tokens locais ainda podem ser validados até expirar;
introspection pode falhar em cada chamada. Escolha política de cache e fail
closed conforme risco. Health da API não deve depender de login real de usuário.

401 indica credencial ausente/inválida e pode incluir WWW-Authenticate. 403
indica identidade estabelecida sem permissão. Evite revelar detalhes que ajudam
enumeração.

## 7. Laboratório seguro

Contract Lab injeta X-Lab-Actor, X-Lab-Tenant e X-Lab-Role para testes locais.
Esses headers são input confiado somente pelo laboratório. Em produção, um
gateway não deve simplesmente encaminhar headers de identidade fornecidos pelo
cliente; remova-os e derive contexto de credencial validada.

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| ID token usado na API | audience/uso errado | access token |
| JWT só decodificado | token falso aceito | validação completa |
| secret na SPA | extração trivial | PKCE |
| token em URL | vazamento em logs | header/cookie seguro |
| header de identidade confiado | impersonação | contexto derivado |
| OAuth artesanal | grande superfície | IdP maduro |

## Exercícios

### Nível 1 — três fluxos

Modele SPA, serviço e CLI. **Aceite:** subject, client, credencial, audience,
expiração e revogação aparecem.

### Nível 2 — matriz JWT

Teste assinatura errada, issuer, audience, exp, nbf, algoritmo e kid. **Aceite:**
todos falham de forma segura e sem segredo no log.

### Nível 3 — rotação

Simule chave antiga/nova e cache JWKS. **Aceite:** overlap funciona, kid
desconhecido não dispara busca arbitrária e rollback está definido.

## Checklist

- [ ] Autenticação não foi confundida com autorização.
- [ ] Mecanismo corresponde ao tipo de cliente.
- [ ] JWT é validado, não apenas decodificado.
- [ ] Tokens têm audiência, prazo e privilégio mínimos.
- [ ] Rotação/revogação foram testadas.
- [ ] Nenhuma credencial aparece em URL ou telemetria.

