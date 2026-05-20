# Azure / Entra ID - Attack Paths

> Cenarios recorrentes em engagements Azure. Conteudo educacional.

---

## 1. Device Code Phishing

Microsoft Entra (antigo Azure AD) suporta device code flow. Atacante inicia auth e envia o codigo para vitima.

```bash
# Iniciar device code para tenant comum
curl -X POST "https://login.microsoftonline.com/common/oauth2/v2.0/devicecode" \
  -d "client_id=04b07795-8ddb-461a-bbee-02f9e1bf7b46" \
  -d "scope=https://graph.microsoft.com/.default offline_access"
```

Resposta inclui `user_code` e `verification_uri`. Engana vitima a digitar - atacante poll endpoint e recebe access_token + refresh_token.

**Mitigacao.** Conditional Access bloqueando device code flow para usuarios privilegiados; phishing-resistant MFA (FIDO2).

---

## 2. Token Theft (PRT, Refresh Token)

PRT (Primary Refresh Token) e armazenado no LSASS de hosts joined ao Entra. Mimikatz tem `dpapi::cloudapkd`.

Refresh tokens de aplicacoes mobile/SPA podem ser longevos (90 dias). Roubar = persistencia.

```powershell
# AzureHound coleta tokens persistidos
azurehound list users --jwt $TOKEN -o azuredata.json
```

**Mitigacao.** Continuous Access Evaluation (CAE), token binding, short refresh TTL, Conditional Access com network/device condition.

---

## 3. App Roles e Service Principals

Procurar Service Principals com permissoes de Graph escalonadas:

```bash
# Via AzureCLI
az ad sp list --query "[?appRoles[?value=='RoleManagement.ReadWrite.Directory']]"

# Via Graph
GET https://graph.microsoft.com/v1.0/servicePrincipals?$filter=...&$select=id,displayName,appRoles
```

App com `RoleManagement.ReadWrite.Directory` -> escalar para Global Admin via Graph.

Outras danger roles:
- `Directory.ReadWrite.All`
- `Application.ReadWrite.All`
- `AppRoleAssignment.ReadWrite.All`
- `PrivilegedAccess.ReadWrite.AzureADGroup`

**Mitigacao.** Consent admin obrigatorio, app permissions review periodica, scope minimo.

---

## 4. Storage SAS Tokens

SAS tokens podem dar acesso amplo a blobs/queues por longos periodos.

```bash
# Listar blobs sem auth (se SAS for permissivo)
curl "https://<acct>.blob.core.windows.net/<container>?restype=container&comp=list&<SAS-TOKEN>"
```

Procurar em:
- URLs em logs (`Authorization=`).
- Codigo client-side.
- Repos publicos.

**Mitigacao.** User Delegation SAS (TTL curto), Stored Access Policies, Lifecycle policies, Entra-auth (no SAS).

---

## 5. Cross-Tenant Trust (Guest users)

Tenants frequentemente convidam guests com permissoes default amplas (membro de "All Users"). 

```bash
# Listar guests no proprio tenant
az ad user list --filter "userType eq 'Guest'"
```

Se o tenant nao restringe `User.Read.All`, qualquer guest enumera o diretorio inteiro.

**Mitigacao.** External Collaboration settings restritivo, AD External Identities com restricoes.

---

## 6. Managed Identity Abuse

VMs/Containers/AppServices podem ter MSI anexada com permissoes em Subscription.

```bash
# De dentro da VM
curl -H Metadata:true "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```

Token devolvido pode `az role assignment list --assignee <objectId>`. Se a MSI tem `Owner` no RG, atacante escala.

**Mitigacao.** Least privilege em MSI, separar identity por workload, RBAC tight.

---

## 7. Azure Subscription Hijacking

`Microsoft.Subscription/aliases` ou owner transfer pode mover subscription para tenant atacante.

**Mitigacao.** Subscription transfer policies, lock administrativo.

---

## 8. Logic Apps / Automation Account

Logic Apps / Automation Runbooks podem rodar como identity privilegiada e ser editados por usuarios menores.

```bash
az logicapp list -o table
az automation account list -o table
```

Editar runbook -> proxima execucao roda nosso codigo com a identidade.

---

## 9. Hybrid Identity Sync

Servidor de Azure AD Connect tem credenciais de sincronizacao com Entra. Comprometer ele = abuse do connector account e password hash sync.

`MSOL_<hash>` ou `Sync_<host>_<hash>` sao contas chave.

**Mitigacao.** Treat sync server como Tier 0, Just-in-time admin, secure score baseline.

---

## 10. Conditional Access Bypass

- Locations confianca-only por IP corporativo - VPN do atacante na faixa.
- "Browser/legacy clients" excluidos sem MFA.
- Named locations sem `Block other locations`.

**Tools.**
- **ROADtools** - enumeracao de Entra completa via APIs.
- **AzureHound** - BloodHound para Azure.
- **BARK** - Better Azure Red Team Kit (modulos PowerShell).
- **MicroBurst** - PowerShell module com varios checks.

## Referencias

- [Microsoft Threat Intelligence blog](https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/)
- [Adsec.es Azure AD red team](https://www.adsec.es/)
- [ROADtools docs](https://github.com/dirkjanm/ROADtools)
