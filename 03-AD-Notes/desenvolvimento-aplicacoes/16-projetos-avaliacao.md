# 16 — Projeto integrador, defesa técnica e avaliação

O encerramento deste módulo não é uma prova de memorização. É a demonstração de
que você consegue transformar regras em uma aplicação utilizável, evoluí-la sem
perder dados, medir uma propriedade relevante e entregar um artefato que outra
pessoa consegue executar. O projeto integra decisões dos capítulos 00–15 e torna
visíveis os trade-offs que exercícios isolados não mostram.

Você pode evoluir o Study Desk ou criar uma aplicação autoral. Em ambos os casos,
o resultado deve ser benigno, local ou conectado somente a uma API própria do
módulo 01, e usar dados sintéticos na avaliação. Sistemas Operacionais e redes
têm módulos próprios; aqui, plataforma e transporte são limites externos, não o
objeto de estudo.

## Objetivos de aprendizagem

Ao concluir, você deverá conseguir:

- recortar problema, público, jornada e não objetivos verificáveis;
- transformar requisitos em invariantes e critérios de aceite;
- manter domínio, apresentação e persistência com fronteiras claras;
- implementar acessibilidade, diagnóstico, desempenho e recuperação;
- planejar versão, plugin opcional, empacotamento, atualização e suporte;
- apresentar evidências reproduzíveis, não apenas uma demonstração feliz;
- defender decisões, limites e alternativas com honestidade técnica;
- avaliar outro projeto usando uma rubrica comum.

## Pré-requisitos e condição de início

Conclua os capítulos anteriores, rode os testes do
[Study Desk](projetos/study-desk/README.md) e releia os critérios dos exercícios
que ainda não domina. Antes de implementar, crie um diretório de evidências com:

```text
docs/
  product-brief.md
  architecture.md
  adr/
  accessibility-report.md
  performance-report.md
  release-plan.md
  runbook.md
fixtures/
tests/
```

O nome exato pode variar. O importante é que outra pessoa encontre a relação
entre requisito, decisão, teste e resultado.

## 1. Duas modalidades

### Projeto guiado — evolução do Study Desk

O projeto existente já oferece formulário acessível, reducer puro, valores
derivados, armazenamento local versionado, importação transacional, exportação,
tema e testes. Evolua-o em incrementos:

1. edição com confirmar/cancelar sem perder o valor anterior;
2. desfazer exclusão com prazo e anúncio acessível;
3. migração de `schemaVersion: 1` para `2` com fixtures;
4. segundo idioma com pluralização e formatação apropriada;
5. formato de exportação Markdown pelo contrato de extensão;
6. orçamento e perfil para 10.000 sessões sintéticas;
7. pacote estático verificável ou alternativa documentada em ADR;
8. plano de release, atualização, restauração e suporte.

Não implemente tudo de uma vez. Cada incremento precisa preservar testes e gerar
evidência própria.

### Projeto autoral

Escolha algo que uma pessoa consiga usar e avaliar em até dez minutos:

- organizador local de referências;
- diário de treino ou estudo;
- editor de checklist com modelos;
- visualizador e filtrador de CSV;
- cliente para a API construída no módulo 01;
- inventário pessoal local;
- catálogo de livros, filmes ou receitas.

Evite escopo que dependa de coleta externa, automação ofensiva, infraestrutura ou
administração de SO. Um produto menor e completo demonstra mais engenharia do que
dez telas sem recuperação nem testes.

## 2. Product brief de uma página

Antes do backlog, escreva:

```markdown
# Produto
Público: estudante que registra sessões no próprio navegador.
Problema: perder a visão do tempo dedicado por assunto.
Jornada principal: registrar, localizar e exportar uma sessão.
Resultado: histórico persistente e resumo compreensível.
Não objetivos: colaboração, conta, sincronização e recomendação automática.
Restrições: local-first, teclado, dados sintéticos na avaliação.
```

Adicione três cenários alternativos e três falhas: entrada inválida, armazenamento
indisponível e importação incompatível, por exemplo. Critérios devem ser
observáveis. “Interface moderna” não é critério; “em zoom 400%, ações permanecem
visíveis sem rolagem bidimensional na largura de referência” pode ser testado.

## 3. Requisitos essenciais

Todo projeto precisa demonstrar:

### Produto e interface

- uma jornada principal completa e pelo menos três estados alternativos/falhos;
- CLI, web ou GUI com contrato de entrada/saída documentado;
- feedback de processamento, sucesso, vazio e erro;
- navegação por teclado, foco, nomes acessíveis, reflow e redução de movimento;
- linguagem clara sem depender apenas de cor ou ícone.

### Estado, dados e integração

- regra de domínio independente da apresentação;
- fonte de verdade e fluxo de eventos identificáveis;
- configuração com precedência, tipos e validação;
- persistência versionada ou cliente de API com timeout/cancelamento/retry seguro;
- importação transacional e exportação, quando houver dados do usuário;
- limites de tamanho, quantidade e formato documentados;
- migração testada a partir da versão anterior suportada.

### Engenharia e entrega

- erros tipados ou códigos estáveis nas fronteiras;
- logs e diagnóstico sem segredo/conteúdo pessoal;
- testes de regra, borda, integração e jornada principal;
- orçamento de pelo menos uma jornada e relatório de profiling;
- artefato testado fora do workspace;
- versão, manifesto, SBOM e proveniência proporcionais ao projeto;
- release notes, licença, changelog, runbook e política de remoção;
- recuperação verificada para uma falha de atualização ou migração.

Plugin não é obrigatório quando não há eixo real de variação. Nesse caso, entregue
uma análise demonstrando por que configuração ou Strategy é suficiente. Criar um
plugin artificial apenas para marcar item reduz a qualidade arquitetural.

## 4. Invariantes do Study Desk

Para o projeto guiado, preserve pelo menos:

- título normalizado para validação, mas texto de exibição não é mutilado;
- duração é inteira e permanece no intervalo documentado;
- ID de sessão é único e não vem diretamente de texto do usuário;
- estado derivado não é persistido como segunda fonte de verdade;
- documento importado só substitui o atual após validação integral;
- versão futura de schema é rejeitada sem apagar dados presentes;
- cancelar edição mantém o registro original;
- desfazer restaura exatamente o item e sua posição sem duplicar ID;
- exportação é estável para a mesma coleção ordenada;
- falha de persistência aparece ao usuário e não finge sucesso.

Escreva testes para as regras antes da interface. Use fixtures pequenas e uma
fixture de limite gerada deterministicamente.

## 5. Arquitetura e ADRs

O diagrama pode permanecer simples:

```text
UI semântica -> handlers/composition root -> casos de uso/reducer
                                              |              |
                                        repositório      serviços estreitos
```

Documente direção de dependência, formato dos DTOs e onde ocorre validação. A UI
não deve conhecer detalhes do armazenamento; o domínio não deve importar DOM. O
composition root cria implementações e liga interfaces.

Escreva ADRs curtos para decisões que alteram custo ou contrato:

1. contexto e problema;
2. forças/qualidades relevantes;
3. opções consideradas;
4. decisão;
5. consequências positivas e negativas;
6. condição de revisão.

ADRs sugeridos: localStorage versus IndexedDB; pacote estático versus PWA;
extensão de exportação versus código no núcleo; migração imediata versus adiada.
Não use ADR para registrar cada função.

## 6. Plano em gates incrementais

### Gate 0 — Descoberta

Entregue brief, jornadas, riscos, não objetivos e wireframe sem dados reais.

**Saída:** escopo cabe no tempo; termos ambíguos viraram critérios.

### Gate 1 — Domínio executável

Implemente entidades/estado, casos de uso e repositório em memória, com testes de
invariantes e falhas.

**Saída:** regra roda sem interface e sem armazenamento real.

### Gate 2 — Jornada vertical

Conecte uma jornada completa à apresentação e ao adaptador de persistência.

**Saída:** outra pessoa conclui a tarefa e recebe feedback correto.

### Gate 3 — Bordas e evolução

Adicione importação, migração, acessibilidade, internacionalização necessária,
limites e diagnóstico.

**Saída:** fixtures inválidas não alteram estado e versão antiga migra.

### Gate 4 — Qualidade mensurada

Execute matriz de testes, auditoria manual de acessibilidade, orçamento e perfil.

**Saída:** relatórios contêm método, resultado, problema e correção.

### Gate 5 — Release

Empacote em ambiente limpo, gere evidências de origem, faça smoke test e ensaie
recuperação.

**Saída:** avaliador recebe os mesmos bytes testados e segue runbook sem ajuda.

Não avance com gate anterior quebrado. Isso reduz o custo de descobrir, no fim,
que a arquitetura impede migração ou teste.

## 7. Matriz de testes obrigatória

| Camada | Casos mínimos |
|---|---|
| domínio | válido, limites, vazio, duplicata e transição inválida |
| reducer/estado | evento conhecido, desconhecido e sequência completa |
| persistência | ausência, round-trip, corrupção, quota/falha simulada |
| migração | v1 válida, no limite, inválida e versão futura |
| interface | sucesso, vazio, erro, foco e anúncio |
| acessibilidade | teclado, zoom, contraste/estado, movimento e leitor suportado |
| desempenho | baseline, orçamento e caminho dominante |
| pacote | instalação/abertura limpa, versão e dependências ausentes |
| atualização | sucesso, interrupção e restauração |

Teste negativo deve provar preservação: após importação inválida, compare o estado
inteiro anterior; após falha na migração, confirme que backup e versão ativa
continuam identificáveis.

## 8. Evidências para entrega

O repositório final contém:

- README com problema, execução, teste, limites e privacidade;
- product brief e arquitetura;
- ADRs relevantes;
- código formatado e sem segredo;
- testes e fixtures sintéticas;
- relatório de acessibilidade com ambiente e itens manuais;
- relatório de desempenho com dados brutos/resumo e perfil;
- manifesto do artefato, hash, SBOM e proveniência declarada;
- matriz de compatibilidade e suporte;
- changelog e release notes;
- runbook de diagnóstico, backup, atualização e recuperação;
- licença e atribuições necessárias.

Uma gravação pode complementar, mas não substitui instruções reproduzíveis. Não
inclua caches, dependências baixadas, dumps pessoais ou credenciais.

## 9. Rubrica analítica de 100 pontos

| Dimensão | Pontos | Evidência de excelência |
|---|---:|---|
| problema, escopo e jornada | 10 | necessidade clara, não objetivos e falhas testáveis |
| domínio, estado e arquitetura | 15 | invariantes isolados, dependências direcionadas e ADRs honestos |
| interface e acessibilidade | 15 | jornada completa por teclado, foco/reflow/anúncio verificados |
| dados, configuração e evolução | 15 | precedência, schema, migração transacional, limites e recuperação |
| testes e diagnóstico | 15 | matriz baseada em risco, fixtures e logs minimizados |
| desempenho | 10 | orçamento, baseline, perfil e melhoria comprovada |
| empacotamento e release | 15 | artefato limpo/verificável, atualização, rollback e suporte |
| documentação e defesa | 5 | execução reproduzível e decisões respondidas com evidência |

Interpretação por dimensão:

- **0%:** ausente ou não executável;
- **25%:** demonstração feliz sem falhas/critério;
- **50%:** implementação básica com evidência parcial;
- **75%:** requisitos completos, bordas relevantes e documentação reproduzível;
- **100%:** além de completo, compara alternativas, mede trade-offs e prova
  recuperação.

Conclusão recomendada: **75 pontos**, nenhum requisito essencial zerado e todos
os bloqueadores abaixo ausentes. Nota alta não compensa perda de dados.

## 10. Bloqueadores de aprovação

O projeto não é aprovado enquanto houver:

- segredo, credencial ou dado pessoal no repositório/log/artefato;
- importação/migração capaz de apagar o estado válido ao falhar;
- jornada principal impossível por teclado no escopo declarado;
- teste principal vermelho ou instrução de execução que não funciona;
- pacote que depende silenciosamente do workspace;
- atualização sem qualquer recuperação testada;
- licença incompatível ou ausência de atribuição obrigatória;
- evidência fabricada, resultado omitido ou versão não identificável;
- função ofensiva, coleta não autorizada ou desvio do uso ético do curso.

Corrija o bloqueador e reavalie; não reduza sua importância por média de pontos.

## 11. Defesa técnica

Prepare uma demonstração de 20–30 minutos:

1. problema, público e jornada principal;
2. regra de domínio executada sem UI;
3. jornada feliz e uma falha real;
4. teclado, foco e reflow;
5. migração de fixture antiga e rejeição da futura;
6. perfil antes/depois da otimização;
7. criação e smoke test do artefato;
8. falha de atualização e recuperação pelo runbook;
9. maior dívida e próximo passo.

Perguntas para defesa:

1. Qual estado é a fonte de verdade e por quê?
2. O que acontece na primeira execução?
3. Em que fronteira dados deixam de ser confiáveis?
4. Como uma importação parcial é impedida?
5. Qual versão antiga é suportada e onde isso é testado?
6. Como a jornada funciona apenas com teclado?
7. Qual dado nunca deve aparecer no diagnóstico?
8. Qual gargalo foi medido e qual hipótese foi rejeitada?
9. O artefato avaliado é exatamente o testado?
10. Como voltar se o schema já tiver mudado?
11. Por que a extensão é plugin, configuração ou código do núcleo?
12. Que decisão você mudaria com dez vezes mais dados?

Responder “a ferramenta faz isso” não basta: mostre contrato e evidência.

## 12. Avaliação por pares

O avaliador começa pelas instruções sem ajuda do autor. Registre tempo e pontos de
ambiguidade, mas não penalize estilo pessoal fora da rubrica. Depois:

1. verifique versão e hash do artefato;
2. execute testes e smoke test;
3. conclua jornada e falha selecionada;
4. inspecione evidência de migração, acessibilidade e desempenho;
5. escolha amostras de requisitos e rastreie até testes;
6. pontue cada dimensão com observação factual;
7. marque bloqueadores separadamente;
8. ofereça uma força, um risco e uma próxima ação concreta.

Conflito de opinião deve voltar ao critério observável. Se a rubrica for ambígua,
registre a ambiguidade para melhorar o curso.

## 13. Diagnóstico de projetos que travaram

- **muitas telas, nada concluído:** reduza para uma jornada vertical;
- **UI difícil de testar:** extraia regra e estado para funções/casos de uso;
- **migração perigosa:** pare funcionalidades e crie fixtures/backups primeiro;
- **testes frágeis:** teste comportamento/contrato, não detalhe incidental;
- **pacote só funciona localmente:** inventarie arquivos e construa em diretório
  limpo;
- **profiling sem causa:** volte à jornada, baseline e maior contribuinte;
- **documentação no fim:** gere evidência em cada gate;
- **plugin domina o projeto:** reduza a API a um caso de variação ou remova-o;
- **release sem volta:** não publique até ensaiar restauração.

## Exercícios em três níveis

### Nível 1 — Especificação avaliável

Produza brief, jornadas, invariantes, não objetivos, riscos, arquitetura e plano de
gates para uma das modalidades. Avalie-o como se você não fosse o autor.

**Aceite:** escopo cabe em cinco incrementos; cada requisito possui critério e
evidência planejada; dados e falhas estão modelados; não antecipa SO ou redes.

### Nível 2 — Candidato completo

Implemente até o Gate 4. Convide uma pessoa para executar jornada sem orientação,
registre problemas e faça uma revisão. Execute matriz de testes, acessibilidade e
profiling.

**Aceite:** todos os requisitos essenciais possuem evidência; testes são verdes;
o estado sobrevive/rejeita falhas corretamente; orçamento tem método reproduzível;
feedback da pessoa gerou ao menos uma melhoria verificável.

### Nível 3 — Release e banca

Produza o artefato final, dossiê de release e runbook. Outro avaliador executa o
smoke test e uma recuperação, aplica a rubrica e conduz a defesa técnica.

**Aceite:** bytes avaliados correspondem ao manifesto; execução não depende do
workspace; recuperação funciona; nenhum bloqueador permanece; pontuação é pelo
menos 75; divergências de avaliação têm decisão documentada.

## Checklist final do módulo 03

- [ ] O problema, público, jornada e não objetivos cabem em uma página.
- [ ] Invariantes de domínio estão separadas da interface.
- [ ] Estado, configuração, dados e erros têm contratos explícitos.
- [ ] Importação e migração preservam o estado anterior ao falhar.
- [ ] A jornada principal funciona por teclado e com reflow.
- [ ] Diagnóstico não expõe segredo nem conteúdo pessoal.
- [ ] O orçamento mede uma jornada real com dados reproduzíveis.
- [ ] O perfil sustenta a otimização escolhida.
- [ ] O artefato final roda fora do workspace.
- [ ] Versão, manifesto, SBOM e proveniência referem-se à mesma entrega.
- [ ] Atualização, rollback/forward fix e remoção estão documentados.
- [ ] O runbook foi executado por outra pessoa.
- [ ] A rubrica foi aplicada com evidências e sem bloqueadores.
- [ ] Sei defender a maior limitação do projeto e o próximo passo.

Concluir o módulo significa ser capaz de entregar uma aplicação pequena, mas
inteira: compreensível para quem usa, verificável para quem mantém e recuperável
quando a realidade contradiz o caminho feliz.
