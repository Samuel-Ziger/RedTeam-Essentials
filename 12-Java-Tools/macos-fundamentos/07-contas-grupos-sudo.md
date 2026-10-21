# 07 — Contas, grupos, autenticação e `sudo`

Uma conta tem identidade, grupos, diretório pessoal e credenciais. Administrador
é uma associação que permite solicitar elevação; não significa que todo
processo execute permanentemente como `root`.

```zsh
id
groups
dscl . -read "/Users/$USER" UniqueID PrimaryGroupID UserShell
sudo -l
```

`sudo` autentica e registra uma elevação conforme política. Leia o comando
inteiro, use caminho absoluto em automação e nunca cole segredo no terminal.
Conta padrão deve bastar para trabalho comum; eleve somente a operação.

Contas de serviço, Secure Token, Bootstrap Token e identidade corporativa são
aprofundados no módulo 13. Conta Apple não é sinônimo de conta Unix local.

## Prática

Compare `id` de uma conta padrão e de uma administradora de laboratório.
Documente três tarefas que precisam de elevação e três que não precisam.
