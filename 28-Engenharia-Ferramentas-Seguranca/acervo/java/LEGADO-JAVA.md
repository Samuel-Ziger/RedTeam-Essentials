# Acervo legado — Java Tools

Utilitários Java 17+ anteriores à rota macOS. O código foi preservado em
`src/main/java` e continua coberto pelo workflow Java.

| Classe | Descrição |
|---|---|
| `PayloadGenerator` | Gera entradas didáticas para testes autorizados de AppSec. |

```bash
cd 28-Engenharia-Ferramentas-Seguranca/acervo/java
mkdir -p build
javac -d build src/main/java/io/redteam/essentials/PayloadGenerator.java
java -cp build io.redteam.essentials.PayloadGenerator --list
```

Esse acervo não integra a formação macOS e deve ser usado somente em ambiente
próprio/isolado ou engagement formalmente autorizado.

---

## Registro histórico integral

> A seção abaixo conserva o conteúdo substantivo do README anterior, com seus
> contratos, sequência, referências e avisos éticos. Ela é um registro de
> preservação e não substitui o currículo atual descrito no [Módulo 28](../../README.md).

> Utilitarios em Java 17+ que complementam Python/PowerShell/Bash.

## Histórico — Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Desenvolvedores com Java básico e contexto de AppSec. |
| Pré-requisitos | Módulos 00 e 07; JDK 17+. |
| Tempo estimado | 3 horas de leitura, build e testes. |
| Ambiente | Somente laboratório próprio/isolado ou engagement autorizado. |
| Evidência final | Build limpo, teste offline e saída sanitizada explicada. |
| Critério de conclusão | Demonstrar o objetivo, explicar limitações e registrar o cleanup. |

## Histórico — Sumario

| Classe | Descricao |
|--------|-----------|
| [`PayloadGenerator`](src/main/java/io/redteam/essentials/PayloadGenerator.java) | Gera payloads de teste para XSS, SQLi, command injection, SSTI, SSRF, LFI e XXE. Suporta URL/Base64 encoding e amostragem aleatoria. |

## Histórico — Build & Run (sem Maven/Gradle)

```bash
cd 28-Engenharia-Ferramentas-Seguranca/acervo/java
mkdir -p build
javac -d build src/main/java/io/redteam/essentials/PayloadGenerator.java
java  -cp build io.redteam.essentials.PayloadGenerator --list
java  -cp build io.redteam.essentials.PayloadGenerator --type xss --count 20 --encode url
java  -cp build io.redteam.essentials.PayloadGenerator --type sqli --out payloads.txt
```

## Histórico — Por que Java?

Muitos engagements de AppSec encontram alvos Java (Spring, Tomcat, JBoss, Java APIs). Ter um arsenal portavel em Java facilita rodar dentro de pipelines corporativos onde apenas JDK esta disponivel. O `PayloadGenerator` e didatico, mas se integra bem com Burp (Intruder) e ferramentas como ffuf via wordlist gerada.

## Histórico — Roadmap

- `BurpExt` - extensao Burp Suite minima.
- `JndiPocServer` - laboratorio local de Log4Shell (apenas em rede isolada).
- `JwtCracker` - HMAC bruteforce em paralelo com `Runtime.availableProcessors()`.

## Histórico — Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [Proteja suas aplicações Java com Spring Security](https://www.youtube.com/watch?v=ptcjeehUbz8) — **AlgaWorks**.
2. [O que é AppSec?](https://www.youtube.com/watch?v=R49E7efhoDA) — **AppSecBR**.
3. [Segurança de Aplicações Web Java: Tudo o que Você Precisa Saber](https://www.youtube.com/watch?v=Ac5mvR892zE) — **SaM Solutions**.
4. [Mercado e Carreira de AppSec (Segurança de Aplicações) com Wagner Elias - Conviso](https://www.youtube.com/watch?v=WniXyKTkxi4) — **Eduardo Santos - WarmSec**.
5. [Introdução ao Spring Boot Security! Tutorial para Aplicações Java Seguras!](https://www.youtube.com/watch?v=S8dNt0cYYRs) — **Carreira Dev Internacional**.
