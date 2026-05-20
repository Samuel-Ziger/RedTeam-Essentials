# 10 - Container Security

> Pentest e hardening de Docker e Kubernetes. Conteudo educacional.

## Sumario

| Documento | Tema |
|-----------|------|
| [docker-escape-techniques.md](docker-escape-techniques.md) | Tecnicas de escape do container para o host (capabilities, mounts, sockets). |
| [kubernetes-attack-paths.md](kubernetes-attack-paths.md) | Recon de cluster, RBAC abuse, pod escape, kubelet API. |
| [hardening-baseline.md](hardening-baseline.md) | Hardening pratico: rootless, seccomp, AppArmor, NetworkPolicy, OPA/Kyverno. |

## Pre-requisitos

- Docker e Kubernetes basicos (pods, services, RBAC).
- `kubectl`, `kubectl-neat`, `kubeshark` ou `k9s` instalados.
- Lab: `kind` ou `minikube` para nao tocar em prod.

## MITRE ATT&CK Containers Matrix

- T1610 - Deploy Container
- T1611 - Escape to Host
- T1613 - Container and Resource Discovery
- T1525 - Implant Container Image
- T1609 - Container Administration Command
- T1552.007 - Container API Credentials
