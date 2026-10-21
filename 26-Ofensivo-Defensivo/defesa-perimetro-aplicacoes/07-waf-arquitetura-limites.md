# 07 — WAF: arquitetura e limites

Web Application Firewall avalia HTTP(S) com regras gerenciadas, regras locais,
limites de taxa e sinais de contexto. Pode registrar, desafiar ou bloquear uma
requisição antes da aplicação. É defesa em profundidade, não correção do código.

## Onde ele ajuda

- bloquear classes conhecidas enquanto a correção é preparada;
- restringir método, caminho, tamanho, tipo e origem;
- reduzir varredura ruidosa e abuso repetitivo;
- aplicar virtual patch temporário e observável;
- padronizar telemetria na borda.

## Onde ele não basta

Um WAF normalmente não entende que o usuário A não pode ler o objeto B, que um
pagamento viola regra de negócio ou que uma credencial válida foi obtida por
phishing. Conteúdo cifrado até a aplicação, protocolos não suportados, origem
direta e parsing diferente também criam lacunas.

## Pipeline de decisão

```text
normalizar → permitir exceção estreita → regras gerenciadas → regras locais
           → rate/bot → log/desafio/bloqueio → origem
```

A ordem e a semântica de ação terminal variam. Uma regra `allow/skip` ampla
pode impedir avaliações posteriores; confirme no fornecedor.

## Ciclo de vida

Comece em observação, use tráfego representativo, associe cada evento a uma
regra e faça exclusão pelo campo/rota mais estreito. Versione alterações, use
canário, monitore latência e tenha rollback. Exceção sem expiração vira dívida.

## Purple Team

Red cria casos negativos que representam classes e limites, sem fornecer uma
sequência de evasão. Blue demonstra log, decisão e caminho de resposta. Purple
abre defeito para a aplicação: o WAF reduz exposição, mas não encerra a causa.
