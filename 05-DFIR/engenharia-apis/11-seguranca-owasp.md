# 11 — Segurança de APIs e OWASP

Segurança de API começa no modelo de dados, identidade e fluxos de negócio. Um
gateway pode validar token, tamanho e frequência; ele não sabe quem é owner de
um objeto, se uma transição é fraudulenta ou se um campo é confidencial.

## Objetivos

- criar threat model por operação e fluxo;
- aplicar os riscos OWASP API Security Top 10 2023;
- limitar recursos e integrações de saída;
- consumir APIs de terceiros como entrada não confiável;
- transformar controle em teste e telemetria.

## 1. Modelo de ameaça

Mapeie:

- ativos e classificação;
- atores legítimos e adversários;
- fronteiras de confiança;
- entradas, saídas e dependências;
- operações caras e fluxos sensíveis;
- abuso de volume, ordem, concorrência e automação;
- prevenção, detecção, resposta e owner.

Threat modeling não é apenas listar injeção. Pergunte como um usuário válido
abusa da função permitida: reservar milhares de unidades, enumerar objetos,
forçar custo computacional ou explorar corrida.

## 2. OWASP API Security Top 10 2023

1. **BOLA:** autorização ausente no objeto.
2. **Broken Authentication:** identidade pode ser assumida ou token mal validado.
3. **Broken Object Property Level Authorization:** campo indevido é lido/alterado.
4. **Unrestricted Resource Consumption:** custo sem limite.
5. **Broken Function Level Authorization:** função privilegiada exposta.
6. **Unrestricted Access to Sensitive Business Flows:** automação abusiva.
7. **SSRF:** servidor acessa destino controlado pelo usuário.
8. **Security Misconfiguration:** defaults, exposição e headers inseguros.
9. **Improper Inventory Management:** versões e hosts esquecidos.
10. **Unsafe Consumption of APIs:** resposta de terceiro confiada demais.

A lista é ferramenta de conscientização, não análise completa de risco. Injeção,
dependência vulnerável e segredo exposto continuam relevantes mesmo fora dela.

## 3. Limites de recursos

Limite bytes comprimidos/descomprimidos, campos, profundidade, itens, page size,
complexidade, tempo, concorrência e frequência. Rate limit por IP não protege
usuário distribuído nem fluxo caro; combine identidade, tenant, operação e custo.

Ao rejeitar, use 413 para corpo grande, 422 para limite semântico, 429 para
frequência e 503 quando a capacidade geral está indisponível. Não leia o corpo
inteiro antes de aplicar o limite.

## 4. SSRF e chamadas de saída

Se usuário fornece URL de webhook ou importação, valide esquema, host e porta;
resolva DNS de forma controlada; bloqueie destinos internos/link-local e
redirecionamentos inesperados; limite resposta, tempo e protocolos. Revalide após
redirecionamento e considere DNS rebinding.

Allowlist explícita é mais forte quando o produto permite. Proxy de egress e
identidade de workload limitam impacto. Não retorne resposta interna bruta.

## 5. Consumo inseguro

APIs parceiras também são não confiáveis:

- valide status, media type, schema e tamanho;
- use timeout, limite de redirecionamento e TLS correto;
- não concatene dados da resposta em SQL, URL ou log;
- não siga link arbitrário;
- preserve circuit breaker e quota;
- trate mudança de enum/campo e resposta parcial;
- proteja segredo e minimize permissões.

Um parceiro comprometido pode atacar sua aplicação através da integração.

## 6. Inventário e configuração

Catálogo precisa de host, ambiente, versão, owner, contrato, dados, exposição,
autenticação, SLO e data de revisão. Ambientes antigos, endpoints debug e versões
esquecidas aumentam superfície.

Defaults seguros incluem schema fechado de escrita, documentação pública apenas
quando prevista, CORS mínimo, métodos necessários, mensagens seguras e
dependências atualizadas. CORS é política do browser, não autenticação da API.

## 7. Controles verificáveis

Para cada risco, registre:

| Risco | Prevenção | Detecção | Teste | Owner |
|---|---|---|---|---|
| BOLA | consulta escopada | denial por motivo | ID de outro tenant | domínio |
| exaustão | limites/custo | saturação/rejeições | corpo/lote máximos | plataforma |
| SSRF | egress/allowlist | destino negado | fixtures de IP interno | integração |

Uma política sem teste pode regredir; um bloqueio sem telemetria vira incidente
invisível.

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| confiar no gateway para ownership | BOLA | domínio/repositório |
| limite só por IP | bypass e injustiça | identidade + custo |
| URL validada só por string | SSRF | resolução/egress |
| resposta parceira confiada | injeção/DoS | validar e limitar |
| API esquecida | versão vulnerável | inventário automatizado |

## Exercícios

### Nível 1 — mapa OWASP

Ligue dez riscos a uma operação do seu domínio. **Aceite:** prevenção, detecção,
teste e owner existem.

### Nível 2 — abuso local

Teste objeto alheio, propriedade read-only, corpo grande, lote, corrida e URL
proibida em serviço local. **Aceite:** falhas são seguras e observáveis.

### Nível 3 — dependência hostil

Crie fake que responde lento, grande, schema errado e redireciona. **Aceite:**
timeout, limite e validação impedem propagação.

## Checklist

- [ ] Threat model cobre usuários legítimos abusivos.
- [ ] OWASP foi traduzido em controles do domínio.
- [ ] Recursos têm limites multidimensionais.
- [ ] Saída de rede é restrita e revalidada.
- [ ] Dependências externas são entradas não confiáveis.
- [ ] Inventário e configuração são verificados no pipeline.

