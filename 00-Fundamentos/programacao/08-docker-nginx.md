# Docker e Nginx: construir, conectar, observar e operar

Docker torna o ambiente da aplicação declarativo; Nginx pode servir arquivos
estáticos e encaminhar requisições para a API. Isso não elimina operação: você
ainda precisa entender processos, portas, redes, dados, sinais, logs e falhas.

Este capítulo usa o [TaskBoard](projetos/taskboard/README.md) como laboratório
real. Todos os serviços ficam locais e a única porta publicada é ligada ao
loopback `127.0.0.1`.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- diferenciar imagem, container, camada, volume, bind mount, rede e registry;
- explicar build context, cache de camadas, `Dockerfile` e `.dockerignore`;
- publicar uma porta apenas no endereço necessário;
- conectar serviços pelo DNS da rede Compose sem publicar a API;
- ler uma configuração Nginx e prever qual `location` atenderá;
- diferenciar health de gateway e health de dependência;
- inspecionar estado, logs, processos, mounts e redes;
- provar persistência e realizar backup/restauração SQLite;
- aplicar hardening básico sem quebrar a execução;
- diagnosticar build, start, DNS, proxy, permissão e aplicação por camada.

## 1. Pré-requisitos e verificação

Você precisa de Docker Engine ou ambiente compatível e do plugin Compose v2.
Os comandos deste material usam `docker compose`, com espaço.

```bash
docker version
docker compose version
docker info
```

O cliente pode estar instalado enquanto o daemon está parado ou inacessível.
Leia separadamente a seção `Client` e `Server` de `docker version`. Evite
resolver permissão executando comandos indiscriminadamente como root; prefira
a instalação rootless ou o grupo/configuração recomendado pela sua plataforma.

Antes do laboratório:

```bash
cd 00-Fundamentos/programacao/projetos/taskboard
docker compose config
```

`config` expande e valida o modelo Compose sem iniciar serviços. Leia o resultado:
serviços, redes, volume, limites, healthchecks e porta publicada.

## 2. O que um container realmente é

Um container é um ou mais processos isolados por mecanismos do sistema
operacional e limitados/configurados pelo runtime. Em Linux, processos de
containers compartilham o kernel do host; por isso container não é uma máquina
virtual completa.

| Conceito | Definição prática | Pergunta útil |
|----------|--------------------|---------------|
| Imagem | conjunto imutável de camadas e metadados | o que será executado? |
| Container | instância/processo criado da imagem | o que está executando agora? |
| Camada gravável | mudanças efêmeras daquele container | pode ser descartada? |
| Volume | armazenamento gerenciado fora da camada do container | o dado deve sobreviver? |
| Bind mount | caminho específico do host montado | esse acoplamento ao host é desejado? |
| Network | domínio de comunicação e descoberta | quem precisa conversar com quem? |
| Registry | armazenamento/distribuição de imagens | de onde veio a imagem? |
| Dockerfile | receita declarativa de build | como reproduzir a imagem? |
| Compose | modelo de serviços relacionados | como executar o conjunto? |

Parar um container preserva sua camada gravável; remover o container a descarta.
Dados importantes não devem depender dela. Imagem também não deve conter
segredos nem dados mutáveis de produção.

## 3. Build context, camadas e cache

Ao executar:

```bash
docker build --tag taskboard-api:local ./api
```

`./api` é o **contexto de build**. O builder só pode usar arquivos enviados
nesse contexto. Contexto desnecessariamente grande deixa build lento e pode
enviar arquivos sensíveis ao builder.

`.dockerignore` exclui itens como:

```text
__pycache__/
*.pyc
.git/
.env
tasks.db
```

Cada instrução relevante produz cache/camada. Se uma entrada muda, aquela etapa
e as seguintes precisam ser reconstruídas. Em projetos com dependências, copie
primeiro o manifesto/lockfile, instale e só depois copie código que muda com
frequência. Nunca reorganize apenas por cache sacrificando correção.

Inspecione sem executar:

```bash
docker image history taskboard-api:local
docker image inspect taskboard-api:local
```

Uma imagem não é “segura porque é pequena”. Tamanho reduz superfície e tempo de
transferência, mas origem, atualização, configuração e privilégios continuam
importando.

## 4. Dockerfile da API, linha por linha

Versão conceitual do arquivo real:

```dockerfile
FROM python:3.14-slim@sha256:DIGEST_FIXADO

ENV APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    APP_DB_PATH=/data/tasks.db

RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app \
    && mkdir -p /app /data \
    && chown -R app:app /app /data

WORKDIR /app
COPY --chown=app:app server.py /app/server.py
RUN python -m py_compile /app/server.py
USER 10001:10001
EXPOSE 8000
STOPSIGNAL SIGTERM
HEALTHCHECK CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=2).read()"]
CMD ["python", "-I", "-u", "-B", "/app/server.py"]
```

- `FROM ...@sha256`: fixa o conteúdo exato da imagem base. A tag continua
  informativa; o digest fornece reprodutibilidade. Atualização exige revisar e
  alterar o digest deliberadamente.
- `ENV`: define defaults da imagem. Compose pode sobrescrevê-los.
- `APP_HOST=0.0.0.0`: necessário para receber conexões vindas da rede do container.
- `RUN`: cria identidade sem login e diretórios com proprietário conhecido.
- `WORKDIR`: define diretório para instruções/comando seguintes.
- `COPY --chown`: inclui apenas o servidor com dono correto.
- `USER`: o processo não roda como root.
- `EXPOSE`: documenta porta esperada; **não publica** no host.
- `py_compile`: falha o build cedo se o arquivo não compilar.
- `HEALTHCHECK`: consulta readiness local da API e do SQLite.
- `STOPSIGNAL`: declara o sinal que inicia o encerramento gracioso.
- `-I`: isola o Python de variáveis `PYTHON*` e caminhos de usuário;
- `-u`: deixa stdout/stderr sem buffer para que os logs cheguem imediatamente;
- `-B`: impede a criação de bytecode `.pyc` em runtime;
- `CMD` em forma JSON: evita shell intermediário e melhora propagação de sinais.

Os comportamentos `-u` e `-B` são flags deliberadas, e não variáveis
`PYTHONUNBUFFERED`/`PYTHONDONTWRITEBYTECODE`: o modo `-I` implica `-E` e ignora
variáveis de ambiente `PYTHON*`. Manter simultaneamente as variáveis e `-I`
daria uma falsa impressão de que elas configuram o processo principal.

`EXPOSE 8000` sozinho não cria acesso. Publicação ocorre por `--publish` ou
`ports` no Compose.

## 5. Dockerfile do Nginx

O gateway remove a configuração padrão, copia a configuração e os arquivos
estáticos, executa `nginx -t` durante o build, remove escrita dos artefatos,
troca para o usuário `nginx` e escuta na porta 8080. O Dockerfile também declara
healthcheck e `STOPSIGNAL SIGQUIT`, usado pelo Nginx para encerramento gracioso.

Portas abaixo de 1024 tradicionalmente exigem privilégio/capability em Linux.
Usar 8080 facilita executar sem root. A publicação externa ainda pode mapear
qualquer porta permitida do host para 8080 do container.

```text
host 127.0.0.1:8099
          |
          | mapeamento de porta
          v
gateway:8080
```

Os arquivos são copiados durante o build. Alterar `app.js` no host não altera
um container existente; reconstrua a imagem:

```bash
docker compose up --build -d
```

Bind mount poderia refletir arquivos em desenvolvimento, mas este projeto
prioriza uma imagem reprodutível próxima do modelo de entrega.

## 6. Compose: serviços, dependências e estado

O TaskBoard declara dois serviços:

```text
gateway
  +-- rede access: porta publicada no loopback
  +-- rede backend: conversa com api

api
  +-- rede backend: sem porta publicada
  +-- volume task-data em /data
```

Trechos essenciais:

```yaml
services:
  api:
    build:
      context: ./api
    init: true
    expose: ["8000"]
    volumes:
      - task-data:/data
    networks:
      - backend

  gateway:
    build:
      context: ./web
    init: true
    ports:
      - "127.0.0.1:${TASKBOARD_PORT:-8099}:8080"
    networks:
      - backend
      - access

networks:
  backend:
    internal: true
  access:
    internal: false

volumes:
  task-data:
    labels:
      app: taskboard
      purpose: sqlite-data
```

O mapeamento de porta segue `IP_DO_HOST:PORTA_DO_HOST:PORTA_DO_CONTAINER`.
O bind explícito em `127.0.0.1` evita exposição acidental em interfaces de rede
do host. `TASKBOARD_PORT` permite trocar a porta no host, mantendo 8099 como
padrão. Ainda assim, qualquer processo local pode tentar acessar o serviço.

`expose` documenta a porta acessível entre redes do Compose; não publica a API.
`init: true` adiciona um init mínimo para sinais e processos filhos.

Na rede `backend`, o DNS do Compose resolve o nome de serviço `api` para o
endereço atual do container. Nunca fixe o IP do container: ele pode mudar ao
recriar.

`depends_on` com `condition: service_healthy` controla a ordem inicial do
gateway. Ele não torna a API permanentemente disponível e não substitui timeout,
tratamento de `502` nem recuperação em runtime.

## 7. Subir e provar a arquitetura

```bash
cd 00-Fundamentos/programacao/projetos/taskboard

docker compose config
docker compose build
docker compose up -d
docker compose ps
```

Espere os healthchecks ficarem saudáveis. Então:

```bash
curl -i http://127.0.0.1:8099/health
curl -i http://127.0.0.1:8099/api/health
curl -i http://127.0.0.1:8099/api/ready
curl -i http://127.0.0.1:8099/api/tasks
```

Resultados esperados:

- `/health`: `204` gerado diretamente pelo Nginx;
- `/api/health`: `200`, liveness da API por meio do proxy;
- `/api/ready`: `200`, API e SQLite prontos;
- `/api/tasks`: `200` e JSON.

Prove quais portas estão publicadas:

```bash
docker compose port gateway 8080
docker compose port api 8000
```

O primeiro deve mostrar `127.0.0.1:8099`. O segundo não deve apresentar uma
porta publicada. Ausência de publicação não significa que a API inexiste; o
gateway a acessa pela rede `backend`.

Observe identidade, processos e mounts:

```bash
docker compose exec api id
docker compose exec gateway id
docker compose top
docker compose exec api ls -ld /app /data /tmp
```

Os processos devem usar identidades sem privilégio. `/data` deve ser gravável
pela API; a raiz do container é read-only no Compose; `/tmp` é `tmpfs` gravável.

## 8. Nginx: estrutura e fluxo

Configuração simplificada do projeto:

```nginx
worker_processes auto;
pid /tmp/nginx.pid;
error_log /dev/stderr notice;

events {
    worker_connections 256;
}

http {
    include /etc/nginx/mime.types;
    access_log /dev/stdout;
    server_tokens off;
    resolver 127.0.0.11 ipv6=off valid=10s;
    client_max_body_size 16k;

    server {
        listen 8080;
        root /usr/share/nginx/html;
        index index.html;

        location = /health {
            access_log off;
            return 204;
        }

        location = /api/health {
            set $api_upstream http://api:8000;
            proxy_pass $api_upstream/health;
        }

        location = /api/ready {
            set $api_upstream http://api:8000;
            proxy_pass $api_upstream/ready;
        }

        location /api/ {
            set $api_upstream http://api:8000;
            proxy_pass $api_upstream;
        }

        location = /taskboard-core.mjs {
            default_type application/javascript;
            try_files $uri =404;
        }

        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
```

### Contextos

- `main`: workers, PID e log de erro;
- `events`: conexões dos workers;
- `http`: MIME types, logs, resolver e limites HTTP;
- `server`: porta e host virtual;
- `location`: tratamento selecionado por URI.

### Seleção de `location`

`location = /health` é correspondência exata e vence apenas para aquele caminho.
`location /api/` é prefixo. `location /` é fallback mais geral.

Exemplos:

| URI | Bloco escolhido | Resultado |
|-----|-----------------|-----------|
| `/health` | `= /health` | Nginx devolve `204` |
| `/api/health` | `= /api/health` | proxy para API `/health` |
| `/api/ready` | `= /api/ready` | proxy para API `/ready` e SQLite |
| `/api/tasks` | `/api/` | URI segue para a API |
| `/taskboard-core.mjs` | `= /taskboard-core.mjs` | módulo ES com MIME JavaScript |
| `/styles.css` | `/` | arquivo estático |
| `/rota-da-interface` | `/` | fallback para `index.html` |

### MIME, módulos ES e `nosniff`

Extensão de arquivo não é o tipo HTTP. O navegador decide como tratar a
resposta pelo `Content-Type`; um arquivo `.mjs` servido como
`application/octet-stream` pode ser recusado como módulo, especialmente quando
`X-Content-Type-Options: nosniff` impede adivinhação do tipo. Nem toda tabela
`mime.types` empacotada por uma imagem declara `.mjs`, por isso o projeto fixa o
tipo no `location` exato.

Prove o contrato pela resposta externa, não apenas pela existência do arquivo:

```bash
curl -sSI http://127.0.0.1:8099/taskboard-core.mjs \
  | grep -iE '^(content-type|x-content-type-options):'
```

Resultado esperado: um `Content-Type` JavaScript e um único `nosniff`. Um teste
estático protege a configuração; o smoke test via gateway protege o comportamento
da imagem realmente construída.

### Por que existe `resolver`

O projeto usa uma variável em `proxy_pass`. O Nginx resolve `api` em runtime pelo
DNS embutido do Docker em `127.0.0.11`. Isso permite que o IP mude após recriar o
container. Fora de Docker, esse endereço e essa estratégia precisam ser adaptados.

### Cabeçalhos encaminhados

O arquivo real envia:

```nginx
proxy_set_header Host $host;
proxy_set_header X-Forwarded-For $remote_addr;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Request-ID $request_id;
```

Esses campos preservam contexto do request original. A aplicação só deve
confiar em cabeçalhos `Forwarded`/`X-Forwarded-*` quando o proxy confiável os
sobrescreve e a topologia está configurada; clientes podem forjar cabeçalhos.
Neste laboratório, o gateway substitui `X-Forwarded-For` e `X-Request-ID` por
valores observados/gerados na borda.

### Timeout e tamanho

O gateway define timeout de cabeçalho/corpo do cliente e de conexão,
envio/leitura do upstream. Também limita corpo a 16 KiB e converte `413`,
`502` e `504` em envelopes JSON estáveis (`502/504` tornam-se `503`).
Um corpo maior pode receber `413` do Nginx antes de chegar à API. Essa defesa em
camadas não remove o limite do backend: a API também pode ser acessada por outra
rota interna no futuro.

Valide configuração antes de recarregar:

```bash
docker compose exec gateway nginx -t
```

No projeto, mudanças de configuração entram na imagem; reconstrua/recrie em vez
de editar manualmente o container.

## 9. Healthcheck, readiness e diagnóstico

Perguntas diferentes:

- **liveness:** o processo continua capaz de executar?
- **readiness:** esta instância deve receber tráfego agora?
- **startup:** a inicialização ainda está dentro do prazo esperado?

O Compose do TaskBoard possui healthcheck para cada serviço. O health do gateway
prova que Nginx responde localmente; não prova que a API ou o banco funcionam.
`/api/health` atravessa o proxy e prova liveness da API; `/api/ready` também
executa uma consulta mínima no SQLite. O healthcheck do container da API usa
readiness; o do gateway permanece independente da API.

Healthcheck deve ser rápido, com timeout, e não depender da internet. Uma consulta
profunda e cara pode derrubar a própria dependência durante sobrecarga.

Inspecione:

```bash
docker compose ps
docker inspect --format '{{json .State.Health}}' "$(docker compose ps -q api)"
docker inspect --format '{{json .State.Health}}' "$(docker compose ps -q gateway)"
```

O JSON inclui as últimas execuções do healthcheck. Não exponha saída que contenha
segredos em outros projetos.

## 10. Logs e inspeção orientada por hipótese

```bash
docker compose logs --tail=100 api gateway
docker compose logs -f api gateway
```

`-f` acompanha até você interromper com `Ctrl+C`; isso não para os containers.
Nginx escreve access log em stdout e error log em stderr. Python usa saída sem
buffer. O runtime coleta ambos.

Teste a rede de dentro do gateway:

```bash
docker compose exec gateway wget -qO- http://api:8000/health
```

Interpretação por camadas:

| Sintoma | Hipótese | Comando inicial |
|---------|----------|-----------------|
| build falha em `FROM` | registry/rede/digest/plataforma | `docker compose build --progress=plain` |
| container sai imediatamente | comando/config/permissão | `docker compose ps -a` e logs |
| `/health` recusa conexão | gateway/porta publicada | `docker compose ps` |
| `/health` funciona, `/api/health` dá `502` | API/DNS/rede | logs + `wget` interno |
| API registra `database is locked` | concorrência/SQLite | logs e carga que reproduz |
| `413` só no gateway | limite Nginx | access/error log e tamanho |
| `permission denied` em `/data` | volume/UID | `id` e `ls -ld /data` |
| frontend antigo após edição | imagem/cache de build/navegador | rebuild e Network do navegador |

Faça uma hipótese antes de executar dez comandos. Guarde a menor saída que
confirma ou refuta a hipótese.

## 11. Persistência: volume não é backup

Crie uma tarefa e liste:

```bash
curl -sS -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Comprovar persistência"}'

curl -sS http://127.0.0.1:8099/api/tasks
```

Recrie os containers preservando o volume:

```bash
docker compose down
docker compose up --build -d
curl -sS http://127.0.0.1:8099/api/tasks
```

O dado sobrevive porque `task-data` existe fora da camada gravável do container.
O comando abaixo mostra o mount resolvido:

```bash
docker inspect --format '{{json .Mounts}}' "$(docker compose ps -q api)"
```

Um volume protege contra recriação do container, não contra exclusão lógica,
corrupção, falha do host ou `down --volumes`. Backup precisa ser uma cópia
independente, verificável e restaurável.

## 12. Backup e restauração SQLite do laboratório

Use somente dados sintéticos. O arquivo de backup pode conter todo o banco;
trate-o como dado sensível em sistemas reais.

### Criar snapshot consistente

Com a aplicação em execução, use a API de backup do SQLite, não uma cópia
cega do arquivo ativo:

```bash
docker compose exec -T api python -c \
  "import sqlite3; source=sqlite3.connect('/data/tasks.db'); target=sqlite3.connect('/tmp/taskboard-backup.db'); source.backup(target); target.close(); source.close()"

docker compose cp api:/tmp/taskboard-backup.db ./taskboard-backup.db
```

Verifique a cópia no host:

```bash
python3 -c \
  "import sqlite3; connection=sqlite3.connect('file:taskboard-backup.db?mode=ro', uri=True); print(connection.execute('PRAGMA quick_check').fetchone()[0]); print(connection.execute('SELECT count(*) FROM tasks').fetchone()[0]); connection.close()"
```

O primeiro valor esperado é `ok`; o segundo é a quantidade de tarefas. Guarde
também hash, data, versão/schema e política de retenção quando o backup importar.

### Restaurar de forma controlada

Confirme que você está no diretório do TaskBoard e que o arquivo existe. A
restauração substitui o estado atual do banco do laboratório.

```bash
test -f ./taskboard-backup.db
docker compose stop api

docker compose run --rm --no-deps \
  --volume "$PWD/taskboard-backup.db:/backup.db:ro" \
  api python -c \
  "import sqlite3; source=sqlite3.connect('file:/backup.db?mode=ro', uri=True); assert source.execute('PRAGMA quick_check').fetchone()[0] == 'ok'; target=sqlite3.connect('/data/tasks.db'); source.backup(target); target.close(); source.close()"

docker compose up -d
curl -sS http://127.0.0.1:8099/api/tasks
```

Parar a API evita escritas concorrentes durante a restauração. O container
temporário reutiliza o volume declarado para `/data` e monta o backup como
somente leitura. Uma restauração não testada é apenas uma esperança de backup.

## 13. Hardening aplicado no projeto

O Compose do TaskBoard inclui:

```yaml
read_only: true
tmpfs:
  - /tmp:rw,noexec,nosuid,nodev,size=16m,mode=1777
cap_drop:
  - ALL
security_opt:
  - no-new-privileges:true
mem_limit: 256m
cpus: 0.50
pids_limit: 64
stop_grace_period: 15s
logging:
  driver: local
  options:
    max-size: 10m
    max-file: "3"
restart: "no"
```

- `read_only`: impede escrita na camada raiz; caminhos necessários recebem volume
  ou `tmpfs`.
- `tmpfs /tmp`: fornece 16 MiB temporários, efêmeros, sem exec/set-ID/dispositivos.
- `cap_drop: ALL`: remove capabilities Linux adicionais.
- `no-new-privileges`: impede ganhar privilégios por execução.
- limites: reduzem impacto de consumo acidental, embora suporte/semântica variem
  por plataforma.
- `pids_limit`: limita criação acidental de processos/threads visíveis como PIDs.
- `stop_grace_period`: concede prazo para o encerramento antes de forçá-lo. No
  TaskBoard, a API usa 15 s porque aguarda handlers ativos; o gateway usa 10 s.
- driver `local` com limites: impede que logs cresçam sem rotação definida.
- `restart: "no"`: falhas permanecem visíveis no laboratório; uma política de
  produção deve evitar loops que escondem defeitos.

Checklist adicional:

- imagens por digest e processo de atualização;
- inventário/SBOM e scan como sinais, não garantia absoluta;
- usuário sem privilégio;
- contexto mínimo e nenhum segredo no build;
- apenas porta necessária, ligada ao endereço necessário;
- rede separada para componentes internos;
- limites de corpo, tempo e recursos;
- logs sem token/cookie/corpo sensível;
- backup, restauração e migração testados;
- TLS e gerenciamento de chaves quando sair do loopback.

O socket Docker equivale a controle amplo do daemon/host em instalações comuns.
Não monte `/var/run/docker.sock` dentro de uma aplicação sem uma arquitetura
que trate explicitamente esse poder.

## 14. Limitações do laboratório

O TaskBoard ensina fundamentos; não é blueprint completo de produção:

- não possui autenticação ou autorização;
- usa HTTP local, sem TLS;
- SQLite aceita concorrência limitada de escrita;
- não implementa migrações versionadas;
- não possui rate limit, tracing ou alta disponibilidade;
- healthchecks são simples;
- Compose local não substitui orquestração, monitoramento e backup de produção.

Não publique a porta em `0.0.0.0`, VPS ou internet. Adicionar senha improvisada
não transforma o laboratório em serviço seguro.

## 15. Encerramento e limpeza

Parar/remover containers e redes do projeto, preservando o volume:

```bash
docker compose down
```

Remover também o volume apaga o banco deste laboratório:

```bash
docker compose down --volumes
```

O segundo comando é destrutivo. Execute apenas no diretório conferido, depois de
decidir que os dados sintéticos podem ser descartados ou que o backup foi testado.
Não use comandos globais de prune como rotina: eles alcançam outros projetos.

## 16. Laboratórios por nível

Faça experimentos destrutivos em branch ou cópia descartável e preserve suas
alterações existentes.

### Nível 1: construir e observar

1. Valide o Compose.
2. Construa e suba os dois serviços.
3. Prove que processos não executam como root.
4. Prove que somente `127.0.0.1:8099` foi publicado.
5. Classifique `/health`, `/api/health` e `/api/tasks` por camada.
6. Pare preservando o volume.

**Evidência:** comandos, saídas essenciais e explicação de cada prova.

### Nível 2: falhas controladas

1. Pare apenas a API: `docker compose stop api`.
2. Confirme que `/health` continua `204` e `/api/health` falha via gateway.
3. Leia logs e explique o status recebido.
4. Inicie novamente: `docker compose start api`.
5. Envie corpo maior que o limite em dados sintéticos e identifique qual camada
   devolveu `413`.
6. Valide a configuração com `nginx -t`.

**Critério:** cada falha possui hipótese, evidência e recuperação documentadas.

### Nível 3: dados e recuperação

1. Crie três tarefas fictícias.
2. Recrie containers e prove persistência.
3. Gere backup consistente.
4. Verifique `quick_check` e contagem.
5. Em ambiente descartável, altere o estado e restaure o backup.
6. Confirme a lista pela API.

**Critério:** uma segunda pessoa consegue restaurar seguindo somente seu runbook.

### Nível 4: mudança operável

1. Acrescente ao TaskBoard um campo seguindo o guia do projeto.
2. Planeje migração antes de mudar schema.
3. Preserve compatibilidade durante a mudança.
4. Atualize testes, health, logs e contrato.
5. Reconstrua e execute teste funcional completo.
6. Documente rollback e limitações.

**Critério:** build limpo, testes verdes, dado persistente e procedimento de
operação reproduzível.

## 17. Exercícios

### Essenciais

1. Explique `EXPOSE` versus `ports` versus `listen`.
2. Diferencie volume nomeado e bind mount.
3. Desenhe as duas redes do TaskBoard.
4. Preveja o `location` escolhido para seis URIs.
5. Explique por que `depends_on` não garante disponibilidade permanente.

### Intermediários

1. Altere um arquivo estático e observe cache de build e cache do navegador.
2. Compare health do gateway com health do caminho completo.
3. Inspecione layers, mounts, UID e capabilities efetivas.
4. Defina limites diferentes e observe falha controlada sob carga local segura.
5. Escreva um runbook “502 no gateway” com árvore de decisão.

### Avançados

1. Desenhe atualização de digest com teste e rollback.
2. Proponha readiness que não sobrecarregue SQLite.
3. Modele migração versionada e restauração para um novo campo.
4. Compare execução rootless com daemon tradicional no seu ambiente.
5. Produza um threat model das fronteiras host→gateway→API→volume.

## Critério de conclusão

- [ ] Explico imagem, container, layer, volume, network e build context.
- [ ] Leio os Dockerfiles do projeto e justifico cada instrução relevante.
- [ ] Provo que a API não publicou porta no host.
- [ ] Explico como o gateway resolve `api` e encaminha cada URI.
- [ ] Diferencio liveness do gateway e saúde do caminho completo.
- [ ] Diagnostico falhas usando uma hipótese e a menor observação necessária.
- [ ] Demonstro persistência após recriar containers.
- [ ] Crio, verifico e restauro um backup com dados sintéticos.
- [ ] Encerro o ambiente conscientemente sem apagar volumes por acidente.
