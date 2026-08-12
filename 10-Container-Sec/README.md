# 10 - Container Security

> Pentest e hardening de Docker e Kubernetes. Conteudo educacional.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários de Docker e Kubernetes. |
| Pré-requisitos | Módulo 00; Docker e kind/minikube locais. |
| Tempo estimado | 10 horas de leitura e 8 horas de prática. |
| Ambiente | Somente laboratório próprio/isolado ou engagement autorizado. |
| Evidência final | Manifesto vulnerável/corrigido, eventos e teardown confirmado. |
| Critério de conclusão | Demonstrar o objetivo, explicar limitações e registrar o cleanup. |

## Sumario

| Documento | Tema |
|-----------|------|
| [docker-escape-techniques.md](docker-escape-techniques.md) | Tecnicas de escape do container para o host (capabilities, mounts, sockets). Inclui **Exercicios praticos** e checklist em Docker/VM local. |
| [kubernetes-attack-paths.md](kubernetes-attack-paths.md) | Recon de cluster, RBAC abuse, pod escape, kubelet API. Inclui **Exercicios praticos** em **kind/minikube**. |
| [hardening-baseline.md](hardening-baseline.md) | Hardening pratico: rootless, seccomp, AppArmor, NetworkPolicy, OPA/Kyverno. |
| [labs/](labs/README.md) | Detecção offline de pod privilegiado em Kubernetes audit log sintético. |

## Fluxo recomendado

1. Hardening baseline — [hardening-baseline.md](hardening-baseline.md).
2. Docker escape em lab local — [docker-escape-techniques.md](docker-escape-techniques.md) + secao **Exercicios praticos**.
3. Kubernetes em cluster local — [kubernetes-attack-paths.md](kubernetes-attack-paths.md) + exercicios com **kind** ou **minikube**.
4. Cleanup obrigatorio (`kind delete cluster` / `minikube delete` / containers de teste).

## Labs sugeridos

| Lab | Uso |
|-----|-----|
| **Docker local / VM descartavel** | Exercicios de escape e hardening |
| **kind** | Cluster K8s local leve (recomendado) |
| **minikube** | Alternativa local com addons |

Nunca praticar escape ou RBAC abuse em clusters de terceiros ou producao.

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

## Etica

Escape de container e abuso de RBAC sem autorizacao sao ilegais e podem comprometer hosts compartilhados. Use apenas kind/minikube ou VMs proprias; siga o checklist no final de cada documento de ataque.
