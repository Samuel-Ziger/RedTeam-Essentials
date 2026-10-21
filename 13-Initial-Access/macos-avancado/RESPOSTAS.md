# Respostas orientativas

## XNU é apenas Mach?

Não. XNU é híbrido: primitivas Mach, subsistema BSD, IOKit e componentes de
segurança cooperam no kernel. Processos Unix e tarefas Mach são visões relacionadas.

## Por que uma assinatura válida não basta?

Ela sustenta identidade/integridade conforme a cadeia e o requisito. Política,
notarização, procedência, entitlements, comportamento e risco ainda importam.

## TCC é permissão Unix?

Não. TCC governa acesso a classes de dados e recursos protegidos com contexto
de identidade de código, usuário e gerenciamento. `root` não o torna irrelevante.

## Perfil instalado prova conformidade?

Não. É preciso saber canal, precedência, aplicabilidade, valor efetivo e status.
DDM melhora declaração/status, mas também exige observação e reconciliação.

## Por que Endpoint Security não é implementado no lab?

Um cliente real requer entitlement, assinatura, System Extension e desenho de
privacidade/latência. O curso ensina arquitetura e análise sem simular autorização
nem pedir que estudantes enfraqueçam o host.

## O capstone está pronto quando?

Quando imagem, política, identidade, software, update, telemetria, privacidade,
recuperação e exceções formam um ciclo mensurável com owners e rollback.
