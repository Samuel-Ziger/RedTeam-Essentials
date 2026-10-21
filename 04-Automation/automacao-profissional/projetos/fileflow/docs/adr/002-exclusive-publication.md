# ADR 002 — Publicação exclusiva

## Status

Aceita para o laboratório local.

## Contexto

Replace atômico evita arquivo parcial, mas sobrescreve um destino que surgiu entre
planejamento e execução.

## Decisão

Copiar para temporário no diretório alvo, validar SHA-256 e publicar por criação
exclusiva via hard link. Se o destino surgiu, preservar e retornar conflito.

## Consequências

O filesystem precisa suportar hard links. A operação não preserva metadados da
origem. Suporte multiplataforma mais amplo exigiria adapter com primitiva exclusiva
equivalente e testes por plataforma.

