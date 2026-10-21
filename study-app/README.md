# Aplicacao local de estudos

Esta interface transforma todo o material didatico do RedTeam Essentials em uma
experiencia visual navegavel. A jornada principal apresenta os modulos `00` a `40`
diretamente, em uma unica sequencia. Tambem permite continuar do ultimo conteudo,
marcar leituras concluidas e descobrir quais laboratorios ja foram desbloqueados pelos
pre-requisitos estudados.

Ha duas formas complementares de navegar:

- **Formacao:** os 41 modulos atuais, em sequencia progressiva;
- **Biblioteca completa:** formacao, laboratorios e projetos,
  ferramentas e codigo, alem da documentacao global do repositorio.

As sete areas tematicas continuam disponiveis como filtros e visoes secundarias. A
barra lateral, o painel e a navegacao anterior/proximo seguem a ordem curricular
`00` -> `40`; ao trocar de modulo, a leitura continua sem interromper a jornada.

A Biblioteca inclui os materiais de Recon, OSINT, Active Directory, DFIR, Web AppSec,
Cloud, C2/evasion, containers, ferramentas Python/Java, Initial Access,
Post-Exploitation e os demais conteudos da especializacao avancada. Codigo, configuracoes, datasets e
imagens possuem visualizacao propria e nunca sao executados pela interface.

A fonte oficial continua sendo o proprio repositorio: a aplicacao nao mantem uma copia
manual do curriculo. Antes de iniciar, um gerador le `MODULE-CATALOG.json`,
`STUDY-CONTENT.json`, os Markdown e os recursos seguros dos modulos e produz um catalogo
estatico para o navegador. Exclusoes de infraestrutura interna sao deliberadas e
documentadas no manifesto; arquivos didaticos elegiveis nao podem ficar sem colecao.

Os modulos `27` a `40` usam `contentPaths` no manifesto para adotar materiais ja
existentes em sua nova ordem curricular. O arquivo permanece no caminho original, mas
aparece no novo modulo com o mesmo identificador estavel; assim links, progresso salvo e
automacoes continuam validos sem manter copias divergentes.

## Inicio rapido

Na raiz do repositorio, execute:

```bash
bash estudo.sh
```

Na primeira execucao, o launcher instala as dependencias travadas pelo `package-lock.json`
com scripts de instalacao desativados. Nas seguintes, ele verifica se a instalacao ainda
esta consistente, gera o catalogo, inicia o Vite somente em `127.0.0.1` e tenta abrir
Chrome ou Chromium. O terminal precisa permanecer aberto enquanto a aplicacao estiver em
uso. Pressione `Ctrl+C` para encerrar o servidor.

Pre-requisitos:

- Python 3;
- Node.js 22.12+ em uma linha LTS par ainda suportada;
- npm;
- Bash;
- Chrome, Chromium ou outro navegador que possa ser aberto por `xdg-open`.

Veja todas as opcoes sem iniciar o servidor:

```bash
bash estudo.sh --help
```

Exemplos:

```bash
# Verifica ambiente e arquivos; nao instala nem inicia nada
bash estudo.sh --check

# Inicia sem abrir o navegador
bash estudo.sh --no-open

# Usa outra porta de loopback
bash estudo.sh --port 4173

# Alternativa por variavel de ambiente
ESTUDO_PORT=4173 bash estudo.sh
```

O endereco padrao e <http://127.0.0.1:5173/>. O launcher nunca faz bind em `0.0.0.0`:
esta e uma aplicacao individual, nao um servico para exposicao na rede.

## Como o progresso funciona

Nao existe conta, backend ou telemetria. Leituras, ultimo ponto visitado e demais estados
da interface ficam no armazenamento local do navegador. Isso tem algumas consequencias:

- perfis diferentes do navegador possuem progressos independentes;
- limpar os dados do site apaga o progresso local;
- outro computador nao recebe sincronizacao automatica;
- uma janela privada normalmente descarta o progresso ao ser fechada.

O percentual geral usa apenas documentos marcados como obrigatorios na Formacao.
Referencias, respostas, solucoes e eventuais materiais fora da rota podem ser lidos e
pesquisados, mas nao alteram artificialmente a conclusao do curso. Em laboratorios,
"marcar como lido" registra somente a leitura do enunciado. A conclusao curricular exige
o checkpoint separado "Concluir laboratorio", usado apenas depois da execucao e revisao
da evidencia. Portanto, ler a instrucao nao conclui o lab nem libera um modulo dependente.
O desbloqueio de laboratorios e uma orientacao pedagogica calculada a partir dos
pre-requisitos do catalogo. Ele nao concede privilegios no sistema nem executa comandos
de laboratorio automaticamente.

## Metadados curriculares explicitos

O gerador continua inferindo ordem, obrigatoriedade e pre-requisitos para cursos que nao
precisam de curadoria manual. Quando a rota pedagogica nao coincide com a ordem fisica
dos arquivos, uma entrada de `courses` em `STUDY-CONTENT.json` pode declarar
`documentOverrides`. Cada override identifica o Markdown pelo `sourcePath` e aceita:

- `order`: posicao inteira, unica e nao negativa dentro da rota do modulo;
- `required`: se o documento faz parte da conclusao curricular;
- `prerequisitePaths`: caminhos exatos que precisam estar concluidos para liberar o item.

Os caminhos, e nao titulos ou indices ocasionais, sao a fonte desses metadados. O ID
publico continua sendo derivado do mesmo `sourcePath`; adicionar ou ajustar um override
nao invalida progresso salvo. Os cinco labs do modulo 00 usam pre-requisitos explicitos,
e o README do TaskBoard e obrigatorio por esse mecanismo. Outros modulos continuam no
fallback inferido ate que precisem de uma rota igualmente especifica.

## Fluxo dos dados

```text
MODULE-CATALOG.json + STUDY-CONTENT.json + fontes seguras
                           |
                           v
                scripts/build_catalog.py
                           |
                           v
          public/generated/catalog.json + content/
                           |
                           v
       React + leitor Markdown/recursos somente para leitura
                           |
                           v
                progresso no navegador local
```

`public/generated/` e um artefato descartavel e ignorado pelo Git. Sempre altere o
Markdown original; na proxima inicializacao o catalogo sera reconstruido.

## Desenvolvimento

Para trabalhar na interface sem o launcher:

```bash
# A partir da raiz do repositorio
python3 study-app/scripts/build_catalog.py

cd study-app
npm ci --ignore-scripts
npm run dev -- --host 127.0.0.1
```

Validacoes disponiveis:

```bash
# Na raiz do repositorio
python3 scripts/validate_study_app.py
python3 -m unittest discover -s study-app/scripts/tests -p 'test_*.py' -v

# Dentro de study-app
npm test
npm run build
```

O gerador tambem aceita caminhos explicitos, o que permite testes isolados:

```bash
python3 study-app/scripts/build_catalog.py \
  --repo-root /caminho/para/RedTeam-Essentials \
  --output /tmp/redteam-study-catalog
```

## Estrutura

```text
study-app/
|-- index.html                 entrada do Vite
|-- package.json               comandos e dependencias diretas
|-- package-lock.json          resolucao reproduzivel das dependencias
|-- public/generated/          catalogo descartavel, nao versionado
|-- scripts/build_catalog.py   compilador Markdown -> catalogo local
|-- scripts/tests/             testes do gerador
|-- src/                       componentes, estilos e regras de progresso
`-- vite.config.js             servidor restrito ao loopback
```

## Seguranca e privacidade

- O conteudo Markdown e renderizado como documento, sem executar HTML arbitrario.
- Codigo, scripts, configuracoes e dados sao exibidos como texto; a aplicacao nao os executa.
- O servidor de desenvolvimento fica restrito a `127.0.0.1`.
- Nenhuma credencial e necessaria ou deve ser adicionada ao projeto.
- `node_modules`, o bundle `dist` e o catalogo gerado nao sao versionados.
- Links externos so recebem trafego quando o estudante decide abri-los.
- A instalacao inicial com `npm ci --ignore-scripts` precisa acessar o registro npm;
  estudar o conteudo depois da instalacao e da geracao ocorre localmente.

Esta interface apresenta material educacional do repositorio. Os limites de escopo,
autorizacao e laboratorio descritos em cada modulo continuam valendo integralmente.

## Solucao de problemas

**A porta esta ocupada:** escolha outra com `bash estudo.sh --port 4173`. O modo
`--strictPort` impede que o Vite troque silenciosamente para uma porta inesperada.

**O navegador nao abriu:** copie o endereco mostrado no terminal. O servidor pode ser
usado normalmente com `--no-open`.

**O catalogo parece antigo:** encerre e execute `bash estudo.sh` outra vez. O gerador roda
antes de cada inicializacao.

**`node_modules` esta incompleto:** execute `bash estudo.sh` outra vez. O launcher valida
as dependencias e usa `npm ci --ignore-scripts` quando a instalacao esta ausente ou
inconsistente.

**A verificacao falhou:** execute `python3 scripts/validate_study_app.py` na raiz. Cada
mensagem `[FAIL]` aponta o arquivo ou o contrato que precisa ser corrigido.

Volte ao [README principal](../README.md) para consultar a organizacao completa das
trilhas e modulos.
