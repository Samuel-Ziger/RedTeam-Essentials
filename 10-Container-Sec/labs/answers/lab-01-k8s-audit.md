# Resposta orientativa — Kubernetes audit

O primeiro evento é leitura permitida de um pod por service account. O segundo
é criação permitida de `debug` por um usuário e contém
`securityContext.privileged=true`. Esse contexto pode remover fronteiras
importantes entre container e host, dependendo de mounts, capabilities e
configuração do runtime.

Uma regra deve combinar `verb=create`, `objectRef.resource=pods`, status 2xx e
qualquer container/initContainer/ephemeralContainer privilegiado. Para reduzir
falsos positivos, considere namespaces aprovados, identidade do pipeline,
janela de mudança e política de admission — sem criar uma allowlist ampla que
oculte abuso.

Mitigação: Pod Security Standards `restricted`, admission policy e RBAC mínimo.
Resposta: preservar o manifesto/audit ID, verificar o pod e remover o recurso
somente conforme o processo de incidente do ambiente.

