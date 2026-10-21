# Laboratório 05 — Capstone de aplicação profissional

## Objetivo

Entregar e defender uma aplicação pequena, completa e sustentável. O capstone
integra produto, domínio, interfaces, persistência, acessibilidade, diagnóstico,
distribuição e suporte. Quantidade de telas não pontua; contratos verificáveis e
recuperação sob falha pontuam.

## Escolha do produto

Escolha um problema local legítimo, como catálogo pessoal, planejador de estudo,
controle de inventário sintético, conversor em lote ou anotador de experimentos.
Evite autenticação, pagamentos, saúde, coleta de dados reais e dependência de
serviço externo. O escopo deve caber em quatro casos de uso essenciais.

Antes do código, entregue uma proposta de uma página:

- pessoa, contexto e trabalho a realizar;
- quatro casos de uso e três não objetivos;
- dados, retenção e modelo de ameaça básico;
- CLI e interface visual que compartilham domínio;
- estados vazios, lentos, inválidos, offline e incompatíveis;
- orçamento de desempenho;
- estratégia de instalação, atualização e recuperação.

## Requisitos essenciais

### Domínio e arquitetura

- regras independentes de UI, rede, relógio e persistência concretos;
- contratos e invariantes representados em tipos/validação;
- pelo menos dois adapters substituíveis ou falsos de teste;
- ADRs para persistência, interface e distribuição;
- dependências apontando para o núcleo, sem ciclo oculto.

### Entrada e configuração

- ajuda e exemplos reais;
- precedência explícita entre padrão, arquivo, ambiente e CLI quando aplicável;
- erros de uso distintos de falhas operacionais;
- saídas de máquina estruturadas e estáveis;
- nenhum segredo embutido ou emitido.

### Dados e evolução

- documento ou schema versionado com limites;
- importação validada integralmente antes do commit;
- exportação/backup e recuperação testados;
- política para versão futura e campo desconhecido;
- fixture de migração ou justificativa de por que ainda não existe migração.

### Interface

- tarefa principal concluída por teclado;
- foco, erro, status, reflow e contraste verificados;
- estado central previsível e operações concorrentes identificadas;
- conteúdo externo inserido como texto;
- locale, datas e números tratados deliberadamente.

### Operação

- logs/eventos estruturados e sanitizados;
- pacote de diagnóstico com consentimento e prévia;
- artefato reproduzível em ambiente limpo;
- teste de instalação, upgrade, remoção e rollback;
- orçamento medido com dados representativos;
- runbook de suporte.

## Plano de execução

1. Congele o contrato de versão 1 e os critérios de aceite.
2. Faça um walking skeleton: caso de uso, adapter falso, CLI e teste.
3. Adicione persistência e fixtures de falha.
4. Ligue a interface visual ao mesmo núcleo.
5. Teste acessibilidade, concorrência, offline e dados incompatíveis.
6. Instrumente, meça e corrija um gargalo real.
7. Empacote e teste em ambiente limpo.
8. Simule upgrade com falha e recuperação.
9. Peça a outra pessoa para executar apenas pelo README.
10. Corrija documentação e produto a partir da observação.

## Demonstração obrigatória

Em até 20 minutos, mostre sem edição de vídeo:

1. ambiente limpo e versão da toolchain;
2. ajuda/primeiro uso;
3. caso essencial pela CLI;
4. o mesmo núcleo pela interface visual;
5. entrada inválida preservando o que pode ser corrigido;
6. importação incompatível sem perda;
7. uso por teclado e zoom;
8. falha de persistência ou rede e recuperação;
9. teste automatizado e orçamento;
10. artefato, hash, diagnóstico e rollback.

Uma gravação é evidência auxiliar. O avaliador deve conseguir repetir os passos
com comandos e fixtures entregues.

## Rubrica de 100 pontos

| Área | Pontos | Evidência principal |
|---|---:|---|
| contrato de produto e escopo | 10 | proposta, estados, aceite e não objetivos |
| arquitetura e domínio | 15 | testes puros, adapters e ADRs |
| CLI/configuração/erros | 10 | matriz de processo e precedência |
| dados, migração e recuperação | 15 | fixtures, round-trip, rollback |
| interface e acessibilidade | 15 | relatório manual e testes de estado |
| resiliência e internacionalização | 10 | cenários de concorrência/offline/locale |
| diagnóstico e privacidade | 10 | catálogo, canário e pacote sanitizado |
| distribuição e release | 10 | artefato limpo, hash e runbook |
| desempenho e comunicação | 5 | orçamento antes/depois e README validado |

Requisitos essenciais são eliminatórios: perda silenciosa de dados, tarefa
inacessível por teclado, segredo em log, artefato impossível de executar ou
testes que dependem de serviço público impedem aprovação mesmo acima de 75.

## Revisão oral

Responda com evidência:

- qual invariante evita o dano mais caro?
- onde ocorre o commit e o que acontece se ele falhar?
- qual estado não pode ser representado e por quê?
- como uma resposta antiga é reconhecida?
- o que uma versão anterior faz com dado futuro?
- que dado diagnóstico foi deliberadamente excluído?
- qual medida mudou sua decisão de desempenho?
- como desinstalar sem destruir dado que o usuário decidiu preservar?

## Checklist final

- [ ] Uma pessoa nova executou pelo README.
- [ ] Todas as fixtures são sintéticas e pequenas.
- [ ] Testes passam duas vezes sem ordem ou rede pública.
- [ ] Falhas deliberadas preservam estado confirmado.
- [ ] A interface passou por teclado, zoom e leitor de tela disponível.
- [ ] O canário não aparece em nenhuma saída ou pacote.
- [ ] O artefato foi verificado fora do workspace.
- [ ] Rollback e versão futura foram demonstrados.
- [ ] Limitações conhecidas e próximos passos estão explícitos.
