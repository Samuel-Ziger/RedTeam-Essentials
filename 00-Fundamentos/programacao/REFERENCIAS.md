# Referências, vídeos e comunidades

> Materiais complementares, revisados em **2026-10-03**. O curso local contém
> a explicação e o código necessários; use estes links para outra perspectiva,
> detalhes de referência e contato com a comunidade.

## Como avaliar uma fonte

Antes de aplicar uma resposta encontrada na internet:

1. confira data, versão e sistema operacional;
2. prefira documentação da linguagem/runtime;
3. reproduza em projeto mínimo;
4. leia a mensagem de erro completa;
5. confirme efeitos e limitações;
6. cite a fonte ao registrar a decisão;
7. nunca cole segredo ou código proprietário em fórum.

Documentação de referência responde “o que esta API faz”. Tutorial ensina uma
sequência. Fórum ajuda em um problema específico. Vídeo oferece intuição, mas é
mais difícil de buscar e atualizar; valide sempre na documentação.

## Roteiro de consulta por etapa

Não abra todas as fontes ao mesmo tempo. Primeiro execute o capítulo local;
depois use a referência indicada para esclarecer uma dúvida específica.

| Etapa local | Consulte para | Prioridade |
|-------------|---------------|------------|
| lógica e Python | sintaxe, tipos e biblioteca padrão | tutorial e documentação oficial do Python |
| terminal e Git | histórico, branches, conflitos e recuperação | Pro Git |
| Java | linguagem, JVM e APIs padrão | Learn Java e Java SE API |
| C | regras da linguagem, compilador e diagnósticos de memória | referência C, GCC e Clang |
| C# | tipos, runtime, recursos e testes | documentação Microsoft Learn |
| JavaScript | linguagem, DOM, promises e Node.js | MDN, TC39 e documentação Node.js |
| HTTP e web | semântica do protocolo e acessibilidade | RFC 9110 e MDN |
| banco de dados | SQL, transações e índices | documentação SQLite |
| entrega | imagem, Compose, proxy e operação | documentação Docker e Nginx |

Use uma especificação para resolver ambiguidade do contrato, uma referência de
API para detalhes de assinatura e um tutorial para aprender a sequência pela
primeira vez. Um post de fórum pode revelar uma hipótese, mas não deve ser a
única base de uma decisão importante.

## Como registrar uma pesquisa técnica

Para uma dúvida que afetou o projeto, preserve:

1. pergunta concreta;
2. versão da linguagem ou ferramenta;
3. fonte e seção consultadas;
4. experimento mínimo;
5. resultado observado;
6. decisão tomada e sua limitação.

Isso evita repetir a pesquisa e torna possível revisar a decisão quando a
versão mudar.

## Documentação oficial e referências técnicas

### Fundamentos e ferramentas

- [Pro Git — livro oficial gratuito](https://git-scm.com/book/en/v2).
- [HTTP Semantics — RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html).
- [SQLite — documentação da linguagem SQL](https://www.sqlite.org/lang.html).
- [MDN — visão cliente/servidor](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Client-Server_overview).
- [MDN — HTML e acessibilidade](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML).

### Python

- [Tutorial oficial do Python](https://docs.python.org/3/tutorial/).
- [Biblioteca padrão](https://docs.python.org/3/library/).
- [`unittest`](https://docs.python.org/3/library/unittest.html).
- [Python Packaging User Guide](https://packaging.python.org/en/latest/).
- [Versões do Python mantidas](https://devguide.python.org/versions/).

### Java

- [Learn Java](https://dev.java/learn/).
- [Java Language Basics](https://dev.java/learn/language-basics/).
- [Documentação das APIs Java SE](https://docs.oracle.com/en/java/javase/).
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/).

### C

- [Referência da linguagem C](https://en.cppreference.com/w/c/language.html).
- [SEI CERT C Coding Standard](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/).
- [Documentação do GCC](https://gcc.gnu.org/onlinedocs/).
- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html).

### C# e .NET

- [Tour da linguagem C#](https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/).
- [Guia de C#](https://learn.microsoft.com/en-us/dotnet/csharp/).
- [Testes em .NET](https://learn.microsoft.com/en-us/dotnet/core/testing/).
- [Política oficial de suporte do .NET](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core).

### JavaScript e web

- [Guia JavaScript — MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide).
- [Aprenda desenvolvimento web — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/).
- [Node.js Learn](https://nodejs.org/learn).
- [Documentação de APIs Node.js](https://nodejs.org/api/).
- [Linhas e situação das versões do Node.js](https://nodejs.org/en/about/previous-releases).
- [Política de fim de vida do Node.js](https://nodejs.org/en/about/eol).
- [ECMAScript Language Specification](https://tc39.es/ecma262/).

### Containers e servidor web

- [Docker Get Started](https://docs.docker.com/get-started/).
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).
- [Compose file reference](https://docs.docker.com/reference/compose-file/).
- [Nginx Beginner’s Guide](https://nginx.org/en/docs/beginners_guide.html).
- [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).

## Vídeos em português

Vídeo é complemento: pause antes da solução, implemente e compare.

- [Primeiros passos na carreira de programação](https://www.youtube.com/watch?v=Oj26AOVuLYw) — Curso em Vídeo.
- [Python #01 — Seja um Programador](https://www.youtube.com/watch?v=S9uPNppGsGo) — Curso em Vídeo.
- [POO Java — instalação e primeiro ambiente](https://www.youtube.com/watch?v=Ucyx_QPfDng) — Curso em Vídeo.
- [Linguagem C — curso completo](https://www.youtube.com/watch?v=2dPbemvBwW4) — prof. Saulo Santos.
- [Curso completo de C# — aula 1](https://www.youtube.com/watch?v=dVzJ3bx68FA) — CFB Cursos.
- [JavaScript — primeiros passos](https://www.youtube.com/watch?v=Ptbk2af68e8) — Curso em Vídeo.

Algumas aulas usam versões antigas de IDE/runtime. Aproveite os fundamentos e
execute com as versões suportadas indicadas na documentação oficial.

## Fóruns e comunidades

- [Stack Overflow em Português](https://pt.stackoverflow.com/) — perguntas
  reproduzíveis e respostas técnicas; leia [Como perguntar](https://pt.stackoverflow.com/help/how-to-ask).
- [TabNews](https://www.tabnews.com.br/) — artigos e discussões em português.
- [DEV Community](https://dev.to/) — relatos e tutoriais; confirme versões.
- [Reddit r/brdev](https://www.reddit.com/r/brdev/) — carreira e comunidade;
  opiniões não substituem fonte técnica.
- [GitHub Discussions](https://docs.github.com/en/discussions) — prefira a
  discussão do projeto específico quando a dúvida é sobre uma biblioteca.

## Blogs e livros abertos

- [Real Python](https://realpython.com/) — artigos práticos de Python.
- [Microsoft .NET Blog](https://devblogs.microsoft.com/dotnet/) — novidades do runtime/ecossistema.
- [Inside.java](https://inside.java/) — notícias técnicas da plataforma Java.
- [web.dev](https://web.dev/learn/) — cursos de web, desempenho e acessibilidade.
- [The Architecture of Open Source Applications](https://aosabook.org/en/) —
  leitura de arquitetura de projetos reais.

## Quando uma resposta externa não deve ser usada

Não copie código quando você não consegue:

- explicar cada entrada, saída e efeito;
- identificar licença/origem;
- testar limites e erros;
- reconhecer dependências e permissões;
- manter o código depois.

Trate código gerado por IA da mesma forma: hipótese que precisa de revisão,
testes, licença compatível e responsabilidade humana.
