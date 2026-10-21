# 02 — Windows Enterprise, LTSC e lifecycle

Windows Enterprise adiciona capacidades de gestão/segurança e direitos definidos
por licenciamento. LTSC atende dispositivos/workloads especializados estáveis;
não é atalho universal para evitar feature updates.

## Catálogo de plataforma

Para cada SKU/build registre:

- caso de uso e owner;
- canal, release, fim de servicing;
- hardware/firmware e drivers aprovados;
- aplicativos críticos e compatibilidade;
- baseline/políticas aplicáveis;
- rota de upgrade e rollback;
- critério de exceção/aposentadoria.

## Servidor

Windows Server LTSC possui ciclo e features próprios. In-place upgrade pode ser
suportado entre caminhos específicos, mas rebuild/migração frequentemente reduz
estado histórico. Escolha por workload, não por conveniência.

## Exercício

Crie uma matriz de lifecycle de três perfis fictícios usando somente datas e
documentação oficial atuais. Defina alerta 18/12/6 meses antes do fim.

