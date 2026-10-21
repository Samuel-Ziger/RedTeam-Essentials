# 12 — Plugins e extensibilidade com contratos seguros

Extensibilidade é a capacidade de adicionar uma variação sem reescrever o núcleo
da aplicação. Isso parece apenas uma decisão de arquitetura, mas muda também o
modelo de compatibilidade e de confiança: um plugin pode receber dados, consumir
recursos, falhar durante a inicialização e permanecer instalado depois que o host
é atualizado. Por isso, “carregar um arquivo e chamar uma função” não constitui
sozinho um sistema de plugins.

Este capítulo usa extensões benignas para o Study Desk, como novos formatos de
exportação e cálculos de resumo. O objetivo não é criar mecanismos de execução
arbitrária. Isolamento de processos e controles próprios de Sistemas Operacionais
serão estudados nos módulos correspondentes.

## Objetivos de aprendizagem

Ao terminar, você deverá ser capaz de:

- decidir se uma necessidade exige plugin ou uma alternativa mais simples;
- especificar manifesto, interface, ciclo de vida e política de falha;
- separar versão da aplicação, da API de plugins e do próprio plugin;
- conceder capacidades explícitas em vez de entregar o objeto inteiro do host;
- validar, registrar, desativar e diagnosticar extensões sem quebrar o núcleo;
- criar testes de contrato reutilizáveis para todas as implementações;
- explicar os limites de segurança de plugins executados no mesmo processo.

## Pré-requisitos

Revise interfaces e injeção de dependência no módulo 02. Neste módulo, tenha
domínio de configuração, validação, estado, persistência e logs, especialmente os
capítulos 02, 03, 05 e 11. Execute também os testes do
[Study Desk](projetos/study-desk/README.md) antes de propor uma extensão.

## 1. Primeiro encontre o verdadeiro eixo de variação

Um sistema extensível precisa de uma pergunta concreta: **o que pode variar sem
alterar a regra central?** No Study Desk, “exportar sessões como texto” pode ser
um eixo de variação; “permitir que qualquer extensão altere todo o estado” é uma
fronteira ampla demais.

Antes de criar uma API de plugins, compare estas opções:

| Necessidade | Opção inicial | Quando evoluir |
|---|---|---|
| trocar cor, limite ou rótulo | configuração validada | quando houver comportamento novo |
| escolher entre algoritmos conhecidos | Strategy registrada no build | quando terceiros precisarem adicionar estratégias |
| transformar arquivo de entrada/saída | comando externo com contrato | quando integração profunda ou baixa latência for essencial |
| avisar outro produto sobre um evento | webhook ou API | quando a extensão precisar atuar dentro da jornada local |
| adicionar painel ao produto | plugin de interface com API mínima | quando a composição visual justificar o acoplamento |

Configuração é dados; plugin é comportamento. Uma configuração declarativa é
mais fácil de validar, migrar e explicar. Um comando externo tem uma fronteira de
entrada e saída clara. Um plugin no mesmo processo compartilha falhas, memória e
as permissões já concedidas ao host. Use-o somente quando esse custo compra uma
experiência necessária.

## 2. O contrato possui mais do que uma função

Um contrato maduro inclui identidade, compatibilidade, capacidades, ciclo de
vida, limites e semântica de erro. Um manifesto simples pode começar assim:

```json
{
  "id": "org.example.study-summary",
  "name": "Resumo de estudo",
  "version": "1.2.0",
  "pluginApi": "1",
  "entry": "index.mjs",
  "capabilities": ["sessions:read", "export:register"]
}
```

Defina limites para tamanho e formato dos campos, recuse propriedades
desconhecidas quando o contrato for estrito e rejeite IDs duplicados. `entry`
nunca deve escapar do pacote esperado após a resolução do caminho. O manifesto
declara intenção; ele não prova que o código respeitará essa intenção.

Uma API mínima em JavaScript poderia ser representada por este contrato:

```js
/**
 * @typedef {Object} StudyDeskPlugin
 * @property {Readonly<{id: string, version: string, pluginApi: "1"}>} metadata
 * @property {(context: PluginContext) => Promise<void>} initialize
 * @property {() => Promise<void>} dispose
 *
 * @typedef {Object} PluginContext
 * @property {(format: ExportFormat) => () => void} registerExportFormat
 * @property {(event: string, fields?: object) => void} log
 */
```

O retorno de `registerExportFormat` é uma função de desregistro. Essa pequena
escolha torna a limpeza observável e testável. O contexto não contém `window`, o
repositório inteiro ou o reducer: fornece somente operações estáveis que o
plugin declarou precisar.

## 3. Ciclo de vida explícito

Modele estados, em vez de depender de convenções implícitas:

```text
descoberto -> validado -> compatível -> inicializando -> ativo
                                              |           |
                                              v           v
                                            falhou <- desativando -> inativo
```

`initialize` deve registrar recursos de forma atômica ou desfazer o que já
registrou ao falhar. `dispose` deve ser idempotente: chamá-lo duas vezes não pode
remover recurso de outro plugin nem lançar uma falha nova. Não execute a extensão
antes de validar manifesto e compatibilidade. Não a marque como ativa antes de a
inicialização concluir.

Ordem também faz parte do contrato. Se dois plugins oferecem o mesmo formato,
você pode rejeitar a duplicata, usar prioridade explícita ou exigir escolha do
usuário. “O último carregado vence” produz comportamento dependente do sistema de
arquivos e dificulta reprodução.

Um registry pequeno evidencia essas decisões:

```js
async function runCleanup(steps) {
  const failures = [];
  for (const step of [...steps].reverse()) {
    try {
      await step();
    } catch (error) {
      failures.push(error);
    }
  }
  return failures;
}

export function createRegistry({supportedApi, makeContext}) {
  const active = new Map();
  let lifecycle = Promise.resolve();

  function serialized(operation) {
    const result = lifecycle.then(operation, operation);
    lifecycle = result.catch(() => undefined);
    return result;
  }

  return {
    activate(plugin) {
      return serialized(async () => {
        const {id, pluginApi} = plugin.metadata ?? {};
        if (typeof id !== "string" || !/^[a-z0-9][a-z0-9.-]{2,127}$/.test(id)) {
          throw new TypeError("plugin_id_invalid");
        }
        if (pluginApi !== supportedApi) throw new Error("plugin_api_unsupported");
        if (active.has(id)) throw new Error("plugin_id_duplicate");

        const cleanup = [];
        try {
          const context = makeContext(fn => cleanup.push(fn));
          await plugin.initialize(context);
          active.set(id, {plugin, cleanup});
        } catch (error) {
          const cleanupFailures = await runCleanup(cleanup);
          if (cleanupFailures.length > 0) {
            throw new AggregateError(
              [error, ...cleanupFailures],
              "plugin_initialize_and_rollback_failed",
              {cause: error},
            );
          }
          throw error;
        }
      });
    },

    deactivate(id) {
      return serialized(async () => {
        const record = active.get(id);
        if (!record) return;
        active.delete(id);
        const failures = [];
        try {
          await record.plugin.dispose();
        } catch (error) {
          failures.push(error);
        }
        failures.push(...await runCleanup(record.cleanup));
        if (failures.length === 1) throw failures[0];
        if (failures.length > 1) {
          throw new AggregateError(failures, "plugin_deactivation_failed", {
            cause: failures[0],
          });
        }
      });
    }
  };
}
```

`runCleanup` tenta todas as etapas em ordem reversa. Se o rollback também falhar,
`AggregateError` preserva a falha original como primeira entrada e `cause`, sem
descartar as falhas secundárias. A desativação remove o registro antes dos efeitos,
portanto uma segunda chamada é no-op mesmo se `dispose` falhou; todas as limpezas
ainda são tentadas. Teste inicialização parcial, múltiplas falhas de limpeza,
desativação repetida e conflito de ID.

O encadeamento `serialized` é uma escolha simples e deliberada: ativações e
desativações são linearizadas na ordem de chamada. Assim, duas ativações do mesmo
ID não atravessam juntas e uma desativação solicitada durante `initialize` espera
e remove o registro em seguida. Para muitos plugins independentes, locks por ID
podem aumentar concorrência, mas precisam preservar essas mesmas garantias.

## 4. Três versões diferentes

Não confunda:

1. **versão do host**, que representa o produto Study Desk;
2. **versão da API de plugins**, que representa o contrato oferecido;
3. **versão do plugin**, que representa sua implementação.

O host `4.3.0` pode continuar oferecendo a API `1`. Um plugin `2.7.1` pode usar
essa API. Atualizar o layout do host não deve obrigar todos os plugins a mudar se
o contrato permaneceu estável.

Uma alteração incompatível na API merece nova versão principal. Antes disso,
prefira capacidades opcionais:

```js
if (context.capabilities.has("export:stream-v2")) {
  // usa a forma nova
} else {
  // permanece na forma suportada pela API 1
}
```

Documente a janela de depreciação, em que versão o aviso começou e qual migração
substitui a função antiga. Negociação excessivamente flexível também custa:
combinações demais viram uma matriz impossível de testar. Suporte poucas versões
de API, declaradas e cobertas por testes.

## 5. Confiança, capacidades e isolamento

Descoberta automática de todo arquivo em um diretório gravável transforma
presença em autorização. Prefira catálogo explícito, instalação confirmada e
lista de extensões habilitadas. Registre origem, versão e hash do pacote. Uma
assinatura pode comprovar integridade e identidade do publicador conforme a
política adotada; ela não afirma que o comportamento é correto ou benigno.

Capacidades são objetos estreitos entregues pelo host. Um exportador precisa ler
uma cópia imutável das sessões e devolver bytes ou texto. Ele não precisa alterar
preferências, apagar registros nem conhecer onde os dados são persistidos.

Se o código não é plenamente confiável, executar no mesmo processo não oferece
isolamento forte. Uma separação por processo ou serviço pode limitar o protocolo,
mas sua implementação depende da plataforma e fica fora do escopo deste módulo.
Aqui, a regra prática é: plugin in-process só para código sob política de
confiança compatível com o host; caso contrário, escolha integração declarativa
ou externa.

Timeout também precisa de precisão. `Promise.race` pode parar de esperar, mas não
cancela automaticamente o trabalho. Passe `AbortSignal` e exija cooperação:

```js
async function runWithDeadline(operation, milliseconds) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), milliseconds);
  try {
    return await operation({signal: controller.signal});
  } finally {
    clearTimeout(timer);
  }
}
```

Trate cancelamento como resultado conhecido. Se a extensão ignora o sinal, o host
deve evitar iniciar novas operações iguais e informar degradação; não prometa uma
interrupção que o mecanismo não fornece.

## 6. Dados, UI e determinismo

Passe snapshots imutáveis ou DTOs versionados, não entidades internas vivas.
Valide o resultado do plugin como qualquer outra entrada. Um exportador deve
declarar `mediaType`, extensão de arquivo e método `serialize`; o host decide o
nome final e inicia o download. Isso impede que cada extensão implemente
diretamente detalhes da interface.

Extensões visuais exigem contratos adicionais: região permitida, foco,
acessibilidade, descarte de listeners e estados de carregamento/erro. HTML pronto
fornecido pelo plugin é difícil de validar. Um modelo de dados limitado, que o
host renderiza com seus próprios componentes, reduz a superfície e mantém
consistência visual.

Ordene contribuições por regra estável, por exemplo `priority` e depois `id`. Não
use horário de descoberta como desempate. Com as mesmas entradas, o catálogo deve
ter a mesma ordem e produzir o mesmo diagnóstico.

## 7. Testes de contrato e diagnóstico

Além dos testes próprios de cada plugin, o host fornece uma suíte reutilizável:

- manifesto válido e rejeição de campos inválidos;
- inicialização e descarte sem recurso pendente;
- compatibilidade nas versões ainda suportadas;
- resposta válida, inválida, vazia e grande dentro do limite;
- cancelamento e falha assíncrona;
- ausência de capacidade não declarada;
- conflito de contribuição e ordem determinística;
- mensagem ao usuário sem detalhes internos ou segredos.

Use um plugin fake que registra chamadas. Não teste uma extensão real para provar
o contrato do registry; isso mistura duas unidades e pode mascarar o defeito.

Eventos úteis são `plugin_validation_failed`, `plugin_api_unsupported`,
`plugin_activation_failed` e `plugin_deactivated`. Inclua ID, versão, versão da
API, etapa e código de razão. Não registre conteúdo exportado nem opções que
possam conter dados pessoais.

Quando um plugin falhar, investigue nesta ordem:

1. o manifesto foi lido integralmente e validado?
2. a API pedida está dentro da matriz suportada?
3. todas as capacidades declaradas foram concedidas?
4. a falha ocorreu na inicialização, execução ou limpeza?
5. o host continua correto com a extensão desativada?
6. o teste de contrato reproduz a mesma classe de falha?

## 8. Aplicação ao Study Desk

Comece com um ponto de extensão pequeno: formatos de exportação. O domínio entrega
uma lista copiada e ordenada de sessões; o plugin retorna `{mediaType, content}`;
o host valida tamanho e tipo antes de oferecer o arquivo. O formato JSON nativo
continua no núcleo porque também representa backup e restauração. CSV ou Markdown
podem ser contribuições opcionais.

Essa separação evita que um plugin de apresentação assuma responsabilidade pela
integridade do backup. Ela também permite medir custo: serialização de muitas
sessões pode receber cancelamento e limite, sem dar acesso ao repositório.

## Erros frequentes e trade-offs

- **API ampla demais:** acelera o primeiro plugin, mas congela detalhes internos.
- **API pequena demais:** força contornos e duplicação. Evolua por casos reais.
- **compatibilidade eterna:** agrada no curto prazo, mas impede correções; publique
  depreciação e fim de suporte.
- **falha silenciosa:** mantém a tela aberta, porém perde confiança; degrade com
  mensagem acionável e diagnóstico.
- **plugin obrigatório:** se o produto não funciona sem ele, talvez seja parte do
  núcleo e deva receber os mesmos testes e ciclo de release.
- **carregamento dinâmico como segurança:** módulo dinâmico é mecanismo de
  composição, não fronteira de proteção.

## Exercícios em três níveis

### Nível 1 — Análise e contrato

Compare configuração, Strategy compilada, comando externo e plugin para: tema,
exportação Markdown e cálculo de sequência de estudos. Escreva o manifesto e a
interface do exportador.

**Aceite:** cada escolha possui necessidade, alternativa rejeitada e custo; o
manifesto tem limites, versão de API e capacidades; a interface não expõe DOM nem
repositório.

### Nível 2 — Registry testável

Implemente um registry em memória, um plugin fake e um exportador Markdown.
Adicione ativação, desativação idempotente, conflito de ID, rollback de
inicialização parcial e logs estruturados.

**Aceite:** testes cobrem sucesso e ao menos seis falhas; a mesma entrada produz a
mesma ordem; após qualquer falha não resta contribuição registrada; logs não
contêm conteúdo das sessões.

### Nível 3 — Evolução compatível do Study Desk

Projete a API 2 com exportação cancelável e resultado por partes. Mantenha uma
matriz pequena de compatibilidade, suíte de contrato para API 1/2, política de
depreciação e plano de recuperação quando uma extensão deixa de responder.

**Aceite:** a mudança incompatível está identificada; plugins antigos têm caminho
documentado; cancelamento não é confundido com interrupção forçada; o host segue
utilizável com qualquer plugin desativado; a decisão está registrada em ADR.

## Checklist de conclusão

- [ ] Sei demonstrar por que a necessidade não cabe em configuração ou Strategy.
- [ ] Manifesto, interface, ciclo de vida e limites estão documentados.
- [ ] Host, API e plugin possuem versões independentes.
- [ ] Descoberta não equivale a autorização para executar.
- [ ] O contexto oferece somente capacidades declaradas.
- [ ] Entradas e resultados da extensão são validados.
- [ ] Inicialização parcial é revertida e descarte é idempotente.
- [ ] Ordem e conflitos têm comportamento determinístico.
- [ ] Há suíte de contrato com falha, cancelamento e compatibilidade.
- [ ] O host continua correto quando todas as extensões estão desativadas.
- [ ] Diagnóstico explica a etapa sem registrar dados do usuário.
- [ ] Consigo explicar por que plugin in-process não é isolamento de segurança.

Ao concluir este capítulo, você não apenas sabe “carregar plugins”: sabe manter
uma plataforma extensível pequena, verificável e capaz de evoluir.
