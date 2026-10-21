# Criptografia I — fundamentos

Este curso ensina a linguagem usada para raciocinar sobre criptografia antes
de apresentar algoritmos de produção. Cada capítulo termina com perguntas de
verificação; os laboratórios usam números pequenos somente para tornar o
processo observável. Segurança real exige primitivas e bibliotecas revisadas.

## Rota

| # | Capítulo |
|---:|---|
| 00 | [Método, laboratório e ética](00-metodo-laboratorio.md) |
| 01 | [Objetivos, ativos e modelos de ameaça](01-objetivos-modelos-ameaca.md) |
| 02 | [Bits, bytes, texto e codificação](02-bits-bytes-codificacao.md) |
| 03 | [Aritmética modular](03-aritmetica-modular.md) |
| 04 | [Primos, MDC e inversos](04-primos-euclides-inversos.md) |
| 05 | [Grupos, corpos e problemas difíceis](05-grupos-corpos-problemas.md) |
| 06 | [Probabilidade, entropia e segurança](06-probabilidade-entropia.md) |
| 07 | [Aleatoriedade, CSPRNG, nonce, salt e IV](07-aleatoriedade-nonce-salt-iv.md) |
| 08 | [Cifras clássicas e lições modernas](08-cifras-classicas.md) |
| 09 | [Sigilo perfeito e one-time pad](09-sigilo-perfeito-otp.md) |
| 10 | [Funções hash e propriedades](10-funcoes-hash.md) |
| 11 | [Colisões, birthday bound e escolhas](11-colisoes-birthday.md) |
| 12 | [MAC e HMAC](12-mac-hmac.md) |
| 13 | [KDF, HKDF e separação de domínio](13-kdf-hkdf.md) |
| 14 | [Senhas, salts e KDFs de memória](14-senhas-kdfs.md) |
| 15 | [Compromissos, árvores de Merkle e transparência](15-compromissos-merkle.md) |
| 16 | [Criptoanálise e canais laterais](16-criptoanalise-canais-laterais.md) |
| 17 | [Projeto final: manifesto verificável](17-projeto-final.md) |

## Como estudar

1. Leia um capítulo e reescreva suas garantias com suas palavras.
2. Execute o laboratório correspondente sem alterar os vetores esperados.
3. Faça uma mudança, preveja o resultado e só então rode os testes.
4. Registre ameaça, propriedade, suposição e limite; não apenas o algoritmo.

## Materiais

- [Laboratórios](laboratorios/README.md)
- [Exemplos executáveis](exemplos/README.md)
- [Glossário](GLOSSARIO.md)
- [Cheatsheet](CHEATSHEET.md)
- [Respostas orientativas](RESPOSTAS.md)
- [Referências](REFERENCIAS.md)
