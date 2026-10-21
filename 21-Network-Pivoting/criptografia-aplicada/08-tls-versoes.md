# 08 — TLS 1.2 e TLS 1.3

TLS protege transporte autenticado contra observação e alteração dentro do
modelo. TLS 1.3 remove opções antigas, cifra mais do handshake e usa suites
separadas do grupo/assinatura. TLS 1.2 continua em legados, mas exige perfil
restrito e plano de retirada; SSL e versões antigas devem ficar desativados.

0-RTT reduz latência, porém permite replay no modelo do protocolo. Só operações
idempotentes e explicitamente preparadas devem aceitá-lo. Terminadores TLS
mudam a fronteira: o trecho posterior também precisa de proteção adequada.

## Prática

Faça uma matriz de versões mínima/máxima, clientes, exceções e data de remoção.
