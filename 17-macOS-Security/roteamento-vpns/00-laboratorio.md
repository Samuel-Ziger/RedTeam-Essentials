# 00 — Laboratório de roteamento

Use prefixos de documentação e o simulador local. VPN real somente entre
equipamentos/VMs próprios; nunca conecte o laboratório a redes corporativas sem
autorização. Não copie chaves ou configurações reais para o repositório.

## Artefatos

- topologia e domínios administrativos;
- tabela RIB esperada e FIB observada;
- política de importação/exportação;
- matriz de fluxos e identidade;
- parâmetros criptográficos sem segredos;
- MOP, validação, rollback e plano de expiração de chaves.

Antes de mudar rota default remotamente, garanta acesso out-of-band ou rollback
automático. Uma rota errada pode remover o próprio caminho de administração.
