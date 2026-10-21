# macOS I — fundamentos e administração local

Curso autocontido para quem nunca usou ou administrou um Mac. A rota parte da
interface e chega a Terminal, APFS, contas, permissões, processos, `launchd`,
logs, backup, recuperação e proteções nativas. Apple Silicon é a plataforma
principal; diferenças relevantes dos Macs Intel são explicadas.

## Contrato de aprendizagem

| Campo | Definição |
|---|---|
| Nível | Iniciante absoluto a administrador local competente |
| Duração | 140–220 horas |
| Pré-requisito | Módulo 00; nenhuma experiência anterior com Mac |
| Ambiente | Mac suportado ou VM autorizada, conta sem dados pessoais e backup |
| Evidência | Inventário sanitizado, diário, restauração e projeto final |
| Conclusão | Administrar, diagnosticar e recuperar um Mac sem reduzir proteções |

## Limite deste módulo

O computador é estudado como sistema local. IP, DNS, Wi-Fi, VPN, firewall,
compartilhamento, SSH e serviços remotos pertencem ao futuro módulo de redes.
Não desative SIP, Gatekeeper, FileVault, XProtect ou TCC para concluir práticas.

## Rota

| # | Capítulo | Resultado |
|---:|---|---|
| 00 | [Método e laboratório](00-metodo-laboratorio.md) | Praticar com evidência e reversão |
| 01 | [Família Mac e macOS](01-familia-mac-macos.md) | Escolher hardware e versão suportados |
| 02 | [Apple Silicon e Intel](02-apple-silicon-intel.md) | Entender arquitetura e cadeia de confiança |
| 03 | [Inicialização e Recovery](03-boot-recovery-instalacao.md) | Instalar, atualizar e recuperar com segurança |
| 04 | [Interface e Ajustes](04-interface-ajustes.md) | Operar Finder, Dock, Spotlight e Ajustes |
| 05 | [Arquivos e hierarquia](05-arquivos-hierarquia.md) | Navegar por caminhos e metadados |
| 06 | [APFS, volumes e snapshots](06-apfs-volumes-snapshots.md) | Administrar armazenamento local |
| 07 | [Contas, grupos e autenticação](07-contas-grupos-sudo.md) | Trabalhar com privilégio mínimo |
| 08 | [Permissões, ACL, flags e xattrs](08-permissoes-acl-xattrs.md) | Explicar quem pode fazer o quê |
| 09 | [Apps, bundles e instalação](09-apps-bundles-instalacao.md) | Instalar software com procedência |
| 10 | [Processos e recursos](10-processos-recursos.md) | Diagnosticar CPU, memória e energia |
| 11 | [`launchd` e tarefas](11-launchd-tarefas.md) | Entender serviços e agentes locais |
| 12 | [Preferences, defaults e plists](12-preferences-plists.md) | Ler configuração estruturada |
| 13 | [Terminal e zsh](13-terminal-zsh.md) | Automatizar consultas seguras |
| 14 | [Pacotes e ferramentas de desenvolvimento](14-pacotes-ferramentas.md) | Controlar dependências locais |
| 15 | [Logs e diagnóstico](15-logs-diagnostico.md) | Investigar falhas por linha do tempo |
| 16 | [Time Machine e recuperação](16-backup-recuperacao.md) | Provar que o backup restaura |
| 17 | [Segurança e privacidade](17-seguranca-privacidade.md) | Verificar as camadas nativas |
| 18 | [Automação local](18-automacao-local.md) | Criar rotinas idempotentes |
| 19 | [Projeto final](19-projeto-final.md) | Entregar um Mac local recuperável |

## Materiais

- [Laboratórios](laboratorios/README.md)
- [Código e testes](exemplos/README.md)
- [Glossário](GLOSSARIO.md)
- [Consulta rápida](CHEATSHEET.md)
- [Respostas orientativas](RESPOSTAS.md)
- [Referências](REFERENCIAS.md)

## Regra operacional

Observe, exporte o estado, mude uma variável, valide e reverta. Não use
"cleaners", scripts de otimização opacos nem comandos com `sudo` cuja
pós-condição você não saiba verificar.
