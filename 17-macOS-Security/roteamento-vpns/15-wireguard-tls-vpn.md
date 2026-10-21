# 15 — WireGuard e VPN baseada em TLS

WireGuard usa pares de chaves pública/privada e associa `AllowedIPs` a roteamento
e seleção de peer. Sua configuração é pequena, mas distribuição, rotação,
revogação, inventário e identidade de usuário continuam problemas operacionais.

Nunca versionar chave privada. Proteja arquivo, gere em endpoint confiável,
revogue removendo peer e use camada de gestão quando escala exigir. `AllowedIPs`
amplos demais podem sequestrar rotas locais; overlaps exigem desenho.

VPNs baseadas em TLS frequentemente atravessam middleboxes com facilidade e
integram autenticação de usuário/MFA. Podem transportar IP ou acesso a aplicações,
dependendo do produto. Rodar sobre TCP e carregar TCP interno pode causar
interações ruins sob perda; opções UDP/QUIC podem evitar.

## Escolha

Compare interoperabilidade, identidade, criptografia, roaming, desempenho,
controle de rota, auditoria, atualização e modelo de suporte, não popularidade.
