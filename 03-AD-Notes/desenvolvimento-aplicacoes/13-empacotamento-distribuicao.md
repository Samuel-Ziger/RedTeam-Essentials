# 13 — Empacotamento, distribuição, atualização e rollback

Código-fonte que funciona no workspace ainda não é um produto distribuível. O
usuário recebe um artefato, instala ou abre esse artefato, conserva dados entre
versões e precisa recuperar-se quando algo dá errado. Empacotamento é a disciplina
que transforma entradas declaradas em uma unidade identificável; distribuição é
como essa unidade chega ao público; atualização é uma migração entre estados; e
rollback é uma estratégia de recuperação, não um botão mágico.

## Objetivos de aprendizagem

Ao concluir, você deverá conseguir:

- escolher um formato de entrega coerente com público e tipo de aplicação;
- declarar entradas, dependências, metadados e matriz de compatibilidade;
- diferenciar build limpo, determinístico, reproduzível e verificável;
- testar o artefato final fora do workspace de desenvolvimento;
- desenhar instalação, atualização, migração, rollback e remoção como estados;
- separar binários, configuração, cache e dados pertencentes ao usuário;
- diagnosticar falhas de distribuição sem pedir dados sensíveis;
- preparar o Study Desk para uma entrega estática ou instalável controlada.

## Pré-requisitos

Você precisa dominar configuração e segredos (capítulo 02), persistência e schema
(capítulo 04), clientes resilientes (capítulo 09) e diagnóstico (capítulo 11).
O capítulo anterior introduziu versões de contratos. Aqui elas entram na entrega.
Não é necessário conhecimento de administração de Sistemas Operacionais.

## 1. Comece pelo contrato de entrega

Antes de selecionar uma ferramenta, responda:

- quem instala e quem usa?
- a aplicação é biblioteca, CLI, serviço, web estática ou desktop?
- quais plataformas e arquiteturas têm suporte declarado?
- há runtime pré-instalado ou ele acompanha o produto?
- onde ficam código, configuração, cache e dados do usuário?
- como verificar versão, origem e integridade?
- como atualizar, reparar, voltar e remover?
- por quanto tempo cada versão recebe suporte?

Uma biblioteca deve se integrar ao gerenciador do consumidor. Uma CLI pode ser
um pacote dependente de runtime ou executável autocontido. Uma aplicação web
estática pode ser um diretório imutável com HTML, CSS, JavaScript e manifesto. Um
desktop pode exigir instalador e integração à plataforma. Não escolha o formato
apenas porque é familiar ao autor.

## 2. Artefatos nos cinco ecossistemas

| Ecossistema | Biblioteca | Aplicação/CLI | Informação crítica |
|---|---|---|---|
| Python | wheel e sdist | pacote, zipapp ou ferramenta de empacotamento | versão do Python, dependências e entry point |
| Java | JAR modular/comum | JAR executável, `jlink`/`jpackage` | versão da JVM, módulos e classe principal |
| C17 | biblioteca estática/dinâmica | executável e pacote da plataforma | ABI, arquitetura e bibliotecas necessárias |
| .NET | pacote NuGet | framework-dependent ou self-contained | runtime, RID e modo de publicação |
| JavaScript/web | pacote npm | arquivos estáticos ou contêiner desktop | engines, módulos, assets e política de cache |

Os nomes indicam famílias, não garantias universais. Por exemplo, “single-file”
não significa necessariamente um único recurso em memória nem ausência de
dependências da plataforma. Registre o comportamento da versão da ferramenta que
você usa e teste no ambiente suportado.

## 3. Dependências e entradas fechadas

Um build começa por um conjunto de entradas conhecido:

```text
fonte + manifesto + lockfile + compilador/runtime + flags + assets
      + scripts de geração + metadados de versão = artefato candidato
```

Declare dependências diretas e mantenha um lockfile quando o ecossistema oferecer
esse mecanismo. O manifesto expressa faixas ou intenção; o lock registra a
resolução concreta. Atualize locks conscientemente e revise mudanças transitivas.
Não baixe “a versão mais recente” silenciosamente durante uma release.

Arquivos gerados precisam de uma fonte identificável. Se o build depende de data,
ordem de diretório, localidade ou caminho absoluto, o resultado pode variar sem
mudança funcional. Elimine a variação quando possível; quando não for, documente
o campo e exclua-o da comparação de forma explícita.

Quatro termos próximos têm diferenças importantes:

- **build limpo:** não reutiliza resíduos não declarados do workspace;
- **determinístico:** mesmas entradas no mesmo ambiente produzem a mesma saída;
- **reproduzível:** partes independentes conseguem recriar resultado equivalente
  a partir das entradas publicadas;
- **verificável:** o destinatário confirma identidade/integridade conforme uma
  política, mesmo quando não recompila.

Um pipeline repetido duas vezes na mesma máquina não prova reprodutibilidade.

## 4. Pipeline de artefato imutável

Separe estágios e promova o mesmo artefato já testado:

```text
checkout identificado
  -> dependências verificadas
  -> build limpo
  -> testes
  -> pacote candidato
  -> inventário + hashes + proveniência
  -> teste de instalação/execução
  -> aprovação
  -> publicação do mesmo conjunto de bytes
```

Não reconstrua para a etapa de publicação: o pacote publicado poderia não ser o
que os testes aprovaram. Armazene versão, identificador do código-fonte, versão
das ferramentas e hashes em um manifesto de release. Não coloque chave privada,
token ou arquivo `.env` no artefato.

Checksum detecta mudança acidental ou divergência em relação ao valor obtido por
um canal confiável. Assinatura relaciona conteúdo e identidade controladora da
chave. Proveniência registra afirmações sobre materiais e processo de build. SBOM
inventaria componentes. Esses controles se complementam; nenhum deles demonstra
sozinho que o programa está livre de defeitos.

## 5. Instalação e primeira execução

Instalar é uma transição que pode falhar no meio. Evite modificar dados do usuário
antes de o produto estar pronto para iniciar. Quando houver substituição de
arquivos, prepare o novo conjunto, valide-o e só então troque a referência ativa
por uma operação tão atômica quanto a plataforma permitir.

Na primeira execução:

1. identifique ausência de configuração sem tratá-la como corrupção;
2. crie apenas estruturas necessárias;
3. use padrões seguros e visíveis;
4. não invente consentimento de telemetria;
5. apresente importação opcional sem sobrescrever dados;
6. registre versão da aplicação e do schema criado.

Mantenha quatro categorias separadas:

| Categoria | Pode ser recriada? | Remoção padrão |
|---|---:|---|
| binário/assets | sim, pelo pacote | remover |
| cache | sim | remover ou oferecer limpeza |
| configuração | geralmente não automaticamente | perguntar/preservar |
| documentos e dados do usuário | não | preservar por padrão |

Desinstalar aplicação não autoriza apagar trabalho. Uma opção “remover todos os
dados” deve citar exatamente o alvo, exigir confirmação clara e, quando possível,
oferecer exportação anterior.

## 6. Atualização como máquina de estados

Não modele o atualizador como `download -> execute`. Use estados observáveis:

```text
ocioso -> consultando -> disponível -> baixando -> verificando
      -> preparando -> migrando -> ativando -> confirmado
                         |             |
                         v             v
                       falhou ------> recuperando
```

O manifesto de atualização precisa ser validado antes de orientar qualquer ação.
Um formato conceitual:

```json
{
  "schemaVersion": 1,
  "channel": "stable",
  "version": "1.4.2",
  "artifact": "study-desk-1.4.2.zip",
  "size": 182431,
  "sha256": "valor-hexadecimal-publicado",
  "minimumDataSchema": 1,
  "maximumDataSchema": 2
}
```

Valide schema, canal, versão, tamanho máximo, formato do hash e compatibilidade.
Baixe para área temporária; imponha limite; verifique comprimento, hash e
assinatura exigida pela política antes de ativar. Um nome recebido no manifesto
não deve escolher livremente um caminho no dispositivo. Detalhes de armazenamento
e permissões pertencem aos módulos de SO; o contrato de aplicação continua sendo
válido independentemente deles.

Canal `stable`, `beta` ou outro deve ser uma escolha explícita. Nunca faça
downgrade automático apenas porque um catálogo remoto anuncia número menor. A
política precisa distinguir versão mais nova, mesma versão, versão revogada e
tentativa de retrocesso.

## 7. Migração e rollback são problemas diferentes

Voltar o executável não significa que uma versão antiga entende dados já
migrados. Antes da atualização, registre a compatibilidade em uma matriz:

| App | Lê schema 1 | Lê schema 2 | Escreve schema |
|---|---:|---:|---:|
| 1.3 | sim | não | 1 |
| 1.4 | sim | sim | 2 |

Uma migração confiável segue `ler -> validar -> transformar em memória/área nova
-> validar resultado -> persistir atomicamente -> confirmar`. Preserve backup
rotulado com versão e tenha teste real de restauração. Se a transformação for
irreversível, o plano de recuperação pode exigir restauração dos dados anteriores,
não apenas rollback do aplicativo.

Três estratégias comuns:

- **migração reversível:** existe transformação de volta, testada;
- **leitura antiga/escrita nova adiada:** a nova versão lê os dois schemas, mas só
  migra após confirmação;
- **forward fix:** mantém o novo schema e entrega correção rápida, com backup para
  casos em que isso não basta.

A escolha depende do risco e deve ser feita antes da falha.

## 8. Study Desk como artefato

Hoje o Study Desk pode ser servido como arquivos estáticos e não exige etapa de
build. Isso já é uma decisão de distribuição. Para criar um artefato:

1. inclua somente `index.html`, `styles.css` e módulos necessários;
2. gere um arquivo `release-manifest.json` com versão e hashes;
3. execute testes antes de montar o pacote;
4. extraia em diretório vazio e sirva essa cópia;
5. conclua cadastro, busca, exportação e importação pelo teclado;
6. confirme que nenhum arquivo do workspace foi necessário;
7. teste exportação v1 antes e depois de uma evolução de schema.

Se escolher PWA ou desktop, escreva um ADR comparando instalação, atualização,
funcionamento offline, acessibilidade, tamanho e capacidade de remoção. “Parece
mais profissional” não é critério suficiente. A versão web estática pode continuar
sendo a melhor forma para um produto local simples.

## 9. Teste daquilo que será entregue

Monte uma matriz enxuta, baseada em suporte declarado:

- plataforma e versão do runtime;
- instalação nova e atualização da versão anterior suportada;
- dados vazios, válidos, antigos, no limite e corrompidos;
- execução sem acesso ao workspace;
- caminho com espaços e caracteres suportados;
- remoção preservando dados;
- restauração após migração interrompida;
- tentativa de pacote truncado ou manifesto incompatível.

Teste o pacote, não apenas a árvore fonte. Um smoke test pode conferir versão,
abrir a jornada principal, gravar um registro sintético, reabrir e exportar. O
ambiente de teste deve começar limpo e o script deve falhar claramente se usar
dependência não declarada.

## 10. Diagnóstico de distribuição

Quando “não instala” ou “não abre”, obtenha um relato mínimo e sanitizado:

1. versão exata e origem do artefato;
2. plataforma dentro da granularidade necessária;
3. hash observado e hash esperado;
4. etapa da máquina de estados que falhou;
5. código de razão, não dump integral;
6. presença de dados anteriores e versão de schema;
7. resultado de repetição em ambiente limpo.

Interprete sintomas:

- funciona no workspace, falha no pacote: entrada ou asset não declarado;
- hash diverge: transferência incompleta, artefato diferente ou publicação
  inconsistente; não prossiga;
- abre após instalação nova, falha ao atualizar: compatibilidade/migração;
- rollback abre mas rejeita dados: schema avançou além da versão antiga;
- somente uma plataforma falha: reveja matriz e artefato específico, sem assumir
  que a lógica de domínio é culpada;
- remoção apaga sessões: classificação incorreta entre app e dados do usuário.

## Trade-offs que precisam ser registrados

- artefato autocontido facilita início, mas aumenta tamanho e responsabilidade de
  atualização do runtime;
- artefato dependente do runtime é menor, mas exige pré-requisito compatível;
- atualização automática reduz defasagem, porém aumenta a exigência de confiança,
  recuperação e comunicação;
- muitos canais aceleram feedback, mas multiplicam combinações de suporte;
- build totalmente reproduzível custa engenharia; ainda assim, entradas fixas,
  manifesto e teste do artefato já elevam muito a confiabilidade;
- migração imediata simplifica o estado estável, mas pode tornar rollback difícil.

## Exercícios em três níveis

### Nível 1 — Contrato e inventário

Escolha artefatos para uma biblioteca, uma CLI e o Study Desk. Faça inventário de
entradas, fontes de variação, runtimes, dados criados e matriz de suporte.

**Aceite:** cada formato deriva do público; fonte e dependências estão fixadas;
configuração/cache/dados estão separados; há instruções de versão e remoção.

### Nível 2 — Pacote verificável do Study Desk

Crie, em uma branch de laboratório, um script de pacote que copie apenas arquivos
necessários e gere manifesto com versão, tamanho e hashes. Teste a cópia em
diretório limpo e produza relatório do smoke test.

**Aceite:** duas execuções com mesmas entradas têm diferenças explicadas ou zero;
nenhum segredo entra no pacote; arquivo ausente faz o teste falhar; o artefato
testado é exatamente o candidato à publicação.

### Nível 3 — Atualização com falha recuperável

Projete uma evolução do schema 1 para 2, com fixture antiga, validação
transacional, backup e plano de rollback. Simule interrupção antes e depois da
ativação e escreva um runbook para suporte.

**Aceite:** nenhuma falha deixa mistura de schemas; backup é restaurado por teste;
rollback do app é distinguido de rollback dos dados; manifesto incompatível ou
truncado nunca é ativado; os eventos de diagnóstico não incluem sessões.

## Checklist de conclusão

- [ ] O formato de artefato deriva do público e do modo de uso.
- [ ] Todas as entradas e ferramentas relevantes do build estão registradas.
- [ ] Dependências são resolvidas de forma controlada.
- [ ] O pipeline promove o mesmo artefato que foi testado.
- [ ] Hash, assinatura, proveniência e SBOM não são tratados como sinônimos.
- [ ] O artefato funciona fora do workspace.
- [ ] Dados, configuração, cache e código têm ciclos de vida distintos.
- [ ] A atualização possui estados, limites, validação e recuperação.
- [ ] Migração de dados é transacional e coberta por fixtures.
- [ ] Rollback de binário e de dados foram avaliados separadamente.
- [ ] Remoção preserva dados do usuário por padrão.
- [ ] A matriz de suporte e o fim de suporte são explícitos.

Uma entrega profissional é aquela que pode ser identificada, instalada, verificada,
atualizada, diagnosticada e removida sem depender da memória de quem a construiu.
