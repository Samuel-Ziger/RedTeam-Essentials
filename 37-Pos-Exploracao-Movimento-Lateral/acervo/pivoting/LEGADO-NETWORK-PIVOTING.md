# Acervo legado — pivoting e segmentação

O módulo 21 agora contém Criptografia III. O analisador offline e sua fixture
continuam disponíveis para compatibilidade:

```bash
python3 37-Pos-Exploracao-Movimento-Lateral/acervo/pivoting/path_analyzer.py \
  37-Pos-Exploracao-Movimento-Lateral/acervo/pivoting/fixtures/topology.json operator database 5432
```

O analisador considera somente arestas e portas declaradas, não abre sockets e
não descobre hosts. Qualquer prática real continua restrita a redes próprias ou
formalmente autorizadas, com allowlist e teardown documentados.

## Conceitos e operação preservados

- pivot é um host autorizado entre zonas explicitamente incluídas no RoE;
- port forwarding reduz a superfície a uma porta;
- proxy SOCKS exige allowlist para não sair do escopo;
- túnel encapsula tráfego, mas criptografia não concede autorização;
- roteamento depende de ida, volta, ACLs, NAT e resolução coerentes.

O plano registra origem, intermediário, destino, porta, janela, responsável,
processo e remoção. Detecção correlaciona conexão de entrada/saída, processo,
DNS/proxy e fluxo. Cleanup encerra processos, routes/listeners e a rede de lab.

---

## Registro histórico integral

> A seção abaixo conserva o conteúdo substantivo do README anterior, com seus
> contratos, sequência, referências e avisos éticos. Ela é um registro de
> preservação e não substitui o currículo atual descrito no [README do módulo 37](../../README.md).

> Planejamento e validação de caminhos de rede em topologias sintéticas ou labs
> isolados. Não use túneis, proxies ou scans contra redes de terceiros.

## Histórico — Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários de redes e pós-exploração. |
| Pré-requisitos | Módulos 00, 01, 14 e 20; roteamento e TCP/IP. |
| Tempo estimado | 6 horas de teoria e 4 horas de análise offline. |
| Ambiente | Fixture versionada ou rede Docker/VM inteiramente própria. |
| Evidência final | Caminho mínimo, regras necessárias, riscos e plano de teardown. |
| Critério de conclusão | Encontrar rotas permitidas/bloqueadas sem tocar rede externa. |

## Histórico — Conceitos

- **Pivot:** host autorizado usado como ponto intermediário para alcançar outra
  zona explicitamente incluída no RoE.
- **Port forwarding:** encaminha uma porta específica; reduz superfície quando
  comparado a acesso amplo.
- **Proxy SOCKS:** permite que ferramentas compatíveis escolham destinos, mas
  aumenta o risco de sair do escopo se não houver allowlist.
- **Túnel:** encapsula tráfego entre pontos; criptografia não concede autorização.
- **Roteamento:** exige caminho de ida e volta, ACLs, NAT e resolução coerentes.

## Histórico — Lab offline

Use [`fixtures/topology.json`](fixtures/topology.json) e execute:

```bash
python3 37-Pos-Exploracao-Movimento-Lateral/acervo/pivoting/path_analyzer.py \
  37-Pos-Exploracao-Movimento-Lateral/acervo/pivoting/fixtures/topology.json operator database 5432
```

O analisador considera somente arestas e portas declaradas. Ele não abre sockets
nem descobre hosts. Compare um caminho permitido até `database:5432` com uma
tentativa bloqueada até `management:3389`.

## Histórico — Planejamento operacional

Antes de um pivot real em lab, registre origem, intermediário, destino, porta,
janela, responsável, processo criado e comando de remoção. Restrinja listeners a
localhost ou interfaces de lab e valide o destino com o scope guard do módulo 20.

## Histórico — Telemetria e detecção

Correlacione conexão de entrada e saída no pivot, criação do processo, DNS/proxy
e fluxo de rede. Administração legítima e healthchecks são falsos positivos
comuns; use identidade, janela e destino para contexto.

## Histórico — Cleanup

Encerre processos, remova routes/listeners temporários, valide portas abertas,
destrua a rede de lab e anexe a confirmação à kill list.

## Histórico — Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [COMO OS PENTESTERS INVADAM REDES INTERNAS COM PIVOTING (DO ZERO AO AVANÇADO)](https://www.youtube.com/watch?v=Lbrn4H7a5wA) — **Cybersegurançanapratica**.
2. [Aula 13 - Pivoting - Comprometendo toda a rede](https://www.youtube.com/watch?v=DhEDUzVO88k) — **Solyd Offensive Security**.
3. [[Aula Pentest] - Tunelamento com socat](https://www.youtube.com/watch?v=_WKiZr5ZF6k) — **Ricardo Longatto**.
4. [Pivoting - De uma simples shell ao servidor principal](https://www.youtube.com/watch?v=kJ7-6qukgM8) — **Ricardo Longatto**.
5. [Aula 11 - Pivoting em redes - Introdução ao Hacking e Pentest - Solyd](https://www.youtube.com/watch?v=FBr-1R8lz_0) — **Solyd Offensive Security**.
