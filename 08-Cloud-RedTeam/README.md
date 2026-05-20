# 08 - Cloud Red Team

> Tecnicas, comandos e mapeamentos para Red Team em AWS, Azure e GCP. Conteudo educacional.

## Sumario

| Documento | Tema |
|-----------|------|
| [aws-attack-paths.md](aws-attack-paths.md) | Vetores comuns: IMDSv1 SSRF, IAM privilege escalation, S3 misconfig. |
| [azure-attack-paths.md](azure-attack-paths.md) | Entra ID (Azure AD), device code phishing, App roles, Storage SAS. |
| [gcp-attack-paths.md](gcp-attack-paths.md) | Service account impersonation, IAM bindings, metadata, Workload Identity. |
| [cloud-recon-tools.md](cloud-recon-tools.md) | Pacu, CloudFox, ScoutSuite, ROADtools, BloodHound for Azure. |

## MITRE ATT&CK Cloud Matrix

Tecnicas mais relevantes:

- T1078.004 - Valid Accounts: Cloud Accounts
- T1098.001/.003 - Account Manipulation
- T1538 - Cloud Service Dashboard
- T1580 - Cloud Infrastructure Discovery
- T1199 - Trusted Relationship (Cross-tenant, federation)
- T1199.002 - Cloud Service Provider
- T1530 - Data from Cloud Storage Object

## Pre-requisitos

- Conhecer pelo menos um IAM (AWS IAM, Azure RBAC ou GCP IAM).
- Familiaridade com APIs REST / SDK.
- Conta de teste isolada com billing limitado.

## Etica

Cloud red team sem autorizacao escrita pode ser violacao do ToS do provider e crime (LGPD/GDPR/CFAA). Sempre confirme escopo e RoE antes de qualquer comando.
