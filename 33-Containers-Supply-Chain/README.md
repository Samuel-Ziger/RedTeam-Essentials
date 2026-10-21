# 33 — Containers, Kubernetes, CI/CD e supply chain

O módulo acompanha o software da imagem ao cluster: build, registro,
identidade de workload, políticas, segredos, telemetria e cadeia de entrega.
Ataque e defesa são exercitados em manifests e eventos locais controlados.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Desenvolvimento, DevOps, plataforma, cloud e DevSecOps. |
| Pré-requisitos | Módulos `27`, `28`, `30` e `32`. |
| Tempo estimado | 40–60 horas. |
| Ambiente | Containers e fixtures locais; cluster descartável quando necessário. |
| Foco | Isolamento, least privilege, proveniência e detecção de deriva. |
| Evidência final | Pipeline endurecido, política verificável e relatório de auditoria. |
| Critério de conclusão | Auditoria concluída e pipeline validado com rollback documentado. |

## Conteúdo curricular

- [Containers, Kubernetes e CI/CD](containers-kubernetes-cicd/README.md)
- [Percurso de segurança de containers](containers-kubernetes-cicd/LEGADO-CONTAINER-SECURITY.md)
- [Baseline de hardening](containers-kubernetes-cicd/hardening-baseline.md)
- [Caminhos de ataque em Kubernetes](containers-kubernetes-cicd/kubernetes-attack-paths.md)
- [Técnicas de escape e controles](containers-kubernetes-cicd/docker-escape-techniques.md)
- [Laboratório de auditoria Kubernetes](containers-kubernetes-cicd/labs/README.md)
- [CI/CD e supply chain](containers-kubernetes-cicd/LEGADO-CICD-SUPPLY-CHAIN.md)

Próximo: [Módulo 34 — Segurança de plataformas](../34-Seguranca-Plataformas/README.md).
