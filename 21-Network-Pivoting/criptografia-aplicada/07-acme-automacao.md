# 07 — ACME e automação

ACME automatiza conta, ordem, autorização, challenge, finalização e renovação.
HTTP-01 e DNS-01 provam controles diferentes; a escolha depende de topologia e
ameaça. Credencial DNS ampla em cada servidor cria risco maior que o certificado.

Automação deve renovar antes da expiração, usar jitter/backoff, validar cadeia e
nome, fazer deploy atômico, recarregar serviço e alertar pelo tempo restante.
Teste staging e rollback sem depender de intervenção na madrugada.

## Verificação

Defina SLO de renovação e três sinais que detectam falha antes da expiração.
