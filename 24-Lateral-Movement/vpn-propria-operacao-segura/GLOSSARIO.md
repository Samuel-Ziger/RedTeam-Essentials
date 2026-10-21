# Glossário

- **Peer:** participante identificado por uma chave pública.
- **Endpoint:** endereço e porta usados para alcançar um peer pela rede externa.
- **AllowedIPs:** associação entre chave pública e prefixos aceitos/roteados;
  funciona como tabela de cryptokey routing, não como ACL completa do host.
- **Handshake:** negociação autenticada de chaves de sessão.
- **Full tunnel:** rota padrão encaminhada pela VPN.
- **Split tunnel:** apenas prefixos selecionados passam pela VPN.
- **NAT/masquerade:** tradução da origem do cliente para saída pelo gateway.
- **Forwarding:** encaminhamento de pacotes entre interfaces pelo kernel.
- **MTU:** maior pacote transmitido sem fragmentação naquele enlace.
- **Kill switch:** política que bloqueia fallback fora do túnel.
- **Keepalive:** pacote periódico opcional para manter mapeamento NAT; não é
  necessário em todos os peers.
- **Console fora de banda:** acesso administrativo que não depende da regra de
  rede sendo alterada.
- **Break glass:** procedimento controlado de recuperação emergencial.

