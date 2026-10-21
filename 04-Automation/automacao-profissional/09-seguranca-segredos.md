# 09 — Segurança, segredos e supply chain da automação

Uma automação costuma concentrar privilégio, credenciais e alcance. Uma falha que
afetaria um item manualmente pode afetar milhares em segundos. Segurança aqui é
limitar o que o processo **pode ler, decidir, executar e publicar**.

## Objetivos

- mapear fronteiras de confiança e superfícies de injeção;
- desenhar identidades e permissões mínimas;
- gerir credenciais sem logs, argumentos ou arquivos acidentais;
- controlar dependências, actions, plugins e artefatos;
- proteger dados, evidências e ambientes de execução.

## 1. Modelo de ameaça proporcional

Liste ativos, atores, fronteiras e efeitos. Para cada entrada, pergunte onde ela
pode chegar:

~~~text
branch/issue/arquivo/API
        -> parser
        -> template/caminho/comando/query
        -> runner com credenciais
        -> artefato ou sistema externo
~~~

Nome de branch, título de issue, célula, variável de ambiente e resposta HTTP são
dados não confiáveis. O fato de virem de uma ferramenta interna não os transforma
em código seguro.

## 2. Evitar injeção

Prefira APIs tipadas e passagem separada de argumentos. Não construa shell, SQL,
regex, template ou caminho por concatenação.

~~~python
# perigoso: entrada altera a gramática do shell
subprocess.run(f"tool --name {name}", shell=True)

# melhor: cada argumento continua dado
subprocess.run(["tool", "--name", name], check=True, timeout=30)
~~~

Mesmo sem shell, valide limites e semântica. Um argumento como nome de arquivo
pode ser interpretado como opção por algumas CLIs; use separador de opções quando
suportado ou uma API direta. Não registre a linha completa se ela contiver segredo.

## 3. Menor privilégio

Construa matriz identidade × ação × ambiente:

| Identidade | Ambiente | Ler | Planejar | Aplicar | Administrar |
|---|---|---:|---:|---:|---:|
| CI pull request | teste | sim | sim | não | não |
| release | produção | artefato | sim | publicação limitada | não |
| operador break-glass | produção | sim | sim | temporário | auditado |

Use identidade própria por ferramenta e ambiente, não conta pessoal compartilhada.
Separe planejar de aplicar. Restringir apenas pela interface é insuficiente: a
credencial também precisa impedir a ação fora do fluxo esperado.

## 4. Ciclo de vida de segredos

Um segredo tem criação, distribuição, uso, rotação, revogação e auditoria.
Prefira identidade de workload e token curto a chave estática.

Não passe segredo em:

- argumento de processo;
- URL ou query string;
- nome de arquivo;
- mensagem de erro;
- cache, artifact ou screenshot;
- variável interpolada em comando do workflow;
- fixture e arquivo de configuração versionado.

Variável de ambiente é melhor que commit, mas não é cofre: processos filhos e
dumps podem vê-la. Leia no ponto de uso, mantenha por pouco tempo e não despeje o
ambiente em diagnósticos.

### Redação e canário

Mascarar pelo valor exato falha se o segredo for codificado, truncado ou colocado
em JSON. Evite registrar a fonte e use allowlist de campos. Em teste, injete um
canário sintético e procure-o em stdout, stderr, logs e artefatos.

## 5. Dados e retenção

Classifique entrada, saída, logs, temporários, quarentena e backup. Para cada um,
defina propósito, acesso, local, criptografia, retenção e remoção. “Temporário”
não significa apagado automaticamente em falha.

Minimize por design. Se contagem e hash resolvem a operação, não copie o payload
para log. Se o operador precisa corrigir um item, armazene-o em repositório protegido
e referencie por ID.

## 6. Dependências e plugins

Bibliotecas, imagens, actions e plugins executam com o poder do processo. Controle:

- origem e mantenedor;
- versão ou digest imutável;
- lockfile e revisão de mudança;
- licença e componentes transitivos;
- vulnerabilidades e prazo de atualização;
- SBOM por artefato;
- assinatura/proveniência quando disponível;
- remoção de dependência abandonada.

Versão fixada reduz mudança surpresa, mas também congela falhas. Automatize
propostas de atualização, execute a suíte e revise o diff.

Plugins exigem manifesto, versão de API, capacidades e isolamento. Carregar código
arbitrário no mesmo processo não cria sandbox. Se a extensão é de confiança menor,
use processo/contêiner e canal restrito, compreendendo que isolamento real depende
da plataforma.

## 7. CI e contribuições não confiáveis

Um pull request pode modificar testes, build e scripts. Não entregue segredos a
código de fork. Separe verificação sem privilégio de publicação protegida.

Cuidados:

- permissões mínimas por job;
- checkout do commit esperado;
- actions fixadas por SHA/digest;
- nenhum eval de valor vindo do evento;
- ambiente protegido para release;
- credencial curta via OIDC quando suportado;
- artifacts validados antes da promoção;
- runners efêmeros ou higienizados.

Cache é aceleração, não fronteira de confiança. Chave manipulável pode permitir
conteúdo inesperado. Revalide o que entra no artefato.

## 8. Execução segura

- dry-run por padrão e apply explícito;
- allowlist de recursos e ambientes;
- limite de itens, bytes, taxa e tempo;
- diretório de trabalho isolado;
- filesystem somente leitura quando possível;
- saída de rede restrita ao necessário;
- processo sem privilégio administrativo;
- aprovação para efeitos de alto impacto;
- kill switch e revogação de credencial ensaiados.

Container não torna código seguro por si só. Capabilities, mounts, socket do host,
identidade e egress ainda determinam o poder real.

## 9. Erros e logs

Mensagem ao usuário informa a ação; evento interno registra classe e correlação.
Não exponha stack trace, token, payload, caminho pessoal ou configuração completa.
Preserve a causa no canal protegido quando necessário.

Uma exceção de sanitização não deve fazer o sistema registrar o objeto original
como fallback. O fallback precisa ser menor e seguro.

## Falhas e diagnóstico

| Sintoma | Causa | Controle |
|---|---|---|
| segredo aparece no log | objeto/config inteira | allowlist e teste canário |
| PR acessa produção | job com permissão ampla | separar trust zones |
| nome vira comando | concatenação | API e argumentos separados |
| plugin compromete host | mesmo processo/poder | capacidade e isolamento |
| pacote muda sem diff | dependência flutuante | lock, digest e provenance |

## Exercícios

### Nível 1 — fronteiras

Marque entradas e sinks de um workflow. **Aceite:** cada dado não confiável tem
parser, limite e uso que não o transforma em código.

### Nível 2 — privilégios

Crie matriz identidade × ação × ambiente. **Aceite:** planejar e aplicar estão
separados, tokens expiram e revogação foi ensaiada.

### Nível 3 — supply chain

Gere SBOM, inventarie actions/plugins e verifique artifact. **Aceite:** origem,
versão, digest e processo de atualização são reproduzíveis.

## Checklist

- [ ] Entradas nunca viram gramática por concatenação.
- [ ] Identidades e ambientes possuem privilégio mínimo.
- [ ] Segredos são curtos, rotacionáveis e ausentes de artefatos.
- [ ] Dados e temporários possuem retenção.
- [ ] Dependências/actions são fixadas e inventariadas.
- [ ] Código não confiável não recebe credencial de publicação.

