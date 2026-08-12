# 12 - Java Tools

> Utilitarios em Java 17+ que complementam Python/PowerShell/Bash.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Desenvolvedores com Java básico e contexto de AppSec. |
| Pré-requisitos | Módulos 00 e 07; JDK 17+. |
| Tempo estimado | 3 horas de leitura, build e testes. |
| Ambiente | Somente laboratório próprio/isolado ou engagement autorizado. |
| Evidência final | Build limpo, teste offline e saída sanitizada explicada. |
| Critério de conclusão | Demonstrar o objetivo, explicar limitações e registrar o cleanup. |

## Sumario

| Classe | Descricao |
|--------|-----------|
| [`PayloadGenerator`](src/main/java/io/redteam/essentials/PayloadGenerator.java) | Gera payloads de teste para XSS, SQLi, command injection, SSTI, SSRF, LFI e XXE. Suporta URL/Base64 encoding e amostragem aleatoria. |

## Build & Run (sem Maven/Gradle)

```bash
cd 12-Java-Tools
mkdir -p build
javac -d build src/main/java/io/redteam/essentials/PayloadGenerator.java
java  -cp build io.redteam.essentials.PayloadGenerator --list
java  -cp build io.redteam.essentials.PayloadGenerator --type xss --count 20 --encode url
java  -cp build io.redteam.essentials.PayloadGenerator --type sqli --out payloads.txt
```

## Por que Java?

Muitos engagements de AppSec encontram alvos Java (Spring, Tomcat, JBoss, Java APIs). Ter um arsenal portavel em Java facilita rodar dentro de pipelines corporativos onde apenas JDK esta disponivel. O `PayloadGenerator` e didatico, mas se integra bem com Burp (Intruder) e ferramentas como ffuf via wordlist gerada.

## Roadmap

- `BurpExt` - extensao Burp Suite minima.
- `JndiPocServer` - laboratorio local de Log4Shell (apenas em rede isolada).
- `JwtCracker` - HMAC bruteforce em paralelo com `Runtime.availableProcessors()`.
