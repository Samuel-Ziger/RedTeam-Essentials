# 03 — Raiz, intermediárias e perfis

Raiz deve ter uso raro, proteção forte e vida compatível com planejamento.
Intermediárias separam ambientes, propósitos e equipes. Perfis definem algoritmo,
validade, nomes, KU/EKU, políticas e extensões permitidas; a requisição não deve
escolher livremente a autoridade do certificado.

Path length e Name Constraints podem limitar sub-CAs, mas suporte e desenho
precisam ser testados. Emissão automatizada usa identidade autenticada, aprovação
adequada e logs imutáveis, sem entregar a chave privada à CA quando o serviço
pode gerá-la localmente.

## Verificação

Desenhe uma hierarquia para usuários, servidores e assinatura de código.
