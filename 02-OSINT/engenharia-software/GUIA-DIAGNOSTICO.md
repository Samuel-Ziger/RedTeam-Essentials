# Guia de diagnóstico — algoritmos, design e qualidade

Diagnosticar software não é tentar correções até a suíte ficar verde. É localizar
a primeira fronteira em que o estado observado deixa de cumprir o contrato,
formular uma hipótese falsificável e preservar a correção num teste. Este guia
usa o Dependency Planner e fixtures sintéticas; não requer serviços externos.

## Fluxo principal

```text
sintoma -> contrato -> menor reprodução -> primeira divergência
        -> hipótese -> experimento discriminante -> correção -> regressão
```

Antes de editar, registre:

- comando exato e diretório;
- entrada mínima, preservando encoding e bytes relevantes;
- saída esperada e propriedade que a define;
- `stdout`, `stderr` e código de saída observados;
- versão do commit, linguagem e runtime;
- se a falha é determinística;
- primeira execução conhecida como boa e primeira ruim, quando houver.

“O algoritmo não funciona” não é reprodução. “No commit X, o fixture com
`A` dependendo de `B` retorna `A,B`, violando `position[B] < position[A]`, em
Python 3.x e Java 17” permite investigar.

## 1. Prove ambiente e linha de base

```bash
git status --short
python3 --version
node --version
java -version
cc --version
dotnet --version
bash 02-OSINT/engenharia-software/testar-curso.sh
```

Não presuma que o binário executado veio do fonte aberto. Confira diretório,
`PYTHONPATH`, classpath, configuração de build e artefatos antigos. O runner do
curso compila em diretório temporário para reduzir contaminação.

Se somente uma linguagem falha, compare semântica antes de culpar o algoritmo:

| Fronteira | Perguntas |
|---|---|
| texto | comparação é ordinal, locale-aware ou por bytes? |
| inteiro | existe overflow, coerção ou precisão limitada? |
| coleção | iteração promete ordem? igualdade e hash concordam? |
| erro | exceção, `Result`, status ou sentinela preserva causa? |
| memória | valor foi copiado, compartilhado, movido ou liberado? |

## 2. Classifique o defeito

### Resultado incorreto

Teste primeiro as invariantes, não a lista inteira:

```text
mesma cardinalidade?
mesmo conjunto, sem duplicatas?
toda aresta u -> v respeita position[u] < position[v]?
desempate prometido foi preservado?
entrada foi modificada sem contrato?
```

Se o conjunto está certo e a relação errada, investigue direção da aresta,
grau e atualização de dependentes. Se a relação está certa, mas a ordem varia,
investigue iteração de hash e comparador total.

### Falha em caso-limite

Reduza para transições: vazio→um, um→vazio, capacidade-1, primeiro/último,
ausente, duplicado, wrap-around. Off-by-one fica mais visível quando você
declara o intervalo (`[low, high)`, por exemplo) e verifica sua preservação a
cada iteração.

### Não termina ou estoura a pilha

Para loop/recursão, identifique uma variante que deve diminuir. Confirme:

- caso-base é alcançável;
- subproblema é estritamente menor;
- vértice é marcado no momento correto;
- estado de backtracking é desfeito;
- memoização usa chave completa;
- profundidade máxima cabe na pilha real.

Converta para pilha explícita quando a profundidade depende de entrada não
confiável. “Tail call” só economiza pilha se a linguagem/runtime garantir.

### Regressão de desempenho

Separe CPU, alocação, I/O e espera. Primeiro conte `V`, `E`, comparações e
operações de heap; depois use profiler. Uma entrada duas vezes maior que leva
quatro vezes mais pode ser coerente com `n²`, efeito de cache ou ruído: repita
com tamanhos suficientes.

Evite estes falsos diagnósticos:

- medir também geração/parse quando a pergunta é o algoritmo;
- comparar primeira execução fria com execução aquecida;
- usar fixture pequeno demais;
- executar debugger/log detalhado dentro da medição;
- comparar implementações com contratos diferentes;
- reportar somente a melhor execução.

### Memória crescente

Determine se o crescimento é pico necessário, cache limitado, retenção
acidental ou vazamento. Procure coleções globais, listeners, closures, slices que
retêm buffers, ciclos e objetos ainda referenciados. Em C, compile uma cópia de
diagnóstico quando suportado:

```bash
cc -std=c17 -g -O1 -fsanitize=address,undefined \
  02-OSINT/engenharia-software/exemplos/c/dependency_graph.c \
  -o /tmp/rte-dependency-graph-asan
/tmp/rte-dependency-graph-asan
unlink /tmp/rte-dependency-graph-asan
```

Sanitizer não prova ausência de defeitos; ele observa caminhos executados.

## 3. Instrumente invariantes, não ruído

Durante a reprodução, registre eventos pequenos:

```text
node=<id> old_indegree=<n> new_indegree=<n-1>
ready=<quantidade> produced=<quantidade>
```

Não imprima o grafo inteiro a cada passo. Asserções temporárias úteis incluem:

- grau nunca negativo;
- item emitido uma única vez;
- `produced <= V`;
- toda dependência indexada existe;
- heap contém somente itens com grau zero ainda não emitidos;
- aplicar/desfazer backtracking restaura o estado anterior.

Depois da correção, transforme a propriedade relevante em teste e remova logs
intrusivos.

## 4. Use diferencial e metamorfismo

Uma implementação simples pode servir de oráculo para entradas pequenas. Para
ordenar, compare com biblioteca; para caminho mínimo pequeno, enumere caminhos;
para topológica, valide propriedades.

Relações metamórficas úteis:

- renomear todos os IDs preserva a estrutura, ajustado o desempate;
- permutar a ordem de entrada não muda resultado determinístico;
- duplicar aresta não muda o grafo quando o contrato usa conjunto;
- adicionar vértice isolado não invalida restrições anteriores;
- multiplicar todos os pesos positivos preserva o caminho mínimo;
- ordenar duas vezes produz o mesmo resultado.

Guarde semente e menor caso que falhou. Aleatoriedade sem reprodução reduz a
utilidade do teste.

## 5. Investigue arquitetura pela direção real

Quando uma mudança toca muitos arquivos, desenhe imports/chamadas reais:

```text
CLI -> caso de uso -> porta <- adapter
                 -> domínio/algoritmo
```

Sinais diagnósticos:

- domínio importa JSON/terminal: detalhe vazou para política;
- teste da regra precisa de arquivo: efeito não foi separado;
- trocar adapter altera algoritmo: contrato está incompleto;
- mocks quebram após renomear método privado: teste acoplado à implementação;
- ciclo de imports: responsabilidade ou contrato está mal posicionado;
- composition root espalhado: decisões de montagem viraram dependências ocultas.

Não responda automaticamente com mais interfaces. Primeiro localize a regra
que muda por motivo diferente.

## 6. Teste instável

Execute o caso isolado e em ordem variada. Procure:

- estado global não restaurado;
- arquivo/porta fixa compartilhada;
- relógio real e fronteira de data;
- aleatoriedade sem seed;
- iteração não ordenada;
- trabalho assíncrono não aguardado;
- dependência de locale/timezone;
- cleanup que apaga recurso de outro teste.

Retry e `sleep` maior escondem o sintoma. Injete relógio, use diretório
temporário exclusivo, aguarde condição observável e limite recursos pelo dono.

## 7. `git bisect` para regressão determinística

Com worktree limpo e um comando que retorna zero no estado bom e não zero no
ruim:

```bash
git bisect start
git bisect bad
git bisect good <commit-conhecido-bom>
git bisect run <seu-script-de-reproducao>
git bisect reset
```

Leia o diff encontrado; o primeiro commit ruim localiza a introdução, não
prova causa. Não use um teste flaky como oráculo de bisect.

## 8. Encerramento do diagnóstico

Uma correção está concluída quando:

- menor reprodução falha antes e passa depois;
- a causa explica todas as evidências relevantes;
- a correção atua na primeira fronteira divergente;
- existe teste de regressão na camada adequada;
- suites adjacentes permanecem verdes;
- desempenho/compatibilidade foram reavaliados;
- logs temporários e artefatos foram removidos;
- commit e, quando necessário, ADR explicam o porquê.

Use o modelo:

```text
sintoma:
impacto e escopo:
menor reprodução:
primeira invariante quebrada:
causa:
correção:
teste de regressão:
riscos/limitações:
```

