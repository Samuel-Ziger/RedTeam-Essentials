# 00 — Laboratório e modelo de configuração

Comece com diagramas e documentos JSON. Um simulador ou switch real é opcional;
se usado, deve ser próprio, isolado e ter configuração salva/rollback.

Separe quatro artefatos:

1. **intento:** segmentos e fluxos necessários;
2. **source of truth:** VLANs, prefixos, portas e donos;
3. **configuração renderizada:** sintaxe do fabricante;
4. **estado observado:** o que o equipamento realmente executa.

Nunca assuma que commit foi aplicado ou que running e startup config coincidem.
Em mudanças remotas, use confirmação/rollback automático quando suportado e
mantenha caminho de gestão independente.

## Segurança

Use VLANs e MACs fictícios. Não conecte loops físicos para “ver o que acontece”.
Não introduza servidor DHCP ou trunk em uma rede de produção.
