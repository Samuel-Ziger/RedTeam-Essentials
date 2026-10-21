# Lab 05 — TaskBoard, Docker e Nginx

## Objetivo

Executar, observar, modificar e defender tecnicamente o projeto integrador. O
resultado não é apenas “subiu”: você deve provar contratos, isolamento,
persistência e cleanup.

Este lab corresponde às fases A–B do Projeto 4 em
[Projetos e avaliações](../09-projetos.md). Preserve suas evidências para o
portfólio. A etapa 6 funciona como ensaio orientado; na entrega do Projeto 4,
a melhoria vertical deve ter especificação, testes e decisões autorais mais
completos, seguidos da fase D de observação e defesa.

## Tempo e ambiente

- 8 a 12 horas;
- Docker Engine com Compose v2;
- navegador e cliente HTTP local;
- portas do projeto livres;
- nenhum serviço externo.

## Limite

O único endereço publicado pelo laboratório deve ser o loopback configurado no
Compose. Não remova esse limite e não reutilize credenciais ou dados reais.

## Etapa 1 — aplicação sem containers

1. Execute os testes da API.
2. Inicie a API em loopback e porta local.
3. Consulte saúde e CRUD com cliente HTTP.
4. Interrompa e confirme que não ficou processo.
5. Localize arquivo SQLite e descreva quando é criado.

Explique por que validar a aplicação antes do container reduz o espaço de busca
de um defeito.

## Etapa 2 — leitura da infraestrutura

Antes do build, explique cada item:

- imagens base e digest;
- ordem das instruções Dockerfile;
- usuário efetivo;
- diretório de trabalho e arquivos copiados;
- comando principal;
- filesystem somente leitura e diretórios temporários;
- capacidades removidas;
- redes <code>backend</code> e <code>access</code>;
- volume <code>task-data</code>;
- healthchecks;
- dependência entre gateway e API;
- publicação <code>127.0.0.1:8099:8080</code>.

Faça o mesmo para os blocos <code>location</code> do Nginx.

## Etapa 3 — validação e execução

No diretório do projeto:

    docker compose config
    docker compose build
    docker compose up -d
    docker compose ps
    docker compose logs --tail=100

Confirme:

- gateway saudável;
- API saudável;
- interface em <code>http://127.0.0.1:8099</code>;
- saúde do gateway;
- saúde da API pelo proxy;
- CRUD completo pela interface.

Registre versões, horário e comandos, não apenas screenshots.

## Etapa 4 — fluxo ponta a ponta

Escolha a criação de uma tarefa e descreva:

1. evento no formulário;
2. objeto JavaScript e serialização JSON;
3. requisição HTTP;
4. seleção de rota no Nginx;
5. validação do corpo na API;
6. transação SQLite;
7. status, cabeçalhos e resposta;
8. atualização segura do DOM.

Associe cada etapa a um arquivo e função/bloco de configuração.

## Etapa 5 — falhas controladas

Trabalhe em uma cópia e faça uma alteração por vez:

1. configure upstream incorreto no Nginx;
2. observe status e logs;
3. restaure e confirme saúde;
4. envie título vazio e corpo inválido;
5. confirme que erro do cliente não vira 500;
6. pare a API e observe comportamento do gateway;
7. reinicie e verifique persistência.

Para cada falha registre hipótese, evidência e correção.

## Etapa 6 — mudança funcional

Adicione uma regra pequena completa que ainda não exista na base, por exemplo
prioridade `low|normal|high`:

- defina valores aceitos, valor padrão, serialização e comportamento para
  tarefas antigas;
- escreva teste que falha;
- implemente migração e backend;
- implemente interface acessível cujo significado não dependa apenas de cor;
- atualize documentação;
- reconstrua imagens;
- execute regressão e prove persistência após recriar os containers.

Não aceite mudança que funcione somente pela interface sem teste do contrato.

## Etapa 7 — cleanup

Primeiro preserve dados:

    docker compose down

Suba novamente e confirme persistência. Depois, quando a evidência estiver
salva e você quiser destruir os dados do exercício:

    docker compose down -v

Liste recursos do projeto e confirme que containers, redes e volume foram
removidos. Não use comandos globais de prune.

## Critérios de aceite

- [ ] A API passou nos testes antes do Docker.
- [ ] A configuração Compose foi validada antes do build.
- [ ] Apenas loopback foi publicado.
- [ ] Os dois serviços ficaram saudáveis.
- [ ] Uma requisição foi explicada ponta a ponta.
- [ ] Pelo menos três falhas foram diagnosticadas por evidência.
- [ ] Uma mudança funcional incluiu teste, código e documentação.
- [ ] Persistência e remoção do volume foram demonstradas separadamente.
- [ ] Nenhum segredo ou dado real entrou em imagem, log ou repositório.

## Defesa final

Sem consultar o código, desenhe os componentes e responda:

- o que continuaria funcionando se a API parasse?
- por que o navegador não chama o nome interno <code>api</code> diretamente?
- o que muda ao reiniciar container, recriar imagem e remover volume?
- healthcheck garante que criar tarefa funciona?
- qual limite reduz corpo excessivo e em qual camada?
- como localizar uma requisição que retornou erro?
- por que filesystem somente leitura ainda permite SQLite neste desenho?

Aprovado significa explicar os mecanismos e limites, não memorizar os comandos.
