# 06 — Revogação, CRL, OCSP e certificados curtos

Revogação comunica que um certificado não deve mais ser aceito antes do fim da
validade. CRL publica listas; OCSP consulta status; stapling leva resposta pelo
servidor. Disponibilidade, privacidade, cache e soft-fail complicam cada modelo.

Certificados curtos reduzem janela e dependência de revogação, mas exigem
automação confiável. Incidente ainda demanda bloquear identidade, rotacionar
chave, investigar emissões e renovar dependentes. Expiração não destrói cópias
da chave.

## Prática

Escreva runbook para chave de serviço exposta: conter, revogar, renovar,
distribuir, verificar e aprender.
