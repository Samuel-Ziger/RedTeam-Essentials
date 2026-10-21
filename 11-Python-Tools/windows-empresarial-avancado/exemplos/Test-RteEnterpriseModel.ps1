[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$model = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
if ($model.schema -ne 'rte.windows.enterprise-model/v1') {
    throw 'Schema de modelo desconhecido.'
}

$errors = [System.Collections.Generic.List[string]]::new()
$known = @{}
$groups = @{}

foreach ($identity in @($model.identities)) {
    $id = [string]$identity.id
    if (-not $id -or $known.ContainsKey($id)) {
        $errors.Add("identidade duplicada ou vazia: $id")
    }
    else {
        $known[$id] = 'identity'
    }
    if (-not [string]$identity.owner) {
        $errors.Add("identidade sem owner: $id")
    }
}

foreach ($group in @($model.groups)) {
    $id = [string]$group.id
    if (-not $id -or $known.ContainsKey($id)) {
        $errors.Add("grupo duplicado ou vazio: $id")
    }
    else {
        $known[$id] = 'group'
        $groups[$id] = $group
    }
    if (-not [string]$group.owner) {
        $errors.Add("grupo sem owner: $id")
    }
}

foreach ($group in $groups.Values) {
    foreach ($member in @($group.members)) {
        $memberId = [string]$member
        if (-not $known.ContainsKey($memberId)) {
            $errors.Add("membro desconhecido em $($group.id): $memberId")
        }
        if ($memberId -eq [string]$group.id) {
            $errors.Add("grupo contém a si mesmo: $memberId")
        }
    }
}

$states = @{}
function Test-RteGroupCycle {
    param(
        [Parameter(Mandatory)][string]$GroupId,
        [string[]]$Stack = @()
    )

    if ($states[$GroupId] -eq 1) {
        $cycle = @($Stack + $GroupId) -join ' -> '
        $errors.Add("ciclo de grupos: $cycle")
        return
    }
    if ($states[$GroupId] -eq 2) {
        return
    }

    $states[$GroupId] = 1
    foreach ($member in @($groups[$GroupId].members)) {
        $memberId = [string]$member
        if ($groups.ContainsKey($memberId)) {
            Test-RteGroupCycle -GroupId $memberId -Stack @($Stack + $GroupId)
        }
    }
    $states[$GroupId] = 2
}

foreach ($groupId in @($groups.Keys | Sort-Object)) {
    Test-RteGroupCycle -GroupId $groupId
}

foreach ($permission in @($model.permissions)) {
    if (-not $known.ContainsKey([string]$permission.principal)) {
        $errors.Add("permissão com principal desconhecido: $($permission.principal)")
    }
    if (-not [string]$permission.resource -or -not [string]$permission.access) {
        $errors.Add('permissão sem resource ou access')
    }
}

[pscustomobject][ordered]@{
    Schema = 'rte.windows.enterprise-model-result/v1'
    Valid = $errors.Count -eq 0
    IdentityCount = @($model.identities).Count
    GroupCount = @($model.groups).Count
    PermissionCount = @($model.permissions).Count
    Errors = @($errors)
}

