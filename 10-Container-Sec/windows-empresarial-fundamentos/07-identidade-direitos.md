# 07 — Identidade, contas de serviço e direitos locais

Contas humanas e de serviço têm ciclos distintos. Uma conta de serviço não
deve permitir logon interativo, compartilhar senha ou ter privilégio amplo.
Managed service accounts dependentes de domínio ficam para a trilha posterior.

## Camadas

- conta/grupo e SID;
- logon rights (`SeServiceLogonRight`, deny rights etc.);
- privileges no token;
- ACL do objeto;
- integrity level e proteções adicionais.

```powershell
Get-LocalUser
Get-LocalGroup
whoami /all
secedit.exe /export /cfg "$env:TEMP\rte-security-policy.inf" /quiet
```

O export de `secedit` pode conter nomes/SIDs; sanitize antes de versionar.

## Modelo de conta local de serviço

Use virtual accounts ou built-in service identities quando suportadas. Se uma
conta local dedicada for inevitável, gere segredo fora do script, negue logon
interativo, conceda somente o direito necessário e defina rotação/owner.

## Exercício

Modele, sem criar, as identidades de um serviço fictício. Liste recurso, direito,
ACL, segredo, owner, auditoria e desativação.

