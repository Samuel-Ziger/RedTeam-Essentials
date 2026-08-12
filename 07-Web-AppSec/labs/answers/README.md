# Respostas orientativas dos labs Web

> Use somente **depois** de executar o lab. As respostas descrevem invariantes
> pedagógicas, não tokens, IDs ou paths que podem variar entre imagens.

## Lab 01 — DVWA SQLi

Uma resposta satisfatória demonstra que um valor legítimo retorna um registro e
que a condição booleana no parâmetro `id` altera a cardinalidade da resposta.
Em Medium, deve mostrar que restringir o frontend não substitui parametrização
no servidor. Evidência mínima: método, path, parâmetro, status, quantidade
aproximada de registros sintéticos e cookies redatados.

**Causa:** concatenação de entrada em SQL. **Correção:** query parametrizada,
conta de banco com menor privilégio, tratamento uniforme de erros e teste de
regressão. **Telemetria:** access log com caracteres/encoding anômalos, erros do
banco e variação incomum de tamanho/latência. Um falso positivo possível é uma
busca legítima contendo apóstrofo.

## Lab 02 — Juice Shop XSS

Uma resposta satisfatória identifica **source**, transformação e **sink**, além
do contexto HTML/atributo/JavaScript. Um `alert` local ou challenge marcado é
evidência suficiente; não há necessidade de coletar cookies.

**Correção:** output encoding contextual, APIs DOM seguras, sanitização quando
HTML for necessário, CSP com nonce e Trusted Types onde suportado. **Telemetria:**
requisições com markup são apenas sinal; XSS DOM pode não chegar ao servidor e
exige CSP reports ou instrumentação do cliente. Texto legítimo com `<` é falso
positivo comum.

## Lab 03 — VAmPI BOLA

Uma resposta satisfatória mantém dois principals separados e compara a matriz
`ação × objeto próprio × objeto alheio`. O resultado vulnerável é um `2xx` com
objeto do usuário B usando credencial de A; o resultado seguro é `403` ou `404`
consistente. Redate JWTs e conteúdo do objeto.

**Correção:** autorização por objeto e tenant no servidor em todas as operações;
IDs opacos não substituem a checagem. **Telemetria:** principal autenticado,
object owner, ação, decisão e correlation ID. Enumeração sequencial pode gerar
falsos positivos em clientes que repetem requests após sincronização.

## Rubrica comum (10 pontos)

| Critério | Pontos |
|----------|--------|
| Escopo e dados exclusivamente locais/sintéticos | 2 |
| Passos e resultado reproduzíveis | 2 |
| Evidência mínima e sanitizada | 2 |
| Causa e mitigação verificável | 2 |
| Telemetria, falso positivo e cleanup | 2 |

Nota mínima sugerida: 8/10.

