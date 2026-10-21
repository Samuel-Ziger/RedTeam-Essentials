# Laboratório 02 — Pipeline, HTTP fake, job e checkpoint

## Objetivo

Evoluir a ferramenta para ingerir um catálogo JSON paginado de um servidor fake,
validar registros e gerar um plano local retomável.

## Contrato

O fake oferece páginas com cursor e fixtures para 200 válido, HTML em 200, JSON
truncado, corpo excessivo, cursor repetido, 429 e 503. Nenhuma Internet pública é
necessária.

Cada registro possui recordId, relativePath, expectedSha256 e schemaVersion. O job
processa uma janela lógica fornecida pela CLI.

## Etapa A — adapter HTTP

Implemente timeout, limite de corpo, Content-Type, schema, maxPages e detecção de
cursor cíclico. Traduza o formato externo para tipo interno.

## Etapa B — pipeline

Separe bytes, decode, parse, schema, regra e plano. Escolha fail-fast ou quarentena
e justifique. Reconcilie recebidos, aceitos, rejeitados e duplicados.

## Etapa C — job

Modele scheduled, running, succeeded, partial, failed e cancelled. A chave usa
jobId + janela + digest da entrada, nunca run ID.

## Etapa D — checkpoint

Persista somente após efeito confirmado. Falhe antes e depois do item 51 e retome.
Se a regra/config mudou, recuse o checkpoint antigo.

## Testes e aceite

- todas as respostas anômalas do fake são classificadas;
- cursor repetido termina sem loop;
- contagens fecham;
- mesma janela duplicada não repete efeito;
- checkpoint nunca salta item não confirmado;
- falha após commit é resolvida por idempotência;
- manifesto informa schema, janela e digest.

## Evidência

Entregue state diagram, fixtures, transcrição da retomada e ADR sobre atomicidade
ou quarentena.

