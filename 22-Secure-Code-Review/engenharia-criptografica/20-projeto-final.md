# 20 — Projeto final: protocolo e plano de migração

Entregue um protocolo local de registros autenticados com versão, key ID,
contador monotônico, contexto, AES-GCM e limites. Use a ferramenta de inventário
para criar plano clássico→pós-quântico de uma organização fictícia.

## Critérios

- especificação byte a byte e máquina de estados;
- chaves separadas por ambiente/propósito e política de nonce;
- rejeição de replay, downgrade, campo extra e adulteração;
- vetores, property tests e corpus de parser;
- observabilidade sem segredo e resposta a comprometimento;
- inventário, prioridades, dependências, owner, prazo, rollback e exit criteria;
- distinção entre padrão final, draft e experimento.

Revisores devem conseguir reproduzir vetores e contestar cada hipótese.
