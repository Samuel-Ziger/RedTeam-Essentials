# Cheatsheet de investigação defensiva

## Ordem

1. autoridade e escopo;
2. preservar fontes voláteis e centrais;
3. registrar relógio/fuso/skew;
4. normalizar sem destruir o original;
5. construir timeline;
6. correlacionar por chaves fortes;
7. testar hipóteses concorrentes;
8. conter proporcionalmente;
9. comunicar fatos, inferências e lacunas;
10. revisar retenção e lições aprendidas.

## Força aproximada de pivôs

| Pivô | Observação |
|---|---|
| request/session/correlation ID | forte dentro do sistema que o emitiu |
| ID de autenticação + dispositivo gerenciado | forte, ainda sujeito a roubo de sessão |
| processo + conexão + usuário no endpoint | forte para atividade do dispositivo |
| IP + porta + protocolo + tempo + NAT log | útil para conectividade, não autoria |
| IP isolado | fraco; pode ser compartilhado/intermediado |
| ferramenta, idioma ou fuso | indício contextual, alto risco de viés |

## Linguagem

- **Fato:** o log X registrou Y.
- **Inferência:** X e Z provavelmente pertencem à mesma sessão porque...
- **Alternativa:** token roubado ou NAT compartilhado também explicam...
- **Confiança:** baixa/média/alta com critérios declarados.
- **Lacuna:** fonte ausente, relógio incerto ou retenção expirada.

