# 10 — Internacionalização, Unicode, tempo e dinheiro

Internacionalização (`i18n`) prepara a arquitetura para idiomas e convenções
diferentes. Localização (`l10n`) adapta mensagens, formatos e conteúdo para um
contexto. Traduzir textos no fim do projeto não corrige um banco que perdeu o
fuso, um cálculo monetário binário ou um layout que presume palavras curtas.

O [Study Desk](projetos/study-desk/README.md) parece simples, mas já manipula
títulos em Unicode, duração, datas de estudo e mensagens com quantidades. Se no
futuro ele tiver planos pagos, dinheiro introduzirá moeda, arredondamento e
auditoria. Esses conceitos devem permanecer tipados no domínio e ser formatados
somente nas bordas.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. separar texto traduzível, dado do usuário e identificador estável;
2. usar catálogos com placeholders nomeados, plural e contexto;
3. explicar bytes, pontos de código, grafemas e normalização Unicode;
4. distinguir instante, data civil, horário local, fuso, offset e duração;
5. modelar recorrência sem presumir que um dia sempre tem 24 horas;
6. representar dinheiro com quantia, moeda e política de arredondamento;
7. formatar sem converter o valor interno em texto prematuramente;
8. testar pseudolocalização, fronteiras de fuso e arredondamentos adversos.

## Pré-requisitos e modelo mental

Você precisa conhecer tipos, validação, serialização e interfaces dos capítulos
anteriores. Não é necessário implementar algoritmos de Unicode, regras de fusos
ou formatação monetária: use bibliotecas mantidas para isso.

```text
valor de domínio tipado
  -> armazenamento sem perda
  -> preferência explícita (locale/fuso/moeda)
  -> formatação na borda
  -> texto e layout variáveis
  -> entrada localizada validada
  -> conversão de volta ao tipo de domínio
```

O princípio central é **não confundir representação com valor**. `2026-10-05`,
`05/10/2026` e `10/5/2026` podem apresentar uma data, mas a string formatada não
deve substituir o tipo de data. `R$ 10,99` é apresentação de uma quantia em BRL,
não um número genérico que pode ser somado a `US$ 10.99`.

## Mensagens não são fragmentos concatenáveis

Extraia mensagens para catálogos por identificador estável:

```text
session.saved = Sessão registrada.
session.count = {count, plural,
  =0 {Nenhuma sessão}
  one {# sessão}
  other {# sessões}}
```

A sintaxe concreta depende da biblioteca, mas o contrato deve permitir que a
tradução controle toda a frase. Evite:

```javascript
// Ruim: presume ordem, espaço, plural e posição do número.
message = count + " sessões encontradas em " + date;
```

Placeholders nomeados preservam significado. Documente se `title` é nome de uma
sessão e se `count` é quantidade. Dê contexto quando a mesma palavra pode ser
verbo ou substantivo. Não use o texto em português como chave: corrigir uma frase
não deveria invalidar todos os catálogos.

Plural não é apenas singular versus plural. Regras variam por idioma e quantidade;
use o mecanismo plural da biblioteca. Gênero, formalidade e seleção contextual
também não devem ser obtidos concatenando pedaços. Tradutores precisam ver a
mensagem inteira, comentário, placeholders e onde ela aparece.

Separe:

- texto da interface, que pertence ao catálogo;
- conteúdo criado pela pessoa, que não deve ser traduzido;
- identificadores e enumerações estáveis, que podem mapear para rótulos;
- mensagens técnicas, que podem ter representação local e código estável.

## Unicode sem simplificações perigosas

“Caractere” pode significar unidades diferentes:

- **byte:** unidade da codificação, como UTF-8;
- **ponto de código:** valor abstrato Unicode;
- **unidade de código:** representação usada por um runtime;
- **grapheme cluster:** o que a pessoa percebe como um caractere.

Um emoji pode usar vários pontos de código; uma letra acentuada pode ser um ponto
pré-composto ou letra mais marca combinante. Por isso, `length` pode contar algo
diferente de “quantos caracteres visíveis”. Limites de armazenamento em bytes,
limites de protocolo e limites percebidos pela pessoa são requisitos distintos.

Normalização transforma sequências canonicamente equivalentes para uma forma
consistente quando o domínio exige comparação. Não normalize às cegas para “tirar
acentos”: isso altera dados e pode unir nomes diferentes. Defina a política para
busca, ordenação e unicidade separadamente.

Maiúsculas e minúsculas também dependem de idioma. Não use conversão ingênua como
regra universal de identidade. Para IDs técnicos, prefira um alfabeto restrito
declarado. Para títulos do Study Desk, preserve a escrita e use comparação
apropriada ao recurso: busca tolerante não precisa mudar o valor armazenado.

Direção de escrita afeta layout e conteúdo misto. Evite ícones direcionais
hardcoded quando “início/fim” é a intenção; prefira propriedades lógicas como
`margin-inline-start`. Teste uma localidade da direita para a esquerda mesmo que
ela não esteja no primeiro lançamento.

## Locale é preferência, não identidade fixa

Idioma da interface, idioma do conteúdo, locale de formatação, fuso e moeda são
preferências diferentes. Uma pessoa pode usar interface em português, números
brasileiros, estudar conteúdo em inglês e viajar para outro fuso. Permita override
e registre a origem da escolha: usuário, configuração ou padrão.

No JavaScript, `Intl` oferece formatadores:

```javascript
const formatMinutes = new Intl.NumberFormat("pt-BR", {
  style: "unit",
  unit: "minute",
  unitDisplay: "long",
});

const formatDate = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "long",
  timeStyle: "short",
  timeZone: "America/Sao_Paulo",
});

console.log(formatMinutes.format(45));
console.log(formatDate.format(new Date("2026-10-05T18:30:00Z")));
```

Instanciar formatadores repetidamente pode ter custo; reutilize-os por locale e
opções quando medição justificar. Não dependa do texto formatado em testes exatos
entre runtimes sem controlar locale e dados de localização. Teste propriedades e
exemplos no ambiente suportado.

Entrada localizada exige política explícita. Um campo decimal `1,5` em um locale
pode significar um e meio; uma função genérica que só troca vírgula por ponto
falha com agrupamento e caracteres diferentes. Use controles e bibliotecas que
conheçam o locale ou aceite um formato canônico claramente documentado.

## O vocabulário correto para tempo

Tempo reúne conceitos que não são intercambiáveis:

| Conceito | Exemplo | Uso |
|---|---|---|
| instante | `2026-10-05T18:30:00Z` | ponto único na linha do tempo |
| data civil | `2026-10-05` | aniversário, dia de estudo |
| hora local | `15:30` | horário sem data/fuso |
| data-hora local | `2026-10-05 15:30` | ainda ambígua sem zona |
| offset | `-03:00` | diferença de UTC naquele instante |
| fuso IANA | `America/Sao_Paulo` | conjunto histórico/futuro de regras |
| duração | `45 minutos` | quantidade de tempo transcorrido |
| período civil | `1 mês` | avanço de calendário, tamanho variável |

Um offset não substitui um fuso. Regras civis podem mudar e um fuso pode usar
offsets diferentes ao longo do tempo. Uma recorrência “toda segunda às 09:00 em
America/Sao_Paulo” precisa manter a hora civil e o fuso; guardar apenas o primeiro
instante em UTC e somar sete vezes 24 horas pode deslocar a reunião em regiões com
mudanças sazonais.

Defina a semântica antes de escolher o tipo:

- sessão concluída: instante de início/fim ou data local + duração?
- meta diária: qual fuso determina a virada do dia?
- lembrete: acompanha o fuso original ou o fuso atual da pessoa?
- expiração: duração exata desde um instante, não “amanhã” ambíguo;
- relatório mensal: mês civil em qual fuso?

Ao receber uma data-hora local em região com transição sazonal, o horário pode não
existir ou ocorrer duas vezes. A biblioteca deve exigir política: rejeitar e pedir
outro horário, escolher ocorrência anterior/posterior ou ajustar conscientemente.
Não deixe um padrão invisível decidir uma obrigação importante.

Para medir duração de uma operação, use o relógio monotônico oferecido pelo
runtime; o relógio civil pode ser corrigido. Para registrar quando algo aconteceu,
use instante de relógio civil. Testes devem injetar um relógio, nunca depender de
“agora” real.

## Dinheiro é quantia mais moeda mais política

Ponto flutuante binário não representa exatamente muitos decimais. Demonstração:

```javascript
console.log(0.1 + 0.2); // normalmente 0.30000000000000004
```

Uma representação comum usa unidades menores inteiras:

```text
Money(amountMinor=1099, currency="BRL")
```

Ela funciona quando a escala da moeda e do caso de uso é conhecida. Em outros
domínios, use decimal arbitrário com escala e arredondamento explícitos. O tipo
deve impedir somar moedas distintas:

```python
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Não é possível somar moedas diferentes.")
        return Money(self.amount + other.amount, self.currency)

    def rounded(self, scale: str = "0.01") -> "Money":
        value = self.amount.quantize(Decimal(scale), rounding=ROUND_HALF_EVEN)
        return Money(value, self.currency)
```

O exemplo é executável e imutável, mas não define toda regra financeira. O produto
precisa registrar:

- quando arredondar: por item, subtotal ou total;
- modo de arredondamento exigido;
- escala da operação e da apresentação;
- limite e risco de overflow nas unidades menores;
- tratamento de valores negativos, reembolso e desconto;
- origem, instante e precisão de taxa de câmbio;
- distribuição de centavos restantes entre parcelas.

Conversão não é apenas multiplicar por taxa. `10 BRL` e `10 USD` não podem ser
somados antes de escolher moeda-alvo, taxa, fonte e instante. Preserve quantia
original e conversão para auditoria. Formatação vem depois:

```javascript
const brl = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});
console.log(brl.format(10.99));
```

O uso de `Number` acima é aceitável apenas para apresentar um valor pequeno já
calculado sob política conhecida; não transforme essa linha no motor monetário.

## As cinco linguagens: tipos antes de strings

| Linguagem | Unicode/texto | Tempo moderno | Dinheiro exato |
|---|---|---|---|
| Python | `str` + `unicodedata` | `datetime`, `zoneinfo` | `decimal.Decimal` ou unidades menores |
| Java | `String`, `Normalizer` | `java.time` | `BigDecimal` + código de moeda |
| C | biblioteca Unicode escolhida | biblioteca/contrato explícito | inteiro verificado ou decimal escolhido |
| C# | `string`, APIs de globalização | `DateTimeOffset`, zonas e tipos adequados | `decimal` + moeda |
| JavaScript | `String`, `Intl` | `Date` e biblioteca/tipos adequados ao domínio | unidades menores/decimal dedicado |

Nenhuma opção remove a necessidade de semântica. Em Java, `BigDecimal` criado a
partir de `double` pode herdar imprecisão; prefira string ou inteiro. Em C, defina
codificação na fronteira e verifique overflow. Em C#, `decimal` não carrega moeda.
Em Python, `datetime` ingênuo não sabe o fuso. Em JavaScript, `Date` representa um
instante, mas sua API histórica mistura apresentação e mutação; encapsule-a.

## Pseudolocalização e estratégia de teste

Pseudolocalização transforma mensagens para revelar texto hardcoded, corte e
concatenação, por exemplo:

```text
Registrar sessão -> [Řëĝïšţřåř šëššåõ…………]
```

Ela deve preservar placeholders e marcação. Crie também uma variante de direção
oposta se o produto pretende suportá-la. Não use pseudotexto como substituto de
revisão linguística; ele encontra defeitos estruturais.

Matriz mínima de testes:

- contagens `0`, `1`, `2`, `11`, `101` em locales com regras distintas;
- string vazia, acento composto/decomposto, emoji combinado e texto RTL;
- instante perto da meia-noite em dois fusos;
- horário local inexistente e duplicado em região apropriada;
- recorrência atravessando mudança sazonal;
- valores `0`, negativo, limite, meio centavo e divisão com resto;
- troca independente de idioma, fuso e moeda;
- importação/exportação mantendo valores canônicos.

Golden tests de strings podem ser úteis para um catálogo controlado, mas tornam-se
frágeis se verificarem saída inteira de bibliotecas cujo banco linguístico muda.
Teste contrato, locale controlado e exemplos críticos.

## Falhas frequentes e diagnóstico

| Sintoma | Causa provável | Evidência | Correção |
|---|---|---|---|
| frase soa invertida | concatenação de fragmentos | chave e placeholders | mensagem inteira no catálogo |
| título “igual” não é encontrado | normalização/comparação inconsistente | pontos de código | política única de busca, sem alterar original |
| sessão cai no dia errado | fuso implícito | instante, zona e locale | regra explícita da virada civil |
| recorrência muda de horário | soma de duração em UTC | série antes/depois da transição | recorrência civil com fuso |
| total difere por centavo | arredondamento em etapas diferentes | valores antes/depois | política documentada e testada |
| layout corta botão | texto fixo/dimensão rígida | pseudolocalização | layout fluido e expansão |

Logs devem registrar códigos, tipos e zonas necessárias ao diagnóstico, não
conteúdo pessoal. Para dinheiro, registre IDs da regra e da taxa, não números de
pagamento. Para texto, não copie títulos do Study Desk para telemetria.

## Exercícios em três níveis

### Nível 1 — Catálogo e formatação

Extraia dez mensagens do Study Desk, incluindo zero/um/muitos. Formate número,
data e duração em dois locales; aplique pseudolocalização e teste texto expandido.

**Critérios de aceite:** nenhum fragmento é concatenado; placeholders têm nomes;
conteúdo da pessoa não é traduzido; troca de locale não muda valores armazenados;
layout continua operável; testes cobrem plural e fallback de chave ausente.

### Nível 2 — Tempo e recorrência

Modele sessão concluída, meta diária e lembrete recorrente. Injete relógio e fuso,
gere ocorrências em uma região com mudança sazonal e explique a política para
horário inexistente/ambíguo.

**Critérios de aceite:** tipos distinguem instante, data e duração; nenhuma função
consulta “agora” escondido; serialização preserva fuso quando necessário; relatório
diário declara zona; testes cobrem meia-noite e transição sazonal.

### Nível 3 — Dinheiro auditável

Implemente um tipo `Money` em uma das cinco linguagens, com soma, desconto,
rateio e conversão registrada. Integre uma tela de plano hipotético ao Study Desk.

**Critérios de aceite:** moedas diferentes não são somadas; arredondamento e escala
são explícitos; rateio preserva o total; conversão guarda valor original, taxa,
fonte e instante; UI formata por locale; testes cobrem limites e restos; nenhum
dado sensível aparece em logs.

## Checklist de conclusão

- [ ] Mensagens completas vivem em catálogos com placeholders nomeados.
- [ ] Plural e contexto usam recurso da biblioteca, não condicionais improvisadas.
- [ ] Sei distinguir bytes, pontos de código e grafemas.
- [ ] Política de normalização, busca e unicidade é explícita.
- [ ] Idioma, locale, fuso e moeda são preferências independentes.
- [ ] Instante, data civil, horário local, fuso, duração e período não se confundem.
- [ ] Recorrência civil preserva hora local e zona quando esse é o requisito.
- [ ] Dinheiro inclui quantia, moeda, escala e arredondamento.
- [ ] Valores internos permanecem tipados; formatação acontece na borda.
- [ ] Pseudolocalização e casos adversos fazem parte dos testes.
