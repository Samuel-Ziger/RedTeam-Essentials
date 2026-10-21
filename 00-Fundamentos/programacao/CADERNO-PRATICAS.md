# Caderno de práticas e evidências

Este caderno transforma a leitura em habilidade observável. Faça os exercícios
na ordem da trilha, dentro de um repositório próprio. Cada entrega deve conter:

- enunciado reescrito com suas palavras;
- exemplos de entrada e saída;
- decisões e invariantes;
- código formatado;
- testes automatizados quando o runtime permitir;
- arquivo curto de retrospectiva com falhas e aprendizados.

Não use dados reais. Nomes, e-mails, tokens e registros devem ser sintéticos.

## Escopo canônico e acompanhamento

Este caderno contém **39 exercícios numerados**: quatro no nível 0, seis no
nível 1, oito no nível 2, seis no nível 3, seis no nível 4, cinco no nível 5
e quatro no nível 6. Para o critério quantitativo do módulo, conclua pelo menos
28. Os cinco laboratórios, os checkpoints, o kata nas cinco linguagens e os
projetos continuam obrigatórios e não entram nessa porcentagem.

Copie esta tabela para seu repositório de evidências:

| Faixa | Total | Mínimo sugerido | Concluídos | Evidência/commit |
|-------|------:|----------------:|-----------:|------------------|
| 0.x | 4 | 4 |  |  |
| 1.x | 6 | 5 |  |  |
| 2.x | 8 | 5 |  |  |
| 3.x | 6 | 4 |  |  |
| 4.x | 6 | 4 |  |  |
| 5.x | 5 | 3 |  |  |
| 6.x | 4 | 3 |  |  |
| **Total** | **39** | **28** |  |  |

Os mínimos por faixa são uma distribuição recomendada para evitar que toda a
prática fique concentrada no início; a regra final continua sendo 28 no total,
sem pular uma faixa inteira. Exercícios espalhados pelos capítulos e guias são
reforço opcional e não mudam o denominador.

## Como avaliar uma solução

Uma solução não está pronta apenas porque produziu uma saída correta uma vez.
Verifique quatro dimensões:

| Dimensão | Pergunta |
|----------|----------|
| Correção | todas as classes de entrada obedecem ao contrato? |
| Clareza | nomes, funções e fluxo tornam a intenção recuperável? |
| Robustez | entradas inválidas e falhas de I/O são tratadas conscientemente? |
| Evidência | os testes falhariam se a regra principal fosse quebrada? |

Para cada exercício, execute ao menos um caso comum, um limite, um caso inválido
e um caso vazio quando vazio fizer sentido.

## Nível 0 — leitura e rastreamento

### 0.1 Rastrear atribuições

Sem executar, determine a saída e registre o valor após cada linha:

    total = 10
    desconto = 2
    total = total - desconto
    desconto = total / 4
    total = total + desconto

Depois execute em Python. Explique por que o nome <code>desconto</code> passou a
representar outro conceito e proponha nomes que evitem isso.

**Evidência:** tabela com linha, <code>total</code>, <code>desconto</code> e
saída prevista.

### 0.2 Tabela-verdade

Construa a tabela-verdade de:

    maior_de_idade AND (tem_ingresso OR esta_na_lista)

Há oito combinações. Depois escreva a condição em duas linguagens e confirme
todas com teste parametrizado ou laço de casos.

**Critério:** explicar a diferença se os parênteses forem removidos, conforme a
precedência da linguagem.

### 0.3 Ramo inalcançável

Analise:

    if nota >= 5:
        conceito = "aprovado"
    elif nota >= 9:
        conceito = "excelente"

Encontre o ramo inalcançável, corrija a ordem e escreva testes para 4.99, 5,
8.99, 9 e 10.

### 0.4 Laço e invariante

Rastreie um algoritmo que soma números de 1 até N. Antes e depois de cada
iteração, registre contador e acumulador. Formule uma invariante do laço.

**Critério:** tratar N igual a zero e rejeitar N negativo de forma documentada.

## Nível 1 — controle de fluxo e funções

### 1.1 Classificador de temperatura

Implemente uma função que recebe graus Celsius e retorna uma categoria definida
por você. Escreva primeiro uma tabela de faixas sem lacunas nem sobreposição.

**Testes obrigatórios:** cada fronteira, valor não finito e tipo incompatível.

### 1.2 FizzBuzz como especificação

Para números de 1 até N:

- múltiplos de 3 produzem “Fizz”;
- múltiplos de 5 produzem “Buzz”;
- múltiplos de ambos produzem “FizzBuzz”;
- outros produzem o próprio número.

Separe a função de classificar um número da função de construir a sequência.
Explique por que a regra mais específica deve ser avaliada primeiro.

### 1.3 Conversor de duração

Receba segundos inteiros não negativos e devolva dias, horas, minutos e
segundos restantes.

**Casos:** 0, 59, 60, 3599, 3600, 86400 e um valor negativo.

**Restrição:** não use biblioteca de data/hora na primeira versão.

### 1.4 Validação de senha didática

Valide apenas regras explícitas de formato: tamanho mínimo, presença de classes
de caracteres e ausência de espaços. Não afirme que isso mede força real.

Retorne todas as violações, não somente a primeira.

**Discussão:** por que armazenar senha em texto ou registrar seu conteúdo seria
incorreto? Este exercício não implementa autenticação.

### 1.5 Estatística descritiva

Calcule quantidade, mínimo, máximo, média e mediana de uma sequência de números.
Defina o comportamento para entrada vazia e não altere a coleção recebida.

**Testes:** quantidade par e ímpar, repetidos, negativos, um único valor e
entrada vazia.

### 1.6 CLI previsível

Exponha o exercício anterior como CLI:

    programa 10 8 4

Defina:

- saída normal legível ou JSON;
- mensagem de uso em <code>stderr</code>;
- código 0 para sucesso e 2 para argumento inválido;
- separador decimal independente de locale quando necessário.

## Nível 2 — coleções e algoritmos

### 2.1 Contador de palavras

Leia texto local, normalize uma regra de caixa e conte frequências. Separe
tokenização, normalização, contagem e apresentação.

**Decisões a documentar:** pontuação, acentos, números e empate na ordenação.

### 2.2 Deduplicação estável

Remova duplicatas preservando a primeira ocorrência. Faça:

1. versão simples de custo quadrático;
2. versão com conjunto auxiliar;
3. medição com entradas crescentes.

Explique a troca entre memória adicional e tempo.

### 2.3 Índice invertido

Dado um conjunto de documentos sintéticos, construa mapa de palavra para IDs de
documento em que ela ocorre.

**Critério:** IDs não podem se repetir no resultado de uma palavra; a saída deve
ser determinística.

### 2.4 Pilha de desfazer

Modele editor mínimo com operações de acrescentar texto e desfazer. A pilha
guarda estados ou comandos; escolha uma abordagem e explique o custo.

**Desafio:** implemente também refazer com uma segunda pilha.

### 2.5 Fila de atendimento

Modele chegada e atendimento FIFO. Não remova do início de um array se a
linguagem oferecer deque adequado; compare custos.

**Casos:** fila vazia, entradas repetidas e tentativa de atender mais itens do
que existem.

### 2.6 Busca binária

Implemente busca em lista ordenada retornando índice ou ausência.

**Testes:** primeiro, último, meio, ausente abaixo/acima, lista vazia, tamanhos
par e ímpar.

**Defesa:** explique a invariante do intervalo e por que a entrada precisa estar
ordenada.

### 2.7 Grafo de dependências

Receba pares “A depende de B” e produza uma ordem válida ou informe ciclo.

**Critério:** um nó sem dependências também aparece; ciclo deve ser distinguido
de referência desconhecida.

### 2.8 Cache LRU conceitual

Implemente cache com capacidade pequena e política de menos recentemente usado.
Primeiro faça uma versão clara, depois discuta como mapa + lista duplamente
ligada permite operações constantes.

Não otimize sem testes de comportamento.

## Nível 3 — modelagem, erros e testes

### 3.1 Conta com invariantes

Modele conta sintética com identificador, saldo e operações de crédito/débito.
Defina se saldo negativo é permitido e proteja a regra dentro do domínio.

**Testes:** valor zero, negativo, acima do saldo e sequência de operações.

### 3.2 Agenda com persistência

Crie agenda CLI com ID, nome e contato fictício. Comandos mínimos:

- adicionar;
- listar;
- buscar;
- atualizar;
- remover.

Persista em JSON ou SQLite. Escreva arquivo temporário e faça substituição
atômica quando usar JSON para reduzir risco de corrupção.

### 3.3 Relógio controlável

Uma função que decide se um item expirou não deve depender diretamente do
relógio global em todo teste. Receba o instante atual ou injete uma abstração.

**Evidência:** teste determinístico antes, exatamente e depois do vencimento.

### 3.4 Pipeline de importação

Importe CSV sintético em três fases:

1. parsing estrutural;
2. validação de campos;
3. persistência.

Produza relatório com aceitos e rejeitados, incluindo linha e motivo, mas não
interrompa todo o lote por um registro inválido.

### 3.5 Teste de mutação manual

Escolha uma regra importante e altere deliberadamente operador, retorno ou
condição. A suíte deve falhar. Se passar, o teste não protege aquela regra.

Registre mutação, teste que deveria detectá-la e melhoria realizada.

### 3.6 Configuração externa

Leia porta e modo de log de argumentos ou variáveis de ambiente. Valide tipo e
faixa na inicialização. Não inclua segredo; demonstre como um nome de variável
seria documentado sem valor real.

## Nível 4 — HTTP, API e banco de dados

### 4.1 Interpretar uma mensagem HTTP

Para uma requisição local, identifique método, caminho, consulta, cabeçalhos e
corpo. Na resposta, identifique status, tipo de conteúdo e tamanho.

Explique quais dados não fazem parte do corpo e por que o fragmento da URL não é
enviado ao servidor.

### 4.2 API de tarefas

Projete antes de implementar:

| Operação | Método e caminho | Sucesso | Erros previstos |
|----------|------------------|---------|-----------------|
| criar | POST /tasks | 201 | 400/415 |
| listar | GET /tasks | 200 | — |
| alterar | PATCH /tasks/{id} | 200 | 400/404 |
| remover | DELETE /tasks/{id} | 204 | 404 |

Defina representação do erro e mantenha tipo de conteúdo coerente.

### 4.3 Integridade relacional

Modele tarefas e etiquetas em SQLite. Use chaves primárias, estrangeiras e
tabela de associação. Tente inserir referência inexistente e observe a
restrição. Ative `PRAGMA foreign_keys = ON` em cada conexão, antes de iniciar a
transação, e confirme que consultar `PRAGMA foreign_keys` devolve `1`; no
SQLite, apenas declarar `REFERENCES` não habilita a fiscalização por padrão.

### 4.4 Transação atômica

Implemente operação que cria tarefa e registra evento na mesma transação.
Provoque falha na segunda etapa e verifique que nenhuma alteração parcial fica
confirmada.

### 4.5 Índice medido

Crie dados sintéticos, observe o plano de uma consulta, adicione índice adequado
e compare plano e tempo. Registre tamanho, número de repetições e ambiente.

**Discussão:** qual custo adicional o índice traz para escrita e armazenamento?

### 4.6 Teste de contrato

Escreva teste que verifica status, cabeçalho e schema mínimo da API. Mude
deliberadamente o nome de um campo no servidor e confirme que o contrato falha.

## Nível 5 — sistemas e concorrência

### 5.1 Processo e código de saída

Crie programa pai que inicia processo filho local, captura saídas separadamente
e trata timeout. Diferencie término normal, erro de validação e processo não
encontrado.

### 5.2 Corrida reproduzida

Em ambiente local, faça duas tarefas atualizarem um contador compartilhado sem
coordenação. Repita até observar perda e depois proteja a seção crítica.

**Relatório:** por que o resultado podia variar e qual invariante o lock protege?

### 5.3 Produtor e consumidor

Use fila limitada. Quando cheia, o produtor deve esperar ou rejeitar conforme
política documentada. Isso demonstra backpressure.

### 5.4 Cancelamento e timeout

Implemente operação assíncrona simulada que aceita cancelamento. Mostre que
parar de esperar não é necessariamente cancelar o trabalho e propague o sinal.

### 5.5 Arquivo binário

Defina formato pequeno com assinatura, versão, tamanho e payload. Escreva e leia
validando truncamento, tamanho excessivo e versão desconhecida.

Não leia tamanho vindo do arquivo sem aplicar limite.

## Nível 6 — entrega local

### 6.1 Dockerfile explicado

Para cada instrução do Dockerfile do TaskBoard, responda:

- qual camada/efeito produz;
- o que invalida o cache;
- qual usuário executa o processo;
- quais arquivos entram na imagem;
- qual comando recebe sinais do container.

### 6.2 Rede do Compose

Desenhe o fluxo navegador → Nginx → API → SQLite. Diferencie:

- porta publicada no host;
- porta interna do container;
- nome DNS do serviço;
- volume;
- rede do Compose.

### 6.3 Diagnóstico operacional

Provoque uma configuração de porta incorreta em uma cópia e investigue com:

    docker compose config
    docker compose ps
    docker compose logs

Restaure a configuração e demonstre o healthcheck saudável.

### 6.4 Cleanup comprovado

Liste containers, rede e volume antes e depois da remoção. Explique a diferença
entre parar, remover containers e remover volumes.

Nunca use comandos de remoção amplos fora do projeto do laboratório.

## Kata transversal nas cinco linguagens

Implemente o mesmo analisador de notas em Python, JavaScript, Java, C e C#:

- aceita uma ou mais notas no intervalo de 0 a 10;
- rejeita texto parcial, não finito e valor fora da faixa;
- calcula média com duas casas;
- conta conceitos A, B, C e D;
- retorna código 0 no sucesso e 2 no erro de uso;
- escreve dados em saída normal e diagnóstico em saída de erro.

Compare:

| Aspecto | Pergunta |
|---------|----------|
| Tipos | em que momento uma incompatibilidade é detectada? |
| Parsing | como a API diferencia valor válido de texto parcial? |
| Coleções | como o mapa de frequências é representado? |
| Erros | exceção, resultado ou código de retorno? |
| Memória | quem determina o lifetime dos valores? |
| Testes | qual ferramenta executa sem dependência externa? |
| Build | qual artefato é produzido e como é executado? |

Os exemplos oficiais em <code>exemplos/</code> são referência depois da sua
primeira tentativa, não solução para copiar.

## Rubrica do portfólio

| Critério | Peso | Evidência |
|----------|------|-----------|
| correção e casos de limite | 30 | testes e demonstração |
| decomposição e contratos | 20 | código e documentação |
| tratamento de erro | 15 | casos inválidos e códigos de saída |
| legibilidade e manutenção | 15 | nomes, módulos, commits e revisão |
| investigação técnica | 10 | relatórios de depuração/medição |
| defesa oral ou escrita | 10 | explicação sem consultar solução |

Para aprovação, alcance ao menos 70/100 e não obtenha zero em correção,
tratamento de erros ou defesa.
