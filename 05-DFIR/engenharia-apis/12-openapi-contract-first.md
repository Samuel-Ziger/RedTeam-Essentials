# 12 — OpenAPI e desenvolvimento contract-first

OpenAPI descreve APIs HTTP em formato processável. Serve para revisão, mocks,
documentação, validação, testes e geração de clientes. Não substitui decisões de
domínio nem prova que a aplicação obedece ao documento.

## Objetivos

- estruturar documento OpenAPI 3.1;
- modelar operações, schemas, problemas e segurança;
- executar fluxo contract-first com feedback de consumidores;
- detectar drift e mudanças incompatíveis;
- usar geração sem entregar controle ao gerador.

## 1. Estrutura essencial

~~~yaml
openapi: 3.1.0
info:
  title: Items API
  version: 1.0.0
paths:
  /v1/items/{itemId}:
    get:
      operationId: getItem
      parameters:
        - name: itemId
          in: path
          required: true
          schema:
            type: string
            pattern: '^[A-Za-z0-9_-]{1,64}$'
      responses:
        '200':
          description: Item encontrado
        '404':
          $ref: '#/components/responses/NotFound'
~~~

info.version é versão do documento/API, não a versão OpenAPI. operationId deve
ser único e estável porque geradores o transformam em nome de método.

O curso usa 3.1.0 no contrato executável por compatibilidade das ferramentas.
Em outubro de 2026 a série publicada inclui OpenAPI 3.2.1. Atualizar a versão do
documento exige validar linter, gateway, geradores e registry; “mais recente” não
garante suporte do ecossistema.

## 2. Schemas e JSON Schema

OpenAPI 3.1 alinha schemas ao JSON Schema 2020-12, com dialeto definido pela
especificação. Modele:

- required versus propriedade opcional;
- additionalProperties;
- limites e patterns;
- readOnly/writeOnly;
- oneOf/anyOf/allOf com exemplos claros;
- discriminator somente quando necessário;
- formatos como anotação que tooling pode ou não validar.

Não crie um schema Item universal. CreateItem, PatchItem, ItemView e ItemEvent
evoluem por motivos diferentes. Composição excessiva torna contrato ilegível e
geração inconsistente.

## 3. Operação completa

Uma operação madura descreve:

- resumo e semântica;
- parâmetros com estilo/encoding;
- requestBody e media types;
- respostas felizes e erros relevantes;
- headers como ETag, Location e Retry-After;
- segurança e scopes;
- idempotência/precondições em texto e exemplos;
- limites e paginação;
- tags, depreciação e links.

Examples precisam validar contra schema. Exemplo incompatível destrói confiança
e pode gerar SDK/teste errado.

## 4. Fluxo contract-first

1. escrever proposta e exemplos de jornadas;
2. modelar operações e problemas;
3. revisar com consumidor, domínio, segurança e operação;
4. validar sintaxe e aplicar lint;
5. gerar mock para testar integração;
6. implementar adapter e domínio;
7. comparar respostas reais com o contrato;
8. fazer diff contra versão publicada;
9. publicar artifact imutável e catálogo.

Contrato aprovado deve ser a entrada do pipeline. Se implementação gera outro
OpenAPI, compare caminhos, métodos, status, media types e schemas para detectar
drift.

## 5. Code-first sem drift

Frameworks geram OpenAPI a partir de tipos, mas não conhecem todas as respostas,
ameaças ou garantias. Complemente anotações e teste o documento gerado. Se existe
spec manual e gerada, uma precisa ser canônica e a outra deve ser comparada.

Não “corrija” o contrato e o código no mesmo commit sem teste que demonstre a
intenção; uma incompatibilidade pode ficar invisível.

## 6. Reuso, referências e bundles

Referências reduzem duplicação, mas arquivos remotos criam disponibilidade e
supply chain. Gere bundle reproduzível, fixe versões e impeça referência a
destino arbitrário. Nomes de componentes fazem parte da ergonomia do SDK.

Evite deep nesting de allOf e ciclos quando geradores suportados divergem.
Teste todas as linguagens prometidas.

## 7. Governança automatizada

Pipeline mínimo:

~~~text
parse -> validate -> lint -> examples -> breaking diff
      -> mock/contract tests -> bundle -> docs/SDK -> publish
~~~

Lint organizacional verifica operationId, nomenclatura, problems, paginação,
segurança e contatos. Exceções precisam de justificativa versionada, não
desabilitação silenciosa.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| spec só para documentação | drift | conformidade no CI |
| resposta 500 omitida | cliente sem contrato | problems comuns |
| examples inválidos | documentação enganosa | validar |
| gerador como fonte de design | domínio ditado pelo framework | revisão primeiro |
| upgrade de versão sem matriz | tooling quebra | compatibilidade |

## Exercícios

### Nível 1 — coleção

Escreva OpenAPI para criar/listar/ler/alterar. **Aceite:** schemas separados,
erros, headers, paginação e segurança existem.

### Nível 2 — conformidade

Valide respostas reais contra o contrato. **Aceite:** alteração de status,
media type ou campo obrigatório falha no teste.

### Nível 3 — evolução

Proponha mudança aditiva e breaking. **Aceite:** diff detecta a segunda, exemplos
e dois SDKs continuam funcionando na primeira.

## Checklist

- [ ] Documento e versão da API não foram confundidos.
- [ ] Schemas representam intenções distintas.
- [ ] Erros e headers fazem parte do contrato.
- [ ] Exemplos são validados.
- [ ] Implementação é comparada ao OpenAPI.
- [ ] Breaking change falha no pipeline.
