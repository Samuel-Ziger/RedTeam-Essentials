# Linux — do zero ao kernel

Esta é a raiz didática do [módulo 06](../README.md). São 31 capítulos, 64
práticas, seis laboratórios avaliativos, exemplos em Bash, AWK, Python e C e um
capstone de reconstrução. O material principal é autocontido.

## Modelo mental

~~~text
hardware
   ↓ firmware/UEFI → bootloader → kernel → initramfs → PID 1
   ↓
kernel: tarefas · memória · VFS · bloco · IPC · dispositivos · segurança
   ↕ syscalls
user space: libc · shell · systemd · serviços · desktop · aplicações
~~~

Linux, em sentido estrito, é o kernel. O sistema chamado informalmente de
Linux combina kernel, bibliotecas, ferramentas, init, política, pacotes,
instalador e repositórios escolhidos por uma distribuição.

## Como estudar

Cada capítulo segue quatro movimentos:

1. objetivos observáveis;
2. modelo técnico e exemplos;
3. exercícios que provocam falhas seguras;
4. checklist para explicar sem copiar comandos.

Não avance por quantidade de páginas. Avance quando conseguir prever o efeito,
executar em ambiente correto, interpretar a saída e reverter. Use o
[caderno de práticas](CADERNO-PRATICAS.md) entre capítulos e o
[guia de diagnóstico](GUIA-DIAGNOSTICO.md) durante as falhas.

## Mapa da progressão

| Faixa | Competência | Marco |
|-------|-------------|-------|
| 00–08 | laboratório, arquitetura, shell, arquivos, texto e permissões | Lab 01 |
| 09–12 | identidades, software, processos e memória | Lab 02 |
| 13–16 | armazenamento, boot e systemd | Lab 03 |
| 17–23 | operação local, automação, observabilidade, backup e hardening | Lab 04 |
| 24–29 | kernel, dispositivos, desempenho, desktop e serviços | Lab 05 |
| 30 | integração e defesa das decisões | Lab 06 |

O [índice principal](../README.md) contém a rota clicável completa. Os
[laboratórios](laboratorios/README.md) definem pré-condições, riscos, produtos e
critérios de aprovação.

## Fronteira com Redes

Linux expõe interfaces, sockets e gerenciadores que o administrador precisa
localizar. Este módulo limita-se a esse estado do host e ao ciclo de vida do
SSH. IP e sub-redes, DNS em profundidade, protocolos, switching, VLAN,
roteamento, VPN, firewall e infraestrutura são ensinados nos módulos 14 a 18.

## Checkpoint inicial

Em uma VM, execute e explique o que já souber:

~~~bash
cat /etc/os-release
uname -a
id
pwd
printf 'shell=%s\n' "$SHELL"
ps -p 1 -o pid,comm,args
findmnt /
~~~

Salve a saída saneada. No capstone você repetirá o diagnóstico e explicará as
camadas, diferenças e limitações de cada campo.

## Validação local

~~~bash
bash testar-curso.sh
~~~

O executor:

- cria somente diretórios temporários;
- testa exemplos e contratos de erro;
- compila C com warnings como erro, quando há compilador;
- valida units quando systemd-analyze está disponível;
- verifica links locais;
- nunca chama sudo, instala serviço ou carrega módulo.

## Definição de pronto

Você concluiu quando outra pessoa consegue reproduzir seu sistema e seus
runbooks, quatro falhas sintéticas são diagnosticadas por evidência e o serviço
é restaurado em uma VM vazia dentro do RTO definido.
