# 01 — Darwin e arquitetura XNU

Darwin é a base Unix open source que inclui kernel XNU, bibliotecas e utilitários;
macOS acrescenta frameworks, interface e componentes proprietários. XNU significa
"X is Not Unix" e combina ideias Mach com BSD e IOKit.

## Camadas

1. hardware e firmware;
2. kernel XNU: `osfmk`, BSD, IOKit, segurança e plataforma;
3. libSystem e syscalls/Mach traps;
4. frameworks e daemons;
5. apps, agentes e ferramentas.

O repositório oficial permite relacionar headers e subsistemas a uma release,
mas o kernel compilado do Mac inclui configuração e componentes específicos.
Não conclua comportamento atual lendo apenas um branch arbitrário.

```zsh
uname -a
sysctl kern.osrelease kern.version
```

## Prática

Escolha uma informação exposta por `sysctl`, localize definição/documentação
e desenhe o caminho do consumidor user space ao subsistema responsável.
