# 08 — Windows doméstico I: fundamentos e administração local

> Primeiro dos quatro módulos Windows. Forma uma base técnica do primeiro boot
> à recuperação, em laboratório local, antes de internals e ambiente empresarial.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Iniciantes, usuários avançados e suporte local em formação |
| Pré-requisitos | Módulo 00; nenhuma administração prévia de Windows |
| Tempo estimado | 240–360 horas |
| Ambiente | Windows 11 oficial e suportado em VM descartável, com dois discos |
| Escopo | Computador doméstico local; sem redes ou identidade empresarial |
| Evidência final | Baseline, restore validado, falha cega e runbook executado por terceiro |
| Critério de conclusão | Seis gates aprovados e computador recuperável entregue |

## O que foi construído

O curso principal em
[windows-domestico-fundamentos/](windows-domestico-fundamentos/README.md) possui:

- 18 capítulos aprofundados, com objetivos, exercícios e checklists;
- 48 práticas atômicas e um guia transversal de diagnóstico;
- seis laboratórios progressivos com pré-requisitos semânticos;
- scripts PowerShell reais para inventário, backup e comparação de manifests;
- projeto de referência e capstone com falha cega;
- glossário, consulta rápida, respostas e referências oficiais.

A progressão cobre edição/build e suporte, UEFI/TPM/Secure Boot, instalação e
OOBE, interface e acessibilidade, arquivos, NTFS, discos e BitLocker, contas,
SIDs, ACL/UAC, processos, serviços, pacotes, Windows Update, Registro, eventos,
backup, Defender, PowerShell, diagnóstico e WinRE.

## Princípio operacional

O aluno aprende um ciclo único e reaplicável:

```text
pergunta → baseline → hipótese → risco → observação → mudança única
        → validação funcional/técnica → rollback → conclusão
```

Snapshots protegem os experimentos; não substituem backup. Toda evidência é
sanitizada. O curso não ensina bypass de OOBE, ativação ou requisitos, imagens
modificadas, debloaters, limpadores de Registro, desativação de segurança ou uso
cotidiano de conta administrativa.

## Limite curricular

Endereçamento, protocolos, DNS, Wi-Fi, compartilhamentos, firewall e acesso
remoto pertencem aos módulos 14–18. Windows internals, DLL, ETW, Sysinternals e
depuração pertencem ao módulo 09. Windows Server, domínio, GPO e identidade
empresarial pertencem aos módulos 10–11. Conteúdo ofensivo avançado começa
somente depois da base, nos módulos 27–40.

## Começar e validar

Leia a [rota do curso](windows-domestico-fundamentos/README.md), prepare a VM e
execute:

```bash
bash 08-Cloud-RedTeam/windows-domestico-fundamentos/testar-curso.sh
```

O teste local valida estrutura e escopo; PowerShell/Pester roda quando disponível.
A CI Windows executa a suíte completa.

## Vídeos complementares em português

O material é autocontido. Vídeos servem para observar interfaces que mudam:

1. [Windows 11 — aulas práticas](https://www.youtube.com/watch?v=5tsjVjPNlZY) — TechTodos.
2. [Arquivos, diretórios e pastas](https://www.youtube.com/watch?v=NMm-ChbYRiw) — TechTodos.
3. [Configurações de segurança](https://www.youtube.com/watch?v=aMmlvhqUZdM) — Dell Brasil.
4. [Ponto de restauração](https://www.youtube.com/watch?v=pPMosd3oFmM) — ASUS Brasil.
5. [Introdução ao PowerShell](https://www.youtube.com/watch?v=u-raJ1cGDgY) — Bóson Treinamentos.

Confirme ações e nomes na documentação oficial da sua build antes de reproduzir
qualquer vídeo.
