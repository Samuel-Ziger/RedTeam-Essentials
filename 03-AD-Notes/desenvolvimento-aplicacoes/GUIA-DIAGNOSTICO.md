# Guia de diagnóstico — Aplicações profissionais

Este guia ensina a investigar sem destruir a evidência nem trocar a causa por
um ritual. Ele vale para os exemplos, o Study Desk e projetos autorais.

## Primeiro princípio: preserve o estado

Antes de limpar cache, reinstalar, apagar configuração ou “tentar do zero”:

1. registre resultado esperado e observado;
2. copie a primeira mensagem de erro, não só a última cascata;
3. anote versões, comando, diretório e configuração efetiva sem segredos;
4. exporte ou faça cópia do dado quando a aplicação permitir;
5. reproduza com fixture sintética em ambiente descartável;
6. altere uma variável por vez.

Limpar tudo pode ocultar migração defeituosa, precedência inesperada ou dado
corrompido. Recuperar o uso sem compreender a causa não encerra o diagnóstico.

## Registro mínimo reproduzível

```text
versão do app/toolchain:
plataforma/runtime/navegador:
comando ou sequência:
entrada sintética:
resultado esperado:
resultado observado:
primeira falha:
estado preservado/backup:
hipótese atual:
experimento de uma variável:
```

Redija caminhos pessoais, tokens e conteúdo livre. Use um valor-canário para
verificar sanitização e nunca transforme log de produção em fixture pública.

## Árvore de triagem

```text
a aplicação inicia?
├─ não → artefato/runtime/permissão/configuração inicial
└─ sim → a entrada foi aceita?
   ├─ não → parser/tipo/faixa/schema/codificação
   └─ sim → o estado mudou corretamente?
      ├─ não → regra/transição/concorrência
      └─ sim → persistiu e foi apresentado?
         ├─ persistência → quota/permissão/atomicidade/migração
         ├─ apresentação → render/foco/locale/formatação
         └─ dependência → timeout/protocolo/retry/conflito
```

Comece na primeira fronteira que divergiu. Um erro visual pode ter origem num
estado inválido; um “erro de banco” pode ser schema recusado corretamente.

## CLI e configuração

| Sintoma | Verifique | Experimento seguro |
|---|---|---|
| ajuda falha | inicialização antecipada | execute `--help` sem arquivo/ambiente |
| perfil inesperado | precedência e vazio | imprima origem, não segredo/valor sensível |
| JSON inválido | diagnóstico misturado | redirecione `stdout` e `stderr` separadamente |
| código sempre 1 | taxonomia perdida | teste uso, domínio e operação como subprocesso |
| funciona só no diretório | caminho relativo | execute a partir de diretório temporário |

Para reproduzir ambiente limpo, use apenas variáveis explicitamente listadas.
Não despeje o ambiente inteiro: ele costuma conter credenciais e identificadores.

## Arquivo, schema e migração

Diagnostique na ordem: tamanho → bytes/codificação → parse → campos → tipos →
limites → versão → invariantes cruzados. Parse bem-sucedido não prova documento
válido.

Casos que devem existir como fixtures:

- vazio/truncado;
- Unicode e fim de linha diferente;
- campo ausente e desconhecido;
- número no lugar de string;
- limite exato e limite + 1;
- ID duplicado;
- data impossível ou não canônica;
- versão futura;
- migração que falha no último item.

Nunca edite o único original para “corrigir”. Calcule hash quando o arquivo for
evidência, trabalhe numa cópia e valide a saída inteira antes do replace.

## Estado, eventos e concorrência

Registre `estado anterior + evento + estado seguinte + efeitos solicitados`.
Para operação assíncrona, inclua request/operation ID. Reproduza com scheduler ou
promessas controladas em vez de `sleep`.

Perguntas úteis:

- o evento era válido nesse estado?
- o reducer alterou o objeto anterior?
- uma resposta velha chegou depois da nova?
- cancelamento interrompeu o efeito ou apenas o interesse?
- sucesso foi exibido antes do commit?
- retry repetiu uma escrita não idempotente?

Se o bug desaparece com logging, suspeite de corrida e ordem, não conclua que o
logger “corrigiu”.

## Interface web e desktop

Separe semântica, layout e comportamento:

1. sem CSS, a ordem e os controles fazem sentido?
2. sem JavaScript, a estrutura inicial é compreensível?
3. a árvore de acessibilidade possui nome, papel e estado?
4. foco está visível e retorna ao lugar lógico?
5. 400% de zoom preserva tarefa?
6. tema, movimento reduzido e cores forçadas são respeitados?
7. o erro está associado ao campo e anunciado uma vez?

Em GUI desktop, confirme que trabalho longo não bloqueia a thread de interface
e que o resultado volta pelo mecanismo do toolkit. Não atualize widgets de uma
thread qualquer para “resolver” congelamento.

## Storage do navegador

`localStorage` pode falhar por quota, política, modo de navegação ou bloqueio do
origin. “Local” não significa permanente nem secreto.

Para o Study Desk:

```bash
cd projetos/study-desk
npm test
python3 -m http.server 8000
```

Use `http://127.0.0.1:8000`; origins diferentes possuem armazenamentos
diferentes. Antes de remover a chave, copie seu valor. Verifique se uma falha de
`setItem` restaura o estado anterior e se recarregar não revela falso sucesso.

## Clientes, offline e conflito

Capture método, endpoint lógico, timeout, número da tentativa, status/classe e
correlação — sem token ou corpo pessoal. Diferencie:

- DNS/conexão/TLS (transporte);
- timeout/cancelamento;
- resposta HTTP não bem-sucedida;
- resposta bem-sucedida com schema inválido;
- conflito de versão;
- operação local ainda pendente.

Use adapter falso para reproduzir. Internet pública acrescenta variáveis e torna
o teste frágil. Antes de retry, responda se a operação é idempotente e se o
servidor reconhece a mesma chave.

## Internacionalização e tempo

Registre locale, zona IANA, instante e entrada original. Não diagnostique apenas
pela string formatada. Verifique:

- chave ausente e fallback;
- regras de plural;
- separador decimal/moeda;
- ordenação com collation;
- offset antes/depois de transição;
- intenção civil versus duração absoluta;
- pseudolocalização e texto expandido.

Alterar o fuso global da máquina pode afetar outros testes; prefira APIs com zona
explícita ou processo descartável.

## Plugins e extensões

Liste manifesto sem executar código quando possível. Valide ID, versão de API,
capacidade e compatibilidade antes de carregar. Registre extensão responsável e
fase da falha. Teste com plugin falso que lança, trava ou devolve dado excessivo.

Desativar uma extensão pode recuperar o host, mas preserve o manifesto e o erro
para análise. Não faça descoberta depender da ordem arbitrária do sistema de
arquivos.

## Empacotamento e instalação

Compare quatro contextos:

1. execução na árvore de fontes;
2. artefato em diretório limpo;
3. instalação nova;
4. upgrade sobre dado antigo.

Se somente o primeiro funciona, procure arquivo não empacotado, caminho absoluto,
dependência global, variável herdada, cache ou runtime implícito. Inventarie o
artefato, verifique hash e rode smoke test sem checkout ao redor.

## Desempenho

Sem cenário e baseline, profiler vira uma coleção de imagens. Registre ambiente,
volume, interação, aquecimento, repetições e percentil. Depois:

1. reproduza com dado representativo;
2. capture perfil;
3. identifique caminho dominante;
4. mude uma variável;
5. repita as mesmas medidas;
6. execute testes de correção e acessibilidade.

CPU, memória, I/O e latência percebida são problemas diferentes. Uma média boa
pode esconder p95 ruim; uma operação rápida pode congelar a interface.

## Release e rollback

Uma release falhou de modo controlado quando o runbook responde:

- qual sinal aciona abortar?
- quem decide e em quanto tempo?
- o schema novo é compatível com versão antiga?
- que backup foi validado?
- como confirmar rollback além de “iniciou”?
- que artefato/hash está em execução?

Não faça downgrade sobre documento futuro sem contrato. Pare, preserve, converta
por migração testada ou use exportação de recuperação.

## Encerramento do incidente

O diagnóstico termina com causa demonstrada, impacto, recuperação verificada,
teste que falhava antes e passa depois, e ação preventiva. Registre também
hipóteses descartadas: elas evitam repetir experimentos caros.

Use este critério final:

```text
mesma entrada + mesmo ambiente controlado
→ falha reproduzível antes
→ mudança explicada
→ sucesso reproduzível depois
→ invariantes antigos ainda passam
```
