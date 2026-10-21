# 06 — Interfaces gráficas desktop

Uma interface desktop não é apenas uma biblioteca que desenha botões. Ela é um
adaptador entre pessoas, eventos do toolkit e casos de uso da aplicação. Quando
essa fronteira é mal definida, validação, persistência e regras acabam presas aos
widgets; quando é bem definida, o mesmo núcleo pode servir uma GUI, uma CLI e
testes automatizados.

Este capítulo usa o [Study Desk](projetos/study-desk/README.md) como referência.
A versão principal dele é web e local-first, mas suas regras — registrar uma
sessão, filtrar estudos, importar dados e calcular totais — também poderiam ser
apresentadas por uma janela desktop. O objetivo não é eleger um toolkit, e sim
aprender contratos que continuam válidos ao trocar de tecnologia.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. explicar o loop de eventos sem confundi-lo com as regras de negócio;
2. separar View, estado de apresentação, casos de uso e persistência;
3. modelar estados de espera, vazio, erro, sucesso, edição e alteração não salva;
4. manter operações demoradas fora do callback visual e tratar cancelamento;
5. criar layout utilizável com teclado, zoom, tema e conteúdo variável;
6. testar a maior parte do comportamento sem abrir uma janela;
7. diagnosticar congelamento, evento duplicado, estado obsoleto e perda de foco;
8. escolher um toolkit por requisitos de produto, não apenas por familiaridade.

## Pré-requisitos e modelo mental

Você deve conhecer funções, objetos, eventos, validação e o fluxo de estado do
[capítulo 05](05-estado-eventos.md). Não é necessário conhecer detalhes de
processos, escalonamento ou drivers; esses assuntos pertencem à trilha de
Sistemas Operacionais.

Use este mapa ao analisar qualquer GUI:

```text
pessoa
  -> gesto (clique, teclado, toque, fechamento)
  -> evento do toolkit
  -> comando do presenter/view model
  -> caso de uso e regra de domínio
  -> resultado tipado
  -> novo estado de apresentação
  -> renderização + foco + anúncio acessível
```

O toolkit é dono do **loop de eventos**. Ele espera entrada, despacha callbacks,
calcula layout e redesenha a janela. Seu código participa desse fluxo; não deve
substituí-lo nem bloquear sua execução. A regra de negócio, por outro lado, não
precisa saber que existe uma janela.

## Escolha de toolkit como decisão de produto

| Linguagem | Opções comuns | Perguntas antes da escolha |
|---|---|---|
| Python | Tkinter, PySide/PyQt, GTK | distribuição simples ou aparência nativa? licença compatível? |
| Java | Swing, JavaFX | runtime alvo inclui o toolkit? biblioteca tem suporte ativo? |
| C | GTK, APIs nativas | quem administra ownership, callbacks e bindings? |
| C# | WPF, WinUI, Avalonia, .NET MAUI | quais plataformas e versões precisam funcionar? |
| JavaScript | Electron, Tauri com frontend web | tamanho, integração nativa e atualização compensam o runtime? |

Nenhuma linha da tabela é uma recomendação universal. Registre uma decisão curta
com: plataformas suportadas, licença, acessibilidade, tamanho do pacote,
capacidade da equipe, integração exigida, estratégia de teste e manutenção
esperada. Uma biblioteca madura que atende ao contrato costuma ser melhor que a
opção mais recente.

## O loop de eventos e a regra de não bloquear

Este exemplo Tkinter é executável com a biblioteca padrão do Python. A função
`calculate_total` é independente da janela; o callback apenas traduz entrada e
saída:

```python
import tkinter as tk
from tkinter import ttk


def calculate_total(raw_minutes: str) -> str:
    try:
        minutes = int(raw_minutes)
    except ValueError as error:
        raise ValueError("Informe minutos como número inteiro.") from error
    if not 1 <= minutes <= 1_440:
        raise ValueError("A duração deve ficar entre 1 e 1440 minutos.")
    return f"Total registrado: {minutes} min"


root = tk.Tk()
root.title("Study Desk")
minutes = tk.StringVar()
feedback = tk.StringVar(value="Informe a duração da sessão.")


def submit() -> None:
    try:
        feedback.set(calculate_total(minutes.get()))
    except ValueError as error:
        feedback.set(str(error))
        entry.focus_set()


frame = ttk.Frame(root, padding=16)
frame.grid(sticky="nsew")
ttk.Label(frame, text="Duração em minutos").grid(row=0, column=0, sticky="w")
entry = ttk.Entry(frame, textvariable=minutes)
entry.grid(row=1, column=0, sticky="ew")
ttk.Button(frame, text="Registrar", command=submit).grid(row=2, column=0, pady=8)
ttk.Label(frame, textvariable=feedback, wraplength=320).grid(row=3, column=0)
entry.focus_set()
root.mainloop()
```

O exemplo é pequeno, mas já expõe duas fronteiras. `calculate_total` pode receber
testes de unidade; o callback é responsável por foco e feedback. Em um produto,
o caso de uso retornaria um tipo como `Success` ou `ValidationError`, em vez de a
View interpretar mensagens arbitrárias.

Operações demoradas não podem executar diretamente em `submit`. A interface
ficaria sem responder, sem repintar e sem aceitar cancelamento. Use a abstração
assíncrona oferecida pelo toolkit e publique o resultado de volta pelo mecanismo
apropriado da UI. O contrato mínimo de uma operação demorada deve responder:

- como iniciar e impedir submissões duplicadas;
- como representar progresso quando ele é mensurável;
- o que “cancelar” garante e o que já pode ter sido concluído;
- como descartar uma resposta de uma operação antiga;
- como recuperar o foco e preservar a entrada após falha.

## Separação entre View, apresentação e domínio

Uma estrutura prática é Model–View–Presentation:

```text
View: widgets, foco e eventos do toolkit
  -> Presenter/ViewModel: estado visual e comandos
      -> caso de uso: regras e resultados do domínio
          -> porta de persistência: contrato de leitura/escrita
```

Considere a tela “Nova sessão” do Study Desk. O presenter pode expor:

```text
StudyFormState
  title: texto atual
  minutes: texto atual
  fieldErrors: mapa campo -> mensagem
  phase: editing | saving | saved | failed
  canSubmit: valor derivado
```

A View envia `TITLE_CHANGED`, `MINUTES_CHANGED`, `SUBMIT_REQUESTED` e
`CANCEL_REQUESTED`. O presenter valida o formato necessário para a interação; o
caso de uso protege as invariantes definitivas. A View não soma minutos, não abre
arquivo diretamente e não decide qual erro pode ser ignorado.

Evite também transformar o presenter em um “objeto Deus”. Separe por jornada:
lista de sessões, formulário, importação e preferências podem ter estados menores.
Um estado global só se justifica quando dois fluxos realmente precisam compartilhar
a mesma fonte de verdade.

## Estados de interface são parte do contrato

Uma tela de lista profissional precisa desenhar mais que o caminho feliz:

| Estado | Conteúdo | Ações possíveis | Foco/feedback esperado |
|---|---|---|---|
| inicial | instrução curta | carregar ou criar | primeira ação útil |
| carregando | indicador e contexto | cancelar, se suportado | não mover foco sem motivo |
| vazio | explicação e próximo passo | registrar sessão | ação primária alcançável |
| sucesso | itens e total | editar, filtrar, exportar | preservar posição lógica |
| erro recuperável | causa compreensível | tentar novamente | mensagem associada à ação |
| alteração não salva | rascunho íntegro | salvar, descartar, voltar | confirmação previsível |

Não sobreponha estados incompatíveis com vários booleanos independentes, como
`loading=true`, `saved=true` e `error=true`. Use uma fase discriminada e dados
associados. Preserve conteúdo estável durante uma atualização sempre que isso
reduzir interrupção; mostre que ele pode estar desatualizado.

Ações destrutivas precisam de proporcionalidade. Remover uma sessão que pode ser
desfeita talvez não exija diálogo. Apagar todo o histórico sem restauração exige
confirmação que identifica o impacto. Desabilitar um comando deve ter motivo
compreensível; às vezes permitir o comando e explicar a correção é mais acessível
que um botão permanentemente opaco.

## Layout, escala e acessibilidade

Posicionar widgets por coordenadas absolutas cria telas que quebram quando a
fonte cresce ou o texto é traduzido. Prefira containers, constraints, tamanhos
preferidos e conteúdo que determine altura. Verifique:

- texto ampliado e traduções maiores;
- janela estreita e redimensionamento gradual;
- ordem de foco coerente com a leitura;
- operação completa sem mouse;
- nome, função e estado expostos ao recurso de acessibilidade do toolkit;
- alto contraste, temas claro/escuro e foco visível;
- mensagens que não dependem apenas de cor ou ícone;
- atalhos que respeitam convenções e não colidem com digitação.

Um botão, item de menu e atalho que executam “Salvar” devem invocar o mesmo
comando. O comando informa se está disponível; cada controle apenas apresenta
essa capacidade. Isso evita três implementações divergentes da mesma regra.

Diálogos exigem cuidado: nome acessível, foco inicial deliberado, contenção de
foco enquanto modal e retorno ao acionador ao fechar. Não abra um diálogo para
toda mensagem. Feedback inline ou uma região de status costuma preservar melhor
o contexto.

## Ciclo de vida e dados não salvos

Desenhe explicitamente:

1. primeira execução sem dados;
2. reabertura com formato antigo que precisa de migração;
3. documento incompatível ou parcialmente inválido;
4. fechamento com alteração não salva;
5. várias janelas sobre o mesmo dado;
6. recuperação de rascunho após interrupção;
7. atualização da aplicação e possível rollback;
8. exportação antes de remover dados locais.

“Perguntar ao fechar” não basta. Se salvar falhar, a janela não deve desaparecer.
Se o documento foi alterado externamente, sobrescrever silenciosamente perde
trabalho. Para o Study Desk, uma política possível é guardar rascunho separado,
comparar a versão conhecida antes de substituir e permitir exportação manual.

## Testes em camadas

Concentre testes rápidos onde há lógica:

- **domínio:** duração válida, totais e invariantes;
- **presenter/reducer:** eventos, transições, mensagens e comandos habilitados;
- **adaptadores:** leitura, gravação e serialização com fakes controlados;
- **integração visual:** binding, foco, teclado e ciclo de vida do toolkit;
- **jornada:** poucos fluxos completos em ambiente representativo.

Um teste do presenter pode simular `SaveFailed` e comprovar que o rascunho
permanece. Um teste visual comprova que o erro recebe foco ou é anunciado. Captura
de tela ajuda em regressão visual, mas não prova semântica ou operação por teclado.

Nas cinco linguagens, mantenha a mesma arquitetura conceitual. Python e JavaScript
podem usar funções e objetos simples; Java e C# podem expressar portas por
interfaces; C pode usar `struct` de contexto e ponteiros de função. O objetivo não
é forçar classes, e sim manter dependências dirigidas ao núcleo.

## Falhas frequentes e diagnóstico

| Sintoma | Hipótese provável | Evidência útil | Correção típica |
|---|---|---|---|
| janela congela | callback fez trabalho demorado | duração do handler e estado visual | mover trabalho e publicar resultado |
| ação ocorre duas vezes | listener registrado em duplicidade | contador por comando/instância | ciclo de registro e descarte explícito |
| resultado antigo aparece | respostas chegaram fora de ordem | ID da operação no log | cancelar ou ignorar ID obsoleto |
| foco “some” | widget focado foi removido | sequência de eventos de foco | escolher destino lógico após render |
| botão e menu divergem | regra duplicada | caminhos de chamada distintos | comando único compartilhado |
| dados somem ao fechar | falha de gravação ignorada | resultado do caso de uso | manter janela/rascunho e informar |

Diagnostique a transição, não apenas a tela final. Registre nomes de eventos,
fase anterior, próxima fase e um identificador efêmero de operação; nunca inclua
conteúdo pessoal, token ou documento completo no log. O
[capítulo 11](11-logs-diagnostico.md) aprofunda essa disciplina.

## Exercícios em três níveis

### Nível 1 — Compreensão e implementação guiada

1. Execute o exemplo Tkinter e escreva testes para `calculate_total`.
2. Acrescente campo de título, validação e mensagem associada ao campo inválido.
3. Documente a ordem de foco e percorra toda a tela apenas com teclado.

**Critérios de aceite:** valores `0`, `1`, `1440`, `1441` e texto não numérico têm
resultado definido; a regra é testada sem GUI; nenhum erro apaga os valores
digitados; o foco continua visível.

### Nível 2 — Integração e estados adversos

Implemente uma lista desktop de sessões sobre uma porta de repositório em memória.
Modele vazio, sucesso, salvando e falha. Simule uma gravação demorada, impeça
submissão duplicada e ofereça cancelamento sem prometer reverter algo já salvo.

**Critérios de aceite:** a janela continua utilizável; apenas o resultado da
operação vigente altera o estado; erro preserva o rascunho; presenter possui
testes determinísticos; a jornada funciona com teclado e texto ampliado.

### Nível 3 — Projeto e decisão técnica

Escolha um toolkit para portar as jornadas principais do Study Desk. Produza uma
decisão arquitetural, um protótipo e uma matriz de estados. Implemente registrar,
editar, excluir com desfazer e exportar dados. Teste fechamento com alteração não
salva e falha injetada de persistência.

**Critérios de aceite:** escolha justificada por requisitos; núcleo não importa o
toolkit; ações equivalentes compartilham comando; não há perda silenciosa;
acessibilidade e ciclo de vida têm evidências manuais e automatizadas; pacote de
diagnóstico não contém os títulos das sessões.

## Checklist de conclusão

- [ ] Sei explicar quem controla o loop de eventos.
- [ ] Regras e persistência não dependem de widgets.
- [ ] Modelei vazio, espera, sucesso, erro e alteração não salva.
- [ ] Operação lenta não bloqueia a interface e possui cancelamento honesto.
- [ ] Resposta obsoleta não substitui a operação vigente.
- [ ] Layout suporta escala, tradução, teclado e alto contraste.
- [ ] Botão, menu e atalho usam o mesmo comando.
- [ ] Fechamento e falha de salvamento não perdem trabalho silenciosamente.
- [ ] Testes do presenter rodam sem janela; poucos testes cobrem integração real.
- [ ] Logs de diagnóstico não expõem conteúdo ou credenciais.
