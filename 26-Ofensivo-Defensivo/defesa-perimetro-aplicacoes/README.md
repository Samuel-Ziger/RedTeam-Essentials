# Defesa de perímetro e aplicações — Purple Team

Este curso liga rede, HTTP, aplicação, identidade e operação. A pergunta não é
"qual regra bloqueia tudo?", mas "qual risco estamos reduzindo, que evidência
prova isso e como evitamos interromper usuários legítimos?".

## Ciclo usado em todos os laboratórios

```text
autoridade e hipótese
        ↓
baseline → teste negativo local → telemetria → diagnóstico
   ↑                                           ↓
reteste ← mudança versionada ← tuning + rollback
```

O papel Red produz requisições sintéticas ou usa um serviço local autorizado.
O papel Blue mede cobertura, falso positivo, latência e disponibilidade. O
facilitador Purple transforma o aprendizado em requisito e teste de regressão.

## Competências ofensivas autorizadas

Ao final, o aluno consegue revisar superfície de borda, construir uma matriz de
conectividade negativa, validar proteção da origem, criar casos de regressão
para WAF/CRS, emular jornadas automatizadas com fixtures, testar fronteiras de
rate limit e avaliar lógica de challenge/MFA. Cada achado inclui evidência,
impacto, limitação, recomendação e reteste.

## Competências defensivas

O aluno também consegue definir políticas default deny, implantar em modo de
detecção/canário, correlacionar edge e origem, ajustar falsos positivos,
proteger o plano administrativo, responder a abuso e restaurar uma versão
conhecida. Disponibilidade, acessibilidade e privacidade fazem parte do aceite.

## Sequência

Estude os capítulos 00–06 antes de alterar qualquer controle. Os capítulos
07–12 cobrem WAFs e fornecedores. Os capítulos 13–18 tratam bots, desafios e
identidade. Os capítulos 19–21 encerram com operação e capstone.

Execute:

```bash
bash testar-curso.sh
```

O teste estrutural, os unitários e as três demonstrações são offline. Para
uma implantação real, use a documentação atual do fornecedor, fixe versões,
proteja segredos e valide rollback em ambiente de homologação.

## Avaliação

- 20% fundamentos e modelo de ameaça;
- 25% qualidade dos testes Purple Team;
- 25% telemetria, tuning e tratamento de falsos positivos;
- 30% projeto final, evidências e comunicação.

Uma resposta só está completa quando separa fato, inferência e limitação.
