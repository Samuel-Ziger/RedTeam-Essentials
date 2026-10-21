# 22 — Hardening e controles de segurança

## Objetivos

- derivar controles de ameaça, ativo, exposição e função do host;
- reduzir serviço, privilégio e escrita mantendo operação e recuperação;
- verificar DAC, MAC, sandbox, atualização, auditoria e segredo em conjunto;
- documentar exceção, evidência, rollback e risco residual.

## Hardening é decisão de risco

Hardening reduz superfície e privilégio mantendo a função do sistema. Uma lista
copiada pode quebrar recuperação, observabilidade ou aplicação sem reduzir o risco
relevante. Comece por ameaças, ativos, exposição e suporte da distro.

## Baseline

Antes de mudar:

```bash
cat /etc/os-release
uname -r
systemctl --failed
systemctl list-unit-files --state=enabled
ss -lntup
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS
getenforce 2>/dev/null || aa-status 2>/dev/null || true
```

Salve inventário de pacotes, contas, sudo, chaves, tarefas, módulos, logs e
configurações. Defina teste funcional e rollback.

## Prioridades de alto retorno

1. usar release suportada e instalar correções;
2. remover/desabilitar serviços e pacotes sem finalidade;
3. limitar processos e listeners locais ao necessário;
4. documentar a exposição que será tratada na trilha de Redes;
5. eliminar contas, chaves e privilégios obsoletos;
6. proteger boot, disco e backups conforme ameaça física;
7. ativar e manter SELinux/AppArmor em modo enforcement suportado;
8. centralizar logs e alertar alterações relevantes;
9. testar recuperação;
10. revisar regularmente deriva do baseline.

## Menor privilégio de serviço

Cada serviço deve ter conta própria, diretórios estritos e somente as
capabilities necessárias. systemd oferece controles como:

```ini
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictSUIDSGID=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
```

Nem toda carga suporta todos. Avalie sugestões com:

```bash
systemd-analyze security app.service
```

A pontuação é heurística; teste comportamento real e acrescente controles em
incrementos.

## SELinux e AppArmor

DAC responde “quem possui e quais bits”; Mandatory Access Control aplica política
adicional mesmo quando DAC permite.

```bash
getenforce 2>/dev/null
ls -Z /var/www 2>/dev/null
sudo ausearch -m AVC -ts recent 2>/dev/null

aa-status 2>/dev/null
journalctl -k -g 'apparmor="DENIED"' 2>/dev/null
```

Não corrija negação desativando enforcement. Primeiro determine se o acesso é
legítimo, restaure label/perfil fornecido pela distro e crie exceção mínima
somente se necessário.

## Kernel e sysctl

Sysctls alteram comportamento global ou por namespace. Valores “seguros”
dependem de função, kernel e rede. Use arquivos versionados em `/etc/sysctl.d`,
comentando requisito, padrão anterior, teste e rollback.

```bash
sysctl kernel.randomize_va_space
sysctl fs.protected_hardlinks fs.protected_symlinks
sysctl net.ipv4.conf.all.rp_filter
```

ASLR, proteções de links, restrição de logs do kernel, BPF e ptrace precisam
ser avaliados. Não aplique um arquivo de Internet inteiro.

## Integridade e auditoria

Auditd registra eventos selecionados no kernel, mas regras excessivas geram
ruído e custo. Ferramentas de integridade comparam estado a baseline confiável;
se o atacante pode alterar baseline e alertas, o controle perde valor.

Monitore ao menos:

- contas, grupos, sudo e chaves SSH;
- units, timers, cron e pacotes;
- bootloader, initramfs, kernel e módulos;
- política MAC e exposição documentada para a trilha de Redes;
- falhas de autenticação e elevação;
- capacidade, backup e estado dos agentes.

## Segredos

Não coloque segredos em argumento, repositório, imagem, log ou variável global
sem avaliar exposição. Use cofre/credenciais do service manager, permissões,
rotação e identidades de workload. Apagar de Git atual não remove histórico;
revogue e rotacione.

## Benchmarks

CIS, DISA STIG e guias de fornecedor são fontes de requisitos e verificações,
não botão universal. Para cada controle registre aplicabilidade, estado,
evidência, exceção, responsável e data de revisão.

## Projeto de hardening

Em clone da VM:

1. defina perfil (serviço local interno);
2. capture baseline e teste funcional;
3. atualize e reduza pacotes/listeners;
4. restrinja identidade, SSH local e unit do serviço;
5. aplique MAC e hardening systemd;
6. configure logs e alertas;
7. rode scanner de baseline como evidência, não verdade absoluta;
8. teste boot, aplicação, backup e recuperação;
9. documente risco residual e exceções.

## Exercícios

1. Produza baseline somente leitura da VM e classifique cada listener, pacote e
   unidade habilitada por necessidade comprovada.
2. Aplique uma diretiva de isolamento por vez à unit didática, execute o teste
   funcional e registre incompatibilidade ou ganho.
3. Analise uma negação MAC sintética e proponha correção mínima sem desativar
   enforcement.
4. Escolha cinco recomendações de um benchmark e documente aplicabilidade,
   verificação, efeito colateral e rollback em vez de aplicá-las em bloco.

## Checklist de domínio

Consigo justificar cada controle por ameaça, demonstrar que ele funciona e
revertê-lo sem perder acesso ou disponibilidade.
