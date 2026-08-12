# 24 - Movimentação lateral

> Planejamento, validação e detecção de movimento entre identidades e hosts em
> topologias sintéticas ou labs autorizados. Não executa comandos remotos.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários de Windows, Linux, AD e redes. |
| Pré-requisitos | Módulos 00, 03, 06, 20 e 21. |
| Tempo estimado | 8 horas de teoria e 6 horas em fixture/lab. |
| Ambiente | Grafo sintético, GOAD próprio ou engagement autorizado. |
| Evidência final | Caminho lateral, precondições, telemetria e cleanup. |
| Critério de conclusão | Comparar três caminhos e rejeitar um fora do RoE. |

## Modelo mental

Movimentação lateral não é sinônimo de execução remota. Um caminho exige:

1. **principal** autenticável;
2. **material permitido** pelo RoE, preferencialmente conta canário;
3. **direito** no host ou serviço de destino;
4. **protocolo e porta** alcançáveis;
5. **controle de escopo** para destino e intermediários;
6. **evidência e cleanup** proporcionais ao objetivo.

## Técnicas e precondições

| Família | Precondição típica | Telemetria principal | Controle |
|---------|--------------------|-----------------------|----------|
| RDP | direito de logon remoto + TCP/3389 | 4624 tipo 10, 4778/4779, EDR | MFA, NLA, PAW, segmentação |
| SMB/Admin Shares | admin local + TCP/445 | 4624 tipo 3, 5140/5145, serviço/processo | firewall, LAPS, deny lateral |
| WinRM | grupo/ACL + 5985/5986 | PowerShell/WinRM Operational, 4624 | HTTPS, JEA, allowlist |
| WMI/DCOM | permissão remota + RPC | WMI Activity, 4688, RPC/firewall | ACL, firewall, EDR |
| SSH | conta/chave + TCP/22 | auth.log/journal, process tree | chaves curtas, bastion, MFA |
| Kerberos/NTLM | material aceito e serviço compatível | 4768/4769/4776 e logon | AES, NTLM reduction, Credential Guard |

O módulo aprofunda e organiza o conteúdo existente em
[`windows_lateral_movement_teoria.md`](../06-Cheatsheets/windows_lateral_movement_teoria.md),
mas usa apenas análise offline para os exercícios automatizados.

Para Linux, siga o guia dedicado de [movimentação lateral em
Linux](linux-lateral-movement.md), cobrindo SSH, sudo, NFS, automação e sockets.

## Lab offline de attack paths

A fixture [`fixtures/lateral-graph.json`](fixtures/lateral-graph.json) modela
principals, hosts, direitos, protocolos e restrições de escopo:

```bash
python3 24-Lateral-Movement/lateral_path_analyzer.py \
  24-Lateral-Movement/fixtures/lateral-graph.json student fileserver
```

O resultado mostra o menor caminho e cada precondição utilizada. Compare:

- `student → fileserver`: permitido por sessão intermediária e WinRM/SMB;
- `student → dc01`: bloqueado por direito/escopo;
- `helpdesk → workstation`: permitido por RDP canário;
- `linux-operator → backup-linux`: permitido por certificado SSH, bastion e NFS read-only;
- `app-linux → prod-secrets`: desabilitado e fora do escopo;
- origem inexistente: rejeitada.

## Execução controlada em lab real

Se o RoE permitir validar um protocolo, use uma conta canário, um único destino
e uma ação inócua como consultar hostname/identidade. Não habilite serviços,
altere registro, crie scheduled task, despeje credenciais ou copie executáveis
para “facilitar” o teste. Registre exatamente o processo e a sessão esperados.

## Evidência mínima

- principal e conta canário (sem senha/token);
- origem, destino, protocolo, porta e horário UTC;
- direito que tornou o caminho possível;
- resultado inócuo e correlation/logon ID;
- eventos observados e eventos esperados ausentes;
- kill list e confirmação de encerramento da sessão.

## Detecção e falsos positivos

Correlacione autenticação remota, administração do recurso e processo no destino.
Ferramentas administrativas, deployment, inventário e help desk são falsos
positivos comuns. Baseline deve considerar identidade, origem habitual, janela,
sequência de hosts e privilégio, sem allowlists permanentes amplas.

## Cleanup

Encerre sessões, remova somente artefatos canário criados, reverta regras/ACLs de
lab, valide listeners e entregue a kill list. Não apague logs do alvo.

## Autoavaliação

- [ ] Diferenciei alcance de rede, autenticação e autorização.
- [ ] Expliquei por que o caminho existe usando precondições do grafo.
- [ ] Um destino bloqueado permaneceu bloqueado.
- [ ] Relacionei protocolo a fontes de telemetria e falsos positivos.
- [ ] Usei evidência mínima, conta canário e cleanup verificável.
