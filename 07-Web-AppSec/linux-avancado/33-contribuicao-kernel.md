# 33 — Desenvolvimento e contribuição ao kernel

## Objetivos

- selecionar uma mudança pequena e justificável;
- preparar commit, teste e mensagem revisáveis;
- usar checkpatch, sparse, sanitizers e matrizes de config;
- entender mantenedores, listas, DCO e revisão.

## Escolha do problema

Comece por bug reproduzível, warning de compilador, teste faltante ou melhoria de
documentação. Não comece com novo subsistema. Confirme se a árvore correta é
mainline, `linux-next`, stable ou do mantenedor do subsistema.

Um patch deve resolver um problema lógico. Refactor, formatação e correção
funcional separados facilitam review e `git bisect`.

## Mensagem

Estrutura:

```text
subsystem: imperative summary

Describe the observable problem and conditions.
Explain the cause.
Explain the change and trade-offs.
State how it was tested.

Fixes: 12-char-id ("original subject")   # quando aplicável
Signed-off-by: Real Name <address>
```

`Signed-off-by` declara concordância com Developer Certificate of Origin; não é
decoração. Não invente tags `Reviewed-by` ou `Tested-by`.

## Ferramentas

```bash
scripts/checkpatch.pl --strict PATCH
scripts/get_maintainer.pl PATCH
make O=build W=1
make O=build C=1
make O=build kselftest
```

Escolha testes do subsistema. Além de config principal, considere `=y`, `=m`,
`=n`, 32/64 bits e endianness quando a mudança tocar layout ou aritmética.

## Revisão

Responda tecnicamente, cite alterações, preserve destinatários relevantes e
envie a série completa ao revisar. Changelog de versão fica depois de `---`, não
na mensagem permanente. Revisão pode rejeitar abordagem, não a pessoa.

## Do relato ao patch

Comece reproduzindo no kernel e config corretos. Reduza o caso até preservar a
invariante violada e confirme se a árvore alvo já contém correção. Procure lore,
issues e commits por mensagem e símbolo. Para regressão, `git bisect` ajuda
somente quando cada ponto é testável e o script classifica good/bad com confiança.

O patch deve ter escopo mínimo, preservar comportamento não relacionado e tratar
erro e lifetime. A mensagem explica problema observável e causa antes da solução.
Comentários no código documentam invariantes difíceis; não repetem o diff.
`Fixes` referencia o commit que introduziu o defeito quando sustentado pelo
histórico, não a última linha tocada.

## Matriz de validação

Compile com warnings relevantes e combinações de Kconfig que incluem, modularizam
e removem o recurso. Execute teste que falha antes e passa depois, selftests do
subsistema e ferramentas estáticas apropriadas. Mudanças concorrentes podem pedir
lockdep, KASAN, KCSAN ou fault injection. Registre arquitetura e o que não foi
testado.

Cada patch da série deve construir e manter testes coerentes para permitir
bisect, review e backport. Mudança preparatória precisa ser justificável sozinha.
Não misture rename mecânico, formatação e correção funcional se isso esconder a
alteração revisada.

## Interação com mantenedores

Leia `MAINTAINERS` e documentação do subsistema. Use versão no assunto da série,
changelog abaixo de `---` e responda inline preservando contexto. Tags recebidas
pertencem ao patch revisado; mudança substancial pode exigir nova revisão.

## Falhas comuns

- desenvolver sobre árvore errada;
- enviar sem teste que demonstra o problema;
- executar checkpatch como substituto de revisão técnica;
- adicionar tags nunca concedidas;
- quebrar build entre patches;
- publicar detalhe sensível antes da coordenação adequada.

## Segurança

Falha explorável não deve ser divulgada publicamente antes da coordenação
apropriada. Siga `Documentation/admin-guide/security-bugs.rst`. O curso não cria
exploit; reprodução mínima deve demonstrar corrupção de forma segura na VM.

## Prática B/C

Prepare uma correção de documentação ou teste local:

1. demonstre problema antes;
2. produza um commit único;
3. execute checkpatch e testes relevantes;
4. gere patch com `git format-patch`;
5. use `get_maintainer` apenas para aprender;
6. **não envie** e-mail real como parte do curso.

## Exercícios

1. Escolha correção documental pequena, identifique árvore e mantenedores e
   escreva mensagem completa sem enviar.
2. Crie teste que falha antes e passa depois de uma mudança local didática.
3. Monte matriz `=y/=m/=n`, warnings, selftests e análise estática.
4. Divida uma mudança em série bisectável e justifique a responsabilidade de
   cada commit.

## Checklist de domínio

- [ ] Confirmo problema, árvore e histórico antes de editar.
- [ ] Escrevo commit com problema, causa, solução, trade-off e teste.
- [ ] Uso DCO e tags sem inventar reconhecimento.
- [ ] Mantenho cada patch compilável, revisável e bisectável.
- [ ] Não envio e-mail real nem material sensível durante o curso.

Fonte: [submitting patches](https://docs.kernel.org/process/submitting-patches.html).
