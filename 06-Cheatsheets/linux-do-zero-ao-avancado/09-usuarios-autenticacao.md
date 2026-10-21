# 09 — Usuários, grupos, PAM e sudo

## Objetivos

- relacionar nomes de conta a UID, GID, NSS e arquivos locais;
- separar identidade, autenticação, autorização, sessão e auditoria;
- administrar contas humanas e de serviço durante todo o ciclo de vida;
- desenhar delegação mínima com sudo e recuperação contra bloqueio.

## Identidade numérica

O kernel trabalha com UID e GID. Nomes são resolvidos pelo Name Service Switch
(NSS), que pode consultar arquivos locais, LDAP, SSSD ou outras fontes.

```bash
id
id -u
id -g
id -G
getent passwd "$(id -un)"
getent group "$(id -gn)"
grep -v '^#' /etc/nsswitch.conf | sed -n '1,20p'
```

Use `getent`, não apenas `grep /etc/passwd`, quando a identidade pode ser
remota.

## Bancos locais

`/etc/passwd` guarda nome, UID, GID primário, campo informativo, home e shell.
O hash de senha local fica em `/etc/shadow`, legível apenas por processos
autorizados. `/etc/group` e `/etc/gshadow` descrevem grupos.

```text
alice:x:1001:1001:Alice Example:/home/alice:/bin/bash
```

O `x` indica que a informação de senha não está naquele campo. Conta, senha,
shell de login e expiração são dimensões diferentes.

## Contas humanas e de serviço

- conta humana: login interativo, home e ciclo de vida associado a uma pessoa;
- conta de serviço: executa uma carga, geralmente sem login interativo;
- conta de sistema: UID em faixa definida pela distro, sem significado universal;
- `nobody`: identidade de baixa confiança genérica, não deve concentrar todos
  os serviços.

Comandos administrativos comuns, praticados apenas na VM:

```bash
sudo useradd --create-home --shell /bin/bash aluno-lab
sudo passwd aluno-lab
sudo usermod --append --groups grupo-lab aluno-lab
sudo userdel --remove aluno-lab
```

Confira as opções da distro: Debian também fornece `adduser`, uma interface de
mais alto nível. Remover a conta não resolve arquivos em volumes externos,
processos ativos, chaves, tokens ou tarefas agendadas.

## Login e sessão

Autenticação prova uma identidade; autorização decide a ação; accounting
registra eventos. Um login pode envolver terminal/SSH/display manager, PAM,
NSS, criação de sessão e ambiente.

```bash
who
w
loginctl list-sessions 2>/dev/null || true
last -n 10
lastlog 2>/dev/null | head
```

## PAM

Pluggable Authentication Modules organiza pilhas por serviço e quatro tipos:

- `auth`: verifica ou estabelece credenciais;
- `account`: verifica validade e restrições da conta;
- `password`: altera tokens de autenticação;
- `session`: prepara e encerra sessão.

Arquivos ficam geralmente em `/etc/pam.d/`. Palavras de controle (`required`,
`requisite`, `sufficient`, `optional` e sintaxe expandida) mudam o fluxo. Uma
edição incorreta pode bloquear todos os logins: mantenha console e snapshot e
use ferramentas da distro.

## `su`, `sudo` e login direto de root

- `su` troca identidade e normalmente exige credencial da conta-alvo;
- `sudo` aplica uma política a um comando e normalmente autentica o chamador;
- login direto como root reduz atribuição e amplia risco operacional.

```bash
sudo -l
sudo -v
sudo -k
```

Edite política somente com `visudo` e prefira arquivos em `/etc/sudoers.d/` com
modo correto. Conceda comandos definidos por função, sem curingas ambíguos,
editores, shells ou programas capazes de executar comandos arbitrários.

Exemplo conceitual, não para copiar sem adaptar:

```text
%operadores ALL=(root) /usr/bin/systemctl status app.service
```

Até um comando aparentemente somente leitura pode ganhar novas funções entre
versões. Teste e revise a política.

## Senhas, bloqueio e MFA

Use senhas exclusivas e longas, rate limiting e MFA quando o serviço suportar.
Bloquear senha (`passwd -l`) não necessariamente bloqueia chave SSH, token ou
outro provedor. Offboarding deve remover todos os métodos, sessões e direitos.

## Exercícios

1. Desenhe o caminho de um login SSH: daemon, PAM, NSS, shell e sessão.
2. Crie e remova uma conta fictícia na VM, inventariando arquivos pelo UID.
3. Explique diferença entre grupo primário, suplementar e grupo do inode.
4. Escreva uma política de menor privilégio em texto e liste maneiras de
   contorná-la que precisam ser testadas.

## Checklist de domínio

Consigo distinguir identidade, autenticação, autorização e sessão, e administro
o ciclo de vida de uma conta sem tratar apenas sua senha.
