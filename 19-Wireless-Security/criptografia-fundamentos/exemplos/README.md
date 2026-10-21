# Exemplos executáveis

| Arquivo | Função |
|---|---|
| [number_theory.py](number_theory.py) | MDC, inverso e exponenciação modular didáticos. |
| [hash_mac.py](hash_mac.py) | SHA-256 e HMAC de arquivo com limite. |
| [password_kdf.py](password_kdf.py) | Registro scrypt versionado e validação estrita. |

Execute `number_theory.py gcd 252 105`, gere o digest da fixture e rode
`python3 -m unittest discover -s exemplos/tests -v`.

O utilitário de senha lê pelo terminal com `getpass`; não aceite senhas em
argumentos, logs ou fixtures. Os parâmetros são pequenos o bastante para CI e
devem ser calibrados de novo em uma aplicação real.
