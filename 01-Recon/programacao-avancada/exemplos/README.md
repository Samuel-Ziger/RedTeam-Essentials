# Clientes da Inventory API em cinco linguagens

Estes programas usam apenas bibliotecas padrão para consultar a API local. Eles
demonstram timeout, status HTTP e descarte de recursos sem esconder o protocolo
atrás de um SDK.

Antes dos bancos, execute todos contra o
[`mock_api.py`](mock_api.py), um servidor de contrato em loopback e porta
efêmera. O runner compila cada linguagem disponível, executa os clientes e
valida a saída:

```bash
bash 01-Recon/programacao-avancada/testar-curso.sh

# Gate formal: falha se faltar runtime/dependência
bash 01-Recon/programacao-avancada/testar-curso.sh --require-all
```

Há testes adicionais do cliente
[Python](python/test_api_client.py) e do cliente
[JavaScript](javascript/api_client.test.mjs). Eles cobrem Problem Details, JSON
inválido, raiz com tipo incorreto e limite de 1 MB sem internet nem porta fixa.

Primeiro inicie o projeto:

```bash
cd 01-Recon/programacao-avancada/projetos/inventory-api
docker compose up --build --detach --wait
bash smoke-test.sh
```

Em outro terminal, a partir da raiz do repositório:

```bash
python3 01-Recon/programacao-avancada/exemplos/python/api_client.py

java 01-Recon/programacao-avancada/exemplos/java/ApiClient.java

gcc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  01-Recon/programacao-avancada/exemplos/c/api_client.c \
  -o /tmp/rte-api-client
/tmp/rte-api-client

dotnet run \
  --project 01-Recon/programacao-avancada/exemplos/csharp/ApiClient.csproj

node 01-Recon/programacao-avancada/exemplos/javascript/api_client.mjs
```

Todos aceitam a variável `INVENTORY_URL`; o cliente C aceita
`INVENTORY_HOST` e `INVENTORY_PORT`, pois implementa HTTP/1.1 diretamente sobre
socket local. Por segurança didática, esse cliente aceita somente
`127.0.0.1`, `localhost` ou `::1`:

```bash
INVENTORY_URL=http://127.0.0.1:8101 python3 \
  01-Recon/programacao-avancada/exemplos/python/api_client.py
```

O cliente C deliberadamente não oferece TLS. Ele é um microscópio do protocolo,
não uma biblioteca HTTP. Use libcurl ou equivalente em software real.

Quando terminar:

```bash
cd 01-Recon/programacao-avancada/projetos/inventory-api
docker compose down
```

Os exemplos fazem somente `GET` e não alteram os dados.

## O que cada implementação ensina

| Cliente | Ênfase | Limite deliberado |
|---------|--------|-------------------|
| [Python](python/api_client.py) | context manager, HTTPError e contrato dinâmico | cliente síncrono |
| [JavaScript](javascript/api_client.mjs) | fetch, AbortSignal e stream limitado | execução Node.js, não navegador |
| [Java](java/ApiClient.java) | futuros concorrentes e InputStream limitado | validação JSON mínima sem dependência |
| [C#](csharp/Program.cs) | HttpClient, cancelamento e records | buffer limitado a 1 MB |
| [C](c/api_client.c) | socket e HTTP/1.1 visível | somente health, sem TLS nem parser JSON |

Compare timeout, redirect, status, limite, desserialização e cleanup no
[Lab 04](../laboratorios/lab-04-contrato-api.md).
