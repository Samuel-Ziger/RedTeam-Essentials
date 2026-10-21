# 11 — Propriedades, fuzzing e falhas

Property-based tests geram entradas e verificam invariantes: decrypt(encrypt(m))
é m; qualquer bit alterado falha; parser nunca trava; saída respeita limites.
Fuzzing explora parsers e state machines com corpus e orçamento limitados.

Não use um oráculo que considera “não lançou exceção” como sucesso. Classifique
timeout, consumo de memória, aceitação divergente e crash. Fuzzing não prova
segurança, mas encontra classes que exemplos manuais perdem.

## Prática

Defina cinco propriedades do formato e um corpus mínimo sem gerar tráfego ou
processar material sensível.
