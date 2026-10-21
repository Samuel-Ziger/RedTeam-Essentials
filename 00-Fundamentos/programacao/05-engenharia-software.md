# Engenharia de software e testes

Escrever uma função que funciona uma vez é programação. Manter um sistema
correto enquanto requisitos, pessoas, dados e ambiente mudam é engenharia de
software. Este capítulo mostra como transformar uma ideia imprecisa em um
contrato observável, organizar o código, testar riscos e investigar falhas.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- separar requisito, regra de negócio, restrição técnica e critério de aceite;
- identificar invariantes e protegê-las no lugar correto;
- dividir interface, aplicação, domínio e infraestrutura sem criar camadas vazias;
- escrever testes de unidade e integração determinísticos;
- decidir quando usar dublê de teste e quando usar a dependência real;
- modelar erros esperados sem esconder defeitos inesperados;
- usar logs, métricas e IDs de correlação para reconstruir um fluxo;
- refatorar preservando comportamento;
- revisar código considerando correção, operação e segurança.

Pré-requisitos: funções, coleções, exceções, arquivos e Git. Os exemplos
usam Python 3.12+ e somente a biblioteca padrão.

## 1. Da frase vaga ao comportamento verificável

Considere o pedido: “quero uma agenda de salas”. Antes de escolher banco ou
framework, descubra o comportamento.

### Vocabulário essencial

| Conceito | Pergunta respondida | Exemplo |
|----------|---------------------|---------|
| Requisito funcional | O que o sistema faz? | Cadastrar uma reserva |
| Requisito não funcional | Com qual propriedade? | Responder em até 300 ms para a carga definida |
| Regra de negócio | O que o domínio permite? | Uma sala não aceita horários sobrepostos |
| Invariante | O que deve ser sempre verdadeiro? | `inicio < fim` |
| Critério de aceite | Como observamos que está pronto? | Conflito devolve erro e não grava reserva |
| Restrição | Qual limite já existe? | Persistência local em SQLite |

“Ser rápido” não é verificável. “No notebook de referência, listar 1.000
reservas em menos de 300 ms no percentil 95” define carga, ambiente, métrica e
limite. Nem todo projeto precisa dessa precisão, mas todo critério precisa ser
observável.

### História e cenários

Uma história descreve valor, não a implementação:

> Como responsável por uma equipe, quero reservar uma sala para evitar que duas
> reuniões ocupem o mesmo local.

Cenários de aceite:

```text
Dado que a sala 12 está livre entre 10:00 e 11:00
Quando solicito esse intervalo
Então a reserva recebe um identificador estável

Dado que a sala 12 já está reservada entre 10:00 e 11:00
Quando solicito 10:30 até 11:30
Então recebo "horário indisponível"
E nenhuma segunda reserva é persistida

Dado que uma reserva termina às 11:00
Quando outra começa exatamente às 11:00
Então a nova reserva é permitida
```

O terceiro caso elimina uma ambiguidade importante: intervalos serão tratados
como semiabertos, `[inicio, fim)`. O instante final não pertence à reserva.

### Perguntas antes do código

1. Qual é a entrada válida e qual é seu limite?
2. Qual estado muda?
3. Qual regra não pode ser violada nem sob concorrência?
4. Como cada erro aparece para o chamador?
5. O que acontece se a dependência falhar depois de parte da operação?
6. Que evidência provará que a entrega funciona?

## 2. Modele primeiro a regra mais importante

A regra de sobreposição pode ser uma função pura: mesma entrada, mesma saída,
sem rede, banco, relógio global ou arquivo.

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Intervalo:
    inicio: datetime
    fim: datetime

    def __post_init__(self) -> None:
        if self.inicio >= self.fim:
            raise ValueError("inicio deve ser anterior ao fim")


def sobrepoe(a: Intervalo, b: Intervalo) -> bool:
    """Compara intervalos semiabertos: [inicio, fim)."""
    return a.inicio < b.fim and b.inicio < a.fim
```

Por que não testar apenas se o início de um intervalo está dentro do outro?
Porque isso falha quando um intervalo contém completamente o outro. A expressão
acima é simétrica e cobre todos os casos.

### Execute e observe

Salve como `intervalos.py` e execute:

```python
from datetime import datetime as dt

from intervalos import Intervalo, sobrepoe

a = Intervalo(dt.fromisoformat("2026-10-03T10:00"), dt.fromisoformat("2026-10-03T11:00"))
b = Intervalo(dt.fromisoformat("2026-10-03T10:30"), dt.fromisoformat("2026-10-03T11:30"))
c = Intervalo(dt.fromisoformat("2026-10-03T11:00"), dt.fromisoformat("2026-10-03T12:00"))

print(sobrepoe(a, b))  # True: existe conflito
print(sobrepoe(a, c))  # False: intervalos adjacentes
```

Uma classe imutável (`frozen=True`) impede que `inicio` seja alterado sem
revalidar `fim`. Isso reduz estados inválidos, mas não resolve sozinho fusos
horários. Em um sistema real, decida explicitamente se aceita datas sem fuso.

## 3. Responsabilidades, coesão e acoplamento

**Coesão** mede quanto as responsabilidades de um módulo pertencem ao mesmo
assunto. **Acoplamento** mede quanto um componente depende dos detalhes de outro.

```text
Interface (CLI/HTTP)
        |
        v
Caso de uso (reservar sala)
        |
        v
Domínio (intervalo e conflito)
        ^
        |
Infraestrutura (SQLite implementa repositório)
```

A seta representa dependência de código. A regra de conflito não deve importar
HTTP nem SQLite. Assim, ela pode ser usada por CLI, API ou teste.

### Uma interface pequena para a fronteira

```python
from typing import Protocol


class RepositorioReservas(Protocol):
    def existem_conflitos(self, sala_id: int, intervalo: Intervalo) -> bool: ...
    def adicionar(self, sala_id: int, intervalo: Intervalo) -> int: ...


class HorarioIndisponivel(Exception):
    pass


def reservar(
    repositorio: RepositorioReservas,
    sala_id: int,
    intervalo: Intervalo,
) -> int:
    if repositorio.existem_conflitos(sala_id, intervalo):
        raise HorarioIndisponivel("horário indisponível")
    return repositorio.adicionar(sala_id, intervalo)
```

O caso de uso conhece as operações de que precisa, não a biblioteca do banco.
Isso é **inversão de dependência** em pequena escala. Não crie uma interface
para cada função por costume; crie uma fronteira quando houver uma dependência
externa, uma variação real ou um ganho claro de teste.

### Sinais de design frágil

- uma função valida HTTP, calcula regra, grava SQL e formata HTML;
- mudar o formato de log exige mudar a regra de negócio;
- um teste de soma precisa iniciar banco e rede;
- módulos importam uns aos outros em ciclo;
- a mesma invariante é implementada com regras diferentes em três telas;
- uma classe recebe muitas dependências não relacionadas;
- o nome do método explica tecnologia, mas não intenção (`runSql2`).

## 4. Testes: o que cada camada prova

| Tipo | Fronteira | Exemplo | Custo e velocidade |
|------|----------|---------|--------------------|
| Unidade | uma regra isolada | conflito de intervalos | muito baixo, muito rápido |
| Integração | componentes reais juntos | repositório + SQLite temporário | médio |
| Contrato | formato entre consumidor e provedor | corpo e status da API | médio |
| Ponta a ponta | fluxo externo completo | navegador cria e conclui tarefa | alto, mais lento |

Muitos testes pequenos protegem regras; alguns testes de integração protegem
fronteiras; poucos testes ponta a ponta protegem jornadas críticas. Isso é uma
heurística, não uma cota fixa.

### Arrange, Act, Assert

```python
import unittest
from datetime import datetime as dt

from intervalos import Intervalo, sobrepoe


class IntervaloTests(unittest.TestCase):
    def test_intervalos_adjacentes_nao_conflitam(self) -> None:
        # Arrange
        existente = Intervalo(dt(2026, 10, 3, 10), dt(2026, 10, 3, 11))
        novo = Intervalo(dt(2026, 10, 3, 11), dt(2026, 10, 3, 12))

        # Act
        resultado = sobrepoe(existente, novo)

        # Assert
        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
```

Salve como `test_intervalos.py` ao lado do primeiro arquivo:

```bash
python3 -m unittest -v test_intervalos.py
```

Saída relevante esperada:

```text
test_intervalos_adjacentes_nao_conflitam ... ok
Ran 1 test
OK
```

O teste descreve comportamento público. Renomear uma variável interna não
deve quebrá-lo.

### Particionamento e valores de fronteira

Para um título de 1 a 120 caracteres, não teste apenas `"Comprar leite"`.

| Partição | Casos representativos |
|----------|------------------------|
| Inválida abaixo | `None`, outro tipo, `""`, somente espaços |
| Válida mínima | 1 caractere após normalização |
| Válida comum | 20 caracteres |
| Válida máxima | 120 caracteres |
| Inválida acima | 121 caracteres |

Para intervalos, cubra: igualdade, adjacência, sobreposição à esquerda,
à direita, contenção e intervalo invertido.

### Qualidades de um teste confiável

- **determinístico:** não depende da ordem, internet ou segundo atual;
- **isolado:** cria seus próprios dados e limpa recursos;
- **específico:** falha por uma razão compreensível;
- **rápido o suficiente:** pode ser executado no ciclo de desenvolvimento;
- **representativo:** prova risco real, não apenas linhas executadas.

Não use `sleep(2)` para esperar uma condição se puder aguardar um evento com
timeout. Não compartilhe banco entre testes. Não dependa de API pública em uma
suíte unitária.

## 5. Dublês de teste sem autoengano

Termos comuns:

- **fake:** implementação simplificada funcional, como repositório em memória;
- **stub:** devolve respostas predeterminadas;
- **spy:** registra chamadas para inspeção;
- **mock:** valida interações esperadas.

Uma fake permite testar o caso de uso rapidamente:

```python
class RepositorioEmMemoria:
    def __init__(self) -> None:
        self.itens: list[tuple[int, Intervalo]] = []

    def existem_conflitos(self, sala_id: int, intervalo: Intervalo) -> bool:
        return any(
            id_existente == sala_id and sobrepoe(existente, intervalo)
            for id_existente, existente in self.itens
        )

    def adicionar(self, sala_id: int, intervalo: Intervalo) -> int:
        self.itens.append((sala_id, intervalo))
        return len(self.itens)
```

Ela não prova que SQL, transação ou constraints estão corretos. Para isso,
escreva um teste de integração com SQLite real e arquivo temporário. Dublês
demais podem produzir uma suíte verde para um sistema que não integra.

## 6. TDD e refatoração segura

TDD é um ciclo de feedback:

1. **vermelho:** escreva o menor teste que descreve o próximo comportamento;
2. **verde:** implemente a solução mais simples que atende ao contrato;
3. **refatore:** melhore estrutura sem mudar o comportamento;
4. repita.

Confirme que o teste vermelho falha pela razão esperada. Um teste que já nasce
verde pode não exercer a mudança. Durante a refatoração, não misture uma nova
regra: mudança estrutural e mudança comportamental juntas dificultam diagnóstico.

TDD é especialmente útil para regras, parsers, conversões e limites. Uma tela
exploratória pode ser prototipada primeiro e estabilizada depois com testes.

## 7. Erros são parte do contrato

Classifique a falha antes de tratá-la:

| Categoria | Exemplo | Resposta adequada |
|-----------|---------|-------------------|
| Entrada inválida | data invertida | erro descritivo; não tentar novamente |
| Regra de domínio | horário ocupado | erro esperado de negócio |
| Dependência transitória | timeout do banco remoto | timeout e retry limitado, se seguro |
| Dependência permanente | credencial inválida | falhar e alertar operador |
| Defeito | variável inesperadamente `None` | log técnico, resposta genérica, correção |

Não capture `Exception` para continuar como se nada tivesse acontecido. Isso
apaga o sinal de defeito e pode confirmar uma operação incompleta.

### Timeout, retry e idempotência

Toda chamada externa deve ter timeout. Retry precisa responder a quatro
perguntas:

1. A falha é provavelmente transitória?
2. Repetir a operação é seguro?
3. Quantas tentativas e qual atraso máximo?
4. Como a falha final será observada?

Repetir um `GET` normalmente é seguro. Repetir uma cobrança `POST` sem chave de
idempotência pode duplicar o efeito. Use atraso crescente com aleatoriedade
controlada em sistemas distribuídos, mas imponha limite total.

## 8. Configuração e segredos

Configuração muda entre ambientes; regra de negócio não deveria mudar.

```python
import os


def read_port() -> int:
    raw = os.environ.get("APP_PORT", "8000")
    try:
        port = int(raw)
    except ValueError as exc:
        raise SystemExit("APP_PORT deve ser inteiro") from exc
    if not 1 <= port <= 65535:
        raise SystemExit("APP_PORT deve estar entre 1 e 65535")
    return port
```

Valide ao iniciar e falhe com mensagem acionável. Um erro de configuração
descoberto no primeiro request é mais caro de diagnosticar.

- Use padrões seguros: bind em `127.0.0.1`, debug desligado, limites explícitos.
- Forneça segredos em runtime; nunca os grave no repositório ou na imagem.
- Não registre token, senha, cookie, chave, corpo sensível ou dado pessoal.
- Diferencie configuração secreta de configuração comum.

## 9. Observabilidade: saber o que aconteceu

Logs contam eventos; métricas mostram tendências; traces conectam etapas de uma
operação distribuída.

```json
{
  "timestamp": "2026-10-03T14:31:52Z",
  "level": "info",
  "event": "reservation_created",
  "reservation_id": 42,
  "room_id": 12,
  "request_id": "01J...",
  "duration_ms": 7
}
```

Um bom evento tem nome estável e campos pesquisáveis. A mensagem
`"deu erro"` não diz qual operação, qual dependência ou qual correlação.
Stack trace pertence ao log restrito do operador, não à resposta do usuário.

Perguntas que o sistema deveria permitir responder:

- qual proporção de requests falhou nos últimos cinco minutos?
- a latência aumentou em qual etapa?
- todas as linhas de um request compartilham o mesmo `request_id`?
- a falha foi entrada inválida, dependência ou defeito?

## 10. Segurança como qualidade do software

Mesmo um projeto introdutório deve:

- validar tipo, formato, tamanho e faixa no servidor;
- usar consultas SQL parametrizadas;
- codificar saída no contexto correto;
- aplicar menor privilégio a processo, arquivo e banco;
- limitar corpo, tempo, concorrência e filas;
- não revelar detalhes internos em erros externos;
- fixar e atualizar dependências por processo controlado;
- manter testes para correções de falhas;
- documentar ameaças que ficaram fora do escopo.

Validação no navegador melhora a experiência, mas não é uma fronteira de
confiança. Qualquer cliente pode enviar HTTP diretamente ao servidor.

## 11. Compatibilidade e evolução

Uma API pública é um contrato. Mudanças potencialmente incompatíveis incluem:

- remover ou renomear campo;
- mudar tipo (`id` numérico para texto);
- tornar obrigatório um campo antes opcional;
- reinterpretar um status ou uma unidade;
- alterar ordenação quando consumidores dependem dela.

Prefira mudança aditiva, período de depreciação e migração documentada.
Versionar toda pequena alteração também tem custo. Primeiro descubra se o
contrato realmente foi quebrado.

Para dados persistidos, mudança de schema exige:

1. migração versionada;
2. compatibilidade durante deploy quando necessário;
3. backup e restauração testados;
4. plano de rollback realista;
5. verificação pós-migração.

## 12. Depuração orientada por hipótese

Evite mudar código aleatoriamente. Use este ciclo:

1. descreva esperado e observado;
2. reduza para a menor reprodução;
3. identifique a primeira camada em que o valor diverge;
4. formule uma hipótese falsificável;
5. adicione uma observação: teste, log, debugger ou consulta;
6. altere uma variável por vez;
7. corrija a causa;
8. escreva teste de regressão;
9. remova instrumentação temporária e documente a conclusão.

Exemplo de hipótese ruim: “o banco está estranho”. Hipótese testável: “a
segunda inserção não foi confirmada porque a exceção saiu do context manager
antes do `COMMIT`”.

## 13. Revisão de código

Revise por risco, não por preferência estética:

1. O comportamento satisfaz cada critério de aceite?
2. Invariantes estão protegidas no servidor e, quando possível, no banco?
3. Entradas, limites, erros e estados parciais foram considerados?
4. A transação cobre toda a mudança que precisa ser atômica?
5. Arquivos, conexões e locks são liberados em sucesso e falha?
6. Há timeout e cancelamento em fronteiras externas?
7. Os testes falhariam se a regra fosse removida?
8. Logs ou mensagens expõem dados?
9. Configuração, migração e operação foram atualizadas?
10. A mudança pode ser revertida com segurança?

Comentário útil explica consequência: “Se duas requisições passarem por esta
consulta antes do insert, ambas podem reservar. Podemos impor unicidade ou
serializar a decisão na mesma transação?”

## 14. Laboratório guiado — reserva de salas

### Nível 1: regra pura

1. Implemente `Intervalo` e `sobrepoe`.
2. Escreva testes para seis relações de intervalo.
3. Prove que adjacência não conflita.
4. Faça intervalo vazio/invertido falhar na construção.

**Critério:** testes não usam arquivo, rede, `sleep` ou relógio atual.

### Nível 2: caso de uso

1. Crie a interface pequena do repositório.
2. Implemente `RepositorioEmMemoria`.
3. Implemente `reservar` e `cancelar` usando IDs, nunca posição da lista.
4. Diferencie `HorarioIndisponivel` de `ReservaNaoEncontrada`.
5. Teste que conflito não altera o repositório.

**Critério:** a regra pode ser chamada por CLI ou HTTP sem ser alterada.

### Nível 3: persistência e concorrência

1. Implemente repositório SQLite com SQL parametrizado.
2. Use banco temporário em cada teste de integração.
3. Garanta atomicidade entre verificar conflito e inserir.
4. Execute duas tentativas concorrentes para o mesmo horário.
5. Documente como o banco impede duas confirmações incompatíveis.

**Critério:** depois do teste concorrente existe no máximo uma reserva para o
mesmo intervalo e o resultado é repetível.

## 15. Exercícios de fixação

### Essenciais

1. Reescreva “o sistema deve ser seguro” como cinco critérios observáveis.
2. Crie a tabela de partições para uma quantidade entre 1 e 99.
3. Explique por que cobertura de linhas alta não prova correção.
4. Classifique cinco erros do TaskBoard como entrada, domínio, dependência ou defeito.
5. Refatore uma função longa somente depois de protegê-la com teste.

### Intermediários

1. Injete um relógio em vez de chamar a hora global dentro da regra.
2. Implemente retry apenas para um erro transitório simulado e limite o tempo total.
3. Crie log JSON com `request_id` sem registrar o corpo da requisição.
4. Escreva um teste que demonstra rollback de duas escritas quando a segunda falha.
5. Compare um fake em memória com SQLite e liste comportamentos que ele não reproduz.

### Avançados

1. Modele uma chave de idempotência para criação de reserva.
2. Defina uma estratégia de migração aditiva sem indisponibilidade.
3. Gere carga concorrente e meça taxa de sucesso e latência p95.
4. Faça uma revisão ameaça→controle→teste para a entrada de reservas.
5. Produza um registro de decisão explicando por que escolheu SQLite ou outro banco.

## Critério de conclusão

- [ ] Consigo transformar uma frase vaga em cenários e limites verificáveis.
- [ ] Sei dizer onde uma invariante deve ser protegida e por quê.
- [ ] Escrevo testes de unidade e integração que falham pela razão correta.
- [ ] Sei quando um fake ajuda e o que ele deixa de provar.
- [ ] Diferencio erro esperado, falha transitória e defeito.
- [ ] Uso timeout e retry somente com limite e sem duplicar efeitos.
- [ ] Consigo depurar formulando e testando hipóteses.
- [ ] Refatoro com os testes verdes antes e depois.
- [ ] Minha entrega inclui comandos de execução, testes, limitações e operação.

Você concluiu este capítulo quando consegue defender as decisões e demonstrar
o comportamento, não apenas quando o código “roda na sua máquina”.
