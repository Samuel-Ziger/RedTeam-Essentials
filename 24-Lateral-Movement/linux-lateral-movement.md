# Movimentação lateral em Linux

> Metodologia para ambientes Linux próprios ou autorizados. O objetivo é provar
> um caminho com conta canário e ação inócua, não instalar acesso persistente,
> coletar chaves ou reutilizar credenciais reais.

## Precondições

Um caminho Linux deve documentar separadamente:

- **alcance:** rota, firewall e porta do serviço;
- **identidade:** conta canário, certificado ou credencial efêmera aprovada;
- **autorização:** grupos, `sudoers`, ACLs, export NFS ou policy da aplicação;
- **confiança:** bastion, agent forwarding, automação, mounts e secrets;
- **objetivo:** consulta inócua que comprova acesso suficiente;
- **reversão:** sessão, arquivo canário, mount, regra ou credencial a remover.

## Famílias de movimento

### SSH

SSH é o caminho mais comum. Analise autenticação por chave/certificado, grupos,
`AllowUsers`/`AllowGroups`, bastion e restrições de comando. Agent forwarding
amplia a confiança do agente local para o host remoto e deve ser evitado ou
fortemente limitado.

**Telemetria:** `auth.log`/journal do `sshd`, origem, usuário, método, fingerprint
da chave/certificado, sessão PAM e árvore de processos.

**Controles:** certificados curtos, MFA no bastion, `PermitRootLogin no`, sem
password quando possível, allowlists, segregação e gravação de sessões.

### Sudo e troca de contexto

`sudo` é elevação local, mas pode habilitar o próximo salto quando o comando tem
acesso a rede, sockets ou credenciais de automação. Revise regras por comando,
host e usuário; não trate participação no grupo como prova suficiente.

**Telemetria:** journal/auth log, TTY, usuário invocador, target user e comando.

### NFS e compartilhamentos

Exports NFS podem expor dados ou confiar em identidade numérica. Verifique
escopo de clientes, `root_squash`, permissões e dados canário. Montar um export
em lab não autoriza copiar dados reais ou alterar binários compartilhados.

**Telemetria:** mountd/NFS server, firewall, auditd e acesso ao filesystem.

### Automação e orquestração

Ansible, SSH multiplexing, runners, cron e ferramentas de gestão conectam muitos
hosts. A análise deve identificar controller, inventory, identidade de execução,
vault/secret store e blast radius. Nunca reutilize chave de produção no lab.

### Containers e Unix sockets

Sockets Docker/Podman, kubeconfigs e service-account tokens podem atravessar a
fronteira host/workload. Trate-os como caminhos de autorização e relacione com
os módulos 10, 16 e 21; não monte socket do host fora de VM descartável.

## Lab offline Linux

A fixture principal inclui o caminho:

```text
linux-operator --ssh-certificate--> bastion-linux
               --ssh-restricted--> app-linux
               --nfs-readonly----> backup-linux
```

Execute:

```bash
python3 24-Lateral-Movement/lateral_path_analyzer.py \
  24-Lateral-Movement/fixtures/lateral-graph.json linux-operator backup-linux
```

O caminho `app-linux → prod-secrets` permanece desabilitado e fora do escopo.

## Validação controlada em lab

Quando autorizado, limite a prova a uma sessão canário e comandos inócuos que
mostrem identidade/hostname. Não copie `~/.ssh`, não enumere agents de outros
usuários, não altere `authorized_keys`, `sudoers`, cron, systemd ou exports.

## Evidência mínima

- origem, destino, porta e fingerprint do host;
- principal canário e método, sem material secreto;
- direito/precondição de cada salto;
- session/process ID e horários UTC;
- logs esperados no bastion e destino;
- arquivo canário, caso usado, com hash e remoção confirmada.

## Detecção e falsos positivos

Correlacione uma mesma identidade ou certificado atravessando hosts, origem
atípica, novo fingerprint, multiplexing e comandos fora do baseline. Deploy,
backup, configuração e suporte são falsos positivos frequentes; contextualize
controller, inventory, janela de mudança e finalidade.

## Cleanup

Encerre sessões e multiplexers, desmonte exports de lab, revogue certificado ou
chave canário, remova arquivos temporários e confirme que `authorized_keys`,
`sudoers`, cron, systemd, sockets e firewall não foram modificados.

## Autoavaliação

- [ ] Diferenciei SSH, sudo, NFS, automação e sockets como trust boundaries.
- [ ] Usei identidade canário/efêmera e não coletei chaves.
- [ ] O caminho fora do escopo permaneceu bloqueado.
- [ ] Documentei telemetria de cada salto e falsos positivos.
- [ ] Revoguei o acesso de laboratório e validei o cleanup.

