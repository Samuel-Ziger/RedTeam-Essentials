# Windows doméstico I — guia de estudo

Esta é a raiz didática do [módulo 08](../README.md). A trilha começa no primeiro
boot e termina com um computador local que outra pessoa consegue diagnosticar e
recuperar usando evidência e runbook.

## Como estudar

Para cada capítulo:

1. leia os objetivos e escreva o que já consegue explicar;
2. reproduza apenas exemplos de consulta em conta comum;
3. faça os exercícios com fixtures e registre previsão;
4. conclua o checklist com evidência, não por sensação;
5. execute o gate quando ele surgir na aplicação.

Use o [caderno de 48 práticas](CADERNO-PRATICAS.md) ao longo da leitura e o
[guia de diagnóstico e recuperação](GUIA-DIAGNOSTICO-RECUPERACAO.md) sempre que
uma hipótese cruzar mais de um componente. O projeto de referência
[computador recuperável](projetos/computador-recuperavel/README.md) mostra a
arquitetura do capstone sem esconder decisões em uma solução pronta.

## Contrato de aprendizagem

| Campo | Definição |
|---|---|
| Nível | Iniciante absoluto a administrador local competente |
| Duração | 240–360 horas |
| Pré-requisito | Módulo 00 e disposição para documentar cada prática |
| Ambiente | VM Windows 11 suportada, UEFI, snapshots e dois discos sintéticos |
| Evidência | Diário, inventário, manifests, timeline, restore e runbook |
| Conclusão | Seis gates e projeto final aprovados sem perder dados ou reduzir proteção |

Algumas edições/builds atuais exigem internet e conta Microsoft no OOBE. A VM
offline de estudo deve ser provisionada por um fluxo oficial compatível antes
dos experimentos. O curso não fornece contorno.

## Rota e gates

| # | Capítulo | Resultado | Gate seguinte |
|---:|---|---|---|
| 00 | [Método e laboratório](00-metodo-laboratorio.md) | Experimento seguro e reproduzível | |
| 01 | [Família e ciclo](01-familia-edicoes-ciclo.md) | Identificar edição/build e suporte | |
| 02 | [Hardware e firmware](02-hardware-firmware.md) | Explicar cadeia de boot e confiança | |
| 03 | [Instalação e OOBE](03-instalacao-oobe.md) | Planejar instalação suportada | |
| 04 | [Interface e configuração](04-interface-configuracoes.md) | Mapear conceito a ferramenta | [Lab 01](laboratorios/01-instalacao-inventario.md) |
| 05 | [Arquivos e caminhos](05-arquivos-caminhos.md) | Operar namespace e metadados | |
| 06 | [Discos e BitLocker](06-discos-volumes-bitlocker.md) | Administrar armazenamento e recuperação | |
| 07 | [Contas, ACL e UAC](07-contas-permissoes-uac.md) | Aplicar privilégio mínimo | [Lab 02](laboratorios/02-arquivos-permissoes.md) |
| 08 | [Processos e serviços](08-processos-servicos.md) | Diagnosticar execução e inicialização | |
| 09 | [Aplicativos e pacotes](09-aplicativos-pacotes.md) | Gerenciar procedência e ciclo de vida | |
| 10 | [Windows Update](10-windows-update.md) | Entender servicing e rollback | |
| 11 | [Registro](11-registro.md) | Alterar chave isolada com segurança | |
| 12 | [Eventos e confiabilidade](12-eventos-confiabilidade.md) | Construir timeline contextual | |
| 13 | [Backup e recuperação](13-backup-recuperacao.md) | Provar restore e escolher WinRE | [Labs 03–04](laboratorios/README.md) |
| 14 | [Defender e segurança](14-defender-seguranca.md) | Interpretar camadas locais | |
| 15 | [Terminal e PowerShell](15-terminal-powershell.md) | Automatizar consultas robustas | |
| 16 | [Diagnóstico e reparo](16-diagnostico-reparo.md) | Testar hipóteses antes de reparar | [Lab 05](laboratorios/05-defender-integridade.md) |
| 17 | [Projeto final](17-projeto-final.md) | Entregar computador recuperável | [Lab 06](laboratorios/06-projeto-recuperacao.md) |

Na aplicação visual, os gates são intercalados com pré-requisitos exatos. Os
documentos de consulta ao fim da rota são opcionais; capítulos, exemplos, guia,
caderno, projeto e laboratórios são obrigatórios.

## Materiais

- [Laboratórios e critérios de aprovação](laboratorios/README.md)
- [Exemplos PowerShell testados](exemplos/README.md)
- [Caderno de práticas](CADERNO-PRATICAS.md)
- [Guia de diagnóstico e recuperação](GUIA-DIAGNOSTICO-RECUPERACAO.md)
- [Projeto de referência](projetos/computador-recuperavel/README.md)
- [Consulta rápida](CHEATSHEET.md)
- [Glossário](GLOSSARIO.md)
- [Respostas orientativas](RESPOSTAS.md)
- [Referências oficiais e comunidade](REFERENCIAS.md)

## Limite do módulo

Este curso trata o computador local. Não configure endereçamento, protocolos,
DNS, Wi-Fi, firewall, compartilhamentos, acesso remoto, domínio ou políticas
empresariais. Se uma ferramenta exibir essas opções, apenas reconheça que existem.

Também não antecipa internals avançados, depuração, DLLs ou técnicas ofensivas.
Esses temas dependem desta base e possuem módulos próprios.

## Regra operacional

Observe, exporte o estado, altere uma variável, valide função e estado técnico,
reverta e compare com a baseline. Pare diante de alvo ambíguo. Não use limpador
de Registro, debloater, imagem modificada, pacote sem procedência ou comando que
você não consiga explicar.

## Validação local

```bash
bash testar-curso.sh
```

O executor não instala dependências nem altera a VM. Na CI Windows, Pester e
análise estática validam os scripts reais.
