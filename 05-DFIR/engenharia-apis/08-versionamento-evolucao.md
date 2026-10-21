# 08 — Versionamento, compatibilidade e retirada

Versionar é administrar mudança. Colocar v1 na URL só identifica uma linha do
contrato; não detecta quebra, migra consumidores nem permite retirada segura. A
primeira estratégia é evoluir de forma compatível e observar uso real.

## Objetivos

- classificar mudanças sintáticas, semânticas e operacionais;
- escolher estratégia de versão com critérios;
- automatizar análise sem confiar somente no diff;
- conduzir depreciação e sunset;
- testar produtor novo com consumidores antigos.

## 1. Compatibilidade em várias dimensões

| Mudança | Risco |
|---|---|
| adicionar operação | geralmente baixo |
| adicionar campo opcional | depende de leitores tolerantes |
| adicionar enum | quebra switches exaustivos |
| remover/renomear campo | alto |
| mudar tipo ou unidade | alto |
| reduzir limite | quebra operacional |
| mudar default | quebra semântica silenciosa |
| mudar ordem/paginação | quebra resultados |
| piorar p99/SLO | quebra operacional |

Um validador de OpenAPI detecta parte das quebras estruturais. Não percebe que
price mudou de centavos para reais ou que status pending agora inclui outro
estado. Revisão de semântica e teste de consumidor continuam necessários.

## 2. Tolerant reader e robustez

Leitores devem ignorar campos desconhecidos quando o contrato permite. Não devem
aceitar significado desconhecido silenciosamente em campos críticos: para enum
novo, use fallback explícito, preserve valor e impeça ação perigosa.

Produtores aceitam somente o contrato de escrita. “Ser liberal no que recebe”
sem limites pode mascarar erro e ampliar superfície. Tolerância de leitura e
validação estrita de comando convivem.

## 3. Estratégias de versão

- **URI:** /v1/items; visível e simples, mas duplica rotas;
- **media type:** Accept com versão; flexível, porém tooling mais complexo;
- **campo de mensagem:** comum em eventos;
- **package/service:** comum em Protobuf/gRPC;
- **evolução aditiva:** mantém identificador enquanto compatível.

Escolha uma política por ecossistema. Versionar toda pequena adição cria versões
demais; nunca versionar transforma quebra silenciosa em regra.

## 4. Expandir e contrair

Migração segura costuma ter fases:

1. adicionar campo/operacão nova;
2. provider suporta forma antiga e nova;
3. consumidores migram e reportam versão;
4. telemetria confirma uso residual;
5. bloquear novos consumidores antigos;
6. remover suporte somente após janela;
7. manter rollback limitado.

Para renomear campo, produzir ambos por um período pode funcionar; em escrita,
receber ambos exige regra de conflito. Dual write sem reconciliação cria
divergência.

## 5. Deprecation e Sunset

Depreciação é aviso; sunset é data de retirada. O processo inclui:

- owner e consumidores inventariados;
- alternativa disponível e guia de migração;
- marcação no contrato e documentação;
- telemetria por identidade/versão;
- comunicação com datas e canal;
- teste de desligamento e rollback;
- evidência de ausência antes da remoção.

Headers Deprecation e Sunset podem complementar, mas não substituem comunicação
e inventário. Cliente offline ou uso mensal exige janela proporcional.

## 6. Eventos e dados persistidos

Evento pode ser armazenado e reproduzido anos depois. Consumidor novo precisa
ler versões históricas ou um upcaster precisa convertê-las. Não reescreva o
significado de event type existente.

Dados persistidos também carregam versão de schema. Deploy de aplicação e
migração devem suportar sobreposição: código antigo com coluna nova e código novo
antes da contração.

## 7. Teste de compatibilidade

Combine:

- diff estático do contrato;
- validação de exemplos;
- consumer-driven contracts;
- replay de tráfego sintético sanitizado;
- suite do cliente antigo contra provider novo;
- canário por versão;
- alerta de uso deprecado.

Uma mudança classificada como compatível pode falhar por gerador específico.
Teste SDKs suportados.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| “só adicionamos enum” | cliente encerra | unknown seguro |
| v2 sem migração | versões eternas | plano de retirada |
| data sem inventário | consumidor oculto quebra | telemetria |
| diff como única prova | semântica muda invisível | revisão e teste |
| evento reescrito | replay diferente | imutabilidade/versionamento |

## Exercícios

### Nível 1 — classificar

Classifique 15 mudanças em compatível, incompatível ou dependente. **Aceite:**
cada “dependente” nomeia a hipótese de consumidor.

### Nível 2 — expand/contract

Renomeie um campo sem downtime. **Aceite:** leitura/escrita, conflito, telemetria,
rollback e remoção estão definidos.

### Nível 3 — cliente antigo

Execute SDK antigo contra provider novo com enum e campo adicionais. **Aceite:**
comportamento desconhecido é seguro e observável.

## Checklist

- [ ] Compatibilidade inclui semântica e SLO.
- [ ] Estratégia de versão é consistente.
- [ ] Há período de sobreposição e rollback.
- [ ] Consumidores e versões são observáveis.
- [ ] Eventos históricos continuam legíveis.
- [ ] Retirada depende de evidência, não apenas data.

