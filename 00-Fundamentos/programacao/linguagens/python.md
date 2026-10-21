# Python: fundamentos sólidos até aplicações confiáveis

Python reduz cerimônia, não responsabilidade. Um programa pequeno ainda precisa
de contratos, validação de entrada, tratamento de falhas e testes. Este guia
ensina primeiro o modelo da linguagem e depois mostra como transformar um
script em código que pode crescer sem se tornar frágil.

Ao terminar, você deverá conseguir explicar não só **o que** o código faz, mas:

- quais valores uma função aceita e devolve;
- quem pode modificar cada objeto;
- em que fronteiras uma operação pode falhar;
- como provar o comportamento com testes;
- qual custo de tempo e memória acompanha a solução.

## 1. Toolchain e primeiro ciclo

Confirme o interpretador e execute um arquivo:

```bash
python3 --version
python3 programa.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

O interpretador lê o código-fonte, compila-o para bytecode e o executa na
máquina virtual da implementação. Em CPython, arquivos `.pyc` são cache de
bytecode, não executáveis portáveis nem proteção do código-fonte.

Para isolar dependências de um projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip --version
deactivate
```

Use `python -m ferramenta` para garantir que a ferramenta pertence ao mesmo
interpretador ativado. Os exemplos deste módulo usam apenas a biblioteca padrão.

## 2. Anatomia do programa

```python
#!/usr/bin/env python3
"""Descrição curta do módulo."""


def saudar(nome: str) -> str:
    return f"Olá, {nome.strip()}!"


def main() -> int:
    print(saudar("Ada"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

A indentação delimita blocos. Quatro espaços são a convenção. O guard de
`__main__` separa dois usos do arquivo:

- executado diretamente: chama `main` e converte o retorno em status do processo;
- importado: define funções sem iniciar a interface de linha de comando.

Isso é essencial para testes: importar lógica não deve imprimir, encerrar o
processo nem acessar a rede.

## 3. Nomes, objetos, tipos e referências

Uma variável Python é um nome ligado a um objeto; não é uma caixa com tipo fixo.

```python
quantidade = 3          # int
preco = 19.90           # float
ativo = True            # bool
nome = "teclado"        # str
ausente = None          # NoneType
```

O objeto tem tipo; o nome pode ser religado. Essa flexibilidade exige contratos
claros. Evite transformar a mesma variável de número em texto no meio da função.

### Tipos numéricos

`int` tem precisão arbitrária limitada pela memória. `float` normalmente segue
IEEE 754 em dupla precisão:

```pycon
>>> 0.1 + 0.2 == 0.3
False
```

Não compare resultados de ponto flutuante por igualdade exata quando há cálculo:

```python
import math

assert math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9, abs_tol=1e-12)
```

Para dinheiro, prefira inteiros em centavos ou `decimal.Decimal` com regra de
arredondamento explícita. Valores `nan` e infinitos são `float`; valide com
`math.isfinite` em domínios que exigem números reais finitos.

### Texto, bytes e Unicode

`str` representa texto Unicode; `bytes` representa octetos. Codificação faz a
ponte entre ambos:

```python
texto = "ação"
dados = texto.encode("utf-8")
assert dados.decode("utf-8") == texto
```

Nunca “adivinhe” codificação silenciosamente. Em arquivos e protocolos, declare
UTF-8 ou a codificação definida pelo contrato.

### Verdade e ausência

Coleções vazias, zero, `None` e `False` são falsy. Não confunda ausência com
zero válido:

```python
if valor is None:       # ausência especificamente
    ...

if not itens:           # coleção vazia
    ...
```

Use `is None`, não `== None`. `is` compara identidade; `==` compara valor.

## 4. Operadores e fluxo de controle

```python
idade = 20

if idade < 0:
    mensagem = "inválida"
elif idade < 18:
    mensagem = "menor"
else:
    mensagem = "maior"
```

As condições são avaliadas de cima para baixo. Ordene faixas para que não haja
buracos ou ramos inalcançáveis. `and` e `or` fazem curto-circuito:

```python
if usuario is not None and usuario.ativo:
    autorizar(usuario)
```

Laços percorrem iteráveis, não apenas índices:

```python
nomes = ["Ana", "Bia", "Caio"]

for posicao, nome in enumerate(nomes, start=1):
    print(posicao, nome)

for nome, nota in zip(nomes, [8, 6, 9], strict=True):
    print(nome, nota)
```

`strict=True` detecta sequências de comprimentos diferentes. Em `while`, deixe
evidente o que altera a condição de parada:

```python
tentativas = 3
while tentativas > 0:
    tentativas -= 1
```

`break` encerra o laço; `continue` avança para a próxima iteração. Use ambos
com parcimônia para preservar um fluxo legível.

## 5. Funções são contratos

```python
def calcular_total(
    valores: list[int],
    *,
    desconto_percentual: int = 0,
) -> int:
    """Devolve o total em centavos após desconto inteiro."""
    if not 0 <= desconto_percentual <= 100:
        raise ValueError("desconto deve estar entre 0 e 100")
    subtotal = sum(valores)
    return subtotal * (100 - desconto_percentual) // 100
```

O `*` torna `desconto_percentual` keyword-only, evitando chamadas ambíguas.
Parâmetros podem ser posicionais, nomeados, variádicos (`*args`, `**kwargs`) ou
restritos. Não use variádicos apenas para fugir de desenhar uma interface.

### Armadilha do default mutável

Defaults são avaliados uma vez, na definição:

```python
# Ruim: todas as chamadas compartilham a mesma lista.
def adicionar_ruim(item, itens=[]):
    itens.append(item)
    return itens


def adicionar(item: str, itens: list[str] | None = None) -> list[str]:
    resultado = [] if itens is None else list(itens)
    resultado.append(item)
    return resultado
```

### Type hints

Anotações documentam e alimentam IDEs/analisadores, mas não validam em runtime:

```python
def dobro(valor: int) -> int:
    return valor * 2

dobro("a")  # executa e devolve "aa" sem um verificador estático
```

Valide dados não confiáveis na fronteira. Use hints para tornar erros internos
visíveis antes da execução.

## 6. Coleções e custo

| Estrutura | Propriedade principal | Operações típicas |
|---|---|---|
| `list` | sequência mutável | índice O(1), append amortizado O(1), busca O(n) |
| `tuple` | sequência imutável | registro simples, chave quando conteúdo é hashable |
| `dict` | chave/valor | busca/inserção média O(1), preserva ordem de inserção |
| `set` | valores únicos | pertencimento médio O(1), união/interseção |
| `deque` | fila de duas pontas | append/pop nas pontas O(1) |

Exemplos:

```python
estoque = {"caderno": 4, "caneta": 12}
estoque["caneta"] += 1

permissoes = {"ler", "editar"}
if "editar" in permissoes:
    print("permitido")

quadrados_pares = [n * n for n in range(10) if n % 2 == 0]
```

Uma compreensão é boa para uma transformação curta. Para validação, múltiplos
efeitos ou vários ramos, um laço explícito comunica melhor.

## 7. Mutabilidade, cópia e identidade

```python
original = [[1], [2]]
copia_rasa = list(original)
copia_rasa[0].append(99)
assert original[0] == [1, 99]
```

A cópia externa não duplicou os objetos internos. Use `copy.deepcopy` somente
quando esse for realmente o contrato; estruturas imutáveis e ownership claro
costumam ser melhores.

Argumentos são passados por compartilhamento de objeto. Uma função pode mutar
um objeto recebido, mas religar seu nome local não altera o nome do chamador:

```python
def registrar(itens: list[str]) -> None:
    itens.append("novo")     # mutação visível ao chamador
```

Documente mutação ou devolva um novo valor. Misturar os dois estilos cria bugs.

## 8. Exceções e fronteiras

Use exceção para uma operação que não consegue cumprir seu contrato:

```python
def porcentagem(texto: str) -> int:
    try:
        valor = int(texto)
    except ValueError as exc:
        raise ValueError(f"percentual inválido: {texto!r}") from exc
    if not 0 <= valor <= 100:
        raise ValueError("percentual fora da faixa")
    return valor
```

`raise ... from exc` preserva causa e acrescenta contexto. Capture a exceção
mais específica possível e somente onde puder recuperar, traduzir ou encerrar
de forma útil. `except Exception: pass` destrói evidência de falhas.

O bloco completo:

```python
try:
    recurso = abrir()
except OSError as exc:
    tratar_falha(exc)
else:
    usar(recurso)       # executa só se não houve exceção
finally:
    liberar()           # executa sempre
```

Prefira context managers (`with`) para recursos; eles tornam cleanup estrutural.

## 9. Modelagem: dataclass, enum e composição

```python
from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"


@dataclass(frozen=True, slots=True)
class Tarefa:
    id: int
    titulo: str
    status: Status = Status.PENDENTE

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("id deve ser positivo")
        if not self.titulo.strip():
            raise ValueError("título obrigatório")
```

`frozen=True` impede reatribuição comum; não torna transitivamente imutáveis
objetos mutáveis dentro da classe. `slots=True` restringe atributos e pode
reduzir memória. Use classe quando dados e invariantes pertencem juntos.

Prefira composição a hierarquias profundas:

```python
from typing import Protocol


class Repositorio(Protocol):
    def salvar(self, tarefa: Tarefa) -> None: ...


def cadastrar(repo: Repositorio, tarefa: Tarefa) -> None:
    repo.salvar(tarefa)
```

O serviço depende de comportamento, não de SQLite, arquivo ou API específicos.

## 10. Módulos, pacotes e imports

À medida que o projeto cresce:

```text
meu_projeto/
├── pyproject.toml
├── src/
│   └── agenda/
│       ├── __init__.py
│       ├── dominio.py
│       ├── repositorio.py
│       └── cli.py
└── tests/
    └── test_dominio.py
```

- módulo: um arquivo `.py`;
- pacote: conjunto importável de módulos;
- import absoluto: `from agenda.dominio import Tarefa`;
- `__init__.py`: define a superfície pública do pacote quando necessário.

Evite executar I/O no topo do módulo. Imports circulares geralmente indicam
responsabilidades mal distribuídas.

## 11. Entrada, arquivos, JSON e escrita segura

Toda entrada externa é texto ou bytes até ser validada:

```python
from pathlib import Path
import json


def carregar_json(path: Path) -> object:
    with path.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)
```

JSON sintaticamente válido ainda pode ter estrutura inválida. Verifique chaves,
tipos, limites e campos desconhecidos depois do parse.

Para reduzir arquivo parcial:

```python
def salvar_json(path: Path, dados: object) -> None:
    temporario = path.with_suffix(path.suffix + ".tmp")
    with temporario.open("w", encoding="utf-8", newline="") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
        arquivo.flush()
    temporario.replace(path)
```

Isso melhora atomicidade no mesmo filesystem, mas não substitui estratégia de
backup, lock entre processos nem `fsync` quando durabilidade é requisito.

Nunca monte caminho sensível concatenando entrada do usuário. Resolva e valide
o diretório permitido antes de abrir.

## 12. Iteradores e geradores

Um iterável produz um iterador; o iterador entrega valores até `StopIteration`.
Geradores implementam esse protocolo com `yield`:

```python
from collections.abc import Iterator
from pathlib import Path


def linhas_validas(path: Path) -> Iterator[tuple[int, str]]:
    with path.open(encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            valor = linha.strip()
            if valor:
                yield numero, valor
```

O processamento é lazy: memória não cresce com o arquivo inteiro. O recurso
permanece aberto até o gerador terminar ou ser fechado. Documente essa vida útil.

## 13. Modelo de memória e runtime

CPython usa contagem de referências mais um coletor para ciclos. Consequências:

- o coletor gerencia memória, não recursos externos em momento garantido;
- arquivos, locks e conexões devem usar `with`;
- manter uma referência global mantém todo o grafo alcançável vivo;
- `del nome` remove um vínculo, não “apaga” necessariamente o objeto;
- objetos têm overhead; milhões de pequenos dicionários podem consumir muito.

O GIL do CPython tradicional permite que apenas uma thread execute bytecode
Python por vez. Threads continuam úteis para I/O. Não baseie correção no GIL:
operações compostas sobre estado compartilhado ainda precisam de sincronização,
e outras implementações/configurações podem ter modelo diferente.

## 14. Concorrência: escolha pelo trabalho

- `asyncio`: muitas operações de I/O com APIs assíncronas;
- `threading`: I/O bloqueante e integração com bibliotecas síncronas;
- `multiprocessing`: paralelismo de CPU com isolamento entre processos;
- `concurrent.futures`: interface de alto nível para pools.

```python
import asyncio


async def executar() -> list[str]:
    async def trabalho(nome: str) -> str:
        await asyncio.sleep(0.01)
        return nome

    tarefas = [trabalho(str(i)) for i in range(3)]
    return list(await asyncio.gather(*tarefas))
```

Defina timeout, cancelamento e limite de concorrência. `async` não torna código
CPU-bound paralelo nem corrige uma função bloqueante. Em Python 3.11 ou mais
recente, `asyncio.TaskGroup` oferece concorrência estruturada e uma política de
falha diferente de `gather`; consulte essa API quando o projeto puder exigir
3.11+.

## 15. Testes, depuração e observabilidade

Um teste segue Arrange, Act, Assert:

```python
import unittest


class PorcentagemTests(unittest.TestCase):
    def test_aceita_limites(self) -> None:
        self.assertEqual(porcentagem("0"), 0)
        self.assertEqual(porcentagem("100"), 100)

    def test_rejeita_texto(self) -> None:
        with self.assertRaises(ValueError):
            porcentagem("dez")
```

Teste caminho feliz, limites, entrada malformada e invariantes. Evite rede,
relógio real e ordem global em teste unitário. Use `tempfile.TemporaryDirectory`
para filesystem.

Ferramentas da biblioteca padrão:

```bash
python3 -m unittest -v
python3 -m pdb programa.py
python3 -m timeit 'sum(range(100))'
python3 -m cProfile programa.py
```

Use `logging` em aplicações; não registre senhas, tokens ou dados pessoais.
Uma exceção com stack trace é evidência: leia da última causa para o contexto.

## 16. Leitura guiada do exemplo real

Abra [`exemplos/python/fundamentos.py`](../exemplos/python/fundamentos.py) e
acompanhe o fluxo:

1. `main` recebe apenas argumentos e coordena a aplicação;
2. `converter_argumentos` transforma texto externo e localiza erros;
3. `validar_nota` mantém uma única definição da invariante;
4. `conceito` é uma função pura e fácil de testar;
5. `analisar` aceita qualquer iterável e materializa conscientemente;
6. `ResumoNotas` dá nome e tipo ao resultado completo;
7. `resumir` preserva uma API simples em dicionário;
8. a saída é JSON determinístico, útil para outro processo.

Execute:

```bash
python3 00-Fundamentos/programacao/exemplos/python/fundamentos.py 10 8 4
python3 00-Fundamentos/programacao/exemplos/python/fundamentos.py --detalhado 10 8 4
python3 -m unittest discover -s 00-Fundamentos/programacao/exemplos/python -v
```

Depois provoque falhas: `11`, `nan`, texto e nenhuma nota. Observe status,
`stderr` e mensagem. Um programa correto também define como falha.

## 17. Exercícios progressivos

1. Adicione o conceito `A+` somente para nota 10 e escreva o teste antes.
2. Calcule mediana sem alterar a coleção recebida.
3. Leia notas de CSV, informando arquivo e linha em cada erro.
4. Faça uma versão streaming que não materializa todas as notas.
5. Persista resumos em JSON com escrita temporária e substituição.
6. Crie uma `Agenda` com `dataclass`, repositório em memória e CLI `argparse`.
7. Troque o repositório por SQLite sem mudar regras de domínio.
8. Meça as versões materializada e streaming com arquivo grande.

Critério de conclusão: explique cada exceção possível, prove os limites com
testes e mostre que importar o módulo não produz efeitos colaterais.
