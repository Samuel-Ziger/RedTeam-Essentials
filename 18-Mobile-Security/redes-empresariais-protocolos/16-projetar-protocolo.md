# 16 — Como projetar um protocolo

Um protocolo é um contrato de interoperabilidade. Comece pelo problema, atores,
transportes, limites e invariantes, não pelo formato de bytes.

## Checklist de especificação

1. objetivos e não objetivos;
2. terminologia normativa (`MUST`, `SHOULD`, `MAY`);
3. papéis e modelo de comunicação;
4. framing e byte order;
5. tipos, campos, limites e canonicalização;
6. máquina de estados e timeouts;
7. erros, retry e idempotência;
8. versionamento, extensões e negociação;
9. autenticação, confidencialidade, integridade e replay;
10. limites de recurso e considerações de segurança;
11. registro de valores e processo de mudança;
12. vetores de teste e interoperabilidade.

Escolha padrão existente quando ele atende; criar protocolo aumenta custo de
revisão, implementação e manutenção. Nunca crie criptografia própria: componha
protocolos revisados como TLS/QUIC.

Neste curso, o RNP/1 é deliberadamente pequeno e local para ensinar framing e
estado; ele não é protocolo de produção.
