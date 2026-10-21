# 00 — Mapa das APIs

Uma API é um contrato observável entre produtores e consumidores. Ela não é a
tela de documentação, a URL ou o framework: é o conjunto de comportamentos que
outras partes podem assumir. Operações, formatos, identidade, autorização,
limites, erros, consistência e política de evolução fazem parte desse conjunto.

## Objetivos

- distinguir interface, implementação, protocolo e produto;
- identificar consumidores, owners, invariantes e limites de confiança;
- escrever uma proposta antes de desenhar endpoints;
- reconhecer garantias verificáveis e promessas vagas;
- conduzir o ciclo de vida da descoberta à retirada.

## 1. Interface pública e implementação privada

O consumidor observa mensagens e efeitos, não classes internas. Trocar o banco
sem mudar o comportamento contratado é uma alteração privada. Renomear um campo,
reduzir um limite, mudar unidade ou devolver um erro diferente é mudança pública,
mesmo que o código pareça pequeno.

~~~text
consumidor -> protocolo -> adapter -> caso de uso -> domínio -> dados
                 ^                                      |
                 +--------- contrato observável <-------+
~~~

Pense em duas fronteiras. Na fronteira sintática, bytes se tornam uma mensagem
válida. Na fronteira semântica, a mensagem expressa uma intenção permitida no
estado atual. Um JSON decodificável pode violar regra de negócio; uma operação
válida pode ser proibida para aquela identidade.

## 2. API como produto

Uma API tem usuários, jornada, suporte, disponibilidade e custo de mudança.
Antes de criar uma rota, responda:

1. Quem consome: aplicação própria, parceiro, pessoa ou serviço?
2. Que decisão ou tarefa o consumidor conclui?
3. Qual estado pertence ao produtor e qual pertence ao consumidor?
4. Quais garantias são necessárias sobre ordem, duplicidade e tempo?
5. Que dados são sensíveis e em que fronteira deixam o domínio?
6. Como o consumidor descobre erro, limite, mudança e retirada?

“Retornar dados do banco” não é um resultado de produto. “Permitir que o
aplicativo mostre pedidos visíveis ao usuário em até dois segundos” é verificável
e já sugere autorização, paginação, latência e frescor.

## 3. Invariantes antes dos endpoints

Invariante é uma condição que precisa permanecer verdadeira. Exemplos:

- um item pertence exatamente a um tenant;
- somente writer altera um item;
- uma chave idempotente não representa dois comandos diferentes;
- a versão cresce em toda alteração aceita;
- evento publicado referencia um estado confirmado.

Transforme cada invariante em prevenção, teste e evidência operacional.

| Invariante | Prevenção | Teste | Evidência |
|---|---|---|---|
| isolamento de tenant | filtro derivado da identidade | acesso cruzado | contador de negações |
| versão monotônica | compare-and-set | corrida concorrente | evento com versão |
| comando único | chave + digest | mesma chave, corpo distinto | conflito registrado |

Sem essa ligação, a frase é intenção arquitetural, não garantia.

## 4. Ciclo de vida

~~~text
necessidade -> modelo -> contrato -> threat model -> revisão
            -> implementação -> conformidade -> publicação
            -> observação -> evolução -> depreciação -> retirada
~~~

API-first expõe decisões no contrato antes de a implementação endurecer.
Code-first deriva a descrição do código e pode ser adequado em protótipos.
Nenhum fluxo elimina revisão com consumidores. O risco do code-first é confundir
anotação do framework com decisão de produto; o risco do API-first é manter uma
especificação bonita que a aplicação não obedece.

O ciclo precisa de gates:

- nenhuma publicação sem owner, versão, classificação e contato;
- nenhuma mudança sem comparação de compatibilidade;
- nenhuma retirada sem inventário de consumidores e telemetria;
- nenhuma garantia sem teste ou observação correspondente.

## 5. Papéis e responsabilidades

- **provider** implementa e sustenta o comportamento;
- **consumer** integra e informa necessidades reais;
- **product owner** prioriza valor e custo de compatibilidade;
- **domain owner** protege linguagem e invariantes;
- **platform team** oferece catálogo, gateway, templates e telemetria;
- **security** modela ameaças e verifica controles;
- **operations** define SLO, alerta, resposta e capacidade.

Responsabilidade compartilhada não significa responsabilidade difusa. Cada API
precisa de um owner final, canal de suporte e prazo de revisão.

## 6. Garantias e não garantias

Um contrato maduro declara também o que não promete:

- paginação oferece ordem estável, mas não snapshot global;
- entrega de evento é ao menos uma vez, portanto pode duplicar;
- resposta 202 confirma aceitação, não conclusão;
- cache pode servir representação ainda fresca dentro do TTL;
- timeout do cliente não prova que o servidor não executou.

Essas frases orientam o consumidor e evitam “garantias por acidente”. Toda
incerteza distribuída precisa de estado consultável, idempotência ou
reconciliação.

## 7. Documento de proposta

Antes de OpenAPI, escreva uma página:

~~~text
Problema:
Consumidores e jornada:
Owner e suporte:
Recursos e invariantes:
Dados e classificação:
Operações críticas:
Garantias e não garantias:
Identidade e autorização:
Limites e abuso:
SLO:
Evolução e retirada:
Alternativas rejeitadas:
~~~

O objetivo não é burocracia; é revelar desacordo barato. Se ninguém consegue
definir a unidade de idempotência ou quem possui o dado, endpoints só escondem a
incerteza.

## Falhas comuns

| Falha | Sintoma | Correção |
|---|---|---|
| tabela vira recurso diretamente | contrato muda com migração interna | modelar linguagem do domínio |
| sucesso é apenas HTTP 200 | consumidor não sabe efeito real | definir pós-condição |
| owner ausente | incidentes e migrações sem decisão | registrar responsabilidade |
| contrato descreve só caso feliz | clientes adivinham retry | catalogar falhas |
| API “interna” sem política | acoplamento invisível cresce | tratar todo consumidor como real |

## Exercícios

### Nível 1 — mapa

Escolha uma aplicação e identifique consumidor, produtor, estado, cinco
operações e cinco falhas. **Aceite:** cada operação possui intenção e
pós-condição; não há endpoints ainda.

### Nível 2 — invariantes

Escreva oito invariantes e ligue cada um a prevenção, teste e evidência.
**Aceite:** pelo menos dois cobrem concorrência ou duplicidade e dois cobrem
autorização.

### Nível 3 — proposta

Produza a proposta de uma API e faça revisão como consumidor, operador e equipe
de segurança. **Aceite:** registre três conflitos, decisão tomada e sinal que
faria reavaliá-la.

## Checklist

- [ ] Consumidores e tarefas estão nomeados.
- [ ] Estado e ownership têm fronteiras explícitas.
- [ ] Invariantes possuem prova, não apenas descrição.
- [ ] Garantias e não garantias estão documentadas.
- [ ] Owner, suporte, SLO e ciclo de vida existem.
- [ ] O contrato não replica acidentalmente o armazenamento.

