# Kubernetes - Attack Paths

> Cenarios comuns em clusters Kubernetes. Conteudo educacional.

---

## 1. Reconnaissance dentro de um Pod comprometido

```bash
# Variaveis e tokens
env | grep -i kube
ls -la /var/run/secrets/kubernetes.io/serviceaccount/
cat /var/run/secrets/kubernetes.io/serviceaccount/token

# API endpoint
echo $KUBERNETES_SERVICE_HOST $KUBERNETES_SERVICE_PORT

# Tente acoes comuns
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
curl -ks -H "Authorization: Bearer $TOKEN" https://$KUBERNETES_SERVICE_HOST/api/v1/namespaces/default/pods
```

---

## 2. RBAC Abuse - permissoes perigosas

| Permissao | Escalada |
|-----------|----------|
| `pods/exec` em namespaces sensiveis | RCE em pods existentes. |
| `secrets get` em kube-system | Credenciais de admin, tokens de SA privilegiados. |
| `pods create` + `serviceaccounts impersonate` | Criar pod com SA privilegiado, conseguir token. |
| `roles/rolebindings create` | Auto-bind a `cluster-admin`. |
| `nodes/proxy` | Hit kubelet API direto -> RCE em qualquer pod. |
| `escalate` em RBAC | Pode editar RoleBinding aumentando proprio acesso. |

```bash
kubectl auth can-i --list                       # o que minha SA pode
kubectl auth can-i create pods -n kube-system   # specific
```

**Mitigacao.** RBAC review trimestral, `kubectl-who-can`, `rbac-lookup`, `Krane`, `kube-score`.

---

## 3. Pod Escape

Configuracoes do pod que permitem escape:

```yaml
spec:
  hostPID: true            # ve processos do node
  hostNetwork: true        # ve a rede do node
  hostIPC: true            # IPC compartilhado
  containers:
  - securityContext:
      privileged: true     # game over
      capabilities:
        add: ["SYS_ADMIN"]
    volumeMounts:
    - mountPath: /host
      name: hostfs
  volumes:
  - name: hostfs
    hostPath:
      path: /
```

**Detection.** OPA/Gatekeeper rule bloqueando `hostPath: /`, `privileged: true`, `hostPID: true`.

---

## 4. kubelet API (10250)

Por padrao, em alguns clusters o kubelet permite `--anonymous-auth=true`. Da acesso a logs, exec, run em pods.

```bash
curl -ks https://<node-ip>:10250/pods
curl -ks https://<node-ip>:10250/run/<namespace>/<pod>/<container> -X POST -d "cmd=id"
```

**Mitigacao.** `--anonymous-auth=false`, `--authorization-mode=Webhook`, NetworkPolicy isolando porta.

---

## 5. etcd Comprometido

`etcd` armazena TODOS os secrets do cluster (em base64, possivelmente sem encryption-at-rest). Acesso direto = takeover.

```bash
ETCDCTL_API=3 etcdctl --endpoints=https://etcd:2379 \
  --cacert=ca.crt --cert=client.crt --key=client.key \
  get / --prefix --keys-only
```

**Mitigacao.** TLS mutuo, network policy, encryption-at-rest (`encryption-config.yaml`).

---

## 6. Container Image Implant (Supply chain)

Substituir uma imagem usada pelo cluster (registry push) com backdoor. Pods pull next time.

**Mitigacao.** Image signing (Sigstore/cosign), AdmissionController que valida assinatura, immutable tags.

---

## 7. SSRF -> Metadata -> Kubernetes

Em GKE/EKS/AKS, pods sem Workload Identity podem acessar metadata do node:

```bash
# AWS EKS
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
# GKE
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
```

Credenciais do node = acesso ao IAM do node group, frequentemente com `eks:*` ou similar.

**Mitigacao.** Workload Identity (IRSA no AWS, WI no GKE, MSI no AKS), Network Policy bloqueando IMDS para pods.

---

## 8. Helm e values inseguros

Helm charts podem definir `securityContext: {}` (vazio) ou montar secrets globais.

```bash
helm list --all-namespaces
helm get values <release>
```

Reviewer: olhar valores rendered (`helm template ... | grep -E 'privileged|hostPath'`).

---

## 9. AdmissionControllers / Webhooks

Webhook mutating mal protegido pode aceitar pod com qualquer config. Webhook validating pode ser bypassado se `failurePolicy=Ignore`.

---

## 10. Service Account Token Volume Projection

A partir do K8s 1.21+, tokens sao montados como **projected** com expiry. Old token = persistente.

```bash
# Verificar
kubectl get pod <pod> -o yaml | grep -A 10 serviceAccountToken
```

Antes de 1.24, tokens eram automounted com TTL infinito.

**Mitigacao.** `BoundServiceAccountTokenVolume` feature (default >=1.21), revogar tokens regularmente.

---

## Ferramentas

| Tool | Uso |
|------|-----|
| **kube-bench** | CIS Kubernetes Benchmark. |
| **kube-hunter** | Penetration tests no cluster. |
| **peirates** | Pentest interativo. |
| **kdigger** | Recon a partir de pod comprometido. |
| **rakkess** | Visualizar `auth can-i` em matriz. |
| **bust-a-kube** | Lab vulneravel oficial para praticar. |

---

## Hardening rapido

```bash
# 1. Pod Security Standards (PSS) "restricted"
kubectl label namespace prod pod-security.kubernetes.io/enforce=restricted

# 2. NetworkPolicy default-deny
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: prod
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
EOF

# 3. seccomp default
# kubelet: --seccomp-default=true
```

---

## Referencias

- [Kubernetes Security Whitepaper](https://kubernetes.io/docs/concepts/security/)
- [Kubernetes ATT&CK Matrix - Microsoft](https://www.microsoft.com/en-us/security/blog/2020/04/02/attack-matrix-kubernetes/)
- [O'Reilly Container Security book](https://learning.oreilly.com/library/view/container-security/9781492056690/)

## Exercicios praticos

Labs **apenas** em `kind` ou `minikube` (cluster local) — nunca em clusters de terceiros / producao.

1. Criar cluster `kind` ou `minikube`; aplicar um Deployment com SA default e listar permissoes com `kubectl auth can-i --list`.
2. Criar RoleBinding excessivo de proposito no lab; obter token de SA e chamar a API — depois remover o binding.
3. Aplicar NetworkPolicy default-deny + PSS `restricted` em um namespace de teste; validar que pods inseguros falham ao criar.
4. Rodar `kube-bench` (ou equivalente) no cluster local e anotar 3 findings com remediacao.

## Checklist de engajamento

- [ ] Cluster e kind/minikube local (ou lab autorizado)
- [ ] kubeconfig aponta para o lab — nao para prod
- [ ] Sem scan/ataque a API servers externos
- [ ] Tokens e kubeconfigs de teste nao commitados
- [ ] Evidencias minimas; sem dados reais de clientes no etcd
- [ ] Cleanup: `kind delete cluster` / `minikube delete` ao terminar
