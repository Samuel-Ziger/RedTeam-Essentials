# Laboratório 03 — Web acessível, resiliência e internacionalização

## Objetivo

Construir uma interface web que continue correta sob teclado, zoom, idioma
diferente, dados remotos lentos e conectividade intermitente. “Funciona na minha
tela” não é critério: cada qualidade precisa de cenário e evidência.

## Base

Faça uma cópia de trabalho do Study Desk ou use sua aplicação dos Labs 01–02.
Sirva por HTTP local. Preserve domínio e repositório; a UI deve ser consumidora
desses contratos, não o lugar onde as regras são reimplementadas.

## Etapa A — Semântica antes de estilo

Crie a interface com landmarks, headings hierárquicos, formulário, `label`,
controles nativos, lista/tabela adequada e região de status. Só use ARIA quando
o HTML não expressar a relação necessária.

Desenhe e teste a ordem de foco para:

1. cadastrar;
2. corrigir campos inválidos;
3. filtrar;
4. iniciar e cancelar atualização;
5. importar e confirmar;
6. excluir e desfazer.

Erro deve ser textual, associado ao campo e anunciado no momento certo. Não
desabilite foco nem apague os valores que a pessoa precisa corrigir.

## Etapa B — Reflow e preferências

Comece em viewport estreito, use unidades relativas e permita expansão de
texto. Verifique 200% e 400% de zoom, tema claro/escuro, contraste elevado,
redução de movimento e cores forçadas quando disponíveis.

Documente qualquer rolagem bidimensional essencial — por exemplo, uma tabela
complexa — e não force a página inteira a rolar horizontalmente por elementos
decorativos. Teste textos pseudolocalizados 30–50% maiores.

## Etapa C — Cliente resiliente

Implemente um adapter de API falso e determinístico. Ele deve simular sucesso,
latência, timeout, desconexão, resposta inválida, erro transitório e conflito.
Modele separadamente:

- primeira carga sem dados;
- atualização preservando dados antigos;
- offline com snapshot local;
- fila pendente;
- envio e confirmação;
- conflito que requer decisão;
- cancelamento e resposta atrasada.

Retry automático só é permitido quando a operação for idempotente ou possuir
chave de idempotência. Use backoff limitado e jitter injetável nos testes; não
faça testes esperarem segundos reais.

## Etapa D — Experiência offline

Defina o que “offline” significa nesta versão. Pode ser apenas continuar lendo
o snapshot local; não declare suporte completo se assets não carregam sem rede.
Mostre última atualização, operações pendentes e risco de conflito. Não esconda
dados anteriores durante refresh.

Teste a sequência: carregar dados, ficar offline, criar operação, fechar/reabrir,
voltar online, sincronizar e receber conflito. Registre qual lado é autoridade e
como o usuário preserva ambas as versões.

## Etapa E — Locale, tempo e dinheiro

Adicione `pt-BR` e `en` usando catálogo, fallback explícito e pluralização.
Formate datas e números com APIs de internacionalização. Armazene instante UTC;
quando a intenção for agenda local, mantenha também zona IANA e regras do
domínio. Se houver valor monetário, use inteiro em unidade menor ou decimal
adequado, nunca aproximação binária sem política.

Casos mínimos:

- zero, um e muitos itens nos dois idiomas;
- mudança de horário de verão em zona escolhida;
- separador decimal diferente;
- texto longo sem truncar ação;
- chave de tradução ausente;
- ordenação com acentos e locale.

## Matriz de verificação

| Dimensão | Procedimento | Evidência esperada |
|---|---|---|
| teclado | Tab, Shift+Tab, Enter, Espaço, Escape | todas as tarefas sem ponteiro |
| zoom | 200% e 400% | conteúdo e ações preservados |
| leitor de tela | fluxo principal e erro | nome, papel, estado e anúncio coerentes |
| rede | latência, timeout, offline e retorno | estado honesto e recuperação |
| concorrência | resposta antiga chega por último | request atual permanece vencedor |
| idioma | `pt-BR`, `en`, pseudo | sem strings soltas ou layout quebrado |

## Evidências e aceite

Entregue relatório manual, testes do reducer/adapter, catálogo de mensagens,
fixture de conflito e gravação curta opcional com transcrição. Automação de
acessibilidade é bem-vinda, mas não substitui teclado, zoom e leitor de tela.

A aprovação exige tarefas essenciais por teclado, reflow utilizável, status
compreensível, conteúdo do usuário inserido como texto e estados de rede sem
perda silenciosa. Os testes não podem depender da internet pública.

## Extensão avançada

Adicione fila persistente com ID de operação, política de retry e reconciliação.
Prove que reiniciar a aplicação não duplica uma operação confirmada e que uma
versão incompatível da fila é recusada ou migrada explicitamente.

## Checklist de domínio

- [ ] HTML nativo fornece a base semântica.
- [ ] Ações essenciais funcionam por teclado e com zoom.
- [ ] Dados anteriores permanecem durante atualização.
- [ ] Resposta atrasada não vence estado mais novo.
- [ ] Locale afeta texto, número, data e ordenação de modo coerente.
- [ ] Offline e sincronização têm limites declarados.
