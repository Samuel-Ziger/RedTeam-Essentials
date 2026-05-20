# GCP - Attack Paths

> Cenarios em Google Cloud. Conteudo educacional.

---

## 1. Metadata Server SSRF

GCE expoe metadata em `169.254.169.254` (alias `metadata.google.internal`).

```bash
# Por padrao precisa do header
curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/?recursive=true"
```

Token devolvido = chave para `gcloud`/`gsutil` no contexto da Service Account anexada.

**Mitigacao.** Workload Identity Federation com OIDC (sem chave persistente), VPC Service Controls.

---

## 2. Service Account Impersonation

Permissao `iam.serviceAccounts.getAccessToken` em SA mais privilegiada =>

```bash
gcloud iam service-accounts list
gcloud auth print-access-token --impersonate-service-account=target-sa@project.iam.gserviceaccount.com
```

Procurar bindings:

```bash
gcloud projects get-iam-policy <project> --format json | jq '.bindings[] | select(.role=="roles/iam.serviceAccountTokenCreator")'
```

**Mitigacao.** Restringir `roles/iam.serviceAccountTokenCreator`, usar Workload Identity em GKE.

---

## 3. IAM Recursive Escalation

Bindings que sao escada:
- `roles/iam.serviceAccountAdmin` -> criar SA + assign roles.
- `roles/iam.securityAdmin` -> editar policy.
- `roles/resourcemanager.projectIamAdmin` -> editar IAM no projeto.
- `roles/owner` em folder pai -> heran em todos os projetos.

```bash
# Verificar tudo que conta atual pode
gcloud projects test-iam-permissions <project> --permissions iam.serviceAccounts.actAs,iam.roles.update
```

---

## 4. GCS Buckets Publicos

```bash
# Sem autenticacao
curl https://storage.googleapis.com/<bucket>/
gsutil ls -L gs://<bucket>/ 2>/dev/null
```

Procurar:
- `allUsers` ou `allAuthenticatedUsers` em ACL.
- `legacyObjectReader` em principals.
- Uniform Bucket-Level Access desativado.

**Mitigacao.** UBLA ligado, Public Access Prevention enforcado, signed URL com TTL curto.

---

## 5. Cloud Functions / Cloud Run

Funcoes/Services com `allUsers` em invokers permitem RCE-as-a-service sem auth.

```bash
gcloud functions list --regions=us-central1
gcloud functions get-iam-policy <fn> --region=us-central1
gcloud run services list
gcloud run services get-iam-policy <svc> --region=us-central1
```

---

## 6. Cross-Project Access via Folder

Folder admin escala para qualquer projeto filho. Empresas grandes fazem `roles/folderAdmin` casualmente.

---

## 7. Compute Instance Metadata Tampering

`compute.instances.setMetadata` + `compute.projects.setCommonInstanceMetadata` permite injetar startup-script ou SSH keys.

```bash
gcloud compute project-info add-metadata --metadata=ssh-keys="$(cat key.pub)"
gcloud compute instances add-metadata <vm> --metadata-from-file=startup-script=script.sh
gcloud compute instances reset <vm>
```

**Mitigacao.** OS Login, separacao admin/operacional, block-project-ssh-keys=true.

---

## 8. Workload Identity (GKE)

Pods sem WI podem assumir SA do node. Mal configurado, qualquer pod alcanca SA com `compute.admin`.

```bash
# Dentro do pod, sem WI configurado:
curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
```

**Mitigacao.** Workload Identity ativo em todos namespaces, network policy bloqueando metadata para pods.

---

## 9. BigQuery / Dataset Permissions

Datasets podem ter ACL aberta. `bq query` pode rodar sem auth se dataset e `allUsers`.

```bash
bq ls --project_id=<id>
bq show --format=prettyjson <id>:<dataset>
```

---

## 10. Cloud SQL Public IP

Procurar instances com IP publico e Authorized Networks 0.0.0.0/0:

```bash
gcloud sql instances list --format="table(name,settings.ipConfiguration.authorizedNetworks)"
```

---

## Ferramentas

- **GCPBucketBrute** - bruteforce nomes de bucket.
- **gcp_enum** - script de Pacu-like.
- **iam-privilege-escalation-in-gcp** (Rhino Security paper).
- **Hayat** - GCP auditing.
- **GCPGoat** - lab vulneravel oficial para praticar.

## Referencias

- [Google Cloud Threat Intelligence](https://services.google.com/fh/files/blogs/threat_horizons_report_q3_2024.pdf)
- [GCP Best Practices](https://cloud.google.com/security/best-practices)
