# Ferramentas de criptografia aplicada

| Artefato | Finalidade |
|---|---|
| [certificate_audit.py](certificate_audit.py) | Inventário offline de PEM X.509. |
| [tls_policy.py](tls_policy.py) | Auditoria de política TLS declarativa. |
| [mini_pki.sh](mini_pki.sh) | Raiz e leaf descartáveis em diretório temporário. |

O auditor não constrói trust path nem declara o certificado confiável. A
mini-PKI se autodestrói e nunca deve ser instalada como raiz real.
