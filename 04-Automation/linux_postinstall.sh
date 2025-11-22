#!/bin/bash

# ================================================================
# Script: Linux Post-Install Automation
# Descrição: Configuração automatizada pós-instalação para Kali/Ubuntu
# Autor: RedTeam Essentials
# Versão: 1.0
# Data: 2025
# ================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║      Linux Post-Install - RedTeam Essentials             ║"
echo "║      Configuração Automatizada v1.0                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verifica se está rodando como root
if [[ $EUID -ne 0 ]]; then
   echo -e "${YELLOW}[!] Este script precisa ser executado como root${NC}"
   echo -e "${YELLOW}[*] Execute: sudo ./linux_postinstall.sh${NC}"
   exit 1
fi

echo -e "${GREEN}[✓] Executando como root${NC}"
echo ""

# ================================================================
# ATUALIZAÇÃO DO SISTEMA
# ================================================================

echo -e "${CYAN}═══ Atualizando Sistema ═══${NC}"
apt update && apt upgrade -y
apt dist-upgrade -y
echo -e "${GREEN}[+] Sistema atualizado${NC}"
echo ""

# ================================================================
# INSTALAÇÃO DE FERRAMENTAS ESSENCIAIS
# ================================================================

echo -e "${CYAN}═══ Instalando Ferramentas Essenciais ═══${NC}"

# Ferramentas de desenvolvimento
apt install -y git vim curl wget build-essential python3-pip

# Ferramentas de rede
apt install -y nmap netcat-traditional tcpdump wireshark

# Ferramentas de pentest (se Kali)
if grep -q "kali" /etc/os-release; then
    echo -e "${CYAN}[*] Kali Linux detectado - instalando ferramentas adicionais${NC}"
    apt install -y metasploit-framework burpsuite zaproxy sqlmap
fi

echo -e "${GREEN}[+] Ferramentas instaladas${NC}"
echo ""

# ================================================================
# CONFIGURAÇÃO DO SISTEMA
# ================================================================

echo -e "${CYAN}═══ Configurando Sistema ═══${NC}"

# Criar estrutura de pastas
PENTEST_DIR="$HOME/Pentest"
mkdir -p "$PENTEST_DIR"/{Tools,Scripts,Wordlists,Exploits,Notes,Labs,Reports,Logs}
echo -e "${GREEN}[+] Estrutura de pastas criada em $PENTEST_DIR${NC}"

# Configurar aliases úteis
cat >> "$HOME/.bashrc" << 'EOF'

# RedTeam Essentials Aliases
alias ll='ls -lah'
alias update='sudo apt update && sudo apt upgrade -y'
alias ports='netstat -tulanp'
alias myip='curl -s ifconfig.me'
alias serve='python3 -m http.server 8000'
EOF

echo -e "${GREEN}[+] Aliases configurados${NC}"
echo ""

# ================================================================
# LIMPEZA
# ================================================================

echo -e "${CYAN}═══ Limpeza do Sistema ═══${NC}"
apt autoremove -y
apt autoclean -y
echo -e "${GREEN}[+] Limpeza concluída${NC}"
echo ""

# ================================================================
# RESUMO
# ================================================================

echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  CONFIGURAÇÃO CONCLUÍDA${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Próximos passos:${NC}"
echo -e "  1. Execute: ${YELLOW}source ~/.bashrc${NC}"
echo -e "  2. Estrutura criada em: ${YELLOW}$PENTEST_DIR${NC}"
echo -e "  3. Teste os aliases: ${YELLOW}ll${NC}"
echo ""
echo -e "${GREEN}Script finalizado!${NC}"
