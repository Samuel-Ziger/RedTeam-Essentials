# 13 — Distribuição, compatibilidade e operação

Uma ferramenta não está pronta quando funciona no checkout do autor. Ela precisa
ser instalada, configurada, atualizada, diagnosticada e removida por outra pessoa
sem depender de arquivos globais ou conhecimento implícito.

## Objetivos

- definir pacote, versão, configuração e plataformas suportadas;
- criar release verificável e smoke test fora do repositório;
- evoluir CLI, config, manifesto e dados com compatibilidade;
- escrever runbook de instalação, operação, rollback e remoção;
- encerrar o ciclo de vida sem deixar credencial, agenda ou dados órfãos.

## 1. Contrato de distribuição

Declare:

- plataformas e arquiteturas;
- runtime incluído ou pré-requisito;
- formato do pacote e canal oficial;
- versão e política de suporte;
- checksum e, quando aplicável, assinatura/proveniência;
- local de configuração, dados, cache e logs;
- como instalar, verificar, atualizar e remover;
- compatibilidade de dados para upgrade/downgrade.

Um zip solto pode ser suficiente, desde que tenha contrato e verificação. Um
instalador sofisticado sem rollback pode ser pior.

## 2. Versionamento multidimensional

Não existe apenas a versão do binário:

| Componente | Exemplo |
|---|---|
| aplicação | 2.3.1 |
| config schema | 3 |
| manifest schema | 2 |
| audit event | file.completed.v1 |
| dados persistidos | 4 |
| plugin API | 2 |

Sem separar, uma mudança na saída JSON pode quebrar integração mesmo em patch
aparentemente inocente. Documente estabilidade de CLI e formatos consumíveis por
máquina.

## 3. SemVer e contrato real

Semantic Versioning ajuda se existe API pública declarada. Major indica quebra,
minor adição compatível e patch correção compatível. Mas “compatível” depende do
contrato: texto humano pode mudar livremente, enquanto JSON, códigos e flags não.

Não use major como licença para quebrar sem migração. Informe depreciação,
substituto, prazo e ferramenta de conversão.

## 4. Configuração

Forneça exemplo sem segredo, schema e comando para imprimir configuração efetiva
com valores sensíveis ocultos. Defina precedência entre defaults, arquivo, ambiente
e CLI. Valor vazio não deve significar ausência por acidente.

Ao carregar:

1. parseie;
2. valide versão e tipos;
3. aplique migração em memória;
4. valide invariantes completas;
5. mostre plano de mudança;
6. preserve backup e publique atomicamente se solicitado.

Versão futura deve ser recusada sem sobrescrever. Downgrade não é seguro se o
programa antigo não entende o schema novo.

## 5. Artefato limpo

Gere a partir de checkout limpo e inventarie conteúdo. Procure:

- segredos, chaves e arquivos de ambiente;
- fixtures internas ou dados pessoais;
- caches, coverage e bytecode;
- caminhos absolutos do desenvolvedor;
- dependência global não declarada;
- permissão executável ausente ou excessiva;
- licença e notices necessários.

Calcule digest após empacotar. Teste o artifact extraído em diretório temporário
sem checkout ao redor.

## 6. CLI operacional

Uma ferramenta operável oferece:

- help sem inicializar rede ou segredo;
- version com versão e, quando útil, commit/build;
- dry-run padrão para efeito material;
- apply explícito;
- formato text e JSON estável;
- códigos de saída documentados;
- comando de diagnose que não vaza ambiente;
- timeout, limite e cancelamento;
- manifesto e correlação por execução.

Confirmação interativa não funciona bem em agenda. Para automação, use flag
explícita e política; para uso humano, resumo e confirmação podem complementar.

## 7. Instalação e primeira execução

Teste como novo usuário:

1. obter do canal oficial;
2. verificar digest/assinatura;
3. instalar sem acesso ao fonte;
4. executar help e version;
5. gerar config de exemplo;
6. rodar dry-run com fixture;
7. aplicar em diretório temporário;
8. localizar logs/dados e remover tudo.

Esse smoke test encontra arquivo não empacotado e dependência herdada.

## 8. Upgrade e rollback

Matriz mínima:

| Cenário | Deve provar |
|---|---|
| instalação nova | defaults e help funcionam |
| N-1 -> N | dados/config migram |
| N com dados atuais | reinício é idempotente |
| rollback binário | dado continua legível ou recusa segura |
| versão futura | original é preservado |

Antes de migrar, valide backup e restauração. “Criamos um backup” não prova que
ele abre. Migração destrutiva pode exigir exportação de recuperação em vez de
downgrade.

## 9. Runbook operacional

Inclua:

- objetivo, owner e escopo;
- dependências e permissões;
- primeiro dry-run;
- agenda, janela e limites;
- sinais normais e alertas;
- falha parcial, uncertain e replay;
- pausa, cancelamento e kill switch;
- rotação/revogação de credencial;
- upgrade, rollback e pós-verificação;
- coleta sanitizada de suporte;
- remoção e retenção.

Comandos destrutivos não devem ser exemplos vagos com variável não validada.
Resolva e confirme alvos específicos.

## 10. Suporte e diagnóstico

Um bundle de suporte é local e opt-in. Mostre prévia, permita excluir itens e
inclua manifesto, versões, configuração redigida e eventos limitados. Nunca envie
automaticamente. Teste com canário para garantir ausência de segredo.

Defina versões suportadas e prazo de correção. Sem isso, operadores mantêm releases
antigas indefinidamente ou atualizam sem previsibilidade.

## 11. Depreciação e fim de vida

O encerramento remove agenda, token, permissão, webhook, storage, alerta e ownership.
Exporte dados quando necessário e comprove remoção segundo a política. Publique
data, substituto e passos. Ferramenta abandonada com credencial ativa é risco.

## Falhas e diagnóstico

| Sintoma | Causa | Verificação |
|---|---|---|
| só funciona no repo | recurso/dependência global | smoke fora do checkout |
| upgrade perde config | migração in-place | cópia, validação, replace |
| downgrade corrompe | schema futuro ignorado | recusa preservando original |
| artifact vaza dado | empacotamento amplo | inventário e scanner |
| ferramenta removida ainda roda | agenda/token órfão | checklist de EOL |

## Exercícios

### Nível 1 — artifact

Empacote e execute fora do repositório. **Aceite:** help, version, dry-run e teste
funcionam sem caminho local ou dependência implícita.

### Nível 2 — migração

Migre config v1 para v2. **Aceite:** falha no último campo preserva v1, versão
futura é recusada e segunda migração não muda o resultado.

### Nível 3 — operação

Ensaie instalação, falha parcial, upgrade, rollback e remoção. **Aceite:** outra
pessoa executa pelo runbook e verifica dados, credenciais, agenda e alerts.

## Checklist

- [ ] Plataformas, runtime e canal oficial estão declarados.
- [ ] Artefato tem versão, digest, inventário e smoke test.
- [ ] CLI e formatos de máquina possuem contrato estável.
- [ ] Upgrade, versão futura e rollback foram testados.
- [ ] Bundle de suporte é sanitizado e opt-in.
- [ ] Fim de vida remove todos os recursos e acessos.

