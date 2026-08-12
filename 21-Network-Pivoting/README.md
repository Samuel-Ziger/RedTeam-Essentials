# 21 - Pivoting e segmentação de redes

> Planejamento e validação de caminhos de rede em topologias sintéticas ou labs
> isolados. Não use túneis, proxies ou scans contra redes de terceiros.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários de redes e pós-exploração. |
| Pré-requisitos | Módulos 00, 01, 14 e 20; roteamento e TCP/IP. |
| Tempo estimado | 6 horas de teoria e 4 horas de análise offline. |
| Ambiente | Fixture versionada ou rede Docker/VM inteiramente própria. |
| Evidência final | Caminho mínimo, regras necessárias, riscos e plano de teardown. |
| Critério de conclusão | Encontrar rotas permitidas/bloqueadas sem tocar rede externa. |

## Conceitos

- **Pivot:** host autorizado usado como ponto intermediário para alcançar outra
  zona explicitamente incluída no RoE.
- **Port forwarding:** encaminha uma porta específica; reduz superfície quando
  comparado a acesso amplo.
- **Proxy SOCKS:** permite que ferramentas compatíveis escolham destinos, mas
  aumenta o risco de sair do escopo se não houver allowlist.
- **Túnel:** encapsula tráfego entre pontos; criptografia não concede autorização.
- **Roteamento:** exige caminho de ida e volta, ACLs, NAT e resolução coerentes.

## Lab offline

Use [`fixtures/topology.json`](fixtures/topology.json) e execute:

```bash
python3 21-Network-Pivoting/path_analyzer.py \
  21-Network-Pivoting/fixtures/topology.json operator database 5432
```

O analisador considera somente arestas e portas declaradas. Ele não abre sockets
nem descobre hosts. Compare um caminho permitido até `database:5432` com uma
tentativa bloqueada até `management:3389`.

## Planejamento operacional

Antes de um pivot real em lab, registre origem, intermediário, destino, porta,
janela, responsável, processo criado e comando de remoção. Restrinja listeners a
localhost ou interfaces de lab e valide o destino com o scope guard do módulo 20.

## Telemetria e detecção

Correlacione conexão de entrada e saída no pivot, criação do processo, DNS/proxy
e fluxo de rede. Administração legítima e healthchecks são falsos positivos
comuns; use identidade, janela e destino para contexto.

## Cleanup

Encerre processos, remova routes/listeners temporários, valide portas abertas,
destrua a rede de lab e anexe a confirmação à kill list.

