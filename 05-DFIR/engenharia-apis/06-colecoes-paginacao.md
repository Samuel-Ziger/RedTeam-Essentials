# 06 — Coleções, filtros, ordenação e paginação

Uma coleção é uma consulta com custo, consistência e ordem. Sem limites, listas
se tornam problema de disponibilidade; sem ordem total, páginas pulam ou repetem
elementos; sem gramática de filtros, o contrato vaza a linguagem do banco.

## Objetivos

- definir consultas públicas seguras e previsíveis;
- escolher offset, cursor ou keyset conscientemente;
- construir ordem total e cursor opaco;
- tratar mutações concorrentes e consistência;
- testar limites, filtros, projeção e navegação.

## 1. Contrato da coleção

Toda coleção deve responder:

- qual conjunto o chamador pode observar;
- qual ordenação padrão e quais alternativas existem;
- que filtros e combinações são permitidos;
- limites padrão/máximo e custo;
- como navegar adiante ou atrás;
- qual garantia existe durante mutações concorrentes;
- se totalCount é exato, aproximado ou ausente.

~~~json
{
  "items": [],
  "page": {
    "limit": 20,
    "next": "opaque-token",
    "hasMore": true
  },
  "links": {
    "self": "/v1/items?limit=20"
  }
}
~~~

O envelope permite evoluir metadados sem trocar a lista por objeto depois.

## 2. Offset e cursor

Offset é simples e permite salto:

~~~text
GET /v1/items?offset=100&limit=20
~~~

Em conjuntos grandes, o banco pode percorrer linhas anteriores. Inserções ou
remoções antes do offset deslocam páginas, causando duplicidade ou omissão.

Keyset usa o último valor ordenado:

~~~sql
WHERE (created_at, item_id) > (:created_at, :item_id)
ORDER BY created_at, item_id
LIMIT :limit_plus_one
~~~

O desempate por item_id cria ordem total. O cursor carrega essa posição de modo
opaco. Keyset navega com estabilidade e custo previsível, mas salto arbitrário e
ordenações livres ficam mais difíceis.

## 3. Cursor opaco e vinculado à consulta

Base64 não torna um cursor confiável. O token deve ter versão, posição, filtros
relevantes e expiração quando necessária; uma assinatura impede adulteração.

~~~json
{
  "v": 1,
  "last": ["2026-10-05T10:00:00Z", "itm_42"],
  "filter": "status=active"
}
~~~

Valide tamanho antes de decodificar, assinatura em tempo constante, schema e
intervalos. Um cursor de status=active não pode ser reutilizado em archived.
Erros retornam código estável, sem revelar chave ou documento interno.

Cursor opaco não é credencial. Autorização continua sendo aplicada em cada
consulta. A assinatura protege integridade, não confidencialidade; não coloque
PII no token se o cliente pode decodificá-lo.

## 4. Mutações durante a navegação

Sem snapshot, a coleção reflete estado por página. Com ordem por criação
imutável, itens novos posteriores podem aparecer; alterações de filtro podem
remover um item entre páginas. Declare essa garantia.

Alternativas:

- snapshot no banco por transação curta;
- snapshot lógico com asOf ou versão máxima;
- cursor com watermark;
- aceitar leitura em movimento e deduplicar no consumidor.

Snapshot longo consome recurso. Não prometa consistência perfeita sem medir o
custo.

## 5. Filtros e ordenação

Não passe expressões livres ao ORM/SQL. Defina uma gramática:

~~~text
status = active | archived
createdAfter = timestamp RFC 3339
sort = createdAt | -createdAt
~~~

Mapeie nomes públicos para campos internos. Limite quantidade de filtros, tamanho
de busca e combinações caras. Busca textual tem tokenização, idioma e ranking;
não trate como igualdade simples.

Ordenação precisa de desempate único. Se o cliente escolhe title, acrescente
item_id. Defina onde null aparece e como collation trata maiúsculas/acentos.

## 6. Projeção e total

fields pode reduzir bytes, mas multiplica formas de cache, autorização e testes.
Nunca permita solicitar propriedade proibida. totalCount pode exigir consulta
cara e variar enquanto páginas são percorridas. Se aproximado, use nome e
documentação explícitos.

Para exportar milhões de itens, não aumente limit: crie job de exportação com
arquivo, expiração e controle de acesso.

## Falhas comuns

| Falha | Sintoma | Correção |
|---|---|---|
| ordem sem desempate | itens repetidos/sumidos | chave total |
| cursor base64 confiado | posição adulterada | schema + assinatura |
| filtro vira SQL | injeção/acoplamento | allowlist e tradução |
| total obrigatório | latência cresce | opcional/aproximado |
| sem limite máximo | exaustão | teto server-side |
| cursor entre filtros | resultados incoerentes | vincular consulta |

## Exercícios

### Nível 1 — keyset

Implemente paginação por created_at e id. **Aceite:** itens com timestamp igual
não somem nem repetem.

### Nível 2 — token

Assine cursor com versão e filtro. **Aceite:** adulteração, tamanho excessivo,
versão desconhecida e filtro diferente recebem erro seguro.

### Nível 3 — concorrência

Insira, remova e altere filtro durante a navegação. **Aceite:** documente a
garantia observada e escolha consciente entre snapshot e coleção móvel.

## Checklist

- [ ] Existe ordem total e limite máximo.
- [ ] Cursor é opaco, validado e vinculado à consulta.
- [ ] Autorização é aplicada em toda página.
- [ ] Filtros são uma gramática permitida.
- [ ] totalCount não cria promessa falsa.
- [ ] Mutações concorrentes têm semântica documentada.

