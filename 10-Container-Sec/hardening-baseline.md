# Hardening Baseline - Docker & Kubernetes

> Recomendacoes praticas para reduzir superficie de ataque. Aplique como baseline e ajuste ao contexto.

---

## Docker / Container Runtime

### Dockerfile

```dockerfile
# 1. Use base minima
FROM gcr.io/distroless/python3-debian12:nonroot AS runtime

# 2. Usuario nonroot
USER 65532:65532

# 3. Diretorios apenas-leitura
WORKDIR /app
COPY --chown=65532:65532 app/ /app/

# 4. Sem shell, sem package manager (distroless)
ENTRYPOINT ["python", "/app/main.py"]
```

### docker run

```bash
docker run \
  --user 65532:65532 \
  --cap-drop=ALL --cap-add=NET_BIND_SERVICE \
  --security-opt no-new-privileges \
  --security-opt seccomp=/path/to/profile.json \
  --read-only --tmpfs /tmp --tmpfs /run \
  --memory=512m --cpus=1 \
  --restart on-failure:5 \
  myapp:1.2.3
```

### Image hygiene

- Tags imutaveis (`@sha256:...`), nao `latest`.
- Scan continuo (Trivy, Grype) - bloquear `HIGH`/`CRITICAL` no CI.
- SBOM gerado por build (`syft` -> `grype`).
- Sign images com cosign (Sigstore).

---

## Kubernetes - Cluster

### Pod Security Standards (PSS)

Use o admission controller built-in. Tres niveis: `privileged`, `baseline`, `restricted`.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: prod
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Pod securityContext

```yaml
spec:
  automountServiceAccountToken: false  # se nao precisar
  securityContext:
    runAsNonRoot: true
    runAsUser: 65532
    runAsGroup: 65532
    fsGroup: 65532
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: registry.example.com/app@sha256:...
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
    resources:
      requests: {cpu: 100m, memory: 128Mi}
      limits:   {cpu: 500m, memory: 512Mi}
    livenessProbe: {...}
    readinessProbe: {...}
```

### NetworkPolicy default-deny

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny, namespace: prod}
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
# Permitir apenas DNS de saida
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-dns-egress, namespace: prod}
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - to:
    - namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: kube-system}}
      podSelector: {matchLabels: {k8s-app: kube-dns}}
    ports:
    - port: 53
      protocol: UDP
```

### RBAC

- Sem `cluster-admin` para applications, apenas humanos com JIT (jit-rbac, kubectl-iam).
- Roles por workload, nao por usuario.
- Audit log com criteria sensiveis (`secrets`, `pods/exec`, `nodes/proxy`).

### Admission policies (OPA Gatekeeper / Kyverno)

Bloquear hard:

- `privileged: true`
- `hostPath:` em volumes
- `hostPID`, `hostIPC`, `hostNetwork`
- `runAsUser: 0` (root)
- `latest` tag
- Images de registries nao-confiaveis

Exemplo Kyverno:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: disallow-host-namespaces}
spec:
  validationFailureAction: enforce
  rules:
  - name: host-namespaces
    match:
      resources:
        kinds: [Pod]
    validate:
      message: "hostPID/IPC/Network proibidos"
      pattern:
        spec:
          =(hostNetwork): "false"
          =(hostIPC): "false"
          =(hostPID): "false"
```

---

## Runtime monitoring

| Tool | O que faz |
|------|-----------|
| **Falco** | Detecta anomalias kernel-level (shell em container, mount suspeito). |
| **Tetragon** | eBPF-based observability + enforcement. |
| **Tracee** | Tracing de syscalls e eventos com regras YAML. |
| **Sysdig Secure** | Comercial: runtime + compliance + posture. |

Regras Falco essenciais (built-in): `Terminal shell in container`, `Write below etc`, `Mkdir binary dirs`, `Outbound Connection to C2 Servers`.

---

## CIS Benchmarks

Use `kube-bench`:

```bash
kube-bench --benchmark cis-1.8
```

Cobertura: master node, worker node, RBAC, policies, networking.

---

## Workload Identity

Em vez de keys de cloud em secrets, use:

- **AWS:** IRSA (IAM Roles for Service Accounts).
- **GCP:** Workload Identity Federation.
- **Azure:** AAD Pod Identity / Workload Identity.

Beneficios: sem rotacao manual, sem credenciais long-lived em pods.

---

## Secrets

- **Nunca** secrets em ConfigMap.
- Usar `Secret` com encryption-at-rest no etcd (`--encryption-provider-config`).
- Ainda melhor: external secret store (HashiCorp Vault, AWS Secrets Manager) com **External Secrets Operator** ou CSI driver.
- Rotacionar secrets regularmente (auto-rotation no Vault).

---

## Checklist final

- [ ] PSS `restricted` em todos os namespaces de aplicacao.
- [ ] NetworkPolicy default-deny + allowlist explicito.
- [ ] RBAC review trimestral.
- [ ] Admission policy bloqueando hostPath/privileged/latest.
- [ ] Image signing (cosign) verificado por admission.
- [ ] Trivy/Grype no CI bloqueando CVEs HIGH/CRITICAL.
- [ ] Falco/Tetragon ativo + alertas.
- [ ] etcd encryption-at-rest.
- [ ] kube-apiserver audit log enviado para SIEM.
- [ ] Workload Identity em vez de cloud keys.
- [ ] External secrets para producao.
- [ ] kube-bench >= 90% pass.
