# Lab 03 — agenda CLI, persistência e testes

## Objetivo

Projetar uma aplicação pequena separando domínio, entrada/saída e persistência.
O foco é estrutura de dados, invariantes, falhas de arquivo e testes em camadas.

## Tempo e ambiente

- 8 a 12 horas;
- Python, Java ou C#;
- diretório temporário para testes;
- dados completamente fictícios.

## Requisitos

Cada contato possui:

- ID inteiro positivo gerado pela aplicação;
- nome de 1 a 80 caracteres após normalização;
- e-mail opcional sintético;
- lista de etiquetas sem duplicatas.

Operações:

- adicionar;
- listar em ordem determinística;
- buscar por ID;
- buscar por parte do nome;
- atualizar;
- remover;
- exportar.

## Arquitetura mínima

Separe:

1. **domínio:** contato e invariantes;
2. **serviço:** regras de criação, busca e mudança;
3. **repositório:** carregar/salvar JSON ou SQLite;
4. **CLI:** parsing, apresentação e código de saída.

O domínio não deve ler argumentos nem imprimir. O repositório não deve decidir
mensagens para o usuário.

## Persistência

Escolha uma opção.

### JSON

- leia o arquivo inteiro com encoding UTF-8;
- valide versão e estrutura;
- grave primeiro em arquivo temporário no mesmo diretório;
- sincronize/feche conforme a API da linguagem;
- substitua o destino somente após gravação completa;
- não deixe arquivo parcialmente escrito em erro simulado.

### SQLite

- crie schema com restrições;
- use parâmetros, nunca concatenação de entrada;
- agrupe mudanças relacionadas em transação;
- ative/verifique chaves estrangeiras se as usar;
- feche conexão de forma determinística.

## Plano de testes

### Unidade

- limites do nome;
- deduplicação de etiquetas;
- busca case-insensitive conforme regra definida;
- ID ausente;
- atualização inválida.

### Integração

- persistir, fechar e recarregar;
- arquivo/banco inicialmente ausente;
- conteúdo corrompido ou schema incompatível;
- rollback de mudança incompleta;
- dois testes não compartilham estado.

### CLI

- comando válido;
- argumento obrigatório ausente;
- ID inválido;
- códigos de saída documentados.

Use diretório temporário criado pelo teste; nunca escreva no diretório pessoal.

## Revisão técnica

Responda:

- qual estrutura permite busca rápida por ID?
- qual operação domina o custo da busca por nome?
- quais invariantes pertencem ao contato?
- qual falha pertence à fronteira de persistência?
- por que capturar toda exceção e continuar corromperia o diagnóstico?
- como a aplicação evoluiria sem acoplar o domínio ao formato JSON?

## Critérios de aceite

- [ ] As quatro responsabilidades estão separadas.
- [ ] O domínio preserva invariantes mesmo sem a CLI.
- [ ] A persistência resiste à falha simulada.
- [ ] Os testes usam estado isolado.
- [ ] Todas as consultas possuem ordem determinística quando exibidas.
- [ ] Nenhuma entrada é concatenada em SQL.
- [ ] O README permite execução por outra pessoa.

## Evidência

Entregue diagrama textual das dependências, fontes, testes, fixture sintética,
comandos de execução, caso de corrupção simulado e retrospectiva.
