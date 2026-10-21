# 15 — Assinaturas: Ed25519, ECDSA e RSA-PSS

Assinatura autentica bytes e detecta alteração para quem confia na chave
pública. Não cifra, não fornece frescor e não prova identidade humana sem um
processo que ligue chave a sujeito. Assine estrutura canônica contendo versão,
propósito e contexto.

Ed25519 oferece API simples e assinatura determinística; ECDSA exige parâmetros
e tratamento cuidadoso de nonce; RSA-PSS é apropriado em ecossistemas RSA.
Defina política de chaves, algoritmo aceito e cadeia de confiança fora do
payload não confiável.

## Prática

Assine a fixture, altere mensagem e assinatura e confirme rejeição uniforme.
