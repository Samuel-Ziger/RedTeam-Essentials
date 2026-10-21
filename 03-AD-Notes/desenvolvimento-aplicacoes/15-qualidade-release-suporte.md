# 15 — Qualidade, release, proveniência e suporte

Release é uma mudança entregue a pessoas. Ela combina decisão de produto,
artefato identificável, evidência de qualidade, comunicação, observação e plano
de recuperação. Um pacote compilado pode ser um candidato; só se torna uma
release quando está associado a versão, escopo, origem, compatibilidade e suporte.

Qualidade também não é uma etapa final executada pelo time de testes. É a soma de
propriedades verificadas ao longo do trabalho: a regra está correta, a interface é
utilizável, os dados sobrevivem, o pacote é íntegro e a equipe consegue responder
a falhas sem coletar informação excessiva.

## Objetivos de aprendizagem

Ao concluir, você deverá conseguir:

- construir uma Definition of Done baseada em risco e evidência;
- distinguir versão de app, API, plugin, dados e artefato;
- planejar branch/tag, build, aprovação e promoção de release;
- explicar o papel de checksum, assinatura, SBOM e proveniência;
- escrever release notes voltadas ao usuário e um runbook executável;
- definir rollout, critérios de interrupção, rollback e forward fix;
- triar relatos por impacto, urgência, frequência e reprodutibilidade;
- operar um ciclo de suporte que transforma defeitos em prevenção.

## Pré-requisitos

Revise testes, documentação e colaboração no módulo 02. Neste módulo, conecte os
capítulos 04 (migração), 08 (acessibilidade), 11 (diagnóstico), 13 (artefatos e
rollback) e 14 (orçamentos). O exemplo será uma release local do Study Desk; não
é necessário administrar servidores ou redes.

## 1. Qualidade por propriedade e evidência

“Está funcionando” precisa ser decomposto. Para cada propriedade, defina evidência
e responsável:

| Propriedade | Evidência mínima |
|---|---|
| correção de domínio | testes de regras, bordas e invariantes |
| integridade de dados | fixtures antigas, migração e restauração |
| usabilidade | jornada observada sem instrução do autor |
| acessibilidade | teclado, foco, zoom e tecnologia assistiva suportada |
| compatibilidade | matriz de versões executada |
| desempenho | orçamento e relatório de baseline |
| privacidade | inventário de dados, minimização e revisão de logs |
| distribuibilidade | smoke test do artefato em ambiente limpo |
| suportabilidade | runbook e pacote de diagnóstico sanitizado |

Cobertura de linhas é um sinal, não uma propriedade do produto. Cem por cento de
cobertura pode não testar migração interrompida ou foco após um erro. Associe
testes a riscos e critérios de aceite.

## 2. Definition of Done e gates

Uma Definition of Done útil é verificável:

- critérios funcionais e estados de erro atendidos;
- testes unitários, integração e jornada principal aprovados;
- acessibilidade manual e automatizada dentro do escopo declarado;
- schemas e contratos compatíveis ou migração documentada;
- configuração, logs, diagnóstico e dados revisados;
- orçamento de desempenho sem regressão material;
- artefato construído e testado fora do workspace;
- dependências, licenças, SBOM e proveniência atualizadas;
- release notes, matriz de suporte e problemas conhecidos prontos;
- backup, rollback/forward fix e runbook exercitados;
- dono do suporte e prazo de manutenção definidos.

Nem toda mudança exige a mesma profundidade. Uma correção de texto não precisa de
teste de migração, mas continua exigindo revisão da interface. Use gates
condicionais baseados no risco; registre por que um gate não se aplica. “Não deu
tempo” não equivale a “não se aplica”.

Gates automáticos bloqueiam fatos objetivos: teste falhou, arquivo ausente, hash
divergiu. Decisões como aceitar um problema conhecido importante exigem aprovação
humana registrada.

## 3. Dimensões de versão

Uma release pode carregar várias versões:

- **aplicação:** conjunto de funcionalidades percebido pelo usuário;
- **API pública/CLI:** contrato consumido por integração;
- **API de plugins:** contrato do capítulo 12;
- **schema de dados/exportação:** forma persistida e regras de migração;
- **artefato/build:** reconstrução específica do mesmo código para um alvo.

Semantic Versioning é adequado quando existe API pública e compromisso claro:
major para incompatibilidade, minor para adição compatível e patch para correção
compatível. Isso não substitui a matriz real. Aplicativos também precisam declarar
quais schemas leem/escrevem e de quais versões atualizam diretamente.

Não determine compatibilidade apenas comparando strings. `1.10.0` e `1.9.0`
exigem parser de versão; `beta` ou metadado de build possuem semântica própria.
Use biblioteca madura do ecossistema e casos de teste, em vez de criar um parser
improvisado.

## 4. Fluxo de release e promoção

Um fluxo pequeno e auditável:

```text
escopo congelado -> revisão de risco -> código identificado -> CI verde
-> artefato candidato -> inventário/SBOM/proveniência -> smoke test
-> aprovação -> tag/release notes -> promoção do mesmo artefato -> suporte
```

A tag deve identificar o código que originou o artefato. O número da versão deve
ser derivado de uma fonte única ou verificado contra manifesto e interface. O
pipeline de publicação não deve recompilar. Se uma correção for necessária, gere
novo candidato e nova evidência; não substitua silenciosamente bytes sob a mesma
versão.

Mantenha separação de funções proporcional ao projeto. Quem escreve pode preparar
a release, mas uma revisão independente do diff, dependências e evidências reduz
pontos cegos. Credenciais de publicação não pertencem a jobs comuns nem ao
repositório.

## 5. SBOM, proveniência, hashes e assinatura

Esses termos respondem a perguntas diferentes:

| Evidência | Pergunta principal |
|---|---|
| hash/checksum | estes bytes correspondem ao valor esperado? |
| assinatura | uma identidade com esta chave aprovou estes bytes/metadados? |
| SBOM | quais componentes e versões compõem o artefato? |
| proveniência | quais materiais e processo afirmam ter produzido o artefato? |
| relatório de testes | quais comportamentos foram verificados? |

Uma SBOM em formato interoperável, como SPDX ou CycloneDX, deve incluir
identificadores suficientes para relacionar componentes ao artefato. Ela não é um
scanner de vulnerabilidade nem substitui revisão de licença. Gere-a a partir da
resolução efetiva e trate-a como artefato versionado da release.

Proveniência descreve, conforme o nível adotado, fonte, materiais, plataforma de
build e identidade do processo. Evite afirmações maiores que a evidência: se o
build aceita entrada manual não registrada, declare essa limitação.

Publique hashes e assinaturas por canal cuja autenticidade faça parte da política.
Um hash obtido no mesmo local comprometido que o pacote não fornece verificação
independente. Proteja ou use identidades efêmeras para assinatura conforme o
ecossistema. Não confunda pacote assinado com pacote seguro; assinatura ajuda a
responder “de onde veio e mudou?”, não “não contém defeito?”.

## 6. Dependências, licença e vulnerabilidades

Antes da release:

1. compare lockfile com a mudança aprovada;
2. identifique dependências novas, removidas e transitivas;
3. confirme origem, licença e política de uso;
4. execute análise disponível e interprete alcance real;
5. atualize avisos e SBOM;
6. registre exceções com dono, justificativa e data de revisão.

Um alerta em componente não significa automaticamente que o produto é afetado;
uma ausência de alerta também não prova segurança. Verifique versão, caminho de
código, configuração e exposição. Nunca esconda alerta apenas para deixar o gate
verde. Corrija, mitigue ou aceite formalmente o risco dentro do modelo do curso.

## 7. Rollout e critério de abortar

Mesmo uma aplicação local pode usar canais `beta` e `stable`. Distribua primeiro
para um grupo que consentiu em testar, observe métricas de falha e depois promova
o mesmo artefato. Defina antes:

- tamanho e duração de cada etapa;
- sinais de saúde: início, erro de migração, perda de dados, travamento;
- limite que pausa ou interrompe a promoção;
- pessoa responsável pela decisão;
- procedimento de rollback ou forward fix;
- comunicação para quem já atualizou.

Feature flags podem separar implantação de ativação. Toda flag precisa de dono,
valor padrão seguro, data de remoção e testes dos estados ainda suportados. Não use
flag para contornar autorização ou sustentar duas arquiteturas para sempre.

Rollback do aplicativo só é seguro quando a versão anterior lê o estado atual.
Caso contrário, recupere backup ou entregue forward fix. O runbook deve dizer qual
opção se aplica; improvisar sob pressão aumenta dano.

## 8. Release notes que ajudam quem usa

Release notes não são uma lista de commits internos. Organize:

```markdown
## Study Desk 1.2.0 — 2026-10-05

### Adicionado
- edição de uma sessão com cancelamento sem perda.

### Alterado
- exportações passam a registrar `schemaVersion: 2`.

### Para atualizar
- faça uma exportação de segurança; a primeira abertura migra dados v1.

### Corrigido
- foco retorna ao título após erro de duração.

### Problemas conhecidos
- catálogos acima do limite documentado podem levar mais tempo para filtrar.

### Como voltar
- restaure a exportação v1 criada antes da migração; veja o runbook.
```

Explique impacto e ação. Evite títulos como “refatora reducer” quando a pessoa
precisa saber que a exclusão agora pode ser desfeita. Vincule notas detalhadas de
migração e suporte, mas mantenha a decisão essencial na própria release.

## 9. Suporte como sistema de aprendizagem

Um formulário mínimo pede:

- versão exata e canal;
- plataforma/runtime no nível necessário;
- passos para reproduzir com dados sintéticos, quando possível;
- resultado esperado e observado;
- código de correlação/razão mostrado pela aplicação;
- se começou após instalação, atualização, importação ou mudança específica;
- diagnóstico sanitizado após prévia e consentimento.

Não solicite banco completo, token, documento pessoal ou screenshot indiscriminado.
Primeiro reproduza com fixture sintética. Se conteúdo for indispensável, minimize,
explique propósito, retenção e método autorizado.

Separe **severidade** (impacto) de **prioridade** (ordem de trabalho). Perda de
dados para uma pessoa pode ter severidade crítica mesmo com baixa frequência.
Uma falha cosmética frequente pode ter alta prioridade de produto, mas não a mesma
severidade. Uma matriz simples:

| Severidade | Exemplo | Resposta inicial |
|---|---|---|
| S1 crítica | perda/corrupção ou app indisponível sem recuperação | interromper rollout, preservar evidência, comunicar |
| S2 alta | jornada principal falha com contorno difícil | triar imediatamente e planejar correção |
| S3 média | função secundária falha com contorno | registrar e priorizar |
| S4 baixa | detalhe visual/documental | backlog com contexto |

Defina tempos de resposta compatíveis com capacidade real; não prometa SLA que o
projeto não sustenta.

## 10. Triagem, incidente e prevenção

Fluxo de triagem:

1. reconheça o relato e preserve o ID;
2. confirme versão, impacto e risco aos dados;
3. indique ação segura imediata, como pausar atualização;
4. reproduza em fixture e ambiente declarados;
5. classifique severidade/prioridade e designe dono;
6. corrija ou mitigue com revisão e testes;
7. confirme com o cenário original sem expor conteúdo;
8. transforme o caso em teste, regra de lint, documentação ou gate;
9. comunique solução e feche retenção dos dados recebidos.

Em incidente, mantenha uma linha do tempo factual: observado, decidido, executado
e verificado. Preserve logs minimizados e hashes dos artefatos relevantes. Uma
retrospectiva sem culpabilização pergunta quais condições permitiram o defeito e
qual barreira concreta será adicionada.

## 11. Ciclo de suporte e fim de vida

Declare:

- versões/canais suportados;
- prazo de correções e atualizações;
- quantas versões anteriores migram diretamente;
- como exportar dados antes do fim de suporte;
- data e comunicação de depreciação;
- destino de documentação e artefatos antigos.

Fim de suporte não deve prender dados. Para o Study Desk, preserve formato de
exportação documentado e instrução de leitura. Um plugin de API antiga recebe
aviso e caminho de migração antes da remoção planejada.

## 12. Exemplo: release 1.2 do Study Desk

Imagine que a versão inclua edição e schema 2. O plano contém:

1. fixtures v1 válidas, vazias, no limite e corrompidas;
2. migração transacional v1→v2 e backup exportável;
3. testes de reducer para confirmar/cancelar edição;
4. teste manual de teclado, foco, zoom e anúncio;
5. orçamento com 10.000 sessões;
6. pacote estático limpo, manifesto, hash, SBOM e proveniência;
7. smoke test do artefato, não do workspace;
8. canal beta com critério de abortar se houver falha de migração;
9. release notes, compatibilidade e runbook de restauração;
10. suporte pronto para reconhecer `migration_failed` sem coletar sessões.

Isso liga produto, engenharia e operação em uma evidência coerente.

## Exercícios em três níveis

### Nível 1 — Dossiê de release

Crie Definition of Done, matriz de versão e release notes para uma mudança do
Study Desk. Inclua riscos, gates aplicáveis e problemas conhecidos.

**Aceite:** todo item da Definition of Done aponta para evidência; versões de app
e schema não se confundem; notas explicam impacto e ação em linguagem de usuário.

### Nível 2 — Artefatos de confiança e suporte

Gere, em laboratório, manifesto de release, hash, SBOM, declaração simples de
proveniência e runbook. Simule três tickets incompletos e faça triagem sem pedir
conteúdo pessoal.

**Aceite:** evidências referem-se aos mesmos bytes; componentes resolvidos aparecem
na SBOM; a proveniência não afirma além do processo real; cada ticket recebe
severidade, informação mínima faltante e próximo passo seguro.

### Nível 3 — Ensaio de rollout e recuperação

Conduza uma release candidata com canal beta, injete falha de migração sintética,
execute o critério de abortar e restaure o estado. Produza linha do tempo e
retrospectiva.

**Aceite:** decisão ocorre pelo limiar predefinido; artefato problemático não é
substituído sob a mesma versão; restauração é demonstrada; comunicação informa
impacto e ação; prevenção termina em teste ou gate verificável.

## Checklist de conclusão

- [ ] Cada propriedade de qualidade possui evidência identificável.
- [ ] Gates automáticos e decisões humanas estão separados.
- [ ] Versões de app, API, plugins, schema e build estão claras.
- [ ] O mesmo artefato testado é promovido para publicação.
- [ ] SBOM, proveniência, hash e assinatura têm papéis distintos.
- [ ] Dependências e licenças foram revisadas a partir da resolução real.
- [ ] Release notes explicam impacto, atualização e recuperação.
- [ ] Critério de abortar existe antes do rollout.
- [ ] Rollback considera compatibilidade dos dados.
- [ ] Suporte coleta somente o necessário e oferece prévia.
- [ ] Severidade não é confundida com prioridade.
- [ ] Todo defeito relevante produz uma barreira preventiva.
- [ ] Fim de suporte preserva uma saída para os dados do usuário.

Uma boa release não é aquela que nunca falha. É aquela cuja qualidade pode ser
explicada, cuja origem pode ser verificada e cuja falha pode ser contida, entendida
e convertida em melhoria.
