# 03 — Base Linux e acesso administrativo

Parta de imagem oficial e minimalista. Em Debian/Ubuntu, atualize o sistema antes
de expor o serviço:

```bash
sudo apt update
sudo apt full-upgrade
sudo reboot
```

Após reiniciar, confirme versão, relógio, interfaces e rotas:

```bash
uname -a
timedatectl status
ip -brief address
ip route
ip -6 route
```

## SSH

Use chave individual, usuário nominal, `sudo` e MFA/bastion quando o risco
exigir. Antes de desabilitar qualquer método de login, prove uma segunda sessão
e mantenha console fora de banda. Não altere várias dimensões de acesso na mesma
mudança.

## Superfície

Liste listeners com `ss -lntup`, pacotes habilitados e unidades em execução.
Remova somente o que compreende. Firewall do provedor e firewall do host são
camadas complementares; documente ambos para evitar regras contraditórias.

## Atualização

Defina janela, reinício, aviso, teste e rollback. Atualização automática sem
observabilidade pode reiniciar serviços em horário inadequado; atualização
manual indefinida deixa vulnerabilidades abertas.

## Prática

Em VM descartável, produza baseline de versão, interfaces, listeners e serviços.
Sanitize hostname, IP e usuário antes de anexar ao relatório.

