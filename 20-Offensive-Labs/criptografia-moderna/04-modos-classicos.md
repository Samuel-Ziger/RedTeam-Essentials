# 04 — ECB, CBC, CTR e limites

ECB cifra blocos iguais de modo igual e revela padrões; não deve proteger dados
estruturados. CBC exige IV imprevisível, padding e autenticação separada. CTR
transforma bloco em fluxo e exige unicidade estrita de contador/nonce.

Esses modos permanecem em protocolos e dados legados, por isso é necessário
reconhecê-los. Para novos formatos prefira AEAD. Migração lê com validação
estrita do formato antigo e grava somente o novo; nunca “corrija” CBC removendo
o erro de padding enquanto mantém ciphertext não autenticado.

## Verificação

Monte uma tabela: requisito de IV/nonce, integridade nativa e risco dominante.
