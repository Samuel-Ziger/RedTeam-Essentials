# Implementações seguras

| Arquivo | Demonstra |
|---|---|
| [secure_envelope.py](secure_envelope.py) | Envelope JSON estrito com AES-256-GCM e AAD. |
| [key_exchange.py](key_exchange.py) | X25519 seguido de HKDF com contexto. |
| [signatures.py](signatures.py) | Assinatura e verificação Ed25519 com domínio. |

Instale a dependência fixada em [requirements-crypto.txt](../../../requirements-crypto.txt)
e rode `python3 -m unittest discover -s exemplos/tests -v`. O código é um
exemplo revisável, não um serviço de custódia de chaves.
