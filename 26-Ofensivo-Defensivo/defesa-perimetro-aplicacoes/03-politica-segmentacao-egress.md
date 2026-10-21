# 03 — Política, segmentação e egress

Política boa descreve intenção antes da sintaxe. Use origem, destino, serviço,
identidade quando disponível, motivo, owner, ticket e expiração. Gere a regra
específica do produto somente depois.

## Zonas e caminhos

Separe borda, aplicação, dados, gestão, build e observabilidade. Não confie em
"rede interna" como identidade. Microsegmentação limita movimento e reduz o
raio de impacto, mas aumenta custo de inventário e troubleshooting.

```yaml
from: edge
to: app-api
service: https
port: 8443
decision: allow
reason: "encaminhamento do proxy"
owner: plataforma
expires: null
logging: accept-and-deny
```

## Saída também é superfície

Egress irrestrito facilita dependências ocultas e amplia incidentes. Modele
DNS, NTP, repositórios, APIs externas, e-mail, storage e telemetria. Prefira
destinos intermediados e identidades de workload quando endereços são
dinâmicos. Defina o que acontece quando uma dependência muda.

## Mudança segura

1. observar fluxo legítimo por janela representativa;
2. criar política como código e revisar;
3. aplicar em modo de log/simulação quando suportado;
4. testar canário e rollback;
5. negar e monitorar impacto;
6. remover exceções vencidas.

## Exercício Purple

Red identifica três comunicações que a aplicação não deveria iniciar. Blue
consulta a matriz, simula negação e define alerta apenas para eventos acionáveis.
Purple registra dependências descobertas; não cria exceção silenciosa para
"fazer funcionar".
