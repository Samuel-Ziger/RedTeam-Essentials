# 02 — Estilos de API e decisões

Estilo de API é uma escolha de acoplamento. REST, RPC, GraphQL, gRPC, eventos e
webhooks organizam mensagens, evolução e operação de formas diferentes. Escolher
pela popularidade normalmente desloca o problema para produção.

## Objetivos

- comparar estilos pelas forças do problema;
- separar padrão de interação, codificação e transporte;
- reconhecer custos operacionais e de compatibilidade;
- registrar decisões reversíveis e irreversíveis;
- combinar estilos sem criar duas fontes de verdade.

## 1. Eixos de decisão

Antes de comparar tecnologias, meça:

- quem controla producer e consumer;
- interação síncrona, assíncrona ou streaming;
- direção e frequência das mensagens;
- latência e disponibilidade esperadas;
- volume, tamanho e necessidade de projeção;
- compatibilidade entre versões;
- ferramentas, browsers, gateways e linguagens;
- observabilidade, suporte e experiência da equipe;
- necessidade de cache, replay, ordem e desconexão.

REST sobre HTTP é estilo; JSON é representação; HTTP/2 é transporte. gRPC usa
RPC, contratos Protobuf e geralmente HTTP/2. Eventos podem viajar em broker,
HTTP ou armazenamento. Não confunda essas camadas.

## 2. Matriz de estilos

| Estilo | Unidade pública | Bom ajuste | Custo dominante |
|---|---|---|---|
| REST/HTTP | recurso e representação | APIs externas e CRUD de domínio | disciplina semântica |
| RPC/HTTP | procedimento | comandos explícitos e integrações controladas | acoplamento à operação |
| GraphQL | grafo e seleção | experiências com projeções variadas | custo e autorização por campo |
| gRPC | serviço e mensagem tipada | comunicação interna poliglota | tooling, proxy e deadline |
| eventos | fato imutável | desacoplamento temporal e fan-out | duplicidade, replay e consistência |
| webhook | callback HTTP | notificação entre organizações | entrega, autenticidade e SSRF |
| streaming | sessão e sequência | atualizações contínuas | backpressure e reconexão |

REST não exige CRUD simples. Uma operação longa pode criar recurso job. RPC não
é inferior; pode representar ações de domínio com clareza. O erro é escolher
RPC genérico com payload sem schema e esconder toda semântica em execute.

## 3. Sincronia e acoplamento temporal

Em uma chamada síncrona, consumidor e produtor precisam estar disponíveis no
mesmo intervalo. A resposta imediata simplifica raciocínio, mas propaga latência
e falha. Em eventos, o produtor publica sem esperar cada consumidor; isso reduz
acoplamento temporal, mas adiciona atraso, duplicidade e necessidade de
reconciliação.

“Assíncrono” pode significar duas coisas:

- HTTP retorna 202 e o cliente consulta um job;
- a integração publica mensagem em canal e consumidores processam depois.

São arquiteturas diferentes. O primeiro ainda possui uma API HTTP de controle;
o segundo exige contrato de mensagem, retenção e processamento.

## 4. Tipagem e evolução

OpenAPI, GraphQL SDL e Protobuf oferecem contratos legíveis por máquinas, mas
compatibilidade depende das regras do formato e do comportamento:

- adicionar campo opcional pode quebrar cliente estrito;
- adicionar valor de enum pode quebrar switch exaustivo;
- remover campo Protobuf e reutilizar seu número corrompe interpretação;
- adicionar campo GraphQL é aditivo, mas mudar resolver pode quebrar semântica;
- evento antigo pode ser reproduzido anos depois.

Escolha o estilo cuja política de evolução combina com a vida real dos
consumidores. Contratos internos também precisam de janela de migração quando
deploys não são perfeitamente simultâneos.

## 5. Combinação consciente

Um produto pode oferecer REST externo, gRPC interno e eventos de domínio. Defina
uma fonte de verdade e traduções explícitas:

~~~text
comando REST -> caso de uso -> transação + outbox
                              |
                              +-> evento publicado
consulta REST <- modelo de leitura atualizado
~~~

Não permita que REST e consumidor de evento alterem o mesmo invariante por
caminhos divergentes. Toda borda precisa compartilhar política de autorização e
identidade sem compartilhar acidentalmente modelos de transporte.

## 6. Registro de decisão

Uma ADR curta contém:

~~~text
Contexto e forças:
Alternativas:
Decisão:
Consequências positivas:
Consequências negativas:
Hipóteses:
Sinal de revisão:
Plano de migração:
~~~

Uma matriz ponderada ajuda, mas não transforma hipótese em fato. Registre a
fonte da nota e faça prova de conceito para as maiores incertezas: proxy suporta
stream? geração de SDK preserva ergonomia? custo GraphQL cabe no orçamento?

## 7. Exemplo de decisão

Para catálogo público, REST/JSON pode ganhar por acessibilidade, cache e
ferramentas. Para busca de várias telas próprias, GraphQL pode reduzir
overfetching. Para cálculo interno de baixa latência sob controle da organização,
gRPC pode oferecer tipagem e deadline. Para notificar parceiros, webhook é mais
viável que exigir acesso ao broker.

Nenhuma conclusão é universal. Se o consumidor é browser legado, se proxy não
suporta HTTP/2 ou se replay regulatório é necessário, a pontuação muda.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| tecnologia antes do problema | custo sem benefício | mapear forças |
| evento usado como RPC | timeout e correlação improvisados | comando/resposta explícitos |
| GraphQL para esconder domínio ruim | resolvers acoplados | corrigir ownership |
| dois estilos escrevem sem coordenação | invariantes divergentes | caso de uso comum |
| ADR sem hipótese revisável | decisão nunca reavaliada | definir sinal |

## Exercícios

### Nível 1 — matriz

Compare REST, gRPC e evento para catálogo, pagamento e notificação. **Aceite:**
use ao menos oito critérios e registre incertezas.

### Nível 2 — combinação

Projete API síncrona que publica evento. **Aceite:** transação, outbox,
duplicidade, fonte de verdade e autorização estão definidas.

### Nível 3 — prova de conceito

Escolha a maior hipótese da matriz e construa experimento mensurável. **Aceite:**
há critério antes do teste, dados coletados e ADR atualizada.

## Checklist

- [ ] Interação e consumidores orientam o estilo.
- [ ] Transporte, codificação e padrão não foram confundidos.
- [ ] Evolução e operação entram na decisão.
- [ ] Combinação possui uma fonte de verdade.
- [ ] Hipóteses críticas foram testadas.
- [ ] ADR registra custo, migração e sinal de revisão.

