# 01 — Ciclo de vida e tipos de chave

Chaves têm propósito: data-encryption key (DEK), key-encryption key (KEK),
assinatura, acordo, autenticação ou raiz. Reutilizar a mesma chave entre
algoritmos, tenants ou ambientes quebra separação de domínio e aumenta o raio
de impacto.

Modele geração, ativação, distribuição, armazenamento, uso, rotação, revogação,
arquivamento e destruição. Registre metadados e identificador, nunca o segredo.
Rotação muda a chave para novas escritas; dados antigos continuam exigindo a
versão anterior até recriptografia ou fim da retenção.

## Prática

Desenhe estados e responsáveis de uma DEK de backup e da KEK que a protege.
