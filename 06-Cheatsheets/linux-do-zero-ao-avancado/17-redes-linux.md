# 17 — Interfaces de conectividade no host Linux

## Objetivos

- descobrir qual componente administra cada interface e arquivo;
- localizar listeners, sockets Unix e resolução vista pelas aplicações;
- separar estado temporário do kernel e configuração persistente;
- produzir evidência suficiente para encaminhar a falha à trilha de Redes.

## Limite deste capítulo

Este é um capítulo de operação do sistema Linux, não um curso de redes.
Endereçamento, sub-redes, DNS em profundidade, protocolos, switching, VLAN,
roteamento, VPN, firewall, Wi-Fi e captura de pacotes pertencem aos módulos 14
a 18. Aqui você apenas localiza o estado que processos, kernel e gerenciadores
do host expõem.

Esse limite evita dois erros: tentar consertar aplicação alterando a rede sem
evidência e acreditar que saber listar endereços equivale a compreender uma
infraestrutura.

## Interface, configuração e proprietário

O kernel mantém o estado efetivo das interfaces. Um gerenciador lê uma fonte de
configuração e converge esse estado. Alterar diretamente o kernel pode ser
temporário e depois ser substituído pelo gerenciador.

~~~bash
ip -brief link
ip -brief address
nmcli general status 2>/dev/null || true
networkctl list 2>/dev/null || true
systemctl is-active NetworkManager systemd-networkd 2>/dev/null || true
~~~

NetworkManager é frequente em desktops e servidores. systemd-networkd aparece
em sistemas declarativos e enxutos. Netplan é uma camada que gera configuração
para um renderer, comum no Ubuntu. Cloud-init, instaladores e agentes de
plataforma também podem regenerar arquivos.

Antes de editar, responda:

1. qual processo administra a interface;
2. qual arquivo ou perfil é a fonte de verdade;
3. se a mudança é temporária ou persistente;
4. como validar sem perder o console;
5. como reverter.

Este módulo não pede alteração de endereço ou rota.

## Loopback

Loopback permite que processos no mesmo host se comuniquem sem depender de uma
interface externa. É a fronteira padrão dos exercícios de serviço:

~~~bash
ip -brief address show dev lo
ss -lnt
ss -lx
~~~

Um serviço ouvindo apenas em loopback não está automaticamente acessível por
outro host. Um socket Unix usa um caminho ou namespace abstrato, não uma porta
IP, e ainda depende de ownership, modo, diretório e namespace.

Use loopback para provar primeiro que processo, configuração e aplicação
funcionam localmente. Exposição entre máquinas será projetada na trilha de
Redes.

## Listener não é processo saudável

~~~bash
ss -lntup
ss -xlp
systemctl status --no-pager app.service
curl --fail --show-error http://127.0.0.1:8080/health
~~~

Um listener demonstra que algum socket foi aberto. Não prova que a aplicação
responde corretamente, que dependências funcionam ou que o serviço está pronto.
Relacione endereço, porta ou caminho ao PID, à identidade, à unit e ao teste
funcional.

Se o processo deveria ouvir e não aparece:

1. leia status e journal;
2. valide a configuração;
3. confirme usuário, diretório e permissão;
4. procure conflito pelo mesmo socket;
5. verifique sandbox e política MAC;
6. execute o teste sob o contexto real da unit.

Não altere firewall para corrigir um processo que nunca abriu o socket.

## Resolução vista pela aplicação

Aplicações normalmente usam o Name Service Switch e o resolver da biblioteca.
Por isso, consultar uma ferramenta DNS isolada não reproduz necessariamente a
mesma resolução.

~~~bash
grep -v '^#' /etc/nsswitch.conf | sed -n '1,20p'
getent hosts localhost
resolvectl status 2>/dev/null || sed -n '1,40p' /etc/resolv.conf
~~~

O arquivo de resolução pode ser link gerenciado e não a fonte primária. Não o
substitua antes de identificar quem o produz. A ordem NSS, cache, arquivo local
e DNS serão aprofundados no módulo 14.

## Namespaces e containers

Processos em namespaces distintos podem enxergar outras interfaces e sockets.
Compare sem alterar:

~~~bash
readlink /proc/self/ns/net
lsns -t net
cat /proc/self/cgroup
~~~

Um serviço dentro de container pode estar saudável no próprio namespace e não
estar publicado no host. Diagnosticar essa travessia exige o modelo de
containers do capítulo 23 e o modelo de redes dos módulos posteriores.

## Handoff para a trilha de Redes

Quando a aplicação passa no teste local e a falha envolve outro host, preserve:

~~~text
horário e fuso:
origem e destino saneados:
serviço e socket esperado:
resultado local:
mensagem exata do cliente:
gerenciador do host:
mudança recente:
~~~

Não conclua “é firewall”, “é DNS” ou “é rota” sem evidência. Esse pacote permite
continuar nos módulos 14 a 18 sem repetir o diagnóstico da aplicação.

## Exercícios

1. Descubra qual gerenciador possui cada interface da VM sem mudar seu estado.
2. Inicie um servidor somente em loopback, encontre processo, socket e unit e
   prove que encerrá-lo remove o listener.
3. Compare a configuração declarada com a configuração efetiva do host e
   registre quem pode regenerar cada arquivo.
4. Classifique cinco sintomas entre problema do processo local e assunto que
   requer os módulos 14 a 18; escreva a evidência mínima para encaminhamento.

## Checklist de domínio

- [ ] Distingo estado efetivo, fonte persistente e gerenciador.
- [ ] Relaciono listener a processo, identidade, namespace e teste funcional.
- [ ] Uso loopback antes de expor um serviço.
- [ ] Não altero rede para mascarar uma falha da aplicação.
- [ ] Sei entregar a investigação aos módulos 14 a 18 com evidência suficiente.
