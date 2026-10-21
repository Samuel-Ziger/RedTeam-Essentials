# Autenticação, autorização e segurança de APIs

Segurança de API é uma propriedade do design, da implementação e da operação.
Ela não pode ser adicionada por um middleware no fim do projeto. Este capítulo
é inteiramente defensivo: modela ameaças em aplicações próprias e ensina a
prevenir, detectar e responder a falhas sem executar ataques contra terceiros.

## Objetivos de aprendizagem

Ao terminar, você deverá conseguir:

- diferenciar autenticação, autorização, sessão e auditoria;
- selecionar sessão, API key ou OAuth/OIDC conforme o contexto;
- aplicar autorização por ação, objeto e tenant;
- construir um threat model com ativos, fronteiras e casos de abuso;
- limitar entrada, consumo de recursos e integrações de saída;
- testar controles negativos e produzir evidência observável.

## Princípios que orientam todas as camadas

- **negação por padrão:** acesso precisa de regra positiva;
- **menor privilégio:** identidade recebe apenas capacidade necessária;
- **defesa em profundidade:** gateway, aplicação e banco protegem riscos
  diferentes;
- **mediação completa:** cada operação sensível reavalia a política;
- **falha segura:** timeout ou erro no componente de política não libera acesso;
- **separação de responsabilidades:** nenhuma credencial concede tudo;
- **observabilidade segura:** decisões ficam auditáveis sem registrar segredo;
- **simplicidade:** fluxo compreensível é mais verificável que magia implícita.

## Autenticação, autorização e auditoria

- **autenticação:** quem é o usuário, workload ou cliente;
- **autorização:** essa identidade pode executar esta ação neste objeto agora;
- **sessão:** como o estado autenticado continua entre chamadas;
- **accounting/auditoria:** o que foi solicitado, decidido e alterado.

Ser autenticado não concede acesso a qualquer identificador. Uma verificação
apenas na rota, como “tem role `user`”, não prova que aquele usuário pertence ao
tenant ou pode editar o produto solicitado.

## Identidades diferentes pedem credenciais diferentes

| Chamador | Opção comum | Observação |
|---|---|---|
| navegador first-party | sessão em cookie | proteger CSRF e fixação de sessão |
| aplicativo móvel/SPA | OAuth/OIDC com fluxo apropriado | token não deve ficar em local inseguro |
| serviço interno | identidade de workload/OAuth client credentials | rotação e audience restrita |
| integração simples | API key com escopo | identifica cliente, não pessoa |
| operador humano | SSO/OIDC + MFA conforme risco | sessão curta para ação privilegiada |

Evite credencial compartilhada por equipe. Sem identidade individual ou de
workload, revogação, atribuição e auditoria ficam fracas.

## Sessões com cookie

Uma sessão server-side usa identificador aleatório e opaco. O estado fica em
armazenamento controlado pelo servidor. O cookie deve considerar:

```http
Set-Cookie: session=<opaque>; Secure; HttpOnly; SameSite=Lax; Path=/
```

- `Secure`: envio apenas sobre HTTPS;
- `HttpOnly`: scripts não leem o valor;
- `SameSite`: reduz envio cross-site, conforme fluxo desejado;
- `Path`/`Domain`: menor escopo necessário;
- expiração absoluta e por inatividade;
- rotação depois de login e elevação de privilégio;
- revogação em logout, troca de senha e incidente.

`HttpOnly` reduz furto via JavaScript, mas não impede que um script comprometido
faça requisições no contexto da sessão. Prevenção de XSS continua necessária.

### CSRF

CSRF importa quando o navegador envia credenciais automaticamente. Defesas
combináveis incluem `SameSite`, token anti-CSRF vinculado à sessão, verificação
de origem e exigir media type não enviável por formulário simples. `GET` nunca
deve executar mudança de estado pretendida.

CORS não é proteção CSRF universal e não é autenticação.

## API keys

Uma API key deve:

- ter entropia suficiente e prefixo identificador que não seja secreto;
- ser exibida integralmente apenas no momento de criação;
- ser armazenada como hash verificável quando não for preciso recuperá-la;
- possuir dono, escopos, ambiente, criação, uso e expiração;
- permitir duas chaves ativas durante rotação;
- ser revogável sem deploy;
- nunca aparecer em query string ou log.

Uma key identifica um cliente/projeto. Se a aplicação precisa saber qual pessoa
aprovou uma operação, adicione identidade humana apropriada.

## OAuth 2.0 e OpenID Connect

OAuth delega autorização; OpenID Connect acrescenta uma camada de identidade.
Use fluxos atuais suportados pelo provedor e biblioteca madura. Não implemente
um authorization server como exercício de produção.

Ao validar um access token, verifique pelo menos:

- assinatura com algoritmo permitido explicitamente;
- emissor (`iss`) exato;
- audience (`aud`) destinada à API;
- validade temporal (`exp`, `nbf`) com tolerância pequena e definida;
- escopos/permissões necessários;
- tipo/uso do token quando o ecossistema o diferencia;
- status de chave e comportamento de rotação;
- tenant/contexto esperado.

Não aceite algoritmo indicado pelo token sem allowlist. Não trate um ID token
como access token. Decodificar um JWT não é validá-lo.

### Tokens autocontidos e opacos

Um JWT permite validação local, mas revogação imediata é mais difícil e claims
ficam visíveis ao portador. Token opaco exige introspecção ou lookup, mas
centraliza estado. A escolha depende de latência, disponibilidade, revogação e
sensibilidade. Nunca coloque segredo no payload de um JWT apenas porque ele está
codificado.

Refresh tokens exigem armazenamento protegido, rotação, detecção de reuso,
revogação e escopo estrito. Access tokens devem ser curtos o suficiente para
limitar exposição sem tornar o sistema indisponível.

## Senhas e recuperação de conta

- armazene hash adaptativo com salt usando configuração atual recomendada,
  como Argon2id, scrypt ou alternativa aprovada no ambiente;
- calibre custo e revise periodicamente;
- aceite senhas longas e gerenciadores de senha;
- evite regras arbitrárias que pioram usabilidade sem reduzir risco;
- compare em tempo apropriado usando biblioteca;
- limite tentativas por conta e contexto sem permitir negação trivial;
- ofereça MFA adequado ao risco;
- proteja reset contra enumeração e token reutilizável;
- invalide ou reavalie sessões após eventos sensíveis.

Hash de senha não é cifra reversível e não deve usar hash rápido isolado.
Nunca registre senha, resposta de recuperação ou token MFA.

## Autorização por objeto e contexto

Modelos comuns podem coexistir:

- **RBAC:** papéis concedem permissões;
- **ABAC:** atributos do principal, objeto e contexto entram na decisão;
- **ReBAC:** relações como membro, proprietário ou gerente;
- **capability:** posse de um token limitado concede uma operação específica.

Uma política legível:

```text
permit update_product when
  principal.active
  and principal.tenant_id == product.tenant_id
  and principal has permission "product:update"
  and product.status != "archived"
```

O repositório pode reforçar isolamento incluindo tenant na consulta:

```sql
SELECT id, name, version
FROM product
WHERE tenant_id = :principal_tenant_id
  AND id = :product_id;
```

Isso reduz o risco de buscar um objeto de outro tenant e esquecer a verificação
depois. Row-level security pode adicionar defesa em profundidade, mas precisa de
configuração e testes; não substitui a política da aplicação.

### 403 ou 404?

Retornar 404 pode ocultar a existência do recurso quando isso faz parte do
modelo. A auditoria interna ainda deve distinguir “inexistente” de “negado”.
Se a existência já for pública, 403 pode ser mais claro. Escolha por política,
não por conveniência de controller.

### Matriz de permissões

| Ação | leitor | editor | administrador | condição adicional |
|---|---:|---:|---:|---|
| listar produto | sim | sim | sim | mesmo tenant |
| criar produto | não | sim | sim | tenant ativo |
| alterar produto | não | sim | sim | não arquivado |
| arquivar produto | não | não | sim | motivo obrigatório |
| ler auditoria | não | não | sim | privilégio separado |

Transforme a matriz em testes. Inclua negação por objeto, tenant, status e
permissão, não apenas testes positivos.

## Threat modeling defensivo

Threat model não é uma lista genérica de ataques. É uma descrição de como este
sistema protege estes ativos contra estes casos de abuso.

### 1. Inventarie ativos

- dados pessoais, financeiros e comerciais;
- credenciais, chaves e sessões;
- integridade de estoque/pedido;
- disponibilidade da API e jobs;
- trilha de auditoria;
- capacidade de emitir eventos ou executar ação administrativa.

### 2. Desenhe fluxos e fronteiras

```text
[navegador não confiável]
        | HTTPS
        v
[gateway] -> [API] -> [PostgreSQL]
                 \-> [outbox] -> [broker] -> [worker] -> [MongoDB]
        ^
        | administração por identidade separada
```

Marque onde identidade muda, dados são persistidos, input não confiável entra
e privilégio aumenta.

### 3. Escreva casos de abuso

Formato útil:

```text
Dado um usuário autenticado de outro tenant,
quando ele referencia um productId válido que não lhe pertence,
então nenhum dado ou diferença temporal relevante é revelado,
a alteração não ocorre e a negação é auditada sem dados sensíveis.
```

Categorias como falsificação de identidade, adulteração, repúdio, exposição,
negação de serviço e elevação de privilégio ajudam a revisar, mas o resultado
precisa terminar em controle, teste, dono e risco residual.

### 4. Priorize e acompanhe

Use impacto, probabilidade, detectabilidade e exposição. Para cada risco:

- decisão: mitigar, evitar, transferir ou aceitar;
- controle preventivo e detectivo;
- teste reproduzível;
- telemetria e runbook;
- responsável e prazo;
- risco residual aceito por quem possui autoridade.

## Validação e injeção

- use placeholders/parâmetros SQL, nunca concatene valores;
- mapeie nomes de coluna e direção de sort por allowlist do servidor;
- construa filtros MongoDB a partir de DTO, sem aceitar operador arbitrário;
- escape saída pelo contexto ao renderizar HTML;
- limite JSON por bytes, profundidade, quantidade e comprimento;
- rejeite media type e encoding inesperados;
- trate upload por tamanho, tipo verificado, nome gerado e armazenamento isolado;
- valide novamente ao cruzar uma fronteira de confiança.

Validação de formato não torna texto seguro para qualquer destino. O mesmo
valor exige tratamento diferente em SQL, HTML, shell, log e cabeçalho.

## Proteção de recursos

Disponibilidade depende de limites coerentes:

| Recurso | Controles |
|---|---|
| request | bytes, headers, profundidade, tempo |
| resposta | paginação, streaming controlado, limite de exportação |
| banco | pool, statement timeout, índice, custo da consulta |
| concorrência | fila limitada, worker count, backpressure |
| retry | tentativas, backoff, jitter, deadline |
| cache | tamanho, TTL, chave com tenant e variações corretas |
| job | quota, prioridade, prazo, cancelamento |

Rate limiting pode combinar identidade, credencial, rota e origem. IP sozinho
é frágil por NAT, proxies e IPv6. Em ambiente distribuído, defina se o limite
é local ou global e como reage quando o armazenamento de quota falha.

Retorne `429` e `Retry-After` quando houver prazo confiável. Rate limit protege
capacidade; não conserta consulta sem índice nem substitui autorização.

## CORS

CORS instrui navegadores sobre leitura de respostas cross-origin. Uma API
continua acessível por clientes não navegador; portanto, CORS não controla quem
pode chamar.

- mantenha allowlist exata de origens confiáveis;
- não reflita qualquer `Origin`;
- origem `*` não combina com credenciais;
- limite métodos e headers realmente necessários;
- cacheie preflight com cuidado e inclua variação correta;
- teste origens permitidas, negadas e `null` conforme o caso.

## SSRF e integrações por URL

Se o produto precisa buscar uma URL fornecida pelo usuário, trate-o como uma
capacidade de rede perigosa:

- prefira destinos cadastrados a URL arbitrária;
- aceite apenas esquema e porta necessários;
- resolva e valide endereços contra faixas proibidas conforme o ambiente;
- revalide a cada redirect e limite sua quantidade;
- use egress proxy/firewall e identidade de rede com menor privilégio;
- imponha timeout e limites de download/descompressão;
- não encaminhe credenciais internas;
- registre destino normalizado e decisão sem segredos.

Uma validação textual isolada não basta: DNS pode mudar e redirects atravessam
novas fronteiras. Centralize a funcionalidade em um cliente seguro.

## Segredos, criptografia e dados

- segredos ficam fora de código, imagem e Compose versionado;
- cada serviço e ambiente possui credencial distinta;
- rotação funciona sem rebuild e é exercitada;
- acesso ao secret manager é de menor privilégio e auditado;
- TLS é validado nas conexões externas e internas relevantes;
- criptografia em repouso inclui gestão, rotação e recuperação de chaves;
- backup recebe proteção equivalente e restore é testado;
- coleta, retenção, exportação e deleção são documentadas.

Não crie algoritmo criptográfico, JWT ou protocolo de autenticação próprio.
Use primitivas e bibliotecas mantidas, com configuração revisada.

## Logs e auditoria

Um log operacional pode conter:

```json
{
  "event": "authorization_decision",
  "requestId": "3bb0a764bd9a",
  "principalId": "usr_42",
  "tenantId": "ten_7",
  "action": "product.update",
  "resourceType": "product",
  "decision": "deny",
  "reasonCode": "tenant_mismatch"
}
```

Nunca registre token, cookie, senha, segredo de cliente ou body integral por
conveniência. Identificadores pessoais podem exigir pseudonimização, controle
de acesso e retenção reduzida. Proteja logs contra quebra de linha e campos de
alta cardinalidade descontrolada.

Auditoria sensível precisa de integridade, acesso restrito, retenção, busca e
processo de revisão. Um arquivo que ninguém consulta não é um controle completo.

## Dependências e cadeia de fornecimento

- mantenha lockfile e origem confiável;
- revise dependências diretas e remova as desnecessárias;
- automatize análise de vulnerabilidades com triagem e prazo;
- gere inventário/SBOM quando o processo exigir;
- verifique assinatura/proveniência de artefatos quando disponível;
- construa imagem mínima, sem compiladores/segredos de build no runtime;
- execute como usuário sem privilégio e filesystem restrito quando possível;
- atualize base e runtime em uma cadência definida.

Um scanner produz evidência, não a decisão final. Avalie alcançabilidade,
impacto, mitigação e versão corrigida.

## Testes de segurança essenciais

Para cada endpoint protegido, cubra:

1. sem credencial;
2. credencial malformada, expirada, issuer e audience errados;
3. identidade válida sem escopo;
4. role correta em outro tenant;
5. objeto inexistente e objeto ocultado;
6. mudança de estado que remove permissão durante o fluxo;
7. campos inesperados, extremos e corpo grande;
8. rate limit e recuperação após a janela;
9. logs sem credenciais ou dado proibido;
10. falha do provedor de identidade ou policy engine.

Execute em laboratório isolado e autorizado. Teste negativo confirma que o
controle nega de forma estável; não requer explorar sistemas de terceiros.

## Resposta a incidente de credencial

Um runbook mínimo responde:

- como revogar key, sessão, client ou chave de assinatura;
- como identificar escopo e janela de uso;
- quais logs confiáveis permitem investigação;
- como rotacionar sem interromper todos os clientes;
- quem decide comunicação e recuperação;
- como preservar evidência e evitar novo vazamento;
- qual teste impede recorrência.

Pratique o runbook. Uma credencial “rotacionável” que nunca foi rotacionada é
uma hipótese, não uma capacidade comprovada.

## Exercícios

1. Construa matriz de permissão para produtos, estoque e auditoria.
2. Converta cada linha em testes positivos e negativos.
3. Desenhe o fluxo de identidade de navegador, API e banco.
4. Faça threat model da Inventory API com cinco casos de abuso priorizados.
5. Defina validação completa de um access token sem implementar criptografia.
6. Projete rotação de API key com duas credenciais simultaneamente válidas.
7. Especifique limites para busca, exportação e upload.
8. Revise um conjunto de logs fictícios e remova campos sensíveis.
9. Escreva runbook para vazamento de credencial de serviço.
10. Modele uma busca de URL externa com egress e redirects controlados.

## Critérios de conclusão

- cada identidade e credencial possui dono, escopo, validade e revogação;
- autorização considera ação, o objeto, o tenant e o contexto;
- todo risco priorizado tem controle, teste, telemetria e responsável;
- entrada e consumo de recursos possuem limites antes do trabalho caro;
- logs e erros são acionáveis sem expor segredo;
- rotação e resposta a incidente foram praticadas;
- testes negativos falham antes de qualquer alteração persistente;
- o risco residual está documentado e aceito conscientemente.

## Checklist de revisão

- [ ] Inventariei ativos, identidades e fronteiras de confiança.
- [ ] Testei autorização por recurso e tenant.
- [ ] Valido issuer, audience, expiração, assinatura e escopo.
- [ ] CORS, CSRF e SSRF têm controles distintos.
- [ ] Entrada, query, pools, jobs e retries possuem limites.
- [ ] Segredos podem ser rotacionados sem commit ou rebuild.
- [ ] Logs são sanitizados, protegidos e realmente revisados.
- [ ] Backup, restore e resposta a incidente foram exercitados.
