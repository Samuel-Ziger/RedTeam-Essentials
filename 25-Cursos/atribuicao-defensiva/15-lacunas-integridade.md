# 15 — Lacunas, integridade e anti-tamper

Ausência de log tem quatro explicações comuns: o evento não ocorreu, a fonte não
coleta, o pipeline falhou ou alguém interferiu. A investigação precisa separar
essas hipóteses.

## Saúde do pipeline

- heartbeat por fonte;
- último evento e atraso de ingestão;
- sequência/contador quando disponível;
- volume por intervalo e tipo;
- erro de parsing e mudança de schema;
- fila, disco e conectividade do agente;
- alterações de configuração e versão.

## Integridade

Use transporte autenticado, armazenamento com acesso restrito, retenção
protegida, hash/assinatura quando o processo exigir e cópia em domínio
administrativo separado. Hash prova que um arquivo não mudou desde o cálculo,
não que sua origem seja verdadeira.

## Imutabilidade

WORM/object lock reduz alteração, mas exige política de retenção, custo e acesso
break-glass. Administrador único com permissão em origem e arquivo central
continua um risco.

## Lacunas esperadas

Manutenção, suspensão de laptop e perda de rede precisam de estados explícitos.
Baseline por classe de ativo evita alertar como ataque todo equipamento offline.

## Prática

Crie três gaps sintéticos e a evidência que diferenciaria falha, manutenção e
interferência.

