# 09 — OWASP CRS, score e tuning

OWASP Core Rule Set é um conjunto genérico de regras para engines compatíveis,
como ModSecurity e Coraza. Ele combina detecções e acumula anomaly score; a
transação é interrompida quando o limiar configurado é atingido.

## Paranoia levels

PL1 busca baixa incidência de falsos positivos. Níveis maiores habilitam
detecções mais agressivas e exigem mais tuning. Não aumente o nível para
compensar falta de inventário. Cobertura que interrompe operação é um controle
mal operado.

## Implantação disciplinada

1. fixe engine e versão do CRS;
2. comece em detecção e preserve IDs de regra;
3. execute testes funcionais e negativos;
4. agrupe falsos positivos por rota, parâmetro e regra;
5. crie exclusão estreita, comentada e testada;
6. habilite bloqueio por canário;
7. reavalie em upgrades.

```text
ruim:  remover a regra globalmente
melhor: excluir o argumento documentado apenas na rota e método necessários
```

O CRS recomenda tuning por exclusões; elevar o limiar temporariamente pode
ajudar no rollout, mas um limiar permanentemente enorme mascara o problema.

## Virtual patch

Uma regra local pode reduzir exposição de uma falha conhecida até a correção.
Registre CVE/defeito, owner, data-limite, testes e condição de remoção. Não
declare a vulnerabilidade corrigida.

## Exercício Purple

Red entrega casos válidos e inválidos para uma rota fictícia. Blue identifica
qual regra contribuiu para o score e propõe a exclusão mínima. Purple verifica
que o caso legítimo passa, o negativo continua detectado e a exceção expira.
