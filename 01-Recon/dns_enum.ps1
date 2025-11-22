# ================================================================
# Script: DNS Enumeration Tool
# Descrição: Script educacional para enumeração DNS segura
# Autor: RedTeam Essentials
# Versão: 1.0
# Data: 2025
# ================================================================

# ⚠️ IMPORTANTE: Use apenas em domínios que você tem autorização!
# Este script é para fins educacionais e de pesquisa.

<#
.SYNOPSIS
    Realiza enumeração DNS de um domínio de forma segura e organizada.

.DESCRIPTION
    Este script coleta informações DNS públicas sobre um domínio:
    - Registros A (IPv4)
    - Registros AAAA (IPv6)
    - Registros MX (Mail Servers)
    - Registros TXT (SPF, DMARC, etc.)
    - Registros NS (Name Servers)
    - Registros SOA (Start of Authority)
    
    Todos os dados são públicos e o script não interage diretamente com o alvo.

.PARAMETER Domain
    O domínio a ser enumerado (ex: exemplo.com)

.PARAMETER OutputFile
    Caminho para salvar os resultados (opcional)

.PARAMETER Verbose
    Mostra informações detalhadas durante a execução

.EXAMPLE
    .\dns_enum.ps1 -Domain "exemplo.com"
    
.EXAMPLE
    .\dns_enum.ps1 -Domain "exemplo.com" -OutputFile "C:\temp\resultado.txt"

.NOTES
    Requisitos: Windows PowerShell 5.1 ou superior
    Não requer privilégios administrativos
#>

# Parâmetros do script
param(
    # Domínio alvo - obrigatório
    [Parameter(Mandatory=$true, HelpMessage="Digite o domínio para enumerar (ex: exemplo.com)")]
    [ValidateNotNullOrEmpty()]
    [string]$Domain,
    
    # Arquivo de saída - opcional
    [Parameter(Mandatory=$false)]
    [string]$OutputFile = "",
    
    # Modo verbose - opcional
    [Parameter(Mandatory=$false)]
    [switch]$VerboseOutput
)

# ================================================================
# FUNÇÕES AUXILIARES
# ================================================================

# Função para exibir banner do script
function Show-Banner {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║         DNS Enumeration Tool - Educational           ║" -ForegroundColor Cyan
    Write-Host "║              RedTeam Essentials v1.0                  ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

# Função para validar se o domínio tem formato válido
function Test-DomainFormat {
    param([string]$DomainToTest)
    
    # Regex simples para validar formato de domínio
    # Aceita: exemplo.com, sub.exemplo.com, etc.
    $domainRegex = '^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    
    if ($DomainToTest -match $domainRegex) {
        return $true
    } else {
        Write-Host "[!] Formato de domínio inválido: $DomainToTest" -ForegroundColor Red
        return $false
    }
}

# Função para criar seção visual no output
function Write-Section {
    param([string]$Title)
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host "  $Title" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host ""
}

# Função para salvar resultados em arquivo
function Save-ToFile {
    param(
        [string]$Content,
        [string]$FilePath
    )
    
    # Se o caminho do arquivo foi fornecido, salva o conteúdo
    if ($FilePath -ne "") {
        try {
            # Add-Content adiciona ao final do arquivo (append)
            Add-Content -Path $FilePath -Value $Content -ErrorAction Stop
        } catch {
            Write-Host "[!] Erro ao salvar no arquivo: $_" -ForegroundColor Red
        }
    }
}

# Função para formatar data/hora
function Get-Timestamp {
    return Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

# ================================================================
# FUNÇÕES DE ENUMERAÇÃO DNS
# ================================================================

# Função para obter registros A (IPv4)
function Get-ARecords {
    param([string]$TargetDomain)
    
    Write-Section "Registros A (IPv4)"
    
    try {
        # Resolve-DnsName é o cmdlet nativo do PowerShell para DNS
        # -Type A especifica que queremos apenas registros A
        # -ErrorAction Stop garante que erros sejam capturados
        $aRecords = Resolve-DnsName -Name $TargetDomain -Type A -ErrorAction Stop
        
        # Verifica se encontrou algum registro
        if ($aRecords) {
            foreach ($record in $aRecords) {
                # IPAddress contém o endereço IPv4
                $output = "[+] IPv4: $($record.IPAddress)"
                Write-Host $output -ForegroundColor Green
                Save-ToFile -Content $output -FilePath $OutputFile
            }
        } else {
            $output = "[-] Nenhum registro A encontrado"
            Write-Host $output -ForegroundColor Yellow
            Save-ToFile -Content $output -FilePath $OutputFile
        }
    } catch {
        # Captura qualquer erro (ex: domínio não existe)
        $output = "[!] Erro ao consultar registros A: $($_.Exception.Message)"
        Write-Host $output -ForegroundColor Red
        Save-ToFile -Content $output -FilePath $OutputFile
    }
}

# Função para obter registros AAAA (IPv6)
function Get-AAAARecords {
    param([string]$TargetDomain)
    
    Write-Section "Registros AAAA (IPv6)"
    
    try {
        # Type AAAA para endereços IPv6
        $aaaaRecords = Resolve-DnsName -Name $TargetDomain -Type AAAA -ErrorAction Stop
        
        if ($aaaaRecords) {
            foreach ($record in $aaaaRecords) {
                $output = "[+] IPv6: $($record.IPAddress)"
                Write-Host $output -ForegroundColor Green
                Save-ToFile -Content $output -FilePath $OutputFile
            }
        } else {
            $output = "[-] Nenhum registro AAAA encontrado"
            Write-Host $output -ForegroundColor Yellow
            Save-ToFile -Content $output -FilePath $OutputFile
        }
    } catch {
        # Muitos domínios não têm IPv6, então isso é comum
        $output = "[-] Sem registros AAAA (IPv6 não configurado)"
        Write-Host $output -ForegroundColor Yellow
        Save-ToFile -Content $output -FilePath $OutputFile
    }
}

# Função para obter registros MX (Mail Exchange)
function Get-MXRecords {
    param([string]$TargetDomain)
    
    Write-Section "Registros MX (Servidores de Email)"
    
    try {
        # Type MX para servidores de email
        $mxRecords = Resolve-DnsName -Name $TargetDomain -Type MX -ErrorAction Stop
        
        if ($mxRecords) {
            foreach ($record in $mxRecords) {
                # NameExchange contém o nome do servidor de email
                # Preference é a prioridade (menor = maior prioridade)
                $output = "[+] Mail Server: $($record.NameExchange) (Prioridade: $($record.Preference))"
                Write-Host $output -ForegroundColor Green
                Save-ToFile -Content $output -FilePath $OutputFile
            }
        } else {
            $output = "[-] Nenhum registro MX encontrado"
            Write-Host $output -ForegroundColor Yellow
            Save-ToFile -Content $output -FilePath $OutputFile
        }
    } catch {
        $output = "[!] Erro ao consultar registros MX: $($_.Exception.Message)"
        Write-Host $output -ForegroundColor Red
        Save-ToFile -Content $output -FilePath $OutputFile
    }
}

# Função para obter registros TXT (Texto - SPF, DMARC, etc.)
function Get-TXTRecords {
    param([string]$TargetDomain)
    
    Write-Section "Registros TXT (SPF, DMARC, Verificações)"
    
    try {
        # Type TXT pode conter várias informações de segurança
        $txtRecords = Resolve-DnsName -Name $TargetDomain -Type TXT -ErrorAction Stop
        
        if ($txtRecords) {
            foreach ($record in $txtRecords) {
                # Strings contém o conteúdo do registro TXT
                $txtContent = $record.Strings -join " "
                
                # Identifica o tipo de registro TXT
                if ($txtContent -like "*v=spf1*") {
                    $type = "SPF (Sender Policy Framework)"
                } elseif ($txtContent -like "*v=DMARC1*") {
                    $type = "DMARC (Domain-based Message Authentication)"
                } elseif ($txtContent -like "*google-site-verification*") {
                    $type = "Google Site Verification"
                } else {
                    $type = "TXT Genérico"
                }
                
                $output = "[+] $type`n    $txtContent"
                Write-Host $output -ForegroundColor Green
                Save-ToFile -Content $output -FilePath $OutputFile
            }
        } else {
            $output = "[-] Nenhum registro TXT encontrado"
            Write-Host $output -ForegroundColor Yellow
            Save-ToFile -Content $output -FilePath $OutputFile
        }
    } catch {
        $output = "[!] Erro ao consultar registros TXT: $($_.Exception.Message)"
        Write-Host $output -ForegroundColor Red
        Save-ToFile -Content $output -FilePath $OutputFile
    }
}

# Função para obter registros NS (Name Servers)
function Get-NSRecords {
    param([string]$TargetDomain)
    
    Write-Section "Registros NS (Servidores de Nomes)"
    
    try {
        # Type NS mostra quais servidores DNS são autoritativos
        $nsRecords = Resolve-DnsName -Name $TargetDomain -Type NS -ErrorAction Stop
        
        if ($nsRecords) {
            foreach ($record in $nsRecords) {
                # NameHost contém o servidor DNS
                $output = "[+] Name Server: $($record.NameHost)"
                Write-Host $output -ForegroundColor Green
                Save-ToFile -Content $output -FilePath $OutputFile
            }
        } else {
            $output = "[-] Nenhum registro NS encontrado"
            Write-Host $output -ForegroundColor Yellow
            Save-ToFile -Content $output -FilePath $OutputFile
        }
    } catch {
        $output = "[!] Erro ao consultar registros NS: $($_.Exception.Message)"
        Write-Host $output -ForegroundColor Red
        Save-ToFile -Content $output -FilePath $OutputFile
    }
}

# Função para obter registro SOA (Start of Authority)
function Get-SOARecord {
    param([string]$TargetDomain)
    
    Write-Section "Registro SOA (Start of Authority)"
    
    try {
        # Type SOA contém informações administrativas da zona DNS
        $soaRecord = Resolve-DnsName -Name $TargetDomain -Type SOA -ErrorAction Stop
        
        if ($soaRecord) {
            foreach ($record in $soaRecord) {
                Write-Host "[+] Servidor Primário: $($record.PrimaryServer)" -ForegroundColor Green
                Write-Host "[+] Email do Administrador: $($record.Administrator)" -ForegroundColor Green
                Write-Host "[+] Serial: $($record.SerialNumber)" -ForegroundColor Green
                
                # Salva no arquivo
                $output = "[+] SOA - Servidor: $($record.PrimaryServer), Admin: $($record.Administrator)"
                Save-ToFile -Content $output -FilePath $OutputFile
            }
        }
    } catch {
        $output = "[-] Não foi possível obter registro SOA"
        Write-Host $output -ForegroundColor Yellow
        Save-ToFile -Content $output -FilePath $OutputFile
    }
}

# ================================================================
# LÓGICA PRINCIPAL DO SCRIPT
# ================================================================

# Limpa a tela para melhor visualização
Clear-Host

# Exibe o banner
Show-Banner

# Registra o início da execução
$startTime = Get-Date
$timestamp = Get-Timestamp

# Validação do domínio
Write-Host "[*] Validando domínio: $Domain" -ForegroundColor Cyan
if (-not (Test-DomainFormat -DomainToTest $Domain)) {
    Write-Host "[!] Domínio inválido. Encerrando..." -ForegroundColor Red
    exit 1
}

Write-Host "[✓] Domínio válido!" -ForegroundColor Green

# Se arquivo de saída foi especificado, prepara o arquivo
if ($OutputFile -ne "") {
    # Cria cabeçalho do arquivo
    $header = @"
════════════════════════════════════════════════════════
DNS ENUMERATION REPORT
════════════════════════════════════════════════════════
Domínio: $Domain
Data/Hora: $timestamp
Ferramenta: RedTeam Essentials DNS Enum v1.0
════════════════════════════════════════════════════════

"@
    
    try {
        # Out-File sobrescreve o arquivo (não append)
        Out-File -FilePath $OutputFile -InputObject $header -Encoding UTF8 -Force
        Write-Host "[*] Resultados serão salvos em: $OutputFile" -ForegroundColor Cyan
    } catch {
        Write-Host "[!] Não foi possível criar arquivo de saída: $_" -ForegroundColor Red
        $OutputFile = ""  # Desabilita salvamento
    }
}

Write-Host ""
Write-Host "[*] Iniciando enumeração DNS de: $Domain" -ForegroundColor Cyan
Write-Host "[*] Timestamp: $timestamp" -ForegroundColor Cyan

# Executa todas as funções de enumeração em sequência
# Cada função é independente e trata seus próprios erros

Get-ARecords -TargetDomain $Domain
Get-AAAARecords -TargetDomain $Domain
Get-MXRecords -TargetDomain $Domain
Get-TXTRecords -TargetDomain $Domain
Get-NSRecords -TargetDomain $Domain
Get-SOARecord -TargetDomain $Domain

# Calcula tempo total de execução
$endTime = Get-Date
$duration = $endTime - $startTime

# Exibe resumo final
Write-Section "Resumo da Execução"
Write-Host "[✓] Enumeração concluída com sucesso!" -ForegroundColor Green
Write-Host "[*] Tempo de execução: $($duration.TotalSeconds) segundos" -ForegroundColor Cyan

if ($OutputFile -ne "") {
    Write-Host "[*] Resultados salvos em: $OutputFile" -ForegroundColor Cyan
    
    # Adiciona rodapé ao arquivo
    $footer = @"

════════════════════════════════════════════════════════
Execução finalizada em: $(Get-Timestamp)
Tempo total: $($duration.TotalSeconds) segundos
════════════════════════════════════════════════════════
"@
    Save-ToFile -Content $footer -FilePath $OutputFile
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Obrigado por usar RedTeam Essentials!" -ForegroundColor Cyan
Write-Host "  Use este conhecimento de forma ética e legal." -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ================================================================
# FIM DO SCRIPT
# ================================================================

<#
NOTAS DE USO:

1. Execução básica:
   .\dns_enum.ps1 -Domain "exemplo.com"

2. Salvar resultados:
   .\dns_enum.ps1 -Domain "exemplo.com" -OutputFile "C:\resultados\dns_exemplo.txt"

3. Modo verbose (futuro):
   .\dns_enum.ps1 -Domain "exemplo.com" -VerboseOutput

DICAS:
- Use sempre em domínios que você tem autorização
- Os dados coletados são públicos e disponíveis via DNS
- Combine com outras ferramentas de OSINT para análise completa
- Documente tudo em seus relatórios de pentest

PRÓXIMOS PASSOS:
- Adicionar enumeração de subdomínios
- Implementar verificação de zone transfer
- Adicionar suporte a múltiplos domínios
- Exportar para JSON/CSV
#>
