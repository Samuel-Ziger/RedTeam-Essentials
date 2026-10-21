# Lab 04 — HTTP, API e SQLite

## Objetivo

Construir serviço HTTP local pequeno e verificá-lo pelo contrato, não somente
por chamadas manuais.

## Tempo e ambiente

- 14 a 20 horas;
- Python 3.12+ para o starter; outra linguagem pode ser usada depois que o
  primeiro fluxo estiver compreendido;
- SQLite;
- bind exclusivo em <code>127.0.0.1</code>;
- cliente HTTP local.

## Comece pelo starter, não por uma página vazia

O diretório [`starter-http/`](starter-http/) contém um servidor real, mas
deliberadamente pequeno: apenas `GET /health`, erros `400/404` em JSON,
serialização e testes de framing básico. Ele usa somente a biblioteca padrão,
porta efêmera nos testes, recusa bind fora de loopback e fecha a conexão quando
um corpo proibido poderia deixar bytes residuais em HTTP/1.1.

Execute a partir da raiz do repositório:

```bash
cd 00-Fundamentos/programacao/labs/starter-http
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 server.py --port 8000
```

Em outro terminal:

```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/desconhecida
```

Antes de mudar o código, localize e explique:

1. `make_server`: composição de host, porta e classe de handler;
2. porta `0` nos testes: o sistema escolhe uma porta livre, evitando colisão;
3. `do_GET`: entrada do framework e decisão de rota;
4. `send_json`: serializa uma vez e mede bytes, não caracteres;
5. `Content-Type` e `Content-Length`: contrato da representação;
6. thread do teste: o cliente e o servidor precisam progredir ao mesmo tempo;
7. `shutdown`, `server_close` e `join`: nenhum processo/thread deve ficar
   abandonado depois do teste.

Copie o starter para seu repositório de exercícios. Mantenha os testes verdes e
faça um commit por etapa abaixo.

## Progressão de construção

### Etapa 1 — domínio sem HTTP nem banco

Crie uma representação de livro e funções que validem título, autor, ano e
status. Elas recebem valores da linguagem, não JSON. Teste vazio, limites,
booleano usado como inteiro e ano imediatamente antes/depois do permitido.

**Gate:** todos os testes de domínio executam sem iniciar servidor ou SQLite.

### Etapa 2 — repositório SQLite isolado

Crie schema em banco temporário e implemente primeiro `create` e `list`. Use
parâmetros, contexto de transação e conversão explícita de linha para domínio.
Depois acrescente `find`, `update_status` e `delete`. Cada teste deve possuir seu
próprio banco ou fixture reiniciada.

**Gate:** CRUD e rollback são provados sem HTTP.

### Etapa 3 — primeira rota de dados

Injete o caminho do banco no handler e implemente somente `GET /books`. Comece
com banco vazio, depois insira pela camada de repositório e consulte pelo socket.
Não leia diretamente a lista interna da aplicação no teste HTTP.

**Gate:** o teste observa `200`, `Content-Type`, tamanho correto e schema JSON.

### Etapa 4 — criação validada

Implemente `POST /books` na ordem:

1. confirmar rota e ausência de query não suportada;
2. exigir `Content-Type: application/json`;
3. interpretar e limitar `Content-Length` **antes** de ler o corpo;
4. ler exatamente os bytes declarados;
5. decodificar UTF-8 e JSON, distinguindo falhas;
6. rejeitar campos ausentes, desconhecidos e tipos errados;
7. chamar validação de domínio;
8. persistir em uma transação;
9. devolver `201`, representação criada e `Location: /books/{id}`.

Escreva um teste que falha para cada decisão antes de implementar a decisão.

### Etapa 5 — completar o recurso

Acrescente `GET /books/{id}`, `PATCH /books/{id}` e
`DELETE /books/{id}` uma rota por vez. Separe:

- parser do caminho e do ID;
- parser de mensagem HTTP/JSON;
- regra de domínio;
- operação do repositório;
- tradução do resultado para status e corpo.

Essa separação impede que `ValueError` de um ID inválido seja confundido com
falha interna do banco. `204` termina os cabeçalhos sem corpo.

### Etapa 6 — concorrência, logs e encerramento

Somente depois do CRUD correto, acrescente request ID, status e duração ao log.
Teste dois clientes com barreira/evento para tornar a sobreposição observável.
Defina timeout de lock e explique por que SQLite continua tendo um escritor por
vez. Por último, trate interrupção e prove que o teste encerra servidor, threads
e conexões.

Se optar por framework, mantenha os mesmos gates. O framework reduz código de
protocolo, mas não decide suas invariantes, transações ou testes.

## Domínio

Implemente catálogo sintético de livros:

- ID inteiro;
- título de 1 a 120 caracteres;
- autor de 1 a 80;
- ano entre 1450 e o ano atual definido pela aplicação;
- status “disponível” ou “emprestado”.

Não use nomes ou registros reais.

## Contrato mínimo

| Ação | Método e caminho | Sucesso |
|------|------------------|---------|
| saúde | GET /health | 200 |
| listar | GET /books | 200 |
| obter | GET /books/{id} | 200 |
| criar | POST /books | 201 e Location |
| alterar status | PATCH /books/{id} | 200 |
| remover | DELETE /books/{id} | 204 |

Defina uma representação única de erro, por exemplo campos <code>error</code>,
<code>message</code> e <code>requestId</code>. Não devolva detalhes internos do
banco.

## Regras HTTP

- aceite JSON apenas com Content-Type apropriado;
- aplique limite pequeno ao corpo;
- diferencie JSON malformado de regra de domínio inválida;
- use 404 para recurso ausente, não para erro de validação;
- envie Content-Length ou fechamento correto conforme biblioteca;
- não inclua corpo em resposta 204;
- mantenha erros do cliente fora do status 500.

## Banco

Crie migração/schema versionado. Use:

- chave primária;
- restrições coerentes;
- parâmetros;
- transação por operação de escrita;
- índice somente após justificar consulta;
- conexão com lifetime claro.

## Testes

Execute o servidor em porta efêmera durante os testes. Cubra:

- ciclo criar → obter → alterar → remover;
- Content-Type ausente/incorreto;
- JSON quebrado;
- corpo vazio e acima do limite;
- campos ausentes, extras e tipos errados conforme política;
- limites de título/ano;
- ID inexistente;
- resposta 204 sem corpo;
- persistência após reiniciar;
- duas operações concorrentes sem banco corrompido.

Cada teste deve controlar seu banco ou limpar o estado explicitamente.

## Observabilidade

Registre um evento por requisição com:

- request ID;
- método e caminho normalizado;
- status;
- duração;
- erro classificado quando houver.

Não registre corpo, cabeçalho de autorização ou dados sensíveis.

## Experimentos

1. Envie o mesmo POST duas vezes e explique o resultado.
2. Compare isso com uma atualização idempotente.
3. Provoque lock curto no SQLite e observe timeout/tratamento.
4. Interrompa o servidor durante uma escrita de teste e verifique integridade.
5. Observe plano de consulta antes/depois de um índice justificado.

## Critérios de aceite

- [ ] O serviço só escuta em loopback.
- [ ] Contrato e representação de erro estão documentados.
- [ ] Status distinguem sintaxe, validação, ausência e falha interna.
- [ ] SQL usa parâmetros e transações.
- [ ] Testes exercitam o protocolo real por socket local.
- [ ] Logs permitem correlacionar uma requisição sem expor conteúdo.
- [ ] Reinício preserva dados confirmados.
- [ ] O cleanup remove banco e processos do laboratório.
