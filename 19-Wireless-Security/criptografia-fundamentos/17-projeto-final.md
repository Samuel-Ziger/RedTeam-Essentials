# 17 — Projeto final: manifesto verificável

Crie uma ferramenta offline que recebe uma pasta de fixtures e produz manifesto
canônico com caminho relativo, tamanho e SHA-256. Depois autentique o manifesto
com HMAC usando uma chave descartável fornecida fora do arquivo. A verificação
deve rejeitar arquivo alterado, ausente, extra, manifesto ambíguo e tag inválida.

## Entregáveis

- modelo de ameaça e limites (HMAC não atribui autoria entre detentores);
- formato versionado e ordem determinística;
- chave fora do repositório e exemplo somente sintético;
- testes positivos e negativos, sem acesso à rede;
- procedimento de rotação, recuperação e exclusão da chave de laboratório.

## Critério

Outra pessoa deve conseguir implementar o verificador apenas com sua
especificação e obter os mesmos bytes e tags nos vetores de teste.
