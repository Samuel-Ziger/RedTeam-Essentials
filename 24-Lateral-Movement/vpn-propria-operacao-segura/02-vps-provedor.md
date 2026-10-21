# 02 — VPS, provedor e responsabilidade

Escolher uma VPS é escolher dependências. Avalie suporte, localização, política
de privacidade, retenção, segurança de conta, console, snapshots, proteção
DDoS, IPv6, largura de banda, limites de egress e processo de abuso.

## Requisitos mínimos

- distribuição suportada e atualizações de segurança;
- endereço público e UDP de entrada;
- console de recuperação independente da rede configurada;
- capacidade compatível com usuários e criptografia;
- firewall de borda configurável;
- MFA na conta do provedor e alertas administrativos;
- documentação de tratamento de dados e encerramento.

Não escolha com base em propaganda de “anonimato”. Cadastro e pagamento são
relações administrativas legítimas; este curso não ensina a escondê-las.

## Região e desempenho

Distância aumenta latência. Região também afeta residência de dados e contratos.
Meça requisitos antes de decidir: RTT, throughput, disponibilidade, volume de
egress e necessidade de IPv6.

## Descarte

Revogue peers, remova DNS, exporte somente evidências necessárias, destrua
snapshots conforme política e confirme encerramento da instância e recursos
associados. Chaves cliente permanecem responsabilidade dos dispositivos.

## Prática

Crie uma matriz de três ofertas sem contratar: segurança de conta, console,
rede, dados, custo e saída. Registre fontes e data.

