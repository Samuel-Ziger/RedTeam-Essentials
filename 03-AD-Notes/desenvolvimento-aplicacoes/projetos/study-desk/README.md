# Study Desk

Aplicação web local-first de referência para registrar sessões de estudo. Não é
um snippet: o projeto torna observáveis contratos de domínio, estado, DOM,
persistência, importação, recuperação e acessibilidade sem esconder essas
fronteiras atrás de framework ou dependência de runtime.

## Funcionalidades e garantias

- cadastro com validação de assunto e duração;
- histórico, busca, total derivado e exclusão;
- fluxo unidirecional com reducer puro e estados imutáveis;
- persistência em `localStorage` por adapter testável;
- documento JSON com schema versionado e validação simétrica;
- importação transacional: valida tudo antes de trocar o estado;
- IDs ASCII seguros, datas UTC canônicas e detecção de duplicatas;
- limites de título, filtro, documento e quantidade de sessões;
- rollback em memória quando o armazenamento recusa uma gravação;
- degradação explícita para memória quando o Storage é inacessível ou ilegível,
  preservando o valor persistido original;
- tema claro/escuro persistido sem bloquear a função principal;
- conteúdo importado inserido com `textContent`, nunca interpretado como HTML;
- política local de conteúdo (CSP) e referrer restrito;
- feedback por região de status e erros associados aos campos;
- layout responsivo, foco visível, redução de movimento e cores forçadas;
- 35 testes de domínio, reducer, schema, repositório e contrato estático.

Os dados não saem do navegador nesta versão. Isso não garante sigilo, backup ou
retenção: extensões, perfil compartilhado, acesso ao dispositivo, limpeza do
navegador e políticas de quota continuam no modelo de ameaça. Exporte uma cópia
quando o histórico for importante.

## Arquitetura

```text
index.html + styles.css ------ apresentação semântica
            |
          app.mjs ------------ eventos, renderização e composition root
          /     \
   domain.mjs   repository.mjs
   regras/estado  adapter Storage
```

`domain.mjs` não importa DOM nem armazenamento; por isso os testes rodam no
Node.js. `repository.mjs` depende apenas do contrato estrutural de Storage. A
aplicação escolhe `localStorage`, conecta efeitos e converte falhas em feedback.

Documentação de engenharia:

- [arquitetura e fluxos](docs/architecture.md);
- [ADR 001 — local-first e documento versionado](docs/adr/001-local-first-versioned-document.md);
- [ADR 002 — commit de estado e erros](docs/adr/002-state-commit-and-errors.md);
- [runbook de diagnóstico e recuperação](RUNBOOK.md).

## Executar

Na pasta do projeto:

```bash
python3 -m http.server 8000
```

Abra `http://127.0.0.1:8000`. Servir por HTTP preserva o comportamento de módulos
ES. Abrir `index.html` diretamente pode ser bloqueado pela política do navegador
e cria um contexto de armazenamento diferente.

## Testar

```bash
npm test
```

O projeto não exige `npm install`: usa apenas `node:test`. A suíte cobre:

- criação, validação, resumo, filtro e imutabilidade;
- eventos válidos, desconhecidos e payloads fora do contrato;
- round-trip, campos extras, versões futuras, IDs e datas;
- limites antes do parse e duplicatas antes da exportação;
- falhas injetadas de leitura, escrita e remoção no Storage;
- ausência de escrita quando a entrada já é inválida;
- semântica essencial, limites de formulário, CSP e `textContent`.

Para validar também os exemplos das cinco linguagens:

```bash
bash ../../testar-curso.sh
```

## Contratos observáveis

### Sessão

| Campo | Contrato |
|---|---|
| `id` | ASCII, 1–120 caracteres, único; letras, números, `.`, `_` e `-` |
| `title` | 1–80 unidades de código UTF-16, sem espaço externo ou controles |
| `minutes` | inteiro de 1 a 1.440 |
| `createdAt` | instante UTC canônico `YYYY-MM-DDTHH:mm:ss.sssZ` |

O arquivo selecionado aceita no máximo 5 milhões de bytes; depois da leitura, o
texto aceita 5 milhões de unidades UTF-16. O documento contém no máximo 10 mil
sessões. Esses limites controlam custo e dão mensagens previsíveis; não tornam
Web Storage adequado a grandes bases.

A UI descreve esse limite como “posições de texto”: `String.length` e o atributo
HTML `maxlength` contam unidades UTF-16, não grafemas percebidos. Alguns emoji
ocupam duas posições; os testes fixam esse comportamento para não confundi-lo
com o modelo de Unicode discutido no capítulo 10.

A versão 1 usa `JSON.parse`; chaves JSON repetidas seguem a semântica do parser
(o último valor é observado) e não podem ser detectadas depois do parse. O
validador recusa campos ausentes/desconhecidos no objeto resultante, mas não
promete rejeitar duplicatas lexicais. Suporte estrito exigiria outro parser.

### Estado e commit

O reducer calcula um novo estado sem alterar o anterior. `dispatch` tenta salvar
o snapshot e só confirma a mudança depois. Se `setItem` falhar, a referência ao
estado anterior é restaurada e o usuário recebe diagnóstico. Isso evita falso
sucesso em memória, mas não transforma múltiplas chaves de Web Storage numa
transação.

Se o getter do Storage for bloqueado ou o snapshot inicial não puder ser lido, a
inicialização troca para um adapter em memória e avisa que mudanças valem apenas
na aba. Ela não sobrescreve automaticamente o valor persistido problemático; a
pessoa pode continuar, exportar uma cópia nova e diagnosticar o original.

## Formato exportado

```json
{
  "schemaVersion": 1,
  "exportedAt": "2026-10-05T12:00:00.000Z",
  "sessions": [
    {
      "id": "session-1",
      "title": "Grafos",
      "minutes": 45,
      "createdAt": "2026-10-05T11:00:00.000Z"
    }
  ]
}
```

A importação verifica tamanho, JSON, campos exatos, versão, timestamp, limites e
todas as sessões antes de pedir confirmação e substituir dados. Versões futuras
são recusadas, pois ainda não existe migração segura. Uma recusa não modifica o
histórico confirmado.

## Teste manual de acessibilidade

1. Use Tab/Shift+Tab e conclua cadastro, busca, exportação e importação.
2. Envie formulário vazio e confirme foco/mensagem no primeiro campo inválido.
3. Aumente zoom a 400% e confirme reflow sem perder ações.
4. Ative redução de movimento, tema escuro e cores forçadas, se disponíveis.
5. Use a árvore de acessibilidade e um leitor de tela disponível.
6. Confirme que exclusão, falha de persistência e importação anunciam resultado.
7. Importe título que parece HTML e confirme exibição literal, sem interpretação.

Automação impede regressões simples; ela não certifica acessibilidade. Registre
navegador, tecnologia assistiva, sequência, resultado e limitação encontrada.

## Diagnóstico rápido

- página sem script: confirme servidor HTTP e console;
- histórico ausente: confirme origin e chave `study-desk:sessions:v1`;
- importação recusada: preserve o original e verifique versão/limites/datas;
- gravação falha: exporte se possível, depois investigue quota e política;
- interface lenta: use fixture sintética e profiler antes de otimizar;
- tema não persiste: a função principal deve continuar utilizável.

Não limpe todo o armazenamento como primeiro passo. Siga o [runbook](RUNBOOK.md)
para preservar evidência e recuperar sem destruir outros dados do origin.

## Não objetivos atuais

- conta, autenticação, sincronização ou colaboração;
- criptografia do histórico no navegador;
- garantia de backup ou permanência;
- Service Worker e funcionamento integral sem rede;
- IndexedDB, anexos ou consultas de grande volume;
- coordenação de edição entre várias abas;
- telemetria ou envio automático de diagnóstico.

## Evoluções propostas

1. desfazer exclusão com expiração;
2. edição com cancelamento;
3. catálogo `pt-BR`/`en` e pluralização;
4. migração `schemaVersion 1 → 2` com fixtures;
5. adapter IndexedDB mantendo o domínio intacto;
6. empacotamento PWA ou desktop acompanhado de ADR;
7. cliente opcional para a API do módulo 01, com conflito e fila offline;
8. coordenação entre abas com política de versão;
9. profiling para 10 mil registros e orçamento de interação;
10. pacote de diagnóstico local, sanitizado e pré-visualizável.
