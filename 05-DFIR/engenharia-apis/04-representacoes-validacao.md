# 04 — Representações, schemas e validação

JSON é uma codificação. O contrato precisa definir forma, limites e significado:
tipos, obrigatoriedade, null, precisão, unidade, enum, propriedades desconhecidas
e invariantes entre campos. Validação robusta ocorre em camadas e não confunde
normalização com segurança.

## Objetivos

- projetar schemas distintos para comando, recurso e evento;
- aplicar validação sintática, estrutural, semântica e de negócio;
- definir ausência, null, default e campos desconhecidos;
- limitar tamanho, profundidade e cardinalidade;
- preservar compatibilidade e precisão entre linguagens.

## 1. Representações diferentes do mesmo conceito

~~~json
{
  "title": "Guia de APIs",
  "status": "draft",
  "tags": ["design", "http"]
}
~~~

Uma criação pode aceitar apenas title e tags. A resposta inclui id, status,
version e timestamps. O evento inclui apenas dados necessários ao consumidor.
Reusar um único modelo gera mass assignment, campos somente leitura aceitos e
eventos acoplados ao formato de consulta.

~~~text
CreateItem != UpdateItem != ItemView != ItemCreatedEvent
~~~

Compartilhe conceitos deliberadamente, não classes inteiras por conveniência.

## 2. Camadas de validação

1. **Transporte:** tamanho, Content-Type e codificação são aceitos?
2. **Sintaxe:** o documento pode ser decodificado?
3. **Estrutura:** tipos, campos e limites seguem o schema?
4. **Semântica local:** formato, intervalo e relação entre campos fazem sentido?
5. **Negócio:** a operação preserva invariantes no estado atual?
6. **Autorização:** a identidade pode executar a ação nesse objeto e propriedade?
7. **Destino:** o valor será codificado corretamente para SQL, HTML, log ou URL?

Validar e-mail não autoriza contato; escapar HTML não torna a string segura em
SQL. Cada camada responde uma pergunta diferente.

## 3. Ausente, null e default

Em atualização parcial:

- campo ausente pode significar “não alterar”;
- campo com null pode significar “limpar”;
- valor vazio pode ser dado válido ou inválido;
- default aplicado pelo servidor pode mudar no futuro.

Declare a semântica. Se middlewares ou geradores removem null, o contrato de
PATCH pode ser destruído. Em resposta, omitir campo e retornar null também pode
ter significados distintos para consumidores.

## 4. Números, datas e Unicode

JSON possui number, mas linguagens têm limites diferentes. Inteiros maiores que
2^53−1 perdem precisão em Number do JavaScript; IDs numéricos grandes devem ser
strings quando precisão integral é essencial. Valores monetários usam unidade
menor inteira ou decimal explícito, nunca float sem política.

Datas devem incluir offset ou Z quando representam instante. Data civil,
duração e timestamp são conceitos diferentes. Normalize para comparação, mas
preserve requisitos de exibição fora do domínio.

Comprimento de string pode significar bytes, code points ou grapheme clusters.
Limite de armazenamento e limite de produto não são necessariamente iguais.
Normalize Unicode somente com decisão documentada; duas sequências visualmente
iguais podem ter bytes diferentes, afetando hash e assinatura.

## 5. Propriedades desconhecidas

Rejeitar extras protege comandos contra erro de digitação e mass assignment.
Tolerar extras ajuda leitores a sobreviver a evolução aditiva. Assim, uma
política comum é:

- comandos de escrita: schema fechado;
- respostas/eventos consumidos: leitor tolerante a campos novos;
- extensões: namespace explícito e limites.

Isso não é universal, mas precisa ser consistente. Um proxy que remove campos
desconhecidos pode impedir evolução transparente.

## 6. Limites de recursos

Defina:

- tamanho total do corpo;
- comprimento de strings e quantidade de itens;
- profundidade e número de propriedades;
- intervalo numérico e escala decimal;
- tamanho de lote e complexidade;
- tempo gasto em parse/validação.

Schema válido ainda pode consumir memória ou CPU excessiva. Faça rejeição cedo,
antes de carregar corpo enorme. Compressão requer limite após descompressão para
evitar expansão inesperada.

## 7. Normalização e canonicalização

Normalizar title pode remover espaços externos e converter sequências internas.
Canonicalização para digest precisa ser determinística: ordem de propriedades,
codificação, números e Unicode importam. Nunca calcule idempotência sobre JSON
bruto se duas serializações equivalentes devem representar a mesma intenção.

~~~python
def canonical_command(title: str) -> dict[str, str]:
    normalized = " ".join(title.split())
    if not 3 <= len(normalized) <= 80:
        raise ValueError("title fora do limite")
    return {"title": normalized}
~~~

## 8. Compatibilidade

Adicionar campo opcional só é compatível se leitores ignoram extras. Restringir
enum, reduzir maxLength, trocar unidade ou mudar default pode ser breaking.
Compatibilidade sintática não prova compatibilidade semântica. Teste exemplos de
clientes reais e faça diff do schema publicado.

## Falhas comuns

| Falha | Risco | Correção |
|---|---|---|
| mesmo DTO em todas as bordas | mass assignment/acoplamento | schemas por intenção |
| float para dinheiro | arredondamento | inteiro menor/decimal |
| sem limite de lista | exaustão | teto e paginação |
| sanitização genérica | falsa segurança | encoding no destino |
| null não definido | remoção acidental | semântica explícita |
| enum fechado no cliente | quebra aditiva | fallback seguro |

## Exercícios

### Nível 1 — quatro schemas

Escreva Create, Patch, View e Event para um item. **Aceite:** server-only, segredo,
null e propriedades desconhecidas estão definidos.

### Nível 2 — fronteiras

Teste corpo grande, lista vazia/máxima, Unicode composto, inteiro maior que 2^53
e campo extra. **Aceite:** resultado e código estável estão documentados.

### Nível 3 — compatibilidade

Evolua o schema por três versões e execute clientes antigo e novo. **Aceite:**
identifique quebra sintática, semântica e de limite separadamente.

## Checklist

- [ ] Comando, recurso e evento não compartilham DTO por acidente.
- [ ] Ausente, null, vazio e default têm significado.
- [ ] Precisão, unidade, data e Unicode estão definidos.
- [ ] Há limites de corpo, coleção, profundidade e tempo.
- [ ] Escrita rejeita propriedades não permitidas.
- [ ] Compatibilidade é testada com consumidores.

