# 16 — systemd, unidades, timers e journal

## Objetivos

- distinguir ativação, estado, habilitação e dependência de unidades;
- escrever serviço e timer com identidade, diretórios e limites explícitos;
- validar override sem editar artefato fornecido pelo pacote;
- diagnosticar ambiente, execução, reinício e logs por evidência.

## systemd não é apenas `systemctl`

systemd é uma suíte. O service manager roda como PID 1 no sistema e também
pode existir por usuário. Ele administra unidades, dependências, cgroups,
ativação, estado e integração com journal, logind, resolved, networkd e outros
componentes que a distro pode ou não adotar.

## Tipos de unidade

| Sufixo | Representa |
|--------|------------|
| `.service` | processo/serviço |
| `.socket` | socket que pode ativar serviço |
| `.timer` | agenda ativa outra unidade |
| `.path` | observa caminho |
| `.mount`/`.automount` | montagem |
| `.target` | ponto de sincronização/grupo |
| `.slice`/`.scope` | organiza recursos/cgroups |

```bash
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service
systemctl status cron.service 2>/dev/null || systemctl status crond.service
```

`active`, `enabled` e `running` não são sinônimos. Active descreve estado
atual; enabled instala dependência para ativação futura; serviços `oneshot`
podem ficar active/exited.

## Dependência e ordem

`Requires=`/`Wants=` expressam relação de necessidade; `After=`/`Before=`
expressam ordem quando ambas participam da transação. `After=network.target`
não garante Internet ou DNS operacional. Modele o recurso real, tolerância a
retry e integração do gerenciador de rede.

```bash
systemctl list-dependencies --reverse ssh.service 2>/dev/null
systemctl show -p Wants,Requires,After ssh.service 2>/dev/null
```

## Escrever um serviço

Exemplo didático em `exemplos/systemd/curso-observador.service`:

```ini
[Unit]
Description=Observador didatico do curso Linux
After=local-fs.target

[Service]
Type=oneshot
ExecStart=/usr/local/libexec/curso-observador
User=curso-observador
Group=curso-observador
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
```

`ExecStart` não passa por uma shell por padrão; `>`, pipes e expansões de shell
não funcionam como em um terminal. Use executável/script explícito. Prefira
serviço em foreground; `Type=forking` é para daemons legados.

## Overrides e precedência

Não edite unit de `/usr/lib`/`lib` fornecida pelo pacote. Crie override:

```bash
sudo systemctl edit app.service
systemctl cat app.service
systemd-delta
sudo systemctl daemon-reload
sudo systemctl restart app.service
```

`daemon-reload` relê unidades; não reinicia automaticamente serviços.
Valide antes:

```bash
systemd-analyze verify caminho/app.service
```

## Restart e falha

`Restart=on-failure` pode aumentar resiliência, mas também criar loop. Combine
backoff/rate limit, timeout, watchdog quando suportado e alerta. `ExecStartPre`
não substitui validação offline nem migração transacional.

```bash
systemctl show app.service -p Result,ExecMainStatus,NRestarts
systemctl reset-failed app.service
```

## Timers

Timers substituem muitos usos de cron com estado e logs:

```ini
[Timer]
OnCalendar=daily
RandomizedDelaySec=15m
Persistent=true
Unit=curso-observador.service
```

`Persistent=true` pode executar após boot uma ocorrência perdida. Para tarefas
em frota, randomized delay evita que todos os hosts iniciem juntos.

```bash
systemctl list-timers --all
systemd-analyze calendar 'Mon..Fri *-*-* 09:00:00'
```

## Journal

```bash
journalctl -u ssh.service --since '-1 hour'
journalctl -b
journalctl -b -1
journalctl -p warning..alert
journalctl -f
journalctl --disk-usage
```

O journal guarda campos estruturados, boot ID, unidade e prioridade. Persistência
e retenção dependem de configuração e espaço. Encaminhamento remoto protege
contra perda do host, mas exige privacidade e controle de acesso.

## Unidades de usuário

```bash
systemctl --user status
journalctl --user
loginctl show-user "$(id -un)" -p Linger
```

Unidades de usuário não ganham privilégio. Linger permite manager sem sessão
ativa e deve ser deliberado.

## Método de troubleshooting

```bash
systemctl status --no-pager app.service
systemctl cat app.service
systemctl show app.service
journalctl -u app.service -b --no-pager
systemctl list-dependencies app.service
systemd-analyze verify /caminho/app.service
```

Leia o primeiro erro causal, confirme usuário, caminhos absolutos, ambiente,
diretório de trabalho, permissões, MAC, montagem e limites. O ambiente de uma
unit é intencionalmente menor que o terminal interativo.

## Exercícios

1. Valide as unidades de exemplo sem instalá-las e explique cada diretiva de
   isolamento aplicada ao serviço.
2. Crie uma cópia propositalmente inválida, encontre a primeira causa com o
   verificador e restaure a versão correta.
3. Modele um timer diário com atraso aleatório e determine o que ocorre quando
   a máquina permanece desligada no horário planejado.
4. Compare start, enable, reload, restart, daemon-reload e reset-failed por
   efeito observável e por situação de uso.

## Checklist de domínio

Consigo escrever, validar, endurecer, ativar, observar e reverter uma unit sem
editar arquivo do pacote ou confundir enable com start.
