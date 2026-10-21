# 08 — Automação de navegador, planilhas e documentos

Automação de interface trabalha sobre uma representação destinada a pessoas e
por isso é mais frágil que uma API. Use-a para jornadas legítimas e autorizadas,
nunca para contornar CAPTCHA, autenticação, limites ou controle de acesso.

## Objetivos

- decidir quando UI automation é justificável;
- usar locators semânticos e esperas por condição;
- isolar sessão, dados, downloads e evidências;
- gerar CSV, planilha e documentos sem interpretação perigosa;
- validar templates e publicar artefatos deterministicamente.

## 1. Ordem de preferência

1. biblioteca/função local;
2. API oficial estável;
3. exportação/importação documentada;
4. automação do navegador;
5. coordenadas de tela apenas em ambiente rigidamente controlado.

Uma API costuma oferecer contrato, erros estruturados e versionamento. UI muda por
layout, tradução, teste A/B e estado visual. Se a UI for necessária, registre a
jornada suportada e ownership de manutenção.

## 2. Ambiente e identidade

Use conta de teste ou identidade dedicada com menor privilégio. Separe perfis por
ambiente e não reutilize o perfil pessoal do navegador. Configure:

- base URL permitida;
- diretório temporário de download;
- locale, zona e viewport quando relevantes;
- política de cookies e storage;
- limpeza após execução;
- retenção sanitizada de screenshot, trace e vídeo.

Captura pode conter token, mensagem, nome ou documento. Gere apenas na falha quando
possível, restrinja acesso e remova segundo retenção.

## 3. Locators semânticos

Prefira papel, nome acessível, rótulo e texto estável. Se o produto oferece test ID,
trate-o como contrato explícito.

~~~javascript
await page.getByRole("button", { name: "Gerar relatório" }).click();
await page.getByLabel("Período").fill("2026-10");
await expect(page.getByRole("status")).toHaveText("Relatório pronto");
~~~

Evite seletores por posição, classes de estilo e cadeias longas de DOM. Um locator
que encontra dois elementos deve falhar: escolher o primeiro oculta ambiguidade.

## 4. Espera por condição

Sleep fixo é simultaneamente lento e instável. Aguarde o estado observável:

- controle habilitado;
- resposta ou evento esperado;
- URL/estado de navegação;
- arquivo concluído;
- texto/status final;
- spinner ausente **e** resultado presente.

Não dependa apenas de network idle: aplicações com telemetria ou conexão longa
podem nunca ficar ociosas. Toda espera tem timeout e diagnóstico do estado visto.

## 5. Jornada e pós-condição

Clique bem-sucedido não prova efeito. Depois de submeter:

1. observe a confirmação da interface;
2. capture identificador do resultado;
3. consulte o estado por API ou UI quando possível;
4. registre evidência sem dado sensível;
5. torne repetível ou detecte duplicata.

Se uma queda ocorrer entre clique e confirmação, o estado é incerto. Não clique
novamente até reconciliar.

## 6. Downloads e uploads

Para upload, valide arquivo, tamanho e tipo antes de selecionar. Nunca aceite
caminho vindo de fonte não confiável sem raiz autorizada.

Para download:

- aguarde o evento de download;
- grave em diretório temporário exclusivo;
- limite tamanho e tempo;
- valide nome lógico, Content-Type e assinatura/magic bytes quando aplicável;
- calcule hash e parseie antes de publicar;
- não confie no nome sugerido pelo servidor.

## 7. CSV e injeção de fórmula

CSV não carrega tipo formal. Planilhas podem interpretar célula iniciada por
sinais como igual, mais, menos ou arroba como fórmula. Dados não confiáveis nunca
devem virar código por acidente.

Defina o consumidor. Para exportação humana a planilha, aplique estratégia segura
documentada e teste no software suportado. Para intercâmbio entre sistemas,
prefira formato tipado como JSON com schema, quando possível.

Além disso, use biblioteca CSV para quoting, newline e delimitador. Locale altera
separador decimal e, em algumas ferramentas, delimitador de colunas; não deixe que
a configuração da máquina mude o contrato silenciosamente.

## 8. Planilhas

Modele a planilha como schema:

| Coluna | Tipo lógico | Obrigatória | Regra |
|---|---|---:|---|
| customer_id | texto | sim | ID opaco, não número |
| amount_minor | inteiro | sim | maior ou igual a zero |
| event_date | data ISO | sim | AAAA-MM-DD |
| note | texto | não | máximo e sem fórmula |

ID com zero inicial deve permanecer texto. Datas armazenadas como números seriais
dependem do formato. Fórmula e valor calculado são coisas diferentes; defina qual
o leitor usa.

## 9. Templates e documentos

Template separa conteúdo de layout. Antes de gerar em lote:

1. inventarie placeholders esperados;
2. rejeite ausentes, duplicados ou desconhecidos conforme contrato;
3. escape conteúdo para o formato alvo;
4. gere em diretório temporário;
5. reabra/parseie o resultado;
6. verifique páginas, campos e tamanho;
7. publique atomicamente.

Substituição textual em XML, HTML ou documento compactado pode quebrar estrutura
e permitir injeção. Use a biblioteca do formato e APIs de texto.

## 10. PDF e renderização

PDF visualmente correto pode ter texto inacessível, fonte ausente ou página
cortada. Teste:

- contagem e tamanho de páginas;
- texto esperado extraível;
- fontes e caracteres especiais;
- tags/ordem de leitura quando acessibilidade for requisito;
- determinismo ou campos variáveis excluídos do digest;
- impressão em configuração suportada.

Golden screenshot detecta mudança visual, mas é sensível a fonte e renderizador.
Combine com asserts estruturais e tolerância justificada.

## 11. Termos, privacidade e limites

Automatize apenas sistemas próprios ou autorizados e respeite termos e quotas.
CAPTCHA é sinal de que o sistema exige interação ou outra integração; não o
contorne. Não use sessão de outra pessoa nem armazene credenciais no script.

## Falhas e diagnóstico

| Sintoma | Causa | Evidência |
|---|---|---|
| teste flaky | sleep/seletor estrutural | trace sanitizado e locator |
| duplicou envio | retry após estado incerto | ID e consulta do resultado |
| CSV executa fórmula | campo não neutralizado | fixture com prefixos perigosos |
| documento corrompido | substituição textual | validação do formato |
| funciona só local | locale/fonte/perfil | ambiente fixado |

## Exercícios

### Nível 1 — jornada semântica

Automatize formulário local por papel/rótulo e condição. **Aceite:** zero sleep
fixo e uma alteração de layout não quebra a jornada.

### Nível 2 — exportação

Gere CSV com Unicode, aspas, newline e prefixos de fórmula. **Aceite:** round-trip
preserva dados e o consumidor suportado não interpreta texto como fórmula.

### Nível 3 — documentos

Gere cem documentos com staging e validação. **Aceite:** placeholder ausente
aborta antes da publicação, relatório reconcilia todos e artefatos são sanitizados.

## Checklist

- [ ] API foi considerada antes da UI.
- [ ] Conta, perfil, URL e dados são isolados.
- [ ] Locators usam semântica e esperas observam condição.
- [ ] Efeito é confirmado além do clique.
- [ ] CSV/planilha não interpreta dado como fórmula.
- [ ] Templates são validados e artefatos publicados atomicamente.

