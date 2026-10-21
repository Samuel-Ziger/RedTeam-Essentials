# 03 — Validação, erros e feedback ao usuário

Validação protege invariantes e ajuda a pessoa a corrigir uma ação. Tratamento
de erro preserva estado e oferece recuperação quando algo falha. Feedback torna
essas decisões observáveis. “Algo deu errado” não cumpre nenhum desses contratos.
Neste capítulo, o Study Desk ganha falhas tipadas e mensagens acionáveis sem
expor detalhes internos.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- posicionar cada regra na camada que realmente pode garanti-la;
- distinguir erro de campo, regra de domínio, conflito e falha interna;
- modelar falhas esperadas como dados e falhas inesperadas como exceções;
- produzir mensagens úteis sem expor stack trace ou informação sensível;
- preservar entrada e estado confirmado em falhas e cancelamentos;
- testar a relação entre erro interno, feedback e código de saída.

## Pré-requisitos

Reutilize o domínio do capítulo 00, a separação dos canais da CLI do capítulo
01 e a inicialização atômica do capítulo 02. Você deve conhecer exceções, tipos,
testes e funções puras.

## Modelo mental: detectar, classificar, traduzir, recuperar

Um erro percorre fronteiras:

```text
entrada -> detecção -> falha tipada -> política de recuperação
        -> mensagem/código para o usuário + evidência técnica segura
```

Não use a mesma representação em todas as camadas. Uma exceção de biblioteca de
arquivo não é mensagem de produto. A camada de aplicação classifica o problema;
a apresentação escolhe linguagem, campo, formato e canal.

## Camadas de validação

| Camada | O que pode garantir | Exemplo no Study Desk |
|---|---|---|
| parser/controle | sintaxe imediata | `"45"` pode virar inteiro |
| caso de uso | regra contextual | comando permitido no estado atual |
| domínio | invariante durável | duração entre 1 e 1440 |
| persistência | integridade do armazenamento | ID não duplicado |
| apresentação | associação e feedback | erro ligado a `--minutes` |

Uma regra pode ser verificada cedo para melhorar experiência, mas a garantia
continua na fronteira confiável. A CLI pode recusar `minutes=0`; o domínio também
deve recusar porque testes, importação e futura interface chamam o mesmo núcleo.

Evite duplicar constantes manualmente. Exponha metadados ou testes de contrato
para garantir que o intervalo mostrado na ajuda coincide com o aceito.

## Contratos e invariantes do fluxo de erro

Para `RegisterSession.execute`:

- sucesso retorna uma sessão confirmada;
- erro de entrada retorna todos os problemas independentes conhecidos;
- conflito identifica o estado que mudou e permite nova decisão;
- falha de persistência não é rotulada como entrada inválida;
- nenhuma falha anterior à confirmação altera dados;
- uma falha recebe identificador de correlação quando precisa de suporte;
- mensagem pública nunca contém segredo, caminho sensível ou stack trace.

Agrupar erros de campos reduz ciclos de tentativa. Porém, se o documento raiz
não pode ser analisado, não invente erros nos itens que nunca foram lidos.

## Erro como dado

Falhas esperadas formam um vocabulário do produto. Em C#:

```csharp
public enum ErrorKind
{
    Validation,
    Conflict,
    NotFound,
    Persistence,
    Internal
}

public sealed record AppError(
    ErrorKind Kind,
    string Code,
    string MessageKey,
    string? Field = null,
    bool Retryable = false,
    string? SupportId = null);

public abstract record Result<T>
{
    public sealed record Success(T Value) : Result<T>;
    public sealed record Failure(IReadOnlyList<AppError> Errors) : Result<T>;
}
```

`Code` é estável para testes e integrações, como
`session.minutes.out_of_range`. `MessageKey` permite localizar a apresentação.
Não use a frase traduzida como identidade do erro. `Retryable` descreve uma
política conhecida, não um convite genérico para repetir indefinidamente.

Em Java, uma `sealed interface` com variantes; em Python, dataclasses/uniões; em
JavaScript, objetos com `kind` discriminante podem expressar o mesmo modelo. O
importante é impedir combinações incoerentes, como sucesso sem valor.

## Quando usar retorno e quando usar exceção

Use resultado explícito para falhas esperadas e acionáveis: entrada inválida,
item ausente, conflito de revisão. Use exceção quando o contrato normal não pode
continuar: bug, violação de uma suposição interna ou falha inesperada de uma
dependência.

A fronteira da aplicação captura exceções que sabe classificar. Não use
`catch (Exception) { return false; }`: ele apaga causa, confunde categorias e pode
esconder defeito de programa. Se capturar genericamente no topo para evitar
encerrar sem feedback, preserve a causa no diagnóstico seguro e retorne uma falha
interna com ID de suporte.

Não use exceção como navegação esperada em cada campo e não converta toda falha
em booleano. Ambos perdem informação.

## Taxonomia e política de recuperação

| Categoria | Quem pode agir | Recuperação típica |
|---|---|---|
| entrada inválida | usuário | corrigir campo mantendo os demais |
| conflito de estado | usuário/aplicação | comparar, recarregar ou confirmar nova decisão |
| ausência | usuário | escolher outro item ou atualizar lista |
| falha transitória | aplicação | repetir com limite quando a operação é segura |
| dado incompatível | usuário/suporte | migrar, restaurar ou importar cópia |
| falha interna | desenvolvimento/suporte | preservar evidência e corrigir defeito |

“Tente novamente” só é útil se repetir não duplicar efeito. Antes de retry,
defina idempotência, limite, cancelamento e como a pessoa reconhece pendência.

## Mensagem acionável

Uma mensagem útil responde:

1. o que não foi concluído;
2. qual campo ou objeto precisa de atenção;
3. por que, em linguagem adequada;
4. como corrigir ou recuperar;
5. onde encontrar suporte, se necessário.

```text
Não foi possível registrar a sessão.
"Duração" deve ser um número inteiro entre 1 e 1440 minutos.
O valor informado foi preservado para correção.
```

Compare com `ValueError at session.py:37`: isso revela implementação e não
ensina a recuperar. No diagnóstico técnico, guarde classe, cadeia de causas,
operação e ID, aplicando redação de dados sensíveis.

### Vários canais, mesma semântica

Na CLI humana, a frase vai a `stderr`. No modo JSON, retorne um objeto estável:

```json
{
  "schemaVersion": 1,
  "ok": false,
  "errors": [
    {
      "code": "session.minutes.out_of_range",
      "field": "minutes",
      "retryable": false
    }
  ]
}
```

O modo de máquina não precisa receber texto localizado como contrato. A saída
humana e a estruturada devem mapear para a mesma categoria e o mesmo código de
saída do processo.

## Preserve trabalho e estado confirmado

Quando uma entrada falha:

- mantenha valores digitados, inclusive o inválido para edição;
- associe o erro ao campo e, em GUI/web, a um resumo acessível;
- não limpe o formulário nem descarte filtros sem necessidade;
- impeça submissão duplicada durante a operação;
- diferencie “não iniciado”, “pendente”, “confirmado” e “falhou”;
- ofereça cancelar ou desfazer quando o contrato permitir.

Na CLI, preservar entrada significa não alterar dados existentes e mostrar um
comando ou orientação corrigível. Na futura interface gráfica, significa manter
campos e foco coerentes. A regra de negócio é a mesma.

## Validação e importação atômica

Uma importação nunca deve aplicar itens conforme os analisa se o contrato promete
“tudo ou nada”:

```text
bytes limitados -> parse -> schema -> todos os objetos de domínio
                -> plano/resumo -> confirmação -> uma gravação
```

Crie primeiro um candidato em memória. Se o item 80 de 100 falhar, reporte sua
posição e mantenha o repositório anterior. Se a operação permite importação
parcial, isso deve ser outra opção explícita com resultado por item; não um efeito
acidental.

## Operações demoradas e cancelamento

Feedback deve aparecer cedo sem simular progresso falso. Modele:

```text
idle -> running -> succeeded
                -> failed
                -> cancelling -> cancelled
```

Cancelamento é uma solicitação, não garantia instantânea. O caso de uso verifica
o sinal em pontos seguros, interrompe antes da confirmação e informa o que ficou
preservado. Depois de um commit irreversível, a interface não deve afirmar que
cancelou; pode oferecer uma operação compensatória.

## Falhas comuns e diagnóstico

| Sintoma | Causa provável | Como localizar |
|---|---|---|
| regra aceita pela importação, rejeitada pela CLI | invariante duplicada | teste o mesmo valor pelos dois adaptadores |
| mensagem sempre genérica | categoria foi apagada cedo | inspecione cada tradução do erro |
| retry duplica sessão | operação não idempotente | injete falha após salvar e repita |
| erro de campo perde entrada | apresentação reinicializa modelo | teste estado antes/depois da falha |
| stack trace aparece no JSON | exceção foi serializada | use sentinelas no teste de saída |
| erro esperado vira código 10 | mapeamento incompleto | teste tabela `ErrorKind`→exit code |

Comece pela evidência observável: entrada, estado anterior, resultado, estado
posterior e ID de suporte. Localize onde uma categoria foi perdida. Não corrija a
frase antes de confirmar se o estado também foi preservado.

## Exercícios em três níveis

### Nível 1 — classificação

Reescreva dez mensagens genéricas do Study Desk. Para cada uma, indique categoria,
ator que pode agir, próxima ação e informação que não deve ser exposta.

**Critérios de aceite:** mensagens distinguem entrada, conflito e falha interna;
nenhuma recomenda retry sem condição; campo e recuperação estão claros.

### Nível 2 — resultado tipado

Implemente resultado discriminado e mapeadores para texto, JSON e código de saída.
Cubra título vazio, duração fora do limite, item ausente e falha simulada do
repositório.

**Critérios de aceite:** sucesso sem valor e falha sem erro são impossíveis ou
rejeitados; texto e JSON mantêm a mesma semântica; detalhes internos não vazam.

### Nível 3 — atomicidade e cancelamento

Construa uma importação em memória com validação de todos os itens, confirmação
e cancelamento em ponto seguro. Injete falhas em cada etapa.

**Critérios de aceite:** antes da confirmação, toda falha preserva estado byte a
byte equivalente; cancelamento tem estado final explícito; diagnóstico correlaciona
a falha sem incluir dados das sessões.

## Checklist de domínio

- [ ] Sei em qual camada cada regra deve ser garantida.
- [ ] Distingo erro esperado, conflito, falha transitória e defeito interno.
- [ ] Uso tipo/código estável em vez da frase como identidade do erro.
- [ ] Preservo trabalho digitado e estado confirmado quando uma ação falha.
- [ ] Traduzo detalhes técnicos em feedback acionável e seguro.
- [ ] Só repito automaticamente operações cujo efeito está controlado.
- [ ] Modelo cancelamento como transição, não como interrupção mágica.
- [ ] Testo resultado, estado e evidência de diagnóstico juntos.
