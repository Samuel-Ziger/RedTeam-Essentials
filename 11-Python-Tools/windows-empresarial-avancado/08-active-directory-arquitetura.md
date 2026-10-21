# 08 — Arquitetura do Active Directory Domain Services

AD DS é diretório distribuído de objetos, identidade, autenticação,
autorização e política. Domain, tree e forest são fronteiras lógicas; schema e
configuration partitions abrangem a floresta; domain partition contém objetos.

## Componentes

- domain controllers hospedam NTDS database e serviços;
- sites/subnets orientam topologia de replicação;
- Global Catalog fornece atributos parciais multi-domain;
- FSMO roles serializam operações específicas;
- SYSVOL distribui arquivos de política/scripts;
- DNS é dependência estrutural e será ensinado com redes.

## Fronteiras de segurança

Forest é a principal fronteira administrativa/segurança do AD. Domain não deve
ser tratado automaticamente como isolamento contra administradores da floresta.
Modelo de tiers, privileged access workstations e delegação reduzem exposição.

## Backup e tempo

AD depende de replicação, time e recuperação system-state/forest. Snapshot
arbitrário de DC não é plano de backup.

## Limite prático

Não promova DC ainda. Modele objetos e decisões offline; DNS, replicação,
Kerberos e trusts operacionais aguardam redes/identidade integrada.

