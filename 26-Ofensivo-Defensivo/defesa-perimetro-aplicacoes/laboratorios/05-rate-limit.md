# Laboratório 05 — Token bucket

## Executar

```bash
python3 ../exemplos/token_bucket.py ../fixtures/eventos-rate-limit.json
```

## Red

Preveja o resultado antes de executar. Adicione eventos exatamente na fronteira,
um custo maior que um e uma chave de outro tenant. Não gere requisição real.

## Blue

Explique capacidade, refill, burst e tokens restantes. Defina métricas para
rejeição normal, abuso e falha do backend de estado.

## Purple

Teste determinismo, isolamento de chave e rejeição de tempo regressivo. Proponha
chaves distintas para login anônimo, API por tenant e export de relatório.
Registre a tolerância a overshoot em uma implantação distribuída.
