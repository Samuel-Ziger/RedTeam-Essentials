# 02 — Composição e limites de garantia

Componentes seguros podem compor um sistema inseguro. Cifrar sem autenticar,
assinar estrutura ambígua, reutilizar chave entre propósitos ou omitir versão do
transcript são falhas de composição. Use construções prontas como AEAD e HPKE.

Declare ordem e binding: identidade, papel, versão, algoritmo, chave, mensagem e
contexto precisam estar criptograficamente ligados quando influenciam decisão.
Teste substituição cruzada entre usuários, ambientes e objetos.

## Verificação

Um ciphertext válido para tenant A pode ser movido para B? Mostre onde o tenant
entra na AAD ou na derivação.
