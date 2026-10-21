# Laboratório P01 — integração final

Use os requisitos e a rubrica de [Projeto final](../30-projeto-final.md).

## Fases

1. **Design:** requisitos, diagrama, ameaças, RPO/RTO e decisões.
2. **Build:** instalação, contas, armazenamento, rede e serviço.
3. **Operate:** logs, métricas, alertas, atualização e runbooks.
4. **Break:** três falhas sintéticas sorteadas.
5. **Recover:** diagnóstico, rollback e restore cronometrados.
6. **Defend:** apresentação oral e revisão por outro aluno.

## Gate de cada fase

Não avance se:

- há segredo no Git;
- backup ainda não foi restaurado;
- SSH é o único acesso e não há console;
- a mudança não tem rollback;
- um comando destrutivo usa glob/variável não validada;
- o serviço roda como root sem requisito documentado;
- logs contêm dados pessoais ou credenciais;
- o healthcheck não prova comportamento relevante.

## Revisão por pares

O revisor recebe apenas README e runbooks e tenta:

1. reproduzir o ambiente;
2. encontrar o serviço e sua configuração efetiva;
3. interpretar um alerta;
4. executar rollback;
5. restaurar em caminho vazio.

Toda pergunta necessária que não esteja documentada vira melhoria do projeto.
