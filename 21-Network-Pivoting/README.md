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

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [COMO OS PENTESTERS INVADAM REDES INTERNAS COM PIVOTING (DO ZERO AO AVANÇADO)](https://www.youtube.com/watch?v=Lbrn4H7a5wA) — **Cybersegurançanapratica**.
2. [Aula 13 - Pivoting - Comprometendo toda a rede](https://www.youtube.com/watch?v=DhEDUzVO88k) — **Solyd Offensive Security**.
3. [[Aula Pentest] - Tunelamento com socat](https://www.youtube.com/watch?v=_WKiZr5ZF6k) — **Ricardo Longatto**.
4. [Pivoting - De uma simples shell ao servidor principal](https://www.youtube.com/watch?v=kJ7-6qukgM8) — **Ricardo Longatto**.
5. [Aula 11 - Pivoting em redes - Introdução ao Hacking e Pentest - Solyd](https://www.youtube.com/watch?v=FBr-1R8lz_0) — **Solyd Offensive Security**.
