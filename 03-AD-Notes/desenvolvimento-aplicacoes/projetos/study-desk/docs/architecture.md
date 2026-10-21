# Arquitetura executável do Study Desk

## Contexto e fronteiras

O Study Desk registra sessões de estudo no navegador. A versão atual não possui
servidor, conta, sincronização ou telemetria. O navegador é simultaneamente a
plataforma de interface e o limite de persistência:

```text
pessoa -> HTML/DOM -> app.mjs -> reducer/domain.mjs -> novo estado
                              -> repository.mjs -> localStorage do origin
                              -> DOM/textContent -> pessoa
```

“Local-first” descreve a experiência desta versão: leitura e escrita principais
acontecem localmente. Não significa backup, segredo, disponibilidade permanente
ou acesso em outro perfil. Dados de Web Storage podem ser apagados pela pessoa,
pelo navegador ou por políticas do ambiente.

## Componentes e direção das dependências

```text
index.html + styles.css -------- estrutura, semântica e apresentação
             ^
             |
          app.mjs -------------- composition root, eventos e renderização
          /     \
         v       v
 domain.mjs     repository.mjs -- adapter para Storage
 contratos       |
 estado puro     v
             Web Storage
```

- `domain.mjs` não importa DOM, navegador ou armazenamento;
- `repository.mjs` converte entre documento versionado e a interface `Storage`;
- `app.mjs` escolhe o adapter concreto, conecta eventos e traduz falhas em
  feedback;
- `index.html` fornece semântica nativa antes de JavaScript;
- `styles.css` trata reflow, foco, contraste, movimento e cores forçadas.

O contrato do repositório é estrutural: qualquer objeto com `getItem`, `setItem`
e `removeItem` pode ser injetado. Os testes usam `MemoryStorage`; a aplicação usa
`localStorage`. A política de sessão não precisa conhecer nenhum dos dois.

## Fluxo de escrita com rollback

1. o handler converte valores do formulário em `createSession`;
2. o domínio valida todos os campos e produz objeto congelado;
3. `reducer` valida o evento e calcula um novo estado sem alterar o anterior;
4. `dispatch` tenta persistir o novo snapshot;
5. se `setItem` falhar, `dispatch` restaura a referência do estado anterior;
6. só depois do commit local a interface confirma sucesso.

Esse rollback cobre o estado em memória. Web Storage não oferece transação entre
chaves; por isso o snapshot de sessões usa uma única chave. Preferência de tema
é independente e sua falha não deve impedir o uso das sessões.

## Fluxo de importação

```text
arquivo -> limite de bytes -> texto -> JSON -> schema exato
        -> versão -> limites -> sessões -> IDs/datas/tipos
        -> resumo e confirmação -> reducer -> persistência -> renderização
```

Nenhum valor importado chega ao estado antes de o documento inteiro passar. A
renderização usa `textContent`, nunca interpreta título importado como HTML. A
versão futura é recusada; aceitar silenciosamente campos desconhecidos tornaria
impossível distinguir dado novo de erro de digitação.

## Invariantes

- IDs usam ASCII operacional seguro e são únicos no snapshot;
- título é não vazio, sem espaço externo, controles ou mais de 80 unidades de
  código UTF-16 (o mesmo limite de `maxlength`);
- minutos são inteiros entre 1 e 1.440;
- datas são instantes UTC canônicos com milissegundos e sufixo `Z`;
- o documento possui somente `schemaVersion`, `exportedAt` e `sessions`;
- no máximo 10 mil sessões, 5 milhões de bytes de arquivo e 5 milhões de
  unidades UTF-16 de texto são processados;
- estados e coleções expostos pelo domínio são congelados;
- evento desconhecido falha, em vez de esconder erro de digitação;
- conteúdo do usuário entra no DOM como texto;
- falha de armazenamento não confirma uma alteração não persistida.
- Storage bloqueado ou snapshot inicial ilegível ativa modo volátil explícito e
  preserva o valor persistido original.

## Atributos de qualidade

| Atributo | Decisão observável | Evidência |
|---|---|---|
| correção | validação simétrica na importação e exportação | testes de domínio |
| acessibilidade | HTML nativo, foco, status, reflow e forced colors | contrato estático + roteiro manual |
| modificabilidade | domínio separado de DOM e Storage | testes Node sem navegador |
| recuperabilidade | exportação e rollback em falha de persistência | fixture + testes do adapter |
| desempenho | limites explícitos e estado derivado | orçamento e profiling no curso |
| privacidade | sem rede/telemetria na versão atual | inspeção de código e CSP local |
| diagnosticabilidade | erros de Storage identificam operação e causa | testes de falha injetada |

Testes estáticos não provam acessibilidade nem segurança completas. Eles impedem
regressões básicas; teclado, zoom, leitor de tela, contraste, importação real e
falha de quota continuam exigindo verificação manual ou automação de navegador.

`JSON.parse` também elimina chaves lexicais duplicadas antes da validação. A v1
aceita a semântica do parser e não declara detecção dessas duplicatas; mudar essa
garantia exige parser limitado que preserve ocorrências e novos vetores de teste.

## Não objetivos atuais

- autenticação, sincronização e colaboração;
- criptografia de dados no navegador;
- funcionamento offline com Service Worker;
- instalação PWA ou pacote desktop;
- IndexedDB, anexos e consultas de grande volume;
- edição simultânea em várias abas;
- garantia de backup ou retenção.

Essas capacidades mudam o modelo de consistência e precisam começar por
requisito, cenário de falha, contrato de compatibilidade e ADR.
