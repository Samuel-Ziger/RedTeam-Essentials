# Dependency Planner

Aplicação de referência do curso. Ela lê tarefas de um arquivo JSON, valida o
grafo, produz uma ordem executável, agrupa trabalho paralelo e calcula o caminho
crítico considerando a duração de cada tarefa.

O objetivo não é competir com uma ferramenta de gestão. É mostrar como algoritmo,
modelo de domínio, arquitetura, erros, testes e interface se conectam sem um
framework esconder as decisões.

## O que o projeto prova

- contrato de entrada estrito e limitado antes do processamento global;
- objetos imutáveis com invariantes locais;
- ordenação topológica e lotes paralelos determinísticos;
- caminho crítico por programação dinâmica sobre um DAG;
- separação entre domínio, caso de uso, porta, adapter e apresentação;
- erros previsíveis com canal e código de saída estáveis;
- testes por exemplo, contrato, processo, propriedades e entrada adversarial.

O projeto **não** executa tarefas, aloca pessoas/máquinas nem considera
calendários. “Lotes paralelos” significa apenas que as dependências permitem
iniciar o conjunto junto quando recursos são ilimitados.

## Arquitetura

```text
cli.py  ------------------------------ apresentação e códigos de saída
  |
service.py --------------------------- caso de uso
  |                  |      |
ports.py             graph.py ------- algoritmos puros
  |                         |
  |                       domain.py -- invariantes e resultado
  ^
  |
repository.py ------------------------ adaptador JSON
```

As dependências de código apontam para o núcleo. `graph.py` não conhece arquivo,
JSON ou terminal. Um futuro adaptador SQL pode implementar a mesma porta sem
alterar os algoritmos.

Veja a [arquitetura executável](docs/architecture.md), o
[ADR-001](docs/adr/001-ports-and-adapters.md) e o
[ADR-002](docs/adr/002-deterministic-bounded-input.md). Diagramas são mapas;
imports, testes e execução são a fonte de verdade sobre as fronteiras.

## Formato de entrada

```json
{
  "items": [
    {"id": "modelo", "title": "Modelar dominio", "duration": 3, "dependencies": []},
    {"id": "api", "title": "Criar API", "duration": 5, "dependencies": ["modelo"]}
  ]
}
```

- `id`: string única de ASCII alfanumérico, ponto, sublinhado ou hífen;
- `title`: string não vazia;
- `duration`: inteiro positivo em unidades abstratas;
- `dependencies`: IDs existentes que devem terminar antes da tarefa.

Campos desconhecidos, chaves JSON duplicadas, números não padronizados, inteiros
além do limite seguro do runtime, tipos incorretos e aninhamento excessivo são
rejeitados como erros de validação, sem traceback para quem usa a CLI.

Limites atuais do adapter JSON:

| Elemento | Limite | Motivo |
|---|---:|---|
| documento | 32 MiB | comportar o cenário de 50 mil tarefas sem leitura ilimitada |
| itens | 100.000 | limitar indexação/memória |
| ID | 128 caracteres ASCII seguros | chave operacional e mensagem controláveis |
| título | 512 caracteres | impedir payload textual desproporcional |
| duração | 1.000.000 | domínio didático e soma previsível |
| dependências por item | 10.000 | fan-in limitado explicitamente |

Esses valores são política versionada, não limites universais. Mudá-los exige
fixtures representativos, orçamento de recurso e teste de compatibilidade.

## Executar

Na raiz deste projeto:

```bash
PYTHONPATH=src python3 -m dependency_planner.cli fixtures/valid-project.json
PYTHONPATH=src python3 -m dependency_planner.cli fixtures/valid-project.json --format json
PYTHONPATH=src python3 -m dependency_planner.cli fixtures/cyclic-project.json
```

A última execução termina com código `2`, pois ciclo é um erro esperado de
entrada. Erros vão para `stderr`; resultado válido vai para `stdout`.

O programa não modifica o documento. Uma execução pode ser repetida e deve
produzir os mesmos bytes para a mesma entrada, versão e formato.

## Testar

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Ou execute `../../testar-curso.sh` para testar também os exemplos nas outras
linguagens.

A suíte cobre:

- invariantes locais de `WorkItem`;
- schema, UTF-8, tamanho, cardinalidade, inteiro gigante e aninhamento
  adversarial do adapter;
- resultado vazio, erros de referência/duplicidade e ciclos cujo caminho segue
  o sentido pré-requisito → dependente;
- caminho de ciclo maior que a pilha de recursão do Python;
- todos os DAGs compatíveis com uma ordem de quatro vértices;
- determinismo sob permutação da entrada;
- contrato da CLI, JSON de saída e separação dos canais.

## Decisões importantes

- algoritmo de Kahn com heap: `O(V + E + V log V)`, escolha determinística;
- listas de adjacência: memória `O(V + E)`;
- objetos imutáveis: invariantes locais e testes mais previsíveis;
- adaptador rigoroso: documento inválido falha antes do algoritmo;
- exceções do domínio: a CLI traduz uma vez para mensagem e código de saída;
- caminho crítico em DAG: programação dinâmica sobre a ordem topológica.

O algoritmo do caminho crítico assume recursos ilimitados e durações positivas.
Empates usam ID ordinal para manter a reconstrução estável. A detecção de
ciclo usa pilha explícita para não transformar profundidade de entrada em limite
da pilha do runtime.

## Diagnóstico e operação

Consulte o [RUNBOOK](RUNBOOK.md). Preserve comando, fixture mínimo, status,
`stdout`, `stderr` e primeira invariante violada antes de editar. O projeto não
mantém estado; rollback consiste em executar uma versão anterior conhecida e
comparar propriedades, sem apagar mudanças locais.

## Evoluções propostas

1. crie adaptador CSV mantendo o caso de uso intacto;
2. adicione recurso máximo por lote e documente se o problema muda;
3. exponha o caso de uso por uma API HTTP;
4. persista planos em PostgreSQL;
5. gere visualização DOT sem acoplar o domínio;
6. use teste baseado em propriedades para gerar DAGs aleatórios;
7. faça benchmark com grafos em cadeia, leque e esparsos.

Cada evolução deve começar por requisito, exemplo e ADR quando houver decisão de
longo alcance.

Use o [Lab 05](../../laboratorios/lab-05-dependency-planner.md) para conduzir uma
mudança vertical, criar evidências e fazer a defesa técnica.
