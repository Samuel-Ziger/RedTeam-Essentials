# Lab 02 — Arquivos, permissões e metadados

## Objetivo

Prever e comprovar acesso usando mode bits, ACL, flags e xattrs em fixture.

## Procedimento

1. Crie arquivos sem segredo com modos `600`, `640` e `644`.
2. Registre `ls -leO@` e `stat -x` antes de qualquer alteração.
3. Adicione um atributo `com.example.rte-note` e releia seu valor.
4. Crie uma ACL somente na fixture, teste e remova a regra específica.
5. Compare permissão Unix, ACL e atributo; não confunda seus papéis.

## Critério

A matriz explica owner, grupo, others, regras adicionais e resultado real. O
cleanup restaura modos e remove somente objetos criados no lab.
