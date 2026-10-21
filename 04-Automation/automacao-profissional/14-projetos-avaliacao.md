# 14 — Projeto integrador e avaliação profissional

O encerramento do módulo não mede quantas ferramentas você conhece. Ele mede se
outra pessoa consegue entender, revisar, executar, interromper e recuperar a sua
automação com evidência reproduzível.

## Objetivos

- integrar contratos, dry-run, idempotência, segurança e operação;
- entregar um projeto guiado e um projeto autoral defensável;
- demonstrar falhas injetadas, retomada e compatibilidade;
- avaliar por propriedades, não por quantidade de código.

## 1. Projeto guiado: FileFlow

O [FileFlow](projetos/fileflow/README.md) é uma CLI local que descobre e copia
arquivos permitidos sem remover a origem. O projeto é pequeno para tornar controles
visíveis: planejamento, colisão, criação exclusiva, hash, manifesto e audit JSONL.

Contrato-base:

~~~text
entrada: raiz de origem existente e raiz de destino não aninhada
escopo: arquivos regulares com extensão permitida, sem links
padrão: dry-run sem qualquer mutação
apply: copia apenas ausentes; iguais viram skip; diferentes bloqueiam
integridade: tamanho e SHA-256 verificados
evidência: plano versionado, digest, run ID, relatório e audit log
~~~

### Marcos

1. **Descoberta e plano:** execute fixtures, explique copy/skip/conflict e prove
   ordem determinística.
2. **Execução segura:** aplique, repita, provoque destino concorrente e confirme
   que nada é sobrescrito.
3. **Limites:** adicione max-files e max-total-bytes com teste nos limites.
4. **Evidência:** implemente relatório terminal por operação e reconciliação.
5. **Retomada:** injete falha após N cópias e retome sem duplicar.
6. **Distribuição:** empacote, execute fora do checkout e entregue runbook.

### Invariantes obrigatórios

- dry-run não cria destino, manifesto, audit ou temporário, salvo arquivo de
  manifesto solicitado explicitamente e documentado como saída do planejamento;
- nenhum caminho escapa das raízes;
- symlink e arquivo especial não são seguidos;
- conflito conhecido aborta antes do primeiro copy;
- destino surgido durante apply nunca é sobrescrito;
- fonte modificada depois do plano é recusada;
- repetir preserva o estado de destino;
- cada operação termina em um outcome reconciliável;
- logs não contêm conteúdo nem segredo.

## 2. Projeto autoral

Escolha um problema legítimo e autorizado. Exemplos:

- pipeline de validação CSV/JSON;
- gerador de relatórios a partir de dados sintéticos;
- verificador de links de um site próprio;
- sincronizador controlado entre dois stores locais/fakes;
- coletor de métricas de um serviço de laboratório;
- cliente de API sandbox com paginação e checkpoint;
- gerador de documentos por template.

O projeto não pode depender de varredura, exploração ou serviço de terceiros sem
autorização. A formação-base trabalha com sistemas próprios, fakes e sandboxes.

## 3. Documento de proposta

Antes do código, entregue:

1. pessoa usuária e tarefa;
2. processo manual e exceções;
3. por que automatizar e qual nível de autonomia;
4. entradas, saídas, efeitos e não objetivos;
5. limites de itens, bytes, tempo, taxa e concorrência;
6. modelo de ameaça e dados envolvidos;
7. chave de idempotência e pós-condição;
8. falhas parciais e recuperação;
9. métricas, alertas e ownership;
10. critérios de piloto, expansão e desativação.

A proposta é um gate. Se a pós-condição não pode ser observada, ainda não há
contrato suficiente para implementar apply automático.

## 4. Arquitetura mínima

~~~text
CLI ou scheduler
      |
application service ---- clock/random/id generator
      |
domain planner --------- tipos Plan/Operation/Report
      |
ports ------------------ storage/http/checkpoint/audit
      |
adapters reais e fakes
~~~

O domínio não importa parser de CLI nem SDK do fornecedor. Adapters traduzem
protocolos e classificam falhas. O executor não recalcula regra de planejamento.

## 5. Requisitos funcionais

- CLI com help, version, dry-run padrão e apply explícito;
- schema de entrada/saída versionado;
- validação e limites antes do efeito;
- plano imutável com operação, razão e pré-condição;
- identidade estável e repetição segura;
- checkpoint quando o volume exigir retomada;
- relatório por item e resumo reconciliado;
- modo text para pessoas e JSON para integração;
- configuração sem segredo versionado.

## 6. Requisitos de resiliência

Quando houver dependência externa:

- timeout por tentativa e deadline total;
- retry somente para classe e semântica seguras;
- backoff com jitter injetável;
- rate/concorrência/fila limitados;
- 429 e Retry-After;
- estado uncertain após escrita ambígua;
- dead-letter com replay controlado.

Se o projeto é totalmente local, substitua por falhas relevantes: disco, permissão,
arquivo alterado, destino concorrente e interrupção.

## 7. Segurança e privacidade

- matriz identidade × ação × ambiente;
- nenhuma concatenação de comando/caminho/template;
- allowlist e tamanhos máximos;
- segredo por mecanismo apropriado e canário de vazamento;
- dependências fixadas, inventariadas e atualizáveis;
- artifacts sem fixture sensível, cache ou caminho pessoal;
- retenção para logs, temporários e quarentena;
- uso apenas em ambiente próprio ou autorizado.

## 8. Suíte e demonstração

Testes obrigatórios:

- entrada feliz, vazia, limite e limite + 1;
- dry-run sentinela sem mutação;
- duas execuções idempotentes;
- pré-condição alterada entre plan e apply;
- falha antes e depois do commit;
- cancelamento e relatório parcial;
- configuração/schema anterior e futuro;
- canário ausente de logs/artifacts;
- pacote executado fora do repositório.

A demonstração segue roteiro reproduzível e não edita o estado manualmente para
esconder falha.

## 9. Evidências da entrega

- README com quickstart e contrato;
- ADRs das decisões importantes;
- threat model simples;
- exemplos e fixtures sintéticas;
- testes e relatórios;
- manifesto/SBOM do artifact;
- runbook com falha parcial, replay e rollback;
- changelog e matriz de compatibilidade;
- relatório de experimento de capacidade;
- limitações conhecidas e próximos passos.

## 10. Rubrica

| Dimensão | Pontos |
|---|---:|
| problema, contrato, limites e autonomia | 12 |
| plano, idempotência e dry-run | 15 |
| efeitos, integridade e recuperação | 15 |
| arquitetura, dados e integrações | 12 |
| testes, propriedades e fault injection | 15 |
| segurança, privacidade e supply chain | 12 |
| observabilidade, alertas e runbook | 10 |
| distribuição, compatibilidade e documentação | 9 |
| **Total** | **100** |

Conclusão exige 75 pontos e nenhum gate essencial zerado: dry-run/idempotência,
segurança de efeitos, testes de falha ou operação.

## 11. Defesa técnica

A pessoa avaliadora pode perguntar:

- Qual é o instante exato do commit?
- O que ocorre se a resposta se perder depois do efeito?
- Como sabe que o segundo apply não duplica?
- O que impede caminho, comando ou template injection?
- Onde um segredo poderia vazar?
- Como retomar depois de metade do lote?
- Que métrica detecta atraso sem gerar ruído?
- Como uma versão antiga reage a dado futuro?
- Como remover completamente a automação?

Responder apontando código, teste e evidência vale mais que uma afirmação verbal.

## 12. Critério final

O projeto está pronto quando uma segunda pessoa, em ambiente limpo, consegue:

1. verificar e instalar o artifact;
2. pedir ajuda e validar configuração;
3. executar dry-run e compreender o plano;
4. aplicar em dados sintéticos;
5. repetir sem duplicar;
6. provocar uma falha documentada;
7. diagnosticar e retomar pelo runbook;
8. atualizar ou remover preservando o contrato.

## Checklist

- [ ] Proposta e critérios foram escritos antes do apply.
- [ ] Gates essenciais possuem testes automatizados.
- [ ] Falha parcial e estado incerto aparecem na demonstração.
- [ ] Evidências podem ser reproduzidas por outra pessoa.
- [ ] Limitações e não objetivos são honestos.
- [ ] O projeto opera somente dentro de escopo autorizado.

