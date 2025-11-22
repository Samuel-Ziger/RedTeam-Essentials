# ================================================================
# Script: OSINT Automation Tool
# Descrição: Automação ética de coleta OSINT de domínios
# Autor: RedTeam Essentials
# Versão: 1.0
# Data: 2025
# ================================================================

# ⚠️ IMPORTANTE: Use apenas para pesquisa legal e autorizada!
# Este script coleta apenas informações publicamente disponíveis.

<#
.SYNOPSIS
    Automatiza coleta básica de OSINT de um domínio.

.DESCRIPTION
    Este script realiza coleta automatizada de informações OSINT:
    - Resolução DNS (A, MX, TXT, NS)
    - Enumeração de subdomínios via Certificate Transparency
    - Coleta de informações WHOIS
    - Verificação de tecnologias web
    - Busca de emails públicos
    - Geração de relatório consolidado
    
    Todas as informações são de fontes públicas e legais.

.PARAMETER Domain
    Domínio alvo para coleta OSINT

.PARAMETER OutputDir
    Diretório onde os resultados serão salvos

.PARAMETER IncludeSubdomains
    Se deve incluir enumeração de subdomínios

.PARAMETER DeepScan
    Realiza análise mais profunda (mais demorado)

.EXAMPLE
    .\osint_automation.ps1 -Domain "exemplo.com"
    
.EXAMPLE
    .\osint_automation.ps1 -Domain "exemplo.com" -OutputDir "C:\OSINT\resultado" -IncludeSubdomains

.NOTES
    Requisitos: PowerShell 5.1+, conexão com internet
    Não requer privilégios administrativos
#>

param(
    # Domínio alvo - obrigatório
    [Parameter(Mandatory=$true, HelpMessage="Digite o domínio para análise OSINT")]
    [ValidateNotNullOrEmpty()]
    [string]$Domain,
    
    # Diretório de saída - opcional
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = ".\OSINT_Results",
    
    # Incluir subdomínios - opcional
    [Parameter(Mandatory=$false)]
    [switch]$IncludeSubdomains,
    
    # Scan profundo - opcional
    [Parameter(Mandatory=$false)]
    [switch]$DeepScan
)

# ================================================================
# CONFIGURAÇÕES GLOBAIS
# ================================================================

# Limpa a tela
Clear-Host

# Define cores para output
$ColorSuccess = "Green"
$ColorInfo = "Cyan"
$ColorWarning = "Yellow"
$ColorError = "Red"

# Variável global para armazenar dados coletados
$global:OSINTData = @{
    Domain = $Domain
    CollectionDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    DNS = @{}
    Subdomains = @()
    WHOIS = @{}
    Emails = @()
    Technologies = @()
}

# ================================================================
# FUNÇÕES AUXILIARES
# ================================================================

# Função para exibir banner
function Show-Banner {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor $ColorInfo
    Write-Host "║           OSINT Automation Tool v1.0                     ║" -ForegroundColor $ColorInfo
    Write-Host "║           RedTeam Essentials - Educational               ║" -ForegroundColor $ColorInfo
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor $ColorInfo
    Write-Host ""
}

# Função para criar seção visual
function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
    Write-Host "  $Title" -ForegroundColor $ColorInfo
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
    Write-Host ""
}

# Função para criar diretório de output se não existir
function Initialize-OutputDirectory {
    param([string]$Path)
    
    try {
        # Test-Path verifica se o caminho existe
        if (-not (Test-Path -Path $Path)) {
            # New-Item cria o diretório
            New-Item -ItemType Directory -Path $Path -Force | Out-Null
            Write-Host "[+] Diretório de output criado: $Path" -ForegroundColor $ColorSuccess
        } else {
            Write-Host "[*] Usando diretório existente: $Path" -ForegroundColor $ColorInfo
        }
        return $true
    } catch {
        Write-Host "[!] Erro ao criar diretório: $_" -ForegroundColor $ColorError
        return $false
    }
}

# Função para validar formato de domínio
function Test-DomainFormat {
    param([string]$DomainToTest)
    
    # Regex para validar domínio
    # Formato: exemplo.com, sub.exemplo.com
    $domainRegex = '^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    
    return ($DomainToTest -match $domainRegex)
}

# Função para testar conectividade com a internet
function Test-InternetConnection {
    Write-Host "[*] Testando conectividade com a internet..." -ForegroundColor $ColorInfo
    
    try {
        # Tenta fazer ping no DNS público do Google
        $ping = Test-Connection -ComputerName "8.8.8.8" -Count 2 -Quiet
        
        if ($ping) {
            Write-Host "[✓] Conexão com internet OK" -ForegroundColor $ColorSuccess
            return $true
        } else {
            Write-Host "[!] Sem conexão com internet" -ForegroundColor $ColorError
            return $false
        }
    } catch {
        Write-Host "[!] Erro ao testar conexão: $_" -ForegroundColor $ColorError
        return $false
    }
}

# ================================================================
# FUNÇÕES DE COLETA OSINT
# ================================================================

# Função para coletar registros DNS
function Get-DNSInformation {
    param([string]$TargetDomain)
    
    Write-Section "Coleta de Informações DNS"
    
    # Array para armazenar todos os registros DNS
    $dnsRecords = @{
        A = @()
        AAAA = @()
        MX = @()
        TXT = @()
        NS = @()
        SOA = $null
    }
    
    # Registros A (IPv4)
    try {
        Write-Host "[*] Consultando registros A..." -ForegroundColor $ColorInfo
        $aRecords = Resolve-DnsName -Name $TargetDomain -Type A -ErrorAction SilentlyContinue
        if ($aRecords) {
            foreach ($record in $aRecords) {
                $dnsRecords.A += $record.IPAddress
                Write-Host "  [+] IPv4: $($record.IPAddress)" -ForegroundColor $ColorSuccess
            }
        }
    } catch {
        Write-Host "  [-] Nenhum registro A encontrado" -ForegroundColor $ColorWarning
    }
    
    # Registros AAAA (IPv6)
    try {
        Write-Host "[*] Consultando registros AAAA..." -ForegroundColor $ColorInfo
        $aaaaRecords = Resolve-DnsName -Name $TargetDomain -Type AAAA -ErrorAction SilentlyContinue
        if ($aaaaRecords) {
            foreach ($record in $aaaaRecords) {
                $dnsRecords.AAAA += $record.IPAddress
                Write-Host "  [+] IPv6: $($record.IPAddress)" -ForegroundColor $ColorSuccess
            }
        }
    } catch {
        Write-Host "  [-] Nenhum registro AAAA encontrado" -ForegroundColor $ColorWarning
    }
    
    # Registros MX (Mail Servers)
    try {
        Write-Host "[*] Consultando registros MX..." -ForegroundColor $ColorInfo
        $mxRecords = Resolve-DnsName -Name $TargetDomain -Type MX -ErrorAction SilentlyContinue
        if ($mxRecords) {
            foreach ($record in $mxRecords) {
                $mxInfo = @{
                    Server = $record.NameExchange
                    Priority = $record.Preference
                }
                $dnsRecords.MX += $mxInfo
                Write-Host "  [+] Mail Server: $($record.NameExchange) (Prioridade: $($record.Preference))" -ForegroundColor $ColorSuccess
            }
        }
    } catch {
        Write-Host "  [-] Nenhum registro MX encontrado" -ForegroundColor $ColorWarning
    }
    
    # Registros TXT (SPF, DMARC, etc.)
    try {
        Write-Host "[*] Consultando registros TXT..." -ForegroundColor $ColorInfo
        $txtRecords = Resolve-DnsName -Name $TargetDomain -Type TXT -ErrorAction SilentlyContinue
        if ($txtRecords) {
            foreach ($record in $txtRecords) {
                $txtContent = $record.Strings -join " "
                $dnsRecords.TXT += $txtContent
                Write-Host "  [+] TXT: $txtContent" -ForegroundColor $ColorSuccess
            }
        }
    } catch {
        Write-Host "  [-] Nenhum registro TXT encontrado" -ForegroundColor $ColorWarning
    }
    
    # Registros NS (Name Servers)
    try {
        Write-Host "[*] Consultando registros NS..." -ForegroundColor $ColorInfo
        $nsRecords = Resolve-DnsName -Name $TargetDomain -Type NS -ErrorAction SilentlyContinue
        if ($nsRecords) {
            foreach ($record in $nsRecords) {
                $dnsRecords.NS += $record.NameHost
                Write-Host "  [+] Name Server: $($record.NameHost)" -ForegroundColor $ColorSuccess
            }
        }
    } catch {
        Write-Host "  [-] Nenhum registro NS encontrado" -ForegroundColor $ColorWarning
    }
    
    # Registro SOA
    try {
        Write-Host "[*] Consultando registro SOA..." -ForegroundColor $ColorInfo
        $soaRecord = Resolve-DnsName -Name $TargetDomain -Type SOA -ErrorAction SilentlyContinue
        if ($soaRecord) {
            $dnsRecords.SOA = @{
                PrimaryServer = $soaRecord.PrimaryServer
                Administrator = $soaRecord.Administrator
                SerialNumber = $soaRecord.SerialNumber
            }
            Write-Host "  [+] SOA: $($soaRecord.PrimaryServer)" -ForegroundColor $ColorSuccess
        }
    } catch {
        Write-Host "  [-] Nenhum registro SOA encontrado" -ForegroundColor $ColorWarning
    }
    
    # Armazena no objeto global
    $global:OSINTData.DNS = $dnsRecords
    
    return $dnsRecords
}

# Função para coletar informações WHOIS
function Get-WHOISInformation {
    param([string]$TargetDomain)
    
    Write-Section "Coleta de Informações WHOIS"
    
    Write-Host "[*] Consultando WHOIS..." -ForegroundColor $ColorInfo
    Write-Host "[!] Nota: PowerShell nativo não tem cliente WHOIS integrado" -ForegroundColor $ColorWarning
    Write-Host "[*] Recomendação: Use ferramentas online ou instale módulo específico" -ForegroundColor $ColorInfo
    Write-Host ""
    Write-Host "    Opções recomendadas:" -ForegroundColor $ColorInfo
    Write-Host "    1. https://who.is/$TargetDomain" -ForegroundColor $ColorInfo
    Write-Host "    2. https://whois.domaintools.com/$TargetDomain" -ForegroundColor $ColorInfo
    Write-Host "    3. Comando Linux: whois $TargetDomain" -ForegroundColor $ColorInfo
    
    # Aqui poderíamos fazer uma requisição web para API WHOIS
    # Mas mantemos simples para fins educacionais
    
    $whoisInfo = @{
        Message = "WHOIS deve ser consultado manualmente ou via API"
        Suggestions = @(
            "https://who.is/$TargetDomain",
            "https://whois.domaintools.com/$TargetDomain"
        )
    }
    
    $global:OSINTData.WHOIS = $whoisInfo
    return $whoisInfo
}

# Função para buscar subdomínios via Certificate Transparency
function Get-SubdomainsFromCertificates {
    param([string]$TargetDomain)
    
    Write-Section "Enumeração de Subdomínios (Certificate Transparency)"
    
    Write-Host "[*] Buscando subdomínios via crt.sh..." -ForegroundColor $ColorInfo
    
    try {
        # URL da API do crt.sh
        # Retorna JSON com todos os certificados SSL do domínio
        $url = "https://crt.sh/?q=%25.$TargetDomain&output=json"
        
        Write-Host "[*] Consultando: $url" -ForegroundColor $ColorInfo
        
        # Invoke-RestMethod faz requisição HTTP e converte JSON automaticamente
        # -UseBasicParsing evita dependência do IE
        $response = Invoke-RestMethod -Uri $url -Method Get -UseBasicParsing -TimeoutSec 30
        
        # HashSet para eliminar duplicatas
        $subdomains = @{}
        
        foreach ($cert in $response) {
            # name_value contém o nome do domínio no certificado
            # Pode conter múltiplos domínios separados por \n
            $names = $cert.name_value -split "`n"
            
            foreach ($name in $names) {
                # Remove wildcards (*.exemplo.com -> exemplo.com)
                $cleanName = $name.Trim().Replace("*.", "")
                
                # Adiciona ao HashSet (evita duplicatas automaticamente)
                if ($cleanName -like "*$TargetDomain" -and -not $subdomains.ContainsKey($cleanName)) {
                    $subdomains[$cleanName] = $true
                    Write-Host "  [+] Subdomínio encontrado: $cleanName" -ForegroundColor $ColorSuccess
                }
            }
        }
        
        # Converte HashSet para array
        $subdomainList = $subdomains.Keys | Sort-Object
        
        Write-Host ""
        Write-Host "[✓] Total de subdomínios únicos encontrados: $($subdomainList.Count)" -ForegroundColor $ColorSuccess
        
        # Armazena no objeto global
        $global:OSINTData.Subdomains = $subdomainList
        
        return $subdomainList
        
    } catch {
        Write-Host "[!] Erro ao consultar crt.sh: $_" -ForegroundColor $ColorError
        Write-Host "[*] Isso pode ocorrer se o domínio não tiver certificados SSL públicos" -ForegroundColor $ColorWarning
        return @()
    }
}

# Função para extrair possíveis emails (simulado)
function Get-PossibleEmails {
    param([string]$TargetDomain)
    
    Write-Section "Análise de Padrões de Email"
    
    Write-Host "[*] Gerando possíveis padrões de email..." -ForegroundColor $ColorInfo
    Write-Host "[!] Nota: Esta é uma análise educacional de padrões comuns" -ForegroundColor $ColorWarning
    Write-Host ""
    
    # Padrões comuns de email corporativo
    $commonPatterns = @(
        "contato@$TargetDomain",
        "info@$TargetDomain",
        "suporte@$TargetDomain",
        "vendas@$TargetDomain",
        "admin@$TargetDomain",
        "webmaster@$TargetDomain",
        "rh@$TargetDomain",
        "marketing@$TargetDomain"
    )
    
    Write-Host "Padrões comuns de email para $TargetDomain :" -ForegroundColor $ColorInfo
    Write-Host ""
    
    foreach ($email in $commonPatterns) {
        Write-Host "  [*] $email" -ForegroundColor $ColorInfo
    }
    
    Write-Host ""
    Write-Host "[!] Para coleta real de emails, use:" -ForegroundColor $ColorWarning
    Write-Host "    - theHarvester (CLI)" -ForegroundColor $ColorInfo
    Write-Host "    - Hunter.io (Web)" -ForegroundColor $ColorInfo
    Write-Host "    - Phonebook.cz (Web)" -ForegroundColor $ColorInfo
    
    $global:OSINTData.Emails = $commonPatterns
    return $commonPatterns
}

# Função para verificar tecnologias web (simulado)
function Get-WebTechnologies {
    param([string]$TargetDomain)
    
    Write-Section "Identificação de Tecnologias Web"
    
    Write-Host "[*] Tentando identificar servidor web..." -ForegroundColor $ColorInfo
    
    try {
        # Faz requisição HTTP HEAD para obter headers sem baixar o conteúdo
        $url = "https://$TargetDomain"
        
        # Invoke-WebRequest faz requisição HTTP completa
        # -Method Head solicita apenas cabeçalhos
        $response = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
        
        Write-Host ""
        Write-Host "Cabeçalhos HTTP encontrados:" -ForegroundColor $ColorSuccess
        Write-Host ""
        
        # Cabeçalhos que revelam tecnologias
        $interestingHeaders = @("Server", "X-Powered-By", "X-AspNet-Version", "X-Generator")
        
        foreach ($headerName in $interestingHeaders) {
            if ($response.Headers.ContainsKey($headerName)) {
                $headerValue = $response.Headers[$headerName]
                Write-Host "  [+] $headerName : $headerValue" -ForegroundColor $ColorSuccess
                $global:OSINTData.Technologies += "$headerName : $headerValue"
            }
        }
        
        # Verifica status code
        Write-Host "  [*] Status Code: $($response.StatusCode)" -ForegroundColor $ColorInfo
        
    } catch {
        Write-Host "[!] Não foi possível acessar https://$TargetDomain" -ForegroundColor $ColorWarning
        Write-Host "[*] Tentando HTTP..." -ForegroundColor $ColorInfo
        
        try {
            $url = "http://$TargetDomain"
            $response = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
            Write-Host "  [+] HTTP acessível" -ForegroundColor $ColorSuccess
        } catch {
            Write-Host "[!] Não foi possível acessar o domínio" -ForegroundColor $ColorError
        }
    }
    
    Write-Host ""
    Write-Host "[!] Para análise completa de tecnologias, use:" -ForegroundColor $ColorWarning
    Write-Host "    - Wappalyzer (Browser Extension)" -ForegroundColor $ColorInfo
    Write-Host "    - BuiltWith.com (Web)" -ForegroundColor $ColorInfo
    Write-Host "    - WhatWeb (CLI)" -ForegroundColor $ColorInfo
}

# ================================================================
# FUNÇÕES DE RELATÓRIO
# ================================================================

# Função para gerar relatório em texto
function Export-TextReport {
    param(
        [string]$OutputPath,
        [hashtable]$Data
    )
    
    $reportPath = Join-Path -Path $OutputPath -ChildPath "OSINT_Report_$($Data.Domain)_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
    
    # Cria conteúdo do relatório
    $reportContent = @"
╔═══════════════════════════════════════════════════════════╗
║           RELATÓRIO DE OSINT - REDTEAM ESSENTIALS        ║
╚═══════════════════════════════════════════════════════════╝

INFORMAÇÕES GERAIS
═══════════════════════════════════════════════════════════
Domínio Alvo: $($Data.Domain)
Data/Hora da Coleta: $($Data.CollectionDate)
Ferramenta: OSINT Automation Tool v1.0

═══════════════════════════════════════════════════════════
REGISTROS DNS
═══════════════════════════════════════════════════════════

Registros A (IPv4):
$($Data.DNS.A | ForEach-Object { "  - $_" } | Out-String)

Registros AAAA (IPv6):
$($Data.DNS.AAAA | ForEach-Object { "  - $_" } | Out-String)

Registros MX (Mail Servers):
$($Data.DNS.MX | ForEach-Object { "  - $($_.Server) (Prioridade: $($_.Priority))" } | Out-String)

Registros TXT:
$($Data.DNS.TXT | ForEach-Object { "  - $_" } | Out-String)

Registros NS (Name Servers):
$($Data.DNS.NS | ForEach-Object { "  - $_" } | Out-String)

Registro SOA:
$( if ($Data.DNS.SOA) { "  - Servidor Primário: $($Data.DNS.SOA.PrimaryServer)`n  - Administrador: $($Data.DNS.SOA.Administrator)" } else { "  - Não encontrado" } )

═══════════════════════════════════════════════════════════
SUBDOMÍNIOS ENCONTRADOS
═══════════════════════════════════════════════════════════
Total: $($Data.Subdomains.Count)

$($Data.Subdomains | ForEach-Object { "  - $_" } | Out-String)

═══════════════════════════════════════════════════════════
PADRÕES DE EMAIL
═══════════════════════════════════════════════════════════

$($Data.Emails | ForEach-Object { "  - $_" } | Out-String)

═══════════════════════════════════════════════════════════
TECNOLOGIAS WEB
═══════════════════════════════════════════════════════════

$($Data.Technologies | ForEach-Object { "  - $_" } | Out-String)

═══════════════════════════════════════════════════════════
RECOMENDAÇÕES DE PRÓXIMOS PASSOS
═══════════════════════════════════════════════════════════

1. Verificar WHOIS manualmente para informações de registro
2. Analisar subdomínios encontrados individualmente
3. Fazer reconhecimento web dos domínios ativos
4. Verificar vazamentos de dados com emails encontrados
5. Usar Shodan/Censys para mapear infraestrutura
6. Buscar repositórios GitHub relacionados à organização
7. Fazer OSINT de funcionários via LinkedIn
8. Analisar tecnologias para vulnerabilidades conhecidas

═══════════════════════════════════════════════════════════
DISCLAIMER
═══════════════════════════════════════════════════════════

Este relatório contém apenas informações publicamente disponíveis
coletadas de forma ética e legal para fins educacionais.

Use estas informações de forma responsável e sempre com autorização.

═══════════════════════════════════════════════════════════
FIM DO RELATÓRIO
═══════════════════════════════════════════════════════════
"@

    # Salva o relatório
    try {
        Out-File -FilePath $reportPath -InputObject $reportContent -Encoding UTF8 -Force
        Write-Host "[✓] Relatório texto salvo em: $reportPath" -ForegroundColor $ColorSuccess
        return $reportPath
    } catch {
        Write-Host "[!] Erro ao salvar relatório: $_" -ForegroundColor $ColorError
        return $null
    }
}

# Função para gerar relatório JSON (para integração com outras ferramentas)
function Export-JSONReport {
    param(
        [string]$OutputPath,
        [hashtable]$Data
    )
    
    $jsonPath = Join-Path -Path $OutputPath -ChildPath "OSINT_Report_$($Data.Domain)_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
    
    try {
        # ConvertTo-Json converte hashtable para JSON
        # -Depth especifica quantos níveis de objetos aninhados converter
        $jsonContent = $Data | ConvertTo-Json -Depth 10
        
        Out-File -FilePath $jsonPath -InputObject $jsonContent -Encoding UTF8 -Force
        Write-Host "[✓] Relatório JSON salvo em: $jsonPath" -ForegroundColor $ColorSuccess
        return $jsonPath
    } catch {
        Write-Host "[!] Erro ao salvar relatório JSON: $_" -ForegroundColor $ColorError
        return $null
    }
}

# ================================================================
# LÓGICA PRINCIPAL
# ================================================================

# Exibe banner
Show-Banner

# Registra tempo de início
$startTime = Get-Date

# Valida domínio
Write-Host "[*] Validando domínio: $Domain" -ForegroundColor $ColorInfo
if (-not (Test-DomainFormat -DomainToTest $Domain)) {
    Write-Host "[!] Formato de domínio inválido!" -ForegroundColor $ColorError
    Write-Host "[!] Use o formato: exemplo.com" -ForegroundColor $ColorError
    exit 1
}
Write-Host "[✓] Domínio válido!" -ForegroundColor $ColorSuccess

# Testa conectividade
if (-not (Test-InternetConnection)) {
    Write-Host "[!] Sem conexão com internet. Encerrando..." -ForegroundColor $ColorError
    exit 1
}

# Inicializa diretório de output
if (-not (Initialize-OutputDirectory -Path $OutputDir)) {
    Write-Host "[!] Não foi possível criar diretório de output. Encerrando..." -ForegroundColor $ColorError
    exit 1
}

Write-Host ""
Write-Host "[*] Iniciando coleta OSINT de: $Domain" -ForegroundColor $ColorInfo
Write-Host "[*] Resultados serão salvos em: $OutputDir" -ForegroundColor $ColorInfo
Write-Host ""

# Executa coletas
Get-DNSInformation -TargetDomain $Domain
Get-WHOISInformation -TargetDomain $Domain

# Subdomínios apenas se solicitado
if ($IncludeSubdomains) {
    Get-SubdomainsFromCertificates -TargetDomain $Domain
} else {
    Write-Host ""
    Write-Host "[*] Enumeração de subdomínios desabilitada" -ForegroundColor $ColorInfo
    Write-Host "[*] Use -IncludeSubdomains para ativar" -ForegroundColor $ColorInfo
}

Get-PossibleEmails -TargetDomain $Domain
Get-WebTechnologies -TargetDomain $Domain

# Gera relatórios
Write-Section "Gerando Relatórios"

$txtReport = Export-TextReport -OutputPath $OutputDir -Data $global:OSINTData
$jsonReport = Export-JSONReport -OutputPath $OutputDir -Data $global:OSINTData

# Calcula tempo de execução
$endTime = Get-Date
$duration = $endTime - $startTime

# Resumo final
Write-Section "Resumo da Execução"

Write-Host "[✓] Coleta OSINT concluída com sucesso!" -ForegroundColor $ColorSuccess
Write-Host ""
Write-Host "Estatísticas:" -ForegroundColor $ColorInfo
Write-Host "  - Registros DNS A: $($global:OSINTData.DNS.A.Count)" -ForegroundColor $ColorInfo
Write-Host "  - Registros MX: $($global:OSINTData.DNS.MX.Count)" -ForegroundColor $ColorInfo
Write-Host "  - Subdomínios: $($global:OSINTData.Subdomains.Count)" -ForegroundColor $ColorInfo
Write-Host "  - Padrões de Email: $($global:OSINTData.Emails.Count)" -ForegroundColor $ColorInfo
Write-Host ""
Write-Host "  - Tempo de execução: $([math]::Round($duration.TotalSeconds, 2)) segundos" -ForegroundColor $ColorInfo
Write-Host ""

if ($txtReport) {
    Write-Host "Relatórios gerados:" -ForegroundColor $ColorSuccess
    Write-Host "  - Texto: $txtReport" -ForegroundColor $ColorSuccess
    Write-Host "  - JSON: $jsonReport" -ForegroundColor $ColorSuccess
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
Write-Host "  Próximos passos recomendados:" -ForegroundColor $ColorInfo
Write-Host "  1. Revisar relatórios gerados" -ForegroundColor $ColorInfo
Write-Host "  2. Validar subdomínios encontrados" -ForegroundColor $ColorInfo
Write-Host "  3. Fazer OSINT manual para dados mais profundos" -ForegroundColor $ColorInfo
Write-Host "  4. Usar ferramentas especializadas (Maltego, Recon-ng)" -ForegroundColor $ColorInfo
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
Write-Host ""
Write-Host "Obrigado por usar RedTeam Essentials!" -ForegroundColor $ColorSuccess
Write-Host "Use este conhecimento de forma ética e responsável." -ForegroundColor $ColorSuccess
Write-Host ""

# ================================================================
# FIM DO SCRIPT
# ================================================================

<#
EXEMPLOS DE USO:

1. Básico:
   .\osint_automation.ps1 -Domain "exemplo.com"

2. Com subdomínios:
   .\osint_automation.ps1 -Domain "exemplo.com" -IncludeSubdomains

3. Com diretório customizado:
   .\osint_automation.ps1 -Domain "exemplo.com" -OutputDir "C:\Temp\OSINT" -IncludeSubdomains

PRÓXIMAS MELHORIAS:
- Integrar com APIs de WHOIS
- Adicionar coleta de emails via theHarvester
- Implementar Shodan integration
- Adicionar verificação de vazamentos via HIBP API
- Gerar relatório HTML visual
- Adicionar mode silencioso (-Quiet)
#>
