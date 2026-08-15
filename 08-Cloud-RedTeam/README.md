# 08 - Cloud Red Team

> Tecnicas, comandos e mapeamentos para Red Team em AWS, Azure e GCP. Conteudo educacional.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários de IAM e APIs. |
| Pré-requisitos | Módulo 00; conta sandbox com billing limitado. |
| Tempo estimado | 12 horas por provedor escolhido. |
| Ambiente | Somente laboratório próprio/isolado ou engagement autorizado. |
| Evidência final | Attack path, logs, mitigação e confirmação de teardown. |
| Critério de conclusão | Demonstrar o objetivo, explicar limitações e registrar o cleanup. |

## Sumario

| Documento | Tema |
|-----------|------|
| [aws-attack-paths.md](aws-attack-paths.md) | Vetores comuns: IMDSv1 SSRF, IAM privilege escalation, S3 misconfig. Inclui **Exercicios praticos** e checklist (LocalStack / conta propria). |
| [azure-attack-paths.md](azure-attack-paths.md) | Entra ID (Azure AD), device code phishing, App roles, Storage SAS. Inclui **Exercicios praticos** (tenant / Azure free). |
| [gcp-attack-paths.md](gcp-attack-paths.md) | Service account impersonation, IAM bindings, metadata, Workload Identity. Inclui **Exercicios praticos** (projeto proprio / GCPGoat). |
| [cloud-recon-tools.md](cloud-recon-tools.md) | Pacu, CloudFox, ScoutSuite, ROADtools, BloodHound for Azure. |
| [labs/](labs/README.md) | Fixtures IAM sintéticas AWS/Azure/GCP, analisador offline e respostas orientativas. |

## Fluxo recomendado

1. Escolher um cloud (AWS / Azure / GCP) e ler o attack-paths correspondente.
2. Fazer os **Exercicios praticos** no final de cada arquivo — so em conta/lab proprio.
3. Usar [cloud-recon-tools.md](cloud-recon-tools.md) para enum defensiva/ofensiva em lab.
4. Documentar paths e mitigacoes; cruzar com [07-Web-AppSec](../07-Web-AppSec/) (SSRF→IMDS) quando aplicavel.

## Labs sugeridos

| Lab | Uso |
|-----|-----|
| **LocalStack** / conta AWS sandbox | Exercicios de [aws-attack-paths.md](aws-attack-paths.md) |
| **Azure free** / Learn sandbox | Exercicios de [azure-attack-paths.md](azure-attack-paths.md) |
| **GCP free tier** / GCPGoat | Exercicios de [gcp-attack-paths.md](gcp-attack-paths.md) |

Nunca atacar contas, buckets ou tenants de terceiros.

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

Cloud red team sem autorizacao escrita pode ser violacao do ToS do provider e crime (LGPD/GDPR/CFAA). Sempre confirme escopo e RoE antes de qualquer comando. Use apenas os labs da secao acima e o checklist no final de cada attack-paths.

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [[COMPARATIVO] AWS vs Azure vs GCP - Qual nuvem utilizar?](https://www.youtube.com/watch?v=A523278CPxo) — **Pena Rocks | Cloud. Code. Conquer.**.
2. [Como funciona a Segurança de Dados na nuvem? - Português](https://www.youtube.com/watch?v=FA4_nzMiK0g) — **AWS Developers LATAM**.
3. [Cloud Security Engineer: a profissão mais disputada de 2026 (e como entrar nela)](https://www.youtube.com/watch?v=2WtN_OO59Vw) — **Tech with Guilherme Teles**.
4. [Qual é o Melhor Provedor de Nuvem AWS, Azure, GCP ou OCI?](https://www.youtube.com/watch?v=6zz7wmARw0g) — **EdsInfoBR - Tecnologia e Informação**.
5. [Segurança na AWS | Fundamentos de proteção e compliance na nuvem](https://www.youtube.com/watch?v=CIabKd1bcd0) — **AWS Developers LATAM**.
