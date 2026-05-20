# Cloud Recon Tools

> Comparativo rapido das ferramentas mais usadas em red team de cloud.

| Ferramenta | Cloud | Foco | Stealth | Output |
|------------|-------|------|---------|--------|
| **Pacu** | AWS | Modular exploitation framework | Medio (faz API calls visiveis no CloudTrail) | DB SQLite local |
| **CloudFox** | AWS, Azure | Triage de "para onde ir agora" pos-acesso | Medio | tabelas + JSON |
| **enumerate-iam** | AWS | Brute-force de permissoes | Alto barulho | TXT |
| **awspx** | AWS | Visualizacao tipo BloodHound | Medio | Neo4j |
| **ScoutSuite** | Multi | Audit completo (azul-friendly) | Medio (read-heavy) | HTML report |
| **Prowler** | Multi | Compliance benchmarks (CIS) | Medio | CSV, HTML, JSON |
| **ROADtools** | Azure/Entra | Coleta GraphQL/Graph API completa | Alto barulho | Neo4j + DB |
| **AzureHound** | Azure | BloodHound for Azure | Medio | JSON for BloodHound |
| **BARK** | Azure | Toolkit PowerShell de operacoes | Variavel | depende do modulo |
| **MicroBurst** | Azure | Modulos PowerShell varios | Medio | varios |
| **GCPBucketBrute** | GCP | Enumeracao de buckets | Baixo (so https) | TXT |
| **gcp_enum** | GCP | Enum geral | Medio | TXT |

---

## Workflow tipico AWS pos-acesso

1. **Identidade.** `aws sts get-caller-identity` -> account, user/role, session.
2. **Permissoes.** `enumerate-iam` ou Pacu `iam__enum_users_roles_policies_groups`.
3. **Recursos.** CloudFox `inventory`, `instances`, `endpoints`.
4. **Caminhos privesc.** Pacu `iam__privesc_scan`.
5. **Data.** S3 listing, RDS describe, Secrets Manager list.
6. **Persistencia.** Criar AccessKey extra em user existing (`iam:CreateAccessKey`).

---

## Workflow tipico Azure pos-token

1. **Token info.** `roadtx describe <token>`.
2. **Tenant info.** `roadrecon dump`.
3. **BloodHound import.** `azurehound list` -> upload no BloodHound CE.
4. **App permissions.** Procurar app roles tipo `Application.ReadWrite.All`.
5. **Persistencia.** Adicionar credential a Service Principal, ou Self-assigned role no Privileged Identity Management.

---

## Workflow tipico GCP

1. `gcloud auth list` / `gcloud config list`.
2. `gcloud projects list`.
3. `gcloud projects get-iam-policy <p>` por projeto.
4. `gcloud iam service-accounts list`.
5. `gsutil ls`, `gcloud compute instances list`.
6. Verificar bindings com `iam.serviceAccountTokenCreator`.

---

## Operational Security (OpSec)

- **Use VM dedicada / proxy** para nao revelar IP do laptop.
- **Logs do provider.** CloudTrail / Activity Log gravam tudo - escolha entre velocidade e furtividade.
- **Rotacione user-agent** se possivel (SDKs ja identificam).
- **Bash history.** Limpe `~/.bash_history`, `~/.aws/cli/cache`, `~/.config/gcloud/`.
- **Tokens persistidos.** Nao deixe `~/.aws/credentials` com chaves longas pos-engagement.

---

## Documentacao oficial dos providers (defensivo)

- AWS: [Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/)
- Azure: [Security Operations](https://learn.microsoft.com/en-us/azure/security/fundamentals/operational-best-practices)
- GCP: [Security Foundations Guide](https://cloud.google.com/architecture/security-foundations)
