# 11 — Colisões e birthday bound

Como há infinitas entradas e um número finito de digests, colisões existem. Para
um hash ideal de `n` bits, buscar preimagem custa aproximadamente `2^n`, mas
encontrar alguma colisão custa cerca de `2^(n/2)` pelo efeito aniversário.

Truncar digests reduz essas margens. O tamanho apropriado depende da propriedade:
identificador acidental, MAC truncado e assinatura têm ameaças diferentes.
Não confunda uma colisão demonstrada com recuperação universal de preimagens,
mas migre formatos cujo requisito de colisão deixou de ser atendido.

## Verificação

Qual é a resistência aproximada a colisões de um digest ideal de 256 bits? Por
que essa resposta não significa que SHA-256 tem uma chave de 128 bits?
