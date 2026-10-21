# 01 — Objetivos, ativos e modelos de ameaça

Comece pelo ativo e pelo tempo durante o qual ele precisa de proteção. Um token
de cinco minutos, uma assinatura de atualização e um prontuário de décadas têm
riscos diferentes. Modele o adversário: observa, modifica, repete mensagens,
obtém backups, compromete um endpoint ou mede tempo? Declare também o que ele
não consegue fazer.

A tríade confidencialidade–integridade–disponibilidade é insuficiente sozinha.
Considere autenticidade, frescor, não vinculação, sigilo futuro, resistência a
comprometimento e possibilidade de recuperação. Kerckhoffs orienta que o
sistema deve continuar seguro quando o projeto é público; o segredo é a chave.

## Prática

Modele um backup: dados, metadados, operadores, repositório, período de retenção
e consequências de perda, vazamento, alteração e indisponibilidade.
