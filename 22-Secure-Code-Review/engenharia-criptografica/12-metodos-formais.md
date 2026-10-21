# 12 — Métodos formais e verificação

Model checking explora estados; verificação simbólica analisa protocolos sob
modelos; provas assistidas ligam implementação a especificação. Ferramentas como
TLA+, ProVerif, Tamarin e verificação de código têm escopos distintos.

Um modelo omite detalhes por definição. Declare abstrações, propriedades e
correspondência com código; teste refinamento. Comece por máquinas de estado,
invariantes de nonce e ausência de downgrade antes de tentar formalizar tudo.

## Prática

Escreva invariantes textuais do protocolo: key ID conhecido, contador monotônico,
versão permitida e plaintext somente após autenticação.
