# Lab 06 — Projeto opcional em VPS própria

Somente após concluir as VMs:

1. documente propriedade, provedor e autorização;
2. teste console e snapshot;
3. instale pacotes oficiais;
4. aplique uma mudança por vez;
5. configure um peer de teste;
6. valide em segunda conexão;
7. teste reinício e restauração;
8. execute auditor de política;
9. finalize runbooks e risco residual.

## Critério de parada

Pare se console falhar, SSH ficar instável, houver interface desconhecida,
firewall preexistente não compreendido ou qualquer chave aparecer em log/ticket.

## Cleanup

Revogue peers de teste. Se a VPS não será mantida, remova recursos de rede,
snapshots e DNS conforme o provedor, preservando apenas relatório sanitizado.

