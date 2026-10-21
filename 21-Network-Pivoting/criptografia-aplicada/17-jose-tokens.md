# 17 — JWS, JWE e tokens

JWS assina/autentica; JWE cifra; JWT define claims e pode usar um deles. Base64url
não esconde payload. Verificador fixa algoritmos permitidos, escolhe chave por
configuração confiável e valida `iss`, `aud`, tempo, tipo e claims da aplicação.

Não aceite `alg=none`, confunda chave simétrica/assimétrica ou busque chave em
URL não confiável. Tokens não são revogados magicamente: vida curta, rotação,
sessão e lista de revogação dependem do risco.

## Prática

Especifique matriz de validação antes de escrever código e inclua erro único
para token inválido.
