# Contract Lab API

API local de referência para praticar contrato, implementação, falha e operação.
O domínio é uma coleção fictícia de itens; dados vivem em memória e desaparecem
ao encerrar o processo.

## Controles demonstrados

- modelos estritos e limites de entrada;
- Problem Details RFC 9457 com código e request ID;
- identidade fictícia e autorização no caso de uso;
- isolamento entre tenants;
- cursor opaco, assinado e vinculado ao filtro;
- Idempotency-Key e sinalização de replay;
- ETag, If-None-Match e If-Match;
- máquina de estados que impede reativar item arquivado;
- outbox de eventos em memória;
- assinatura HMAC e proteção local contra replay;
- request ID no header, problema e log JSON;
- OpenAPI-fonte comparado às operações do runtime;
- relógio e geradores de ID injetáveis.

## Limite de identidade

X-Lab-Actor, X-Lab-Tenant e X-Lab-Role apenas injetam uma identidade sintética.
Qualquer cliente pode falsificá-los; nunca use esse mecanismo em produção. Um
sistema real valida credencial em IdP e deriva principal, tenant e papéis.

## Instalação isolada

~~~bash
cd 05-DFIR/engenharia-apis/projetos/contract-lab-api
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
pytest -q
uvicorn contract_lab.api:app --host 127.0.0.1 --port 8000
~~~

Não publique o servidor de desenvolvimento na Internet.

## Chamada local

~~~bash
curl --fail-with-body http://127.0.0.1:8000/v1/items \
  -H 'X-Lab-Actor: ana' \
  -H 'X-Lab-Tenant: escola' \
  -H 'X-Lab-Role: reader'

curl --fail-with-body -X POST http://127.0.0.1:8000/v1/items \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: demo-001' \
  -H 'X-Lab-Actor: ana' \
  -H 'X-Lab-Tenant: escola' \
  -H 'X-Lab-Role: writer' \
  --data '{"title":"Primeiro item"}'
~~~

A documentação interativa fica em http://127.0.0.1:8000/docs. O
[contrato-fonte](contract/openapi.yaml) está versionado junto ao código.

## Arquitetura

~~~text
api.py -> service.py -> domain.py
              |
              +-> store.py

signatures.py fica isolado como componente do laboratório de webhooks.
~~~

**api.py** traduz HTTP, identidade e problemas. **service.py** coordena
autorização, canonicalização e cursor. **store.py** concentra commit em memória,
idempotência, compare-and-set e outbox sob o mesmo lock. Memória local não
substitui storage transacional ou autenticação de produção.

## Contratos demonstráveis

- repetir POST com mesma chave/comando retorna o item original e marca replay;
- usar a chave com outro comando retorna 409 idempotency-conflict;
- alterar cursor ou usá-lo com outro filtro retorna 400 invalid-cursor;
- If-None-Match atual retorna 304 sem corpo;
- dois PATCH com a mesma ETag fazem somente o primeiro vencer;
- item arquivado não volta a active;
- acessar ID real de outro tenant retorna 404;
- todo Problem possui code e requestId;
- eventos são limitados e visíveis apenas ao writer do tenant.

## Limitações deliberadas

- estado e deduplicação somem ao reiniciar;
- cursor usa segredo constante somente no laboratório;
- headers X-Lab não autenticam;
- outbox não tem dispatcher ou broker;
- replay guard é local, não distribuído;
- health comprova apenas que o processo responde.

Esses limites são pontos de extensão, não recomendações de produção.

## Exercícios

1. Persista item, idempotência e outbox numa transação SQLite.
2. Adicione dispatcher com duplicidade e inbox idempotente.
3. Implemente soft delete com nova ETag e política de retenção.
4. Troque headers sintéticos por fake de validador JWT, sem criar um IdP.
5. Valide respostas reais contra schemas do OpenAPI.
6. Adicione dependência fake lenta e propague deadline/cancelamento.
7. Gere clientes em duas linguagens e execute contrato contra ambos.
