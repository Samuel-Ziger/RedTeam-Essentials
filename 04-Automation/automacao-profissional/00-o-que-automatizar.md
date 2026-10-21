# 00 — O que automatizar: decisão, escopo e risco

Automatizar não é transformar uma lista de cliques em código. É delegar decisões e
efeitos a um sistema que pode operar mais rápido, mais vezes e com alcance maior que
uma pessoa. Se o processo original é ambíguo, a automação multiplica ambiguidade. Se
o processo é perigoso, ela multiplica impacto.

Este capítulo ensina a decidir **se**, **quanto** e **como** automatizar antes de
escrever o primeiro executor.

## Objetivos

Ao final, você será capaz de:

- separar tarefa, processo, regra e decisão humana;
- estimar valor, custo total, risco e reversibilidade;
- escolher um nível de autonomia proporcional à evidência;
- desenhar fronteiras, aprovações e condições de interrupção;
- especificar um experimento pequeno antes de construir a solução definitiva.

## Pré-requisitos

Você deve conhecer funções, coleções, exceções, arquivos, testes e linha de
comando. Os módulos 00–03 fornecem essa base. Aqui o foco não é sintaxe, mas a
engenharia do comportamento repetível.

## 1. Tarefa não é processo

Uma tarefa é uma ação: copiar um arquivo, consultar um endpoint, gerar um relatório.
Um processo inclui contexto, decisões, exceções, aprovações e confirmação do
resultado. Automatizar apenas o caminho feliz costuma esconder o trabalho real.

Mapeie o processo observado, não o processo imaginado:

~~~text
gatilho -> receber -> validar -> planejar -> aprovar -> executar
        -> verificar -> registrar -> recuperar ou encerrar
~~~

Para cada etapa, registre:

| Pergunta | Exemplo |
|---|---|
| Quem ou o que inicia? | envio manual, agenda, evento |
| Qual entrada é aceita? | CSV UTF-8 com até 10 mil registros |
| Quem decide exceções? | operador do processo |
| Qual efeito ocorre? | novo arquivo, mensagem, alteração remota |
| Como confirmar? | hash, resposta validada, contagem reconciliada |
| Como interromper? | cancelamento cooperativo, bloqueio de aplicação |
| Como recuperar? | repetir, retomar, compensar ou escalar |

Uma frase como “mandar um e-mail se falhar” descreve notificação, não
recuperação. O processo continua incompleto se ninguém sabe quais efeitos já foram
confirmados.

## 2. Critérios de um bom candidato

Um candidato forte costuma ser frequente, baseado em regras, verificável e
reversível. Use uma matriz em vez de intuição:

| Dimensão | Pergunta | Sinal favorável |
|---|---|---|
| frequência | quantas vezes por período? | repetição suficiente para pagar manutenção |
| variação | os casos seguem regras? | poucas exceções bem definidas |
| verificabilidade | o sucesso é mensurável? | pós-condição objetiva |
| reversibilidade | um efeito pode ser desfeito? | restauração ou compensação segura |
| estabilidade | contratos mudam com que frequência? | interface versionada |
| impacto | uma falha afeta quantos itens? | blast radius limitado |
| sensibilidade | quais dados e poderes estão envolvidos? | menor privilégio possível |

Não automatize por completo uma decisão ética, aprovação financeira ou mudança
irreversível apenas porque a parte mecânica é simples. A melhor solução pode ser um
checklist assistido, um validador ou um gerador de plano sujeito a aprovação.

## 3. Valor e custo total

O cálculo ingênuo usa apenas horas poupadas:

~~~text
economia bruta = execuções x duração manual
~~~

O custo real inclui descoberta, desenvolvimento, testes, credenciais, ambientes,
dependências, observação, mudanças externas, suporte e desativação. Um modelo útil:

~~~text
valor líquido = tempo poupado + erros evitados + feedback antecipado
              - construção - operação - mudança - risco residual
~~~

Não transforme a fórmula em falsa precisão. Registre hipóteses: volume mensal,
taxa de exceção, custo de incidente e vida útil esperada. Revise depois do piloto.

### Exemplo

Uma pessoa consolida 20 arquivos por semana em 45 minutos. A automação pouparia
três horas mensais, mas o formato muda toda semana e apenas uma pessoa entende as
regras. Antes de construir um serviço, crie validação de schema e relatório de
divergências. Esse passo reduz erro e revela as regras ainda implícitas.

## 4. Níveis de autonomia

Autonomia não é binária. Adote o menor nível que entrega valor:

1. **observar:** mede o processo sem recomendar;
2. **recomendar:** aponta ações, mas não gera efeitos;
3. **planejar:** produz plano completo para aprovação;
4. **aplicar com confirmação:** executa efeito delimitado e reversível;
5. **aplicar automaticamente:** atua dentro de limites e escala exceções;
6. **recuperar automaticamente:** retoma ou compensa falhas conhecidas.

Subir de nível exige evidência: taxa de acerto, falhas injetadas, recuperação
ensaiada e visibilidade operacional. Não use confiança no autor como controle.

## 5. Fronteiras e blast radius

Uma automação deve ter limites mensuráveis:

- quantidade máxima por execução;
- tamanho total de entrada e saída;
- tempo máximo e tentativas;
- identidades, ambientes e recursos permitidos;
- tipos de efeito e extensões aceitas;
- taxa de erro que interrompe o lote;
- janela de mudança e aprovação;
- botão de parada e comportamento ao cancelar.

O cancelamento não volta no tempo. Ele impede novo trabalho e aguarda ou encerra
o que está em andamento segundo um contrato. Os efeitos confirmados continuam
existindo e devem aparecer no relatório.

## 6. Da narrativa ao contrato

Considere: “organizar os relatórios recebidos”. Isso ainda não é requisito. Pergunte:

- quais arquivos contam como relatório?
- nomes iguais significam mesmo conteúdo?
- o original pode ser removido?
- subdiretórios são preservados?
- links simbólicos são aceitos?
- colisão sobrescreve, versiona ou bloqueia?
- qual evidência prova o resultado?

Uma primeira especificação segura poderia ser:

~~~text
Descobrir arquivos regulares .txt e .log sob uma raiz autorizada,
sem seguir links. Gerar um plano ordenado. Copiar apenas destinos
ausentes, verificar SHA-256, nunca remover origem e abortar o lote
antes do primeiro efeito se houver colisão diferente.
~~~

Agora existem entradas, efeitos, não objetivos e pós-condições testáveis.

## 7. Piloto e critérios de saída

O piloto deve operar sobre dados sintéticos ou cópias, em volume reduzido. Defina
antes o que encerra, expande ou cancela o experimento:

- encerra com sucesso: cem casos reconciliados, zero sobrescrita e runbook testado;
- expande: falhas conhecidas estão cobertas e o ganho foi observado;
- pausa: contrato externo instável ou exceções acima do limite;
- cancela: benefício menor que operação ou risco não mitigável.

Desativar também é parte do ciclo de vida. Defina responsável, data de revisão e
como retirar agenda, credencial, armazenamento e alertas.

## Falhas comuns e diagnóstico

| Sintoma | Causa provável | Experimento seguro |
|---|---|---|
| muitas exceções manuais | regra ainda implícita | classificar 30 casos reais sanitizados |
| ganho menor que o esperado | custo de triagem omitido | medir tempo ponta a ponta |
| operador não confia no plano | justificativa ausente | incluir regra e evidência por item |
| incidente afeta lote inteiro | limite tardio | aplicar canário e limite de itens |
| ninguém consegue desligar | ownership indefinido | ensaiar parada e remoção |

## Exercícios

### Nível 1 — classificar

Avalie cinco tarefas pela matriz deste capítulo. **Aceite:** cada decisão cita
frequência, verificabilidade, reversibilidade e impacto.

### Nível 2 — modelar

Desenhe o processo completo de uma importação de dados e marque fronteiras de
confiança e aprovação. **Aceite:** o desenho inclui confirmação, falha parcial,
cancelamento e recuperação.

### Nível 3 — defender

Produza proposta de piloto e apresente-a como se outra equipe fosse operá-la.
**Aceite:** há critérios de sucesso, pausa, rollback, ownership e desativação.

## Checklist

- [ ] O processo manual e suas exceções foram observados.
- [ ] Sucesso e falha são verificáveis por outra pessoa.
- [ ] O nível de autonomia é proporcional ao risco.
- [ ] O blast radius possui limites explícitos.
- [ ] Aprovação e cancelamento têm comportamento definido.
- [ ] O piloto usa dados controlados e critérios de saída.

