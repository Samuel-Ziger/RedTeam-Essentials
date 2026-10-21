# 13 — KDF, HKDF e separação de domínio

Uma KDF deriva material de chave com comprimento e propósito definidos. HKDF
primeiro extrai uma chave pseudorrandômica e depois expande saídas rotuladas.
O campo `info` vincula contexto como protocolo, versão e direção; um salt pode
fortalecer a extração, mas não precisa ser secreto.

Derive chaves independentes para criptografia, autenticação e direções de um
canal. Não corte manualmente o mesmo hash para propósitos não documentados. HKDF
não torna senha humana forte: senhas exigem KDF deliberadamente custosa.

## Verificação

Por que `info="client-write"` e `info="server-write"` ajudam mesmo quando o
segredo de entrada é o mesmo?
