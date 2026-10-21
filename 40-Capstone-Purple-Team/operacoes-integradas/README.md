# Capstone Purple Team: operações integradas

O projeto final demonstra que o aluno consegue planejar, executar, observar,
corrigir e comunicar uma operação autorizada completa.

## Fases obrigatórias

| Fase | Evidência mínima |
|---:|---|
| 1. Autoridade | RoE assinada, escopo, riscos, contatos e critérios de parada. |
| 2. Baseline | Arquitetura, inventário, controles e telemetria antes do teste. |
| 3. Hipóteses | Cenários ligados a risco e a objetivos Blue Team. |
| 4. Execução | Evidência mínima, timestamps e log de decisões. |
| 5. Defesa | Detecção, triagem, contenção e comunicação. |
| 6. Melhoria | Correção versionada, rollback e reteste. |
| 7. Encerramento | Limpeza, riscos residuais e apresentação executiva/técnica. |

## Fixtures e ferramentas locais

- [Percurso de laboratórios](../acervo/LEGADO-OFFENSIVE-LABS.md)
- [Correlacionador de reconhecimento](../acervo/tools/recon_correlator.py)
  com [fixture](../acervo/fixtures/recon.json)
- [Matriz de autenticação de API](../acervo/tools/api_auth_matrix.py)
  com [fixture](../acervo/fixtures/api-auth-results.json)

## Critério de conclusão

O portfólio precisa ser reproduzível, distinguir fatos de inferências, proteger
segredos, demonstrar melhoria depois do reteste e registrar a restauração do
ambiente. A qualidade defensiva tem o mesmo peso da validação ofensiva.
