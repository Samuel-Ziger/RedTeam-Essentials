# 10 — Autorização e isolamento entre tenants

Autorização responde se um principal pode executar uma ação sobre um recurso no
contexto atual. Ela precisa estar no caso de uso e na consulta de dados; esconder
botão ou validar somente a rota não protege acesso direto ao objeto.

## Objetivos

- modelar política com sujeito, ação, recurso e contexto;
- comparar RBAC, ABAC, ReBAC e capabilities;
- impedir BOLA, BFLA e exposição de propriedades;
- garantir isolamento em dados, cache, jobs e eventos;
- transformar matriz de autorização em testes.

## 1. Elementos da decisão

~~~text
decision = allow(subject, action, resource, context)
~~~

Subject vem da autenticação validada. Action é uma permissão estável como
item:update. Resource carrega owner, tenant, estado e classificação. Context
pode incluir canal, finalidade ou step-up, mas dados frágeis como IP não devem
ser controle único.

Policy Enforcement Point intercepta a ação; Policy Decision Point avalia a
regra; fonte de atributos fornece dados. Mesmo em código simples, separar esses
papéis melhora teste e observação.

## 2. Modelos

- RBAC agrupa permissões em papéis; simples, mas papéis podem explodir.
- ABAC combina atributos; expressivo, porém exige qualidade e atualização.
- ReBAC usa relações, como member-of ou owner-of.
- Capability concede uma ação delimitada pela posse de token/referência.

Combinações são comuns:

~~~text
allow item:update
se role inclui editor
e principal.tenant_id == item.tenant_id
e item.status != archived
~~~

Negação explícita e default deny evitam que caso desconhecido vire permissão.

## 3. Objeto, função e propriedade

BOLA ocorre quando trocar item_id permite acessar objeto alheio. BFLA permite
chamar função administrativa sem papel. Broken Object Property Level
Authorization ocorre ao ler ou alterar campo que o principal não pode acessar.

Proteções:

- carregar recurso já escopado ao tenant/principal;
- autorizar toda operação e objeto;
- schemas de escrita diferentes por intenção;
- projeção de resposta por permissão;
- testes com identificador válido de outro tenant;
- não confiar em ID não enumerável.

## 4. Multitenancy de ponta a ponta

tenant_id deve ser derivado da identidade, nunca aceito livremente no corpo.
Propague-o em:

- consultas e restrições do banco;
- chaves de cache e idempotência;
- índices de busca;
- armazenamento de arquivo;
- filas, eventos e jobs;
- métricas/auditoria com cardinalidade controlada;
- ferramentas de suporte.

Row-level security pode adicionar defesa no banco, mas não substitui política do
caso de uso. Conexão reutilizada precisa limpar contexto de tenant para não vazar.

## 5. Ausência e ocultação

Quando recurso existe em outro tenant, devolver 404 reduz enumeração. Faça isso
uniformemente; diferenças de tempo, tamanho ou mensagem podem revelar existência.
Operação de suporte autorizada pode ter visão cruzada, mas requer permissão
específica, justificativa, auditoria e limitação.

## 6. Tempo, cache e revogação

Decisões podem ficar obsoletas se papel ou relação muda. Cache de autorização
precisa de TTL e invalidação proporcionais ao risco. Streams e jobs longos devem
reavaliar permissão em pontos definidos. Uma credencial válida não congela
autorização para sempre.

Evite registrar decisões com atributos sensíveis completos. Registre policy ID,
versão, ação, resultado e motivo categórico.

## 7. Matriz e testes

| Sujeito | Ação | Recurso | Estado | Resultado |
|---|---|---|---|---|
| reader A | read | tenant A | active | allow |
| reader A | update | tenant A | active | deny |
| writer A | update | tenant A | active | allow |
| writer A | read | tenant B | active | not found |
| writer A | update | tenant A | archived | deny |

Gere testes positivos e negativos. Teste listagem, acesso direto, propriedade,
lote, exportação e evento; corrigir GET e esquecer export é falha recorrente.

## Falhas comuns

| Falha | Risco | Correção |
|---|---|---|
| filtro só na lista | acesso por ID | escopo no repositório |
| role aceito do body/header | elevação | derivar da identidade |
| admin genérico | privilégio excessivo | ações específicas |
| cache sem tenant | vazamento | chave contextual |
| job não reavalia | acesso após revogação | checkpoints de política |

## Exercícios

### Nível 1 — matriz

Modele quatro sujeitos, seis ações e três estados. **Aceite:** default deny e
propriedades sensíveis estão incluídos.

### Nível 2 — dois tenants

Teste listagem, GET, PATCH, evento e cache com tenants A/B. **Aceite:** nenhum
identificador conhecido atravessa o limite.

### Nível 3 — mudança de permissão

Revogue papel durante job ou stream. **Aceite:** política define quando parar,
como auditar e como evitar efeito posterior.

## Checklist

- [ ] Principal vem de autenticação validada.
- [ ] Ação, objeto e propriedade são autorizados.
- [ ] tenant_id não vem do corpo.
- [ ] Cache, job e evento preservam isolamento.
- [ ] Política tem versão e default deny.
- [ ] Casos negativos usam IDs válidos de outro tenant.

