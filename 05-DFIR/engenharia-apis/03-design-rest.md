# 03 — Design REST orientado a recursos

Em uma API orientada a recursos, a URI identifica algo do domínio, o método
expressa intenção e a representação descreve estado visível. O objetivo não é
eliminar verbos da linguagem, mas estabilizar o contrato ao redor de identidades,
coleções e transições.

## Objetivos

- descobrir recursos a partir do domínio;
- modelar coleções, relações, ações e trabalhos demorados;
- definir transições e invariantes antes das rotas;
- separar identidade pública de chave física;
- desenhar URLs previsíveis sem vazar armazenamento.

## 1. Recurso, representação e comando

Um recurso possui identidade conceitual. Pode ser entidade persistida, coleção,
relação, configuração ou processo:

~~~text
/v1/projects
/v1/projects/{project_id}
/v1/projects/{project_id}/memberships
/v1/exports/{export_id}
~~~

Representação é uma visão serializada do recurso em um instante. Ela pode omitir
campos por autorização ou projeção. Comando é a intenção enviada pelo cliente.
CreateProject e ProjectView não precisam ter o mesmo schema: ID, versão e datas
são gerados pelo servidor; segredo de entrada não deve reaparecer na saída.

## 2. Descoberta pelo domínio

Comece com vocabulário, invariantes e ciclo de vida. Para biblioteca:

- obra descreve conteúdo intelectual;
- cópia é exemplar físico ou licença;
- membro pode reservar;
- empréstimo liga membro e cópia por período;
- devolução é transição do empréstimo, não exclusão do histórico.

Se tudo vira books, o modelo perde identidades relevantes. Rotas devem refletir
o que o consumidor precisa manipular, não joins internos.

## 3. Coleções e membros

Coleção oferece criação, busca e paginação. Membro oferece leitura ou mudança
específica:

~~~http
POST /v1/projects
GET /v1/projects?status=active&limit=20
GET /v1/projects/prj_123
PATCH /v1/projects/prj_123
~~~

Use substantivos estáveis, plural consistente e IDs opacos. Não codifique e-mail
ou dado mutável na URI. Relação aninhada é útil quando o pai define o escopo,
mas profundidade excessiva aumenta acoplamento. Muitas vezes
/memberships/{id} é melhor que uma árvore de cinco níveis.

## 4. Ações e processos longos

Nem toda intenção é CRUD. Se uma ação possui identidade, progresso, resultado ou
cancelamento, modele-a como recurso:

~~~http
POST /v1/exports
Location: /v1/exports/exp_01

GET /v1/exports/exp_01
~~~

~~~json
{
  "id": "exp_01",
  "state": "running",
  "progress": {"completed": 20, "total": 100}
}
~~~

Uma ação instantânea específica pode usar subrecurso ou endpoint de comando,
desde que a semântica seja clara. Evite /execute com campo action porque ele
remove descoberta, autorização por operação e observabilidade.

## 5. Estado e transições

Modele a máquina de estados:

~~~text
draft --publish--> active --archive--> archived
  |                    |
  +-----delete---------+
~~~

Para cada transição, defina precondição, ator, efeito, evento e erro. Se archived
não volta a active, o servidor rejeita; o cliente não deve inferir isso de um
botão desabilitado. Use versão ou ETag para impedir que duas transições baseadas
no mesmo estado se sobrescrevam.

## 6. PUT, PATCH e exclusão

PUT substitui a representação definida no alvo; campos omitidos têm semântica
contratada. PATCH aplica um documento de mudança. JSON Merge Patch trata null
como remoção; JSON Patch descreve operações em caminhos. Um objeto parcial
customizado também é possível, mas documente ausência versus null.

DELETE costuma remover associação ou tornar recurso inacessível. Repeti-lo deve
manter o efeito desejado, mas a resposta pode ser 204 na primeira vez e 404
depois, conforme contrato. Em domínios regulados, “excluir” pode significar
solicitar workflow, anonimizar e preservar evidência mínima.

## 7. Links e descoberta

Links podem indicar recursos relacionados e transições:

~~~json
{
  "id": "exp_01",
  "state": "completed",
  "links": {
    "self": "/v1/exports/exp_01",
    "download": "/v1/exports/exp_01/content"
  }
}
~~~

Isso reduz URLs montadas manualmente. Links não substituem documentação nem
autorização, mas ajudam evolução de localização.

## 8. Identificadores

IDs devem ser estáveis, opacos e validados por comprimento/alfabeto. Sequências
previsíveis não são falha de autorização se toda leitura valida ownership, mas
podem vazar volume. UUID/ULID não eliminam BOLA. Nunca confie em segredo do ID
para proteger objeto.

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| rota espelha tabela | migração quebra contrato | modelar domínio |
| verbo genérico execute | política e métricas opacas | operação/recurso específico |
| PATCH sem semântica | null apaga inesperadamente | declarar formato |
| job 202 sem identidade | consumidor não reconcilia | recurso de operação |
| IDs tratados como autorização | acesso cruzado | política por objeto |

## Exercícios

### Nível 1 — biblioteca

Modele obras, cópias, reservas e empréstimos. **Aceite:** identidade, coleção,
representação, comando e transição estão separados.

### Nível 2 — exportação

Projete criação, consulta, cancelamento e obtenção de uma exportação. **Aceite:**
há 202/201 justificado, Location, estados terminais e idempotência.

### Nível 3 — concorrência

Implemente duas atualizações concorrentes sobre a mesma versão. **Aceite:** uma
é aceita, outra recebe 412 e nenhum campo é perdido.

## Checklist

- [ ] Recursos vêm do domínio, não das tabelas.
- [ ] IDs são opacos e não substituem autorização.
- [ ] Coleções têm limite e ordem.
- [ ] Operações longas possuem recurso consultável.
- [ ] PATCH e null têm semântica explícita.
- [ ] Transições, precondições e erros estão documentados.

