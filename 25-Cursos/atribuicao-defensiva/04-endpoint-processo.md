# 04 — Endpoint e processo

Telemetria de endpoint conecta ação de rede a processo, usuário e árvore de
execução. Fontes incluem criação de processo, login, serviço, script, arquivo,
conexão, alteração de configuração e saúde do agente.

## Campos úteis

- host/device ID estável e hostname histórico;
- usuário, sessão e nível de integridade/privilégio;
- PID e parent PID com horário, pois PIDs são reutilizados;
- caminho, hash, assinatura e origem do arquivo;
- linha de comando com tratamento de segredos;
- destino de rede e processo associado;
- sensor, versão, política e status.

## Limites

Processo com nome legítimo pode ser abusado; nome raro não é automaticamente
malicioso. Linha de comando pode conter dados sensíveis e sofrer truncamento.
EDR ausente cria lacuna, não prova de remoção.

## Correlação

Una processo → conexão → DNS → autenticação → ação de aplicação por IDs e tempo.
Mantenha a direção: um domínio resolvido antes da conexão é apoio, não garantia
de que aquele processo usou a resposta sem dado de endpoint.

## Prática

Na fixture, encontre o processo associado a `req-7f2` e liste evidência que
faltaria para concluir autoria humana.

