# 00 — Como estudar e montar o laboratório

## Objetivos

Construir um ambiente em que errar seja barato, observável e reversível. Linux
é aprendido alterando o sistema; isso exige separar a máquina pessoal da
máquina experimental.

Ao final, você deverá conseguir classificar o risco de uma prática, preparar
snapshot e console de recuperação, registrar evidências reproduzíveis e
interromper um procedimento quando o alvo não puder ser confirmado.

## Ambiente mínimo

Use uma VM com:

- 2 vCPUs;
- 4 GiB de RAM, ou 2 GiB para servidor sem interface gráfica;
- disco virtual de 30–40 GiB com expansão dinâmica;
- NAT para atualizações, sem portas publicadas;
- clipboard desativado quando estiver praticando material não confiável;
- um snapshot chamado `instalacao-limpa`.

KVM/QEMU costuma oferecer melhor integração em um host Linux. VirtualBox,
VMware e Hyper-V também servem. WSL ensina shell e ferramentas, mas não
substitui uma VM para boot, systemd completo, particionamento, drivers ou
kernel.

## Modelo de três ambientes

| Ambiente | Uso | Pode quebrar? |
|----------|-----|---------------|
| VM principal | Capítulos e projeto | Sim, mas com snapshot |
| VM descartável | Boot, disco, kernel e recovery | Sim; deve ser recriável |
| Host pessoal | Ler material e guardar evidências | Não |

Containers são ótimos para comparar user space entre distros, mas compartilham
o kernel do host. Não os use para concluir que testou outro kernel, init,
bootloader ou driver.

## Diário de laboratório

Para cada atividade, registre:

```text
Objetivo:
Hipótese:
Estado antes:
Comandos executados:
Saída relevante:
Estado depois:
Como desfazer:
O que aprendi:
```

Nunca registre senhas, chaves privadas, tokens, IPs de clientes ou dados
pessoais. Use nomes como `alice`, `server01` e `example.test`.

## Ler antes de executar

Para cada comando novo:

1. descubra se ele lê ou altera estado;
2. consulte `type -a comando` para saber o que será executado;
3. abra `man comando` ou `comando --help`;
4. identifique alvo, privilégio e efeito colateral;
5. procure opção de simulação, quando existir;
6. execute sobre dados descartáveis;
7. confira o código de saída com `printf '%s\n' "$?"`.

`sudo` não torna um comando correto; apenas amplia o dano de um comando errado.

## Ciclo de aprendizagem

Em cada capítulo:

1. leia os conceitos;
2. preveja o resultado de cada exemplo;
3. digite, em vez de colar;
4. altere uma variável por vez;
5. provoque uma falha segura;
6. diagnostique pela mensagem, manual e logs;
7. reverta a alteração;
8. explique sem usar jargão circular.

## Laboratório inicial sem privilégio

```bash
lab_dir="$(mktemp -d)"
printf 'laboratorio=%s\n' "$lab_dir"
cd -- "$lab_dir"
mkdir -p entrada saida
printf '%s\n' alpha beta gamma > entrada/itens.txt
wc -l entrada/itens.txt
cp -a entrada/itens.txt saida/copia.txt
cmp entrada/itens.txt saida/copia.txt
cd -- /
rm -rf -- "$lab_dir"
```

Por que o `cd /` vem antes da remoção? Um processo pode manter como diretório
atual um diretório já removido, o que confunde exercícios seguintes. Por que as
variáveis estão entre aspas? Para impedir separação em palavras e expansão de
glob quando caminhos contêm espaços ou caracteres especiais.

## Exercícios

1. Restaure o snapshot inicial e meça o tempo real até a VM voltar a funcionar.
2. Classifique cinco comandos dos capítulos seguintes como leitura, mudança
   reversível ou mudança destrutiva e justifique a classificação.
3. Execute o laboratório inicial com um caminho contendo espaço e confirme por
   que as aspas preservam um único argumento.
4. Escreva um plano de recuperação para perda do terminal, falha de boot e
   seleção acidental do disco errado; nenhum plano pode depender da própria VM.

## Checklist de domínio

- [ ] Tenho snapshot e sei restaurá-lo.
- [ ] Distingo host, VM e container.
- [ ] Sei abrir um segundo console da VM para recuperação.
- [ ] Meu diário guarda estado anterior e reversão.
- [ ] Consigo explicar por que não devo aprender executando tudo com `sudo`.
