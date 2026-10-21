# 18 — SSH e administração remota

## Objetivos

- validar identidade do servidor por canal independente;
- administrar chaves, agente e configuração efetiva do cliente;
- alterar o daemon com validação, sessão de recuperação e menor privilégio;
- diagnosticar autenticação e permissões sem desativar controles de segurança.

## Limite da prática

Neste módulo, pratique primeiro contra localhost ou entre duas VMs privadas
criadas por você. Túneis, pivôs, desenho de acesso entre redes e filtragem
pertencem aos módulos de Redes e às especializações posteriores. O foco aqui é
o ciclo de vida seguro do serviço SSH no sistema operacional.

## O que SSH oferece

SSH cria um canal criptografado, autentica o servidor pela host key e pode
autenticar o cliente por chave, senha, certificado ou integração. Também
transporta execução remota, subsistemas como SFTP e encaminhamento de portas.

## A primeira conexão

```bash
ssh usuario@server01.example.test
```

O aviso de host desconhecido pede que você associe uma chave ao servidor. Não
aceite automaticamente: confirme fingerprint por console, inventário assinado,
DNS SSHFP validado ou outro canal independente. Mudança inesperada pode ser
reinstalação legítima ou interceptação.

```bash
ssh-keyscan server01.example.test  # coleta, mas não autentica por si só
ssh-keygen -F server01.example.test
```

## Chaves de usuário

Ed25519 é uma escolha moderna comum, salvo requisitos de compatibilidade ou
conformidade diferentes:

```bash
ssh-keygen -t ed25519 -a 64 -C 'curso-linux-lab'
ssh-keygen -lf "$HOME/.ssh/id_ed25519.pub"
```

Proteja a chave privada com passphrase. A chave pública pode ser distribuída;
a privada não. Permissões esperadas costumam ser:

```bash
chmod 0700 "$HOME/.ssh"
chmod 0600 "$HOME/.ssh/authorized_keys"
chmod 0600 "$HOME/.ssh/id_ed25519"
```

`ssh-copy-id` instala a chave via acesso existente. Em produção, prefira
provisionamento auditável e remoção centralizada.

## Agente

`ssh-agent` evita redigitar passphrase mantendo uma chave desbloqueada em
memória. Liste e limite tempo:

```bash
ssh-add -l
ssh-add -t 1h "$HOME/.ssh/id_ed25519"
ssh-add -D
```

Agent forwarding expõe capacidade de assinatura a um host intermediário
comprometido enquanto a sessão existe. Prefira ProxyJump e chaves/certificados
adequados ao destino.

## Configuração do cliente

```sshconfig
Host lab-server
    HostName server01.example.test
    User aluno
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

Teste a configuração efetiva:

```bash
ssh -G lab-server | less
ssh -vv lab-server
```

Verbose pode expor nomes e metadados; saneie antes de compartilhar.

## Servidor

Antes de alterar `sshd_config`, mantenha console/sessão aberta e valide:

```bash
sudo sshd -t
sudo sshd -T | less
sudo systemctl reload ssh.service 2>/dev/null || sudo systemctl reload sshd.service
```

Princípios:

- proibir login remoto direto de root quando não houver caso justificado;
- preferir chaves/certificados e MFA conforme risco;
- desabilitar métodos não usados;
- restringir usuários/grupos por política;
- manter host keys protegidas e rotacionáveis;
- aplicar rate limiting e observar falhas;
- limitar forwarding, TTY e comandos para contas de automação;
- atualizar OpenSSH pela distro.

Não desative senha antes de provar, em nova sessão, que a chave e a
recuperação funcionam.

## `authorized_keys` restrita

Uma chave de automação pode receber opções como `from=`, `command=`,
`restrict`, proibição de PTY e forwarding, conforme versão. Isso reduz impacto
de vazamento, mas o comando forçado deve tratar entrada hostil e ambiente.

## Transferência

```bash
sftp lab-server
scp -- arquivo.txt lab-server:/tmp/
rsync -a --protect-args -- arquivo.txt lab-server:/tmp/
```

Confira semântica da versão: OpenSSH moderno usa SFTP como transporte padrão
para `scp`, mas compatibilidade e servidores antigos variam. Para grandes
sincronizações, rsync economiza dados e oferece dry-run.

## Encaminhamento

SSH oferece encaminhamento local, remoto e proxy SOCKS. Esses recursos mudam
o caminho de conectividade e podem atravessar uma segmentação planejada. Neste
módulo, apenas reconheça e desabilite o forwarding quando ele não for requisito.
A prática de túneis, desenho de acesso e controles de rede fica nos módulos 14
a 18 e, para cenários de segurança autorizados, nas especializações posteriores.

## Diagnóstico

1. estado da unit e validação da configuração;
2. listener local associado ao processo esperado;
3. host key e relógio;
4. conexão verbose contra localhost;
5. journal da unit SSH;
6. permissões e ownership da home e do diretório de chaves;
7. PAM, regras de usuário, shell e estado da conta.

Se localhost funciona e outro host falha, preserve essa evidência e continue
o caminho entre máquinas nos módulos 14 a 18.

## Exercícios

1. Gere uma chave exclusiva do laboratório, registre a fingerprint e conecte
   ao serviço local confirmando a host key por console.
2. Inspecione a configuração efetiva do cliente e do servidor e explique a
   origem de três valores que não aparecem no arquivo editado.
3. Restrinja uma chave de automação fictícia e demonstre quais ações continuam
   permitidas; remova a chave ao concluir.
4. Provoque uma falha de ownership em uma cópia de diretório e diagnostique sem
   afrouxar globalmente as permissões.

## Checklist de domínio

Consigo validar host, administrar chaves, restringir automação, alterar sshd
sem me bloquear e explicar os riscos de agente e forwarding.
