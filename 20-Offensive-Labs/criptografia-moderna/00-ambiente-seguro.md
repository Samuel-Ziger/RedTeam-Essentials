# 00 — Ambiente e regras do laboratório

O código usa a biblioteca `cryptography`, que expõe primitivas corretas mas não
decide seu protocolo. Chaves são geradas em memória, dados são sintéticos e
arquivos temporários são descartados. Não reutilize material do curso em
produção nem copie chaves reais para testes.

Toda construção deve declarar versão, algoritmo, identificador de chave,
nonce, dados associados e limites de tamanho. Falha de autenticação encerra o
processamento com um erro único. Testes cobrem round trip e adulteração de cada
campo antes de qualquer integração.

## Gate

Confirme versão da dependência, origem do pacote, backend suportado e política
de atualização. Se a biblioteca faltar, os testes informam a dependência; não
implementam uma cifra alternativa.
