# 02 — Firewalls L3/L4 e estado

Um firewall de rede decide com base em campos como família IP, origem, destino,
protocolo, portas, interface, direção e estado da conexão. Ele não substitui
autenticação nem entende, por si só, a autorização de um objeto em uma API.

## Stateless e stateful

Filtro stateless avalia cada pacote isoladamente. O stateful acompanha fluxos e
pode permitir respostas de conexões estabelecidas sem abrir a mesma porta para
novas conexões externas. A tabela de estado consome recursos: exaustão e timeouts
fazem parte do modelo de disponibilidade.

Uma política conceitual de servidor web é:

```text
entrada:  negar por padrão
          permitir conexões estabelecidas/relacionadas
          permitir HTTPS somente da camada de borda
saída:    negar por padrão, liberar DNS/NTP/update e dependências declaradas
gestão:   permitir somente da rede administrativa autenticada
```

NAT traduz endereços; não é controle de acesso. ACL sem estado pode ser correta
em um roteador, mas precisa representar explicitamente os dois sentidos.

## Teste Purple

Red cria uma matriz de origem, destino, protocolo, porta e resultado esperado.
Blue compara a matriz com regra efetiva, contador e log. Teste pelo menos:

- caminho permitido, resposta e conexão renovada;
- porta adjacente negada;
- IPv4 e IPv6;
- tráfego administrativo fora da origem aprovada;
- retorno após reinício e após expirar o estado.

Não use um scanner de Internet para isso. Fixtures, namespaces ou VMs locais
são suficientes. O resultado deve citar a regra e provar que a persistência é
igual à configuração versionada.

## Falhas comuns

Ordem incorreta, `any/any`, IPv6 esquecido, regra temporária sem expiração,
interface errada e administração exposta. Uma regra bloqueando não prova que
outra rota, IP ou balanceador não contorna o controle.
