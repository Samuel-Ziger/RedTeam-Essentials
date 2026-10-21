# 18 — Operação, logs, rotação e resposta

Uma VPN é serviço contínuo. Mantenha inventário de peers, responsável, finalidade,
endereço, data de criação, última revisão e estado. Não coloque chaves privadas
ou dados pessoais desnecessários nesse inventário.

## Observabilidade mínima

- unidade ativa e reinícios inesperados;
- interface, porta e regras carregadas;
- handshake recente por peer quando esperado;
- bytes agregados para capacidade, com retenção proporcional;
- CPU, memória, perda, latência e espaço;
- falha de atualização e expiração de backup.

WireGuard não autentica “usuários”; a chave representa o peer. Correlacione com
inventário sob controle de acesso. Ausência de handshake pode significar cliente
ocioso, não incidente.

## Ciclos

- patch e reinício testado;
- revisão periódica de peers;
- rotação/revogação;
- restauração de backup;
- teste de console;
- revisão de custo e capacidade;
- auditoria de firewall, DNS e IPv6.

## Incidente

Revogue chave suspeita, preserve eventos centrais, identifique janela, revise
ações administrativas, rotacione segredos relacionados e comunique conforme o
plano. Não apague logs para “limpar” o servidor.

## Privacidade

Defina propósito e retenção antes de coletar. Métricas agregadas normalmente
bastam para saúde; investigação detalhada exige autoridade e caso registrado.

## Prática

Escreva runbook para dispositivo perdido com detecção, revogação, verificação,
substituição e encerramento.

