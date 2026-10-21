# Lab 04 — contrato HTTP e clientes em cinco linguagens

## Resultado esperado

Tratar a API como protocolo observável: status, cabeçalhos, corpo, timeout,
limite e erro. Você executará cinco clientes contra o mesmo servidor falso e
escreverá testes que distinguem transporte, protocolo e domínio.

## Pré-requisitos e tempo

- capítulos 08 a 12;
- Labs 01–03 recomendados;
- Python 3.12+, Node.js 22.12+, compilador C17, Java 17+ e .NET 10 conforme
  disponibilidade;
- 10 a 16 horas.

## Linha de base sem Docker

O arquivo [`exemplos/mock_api.py`](../exemplos/mock_api.py) implementa somente o
contrato necessário em porta efêmera. Ele existe para testar clientes, não para
substituir a Inventory API.

Execute o runner:

```bash
bash 01-Recon/programacao-avancada/testar-curso.sh
```

Ele compila o que estiver disponível e informa cada runtime ausente como
`PULADO`. Para uma entrega formal, instale todos os runtimes e use
`--require-all`.

Estude os clientes:

- [Python](../exemplos/python/api_client.py) e seus
  [testes](../exemplos/python/test_api_client.py);
- [JavaScript](../exemplos/javascript/api_client.mjs) e seus
  [testes](../exemplos/javascript/api_client.test.mjs);
- [Java](../exemplos/java/ApiClient.java);
- [C](../exemplos/c/api_client.c);
- [C#](../exemplos/csharp/Program.cs) e o
  [projeto](../exemplos/csharp/ApiClient.csproj).

## Matriz de contrato

Preencha com função/classe/linha conceitual de cada implementação:

| Decisão | Python | JavaScript | Java | C# | C |
|---------|--------|------------|------|----|---|
| timeout de conexão/leitura | | | | | |
| limite de resposta | | | | | |
| redirect | | | | | |
| status não 2xx | | | | | |
| JSON inválido | | | | | |
| descarte de socket/stream | | | | | |

O cliente C consulta apenas saúde e expõe a mensagem HTTP bruta. Ele não é uma
biblioteca JSON/TLS; essa limitação deve aparecer na sua análise.

## Casos obrigatórios

Acrescente ao mock, um por vez, e teste antes de alterar o cliente:

1. resposta 409 com `application/problem+json`;
2. JSON truncado;
3. raiz JSON como array;
4. `Content-Length` acima de 1 MB;
5. corpo acima do limite sem `Content-Length`;
6. resposta que nunca termina, validando timeout;
7. item de produto sem `sku`;
8. redirect para provar a política escolhida.

Restaure o mock compartilhado ao final ou trabalhe numa branch/cópia. Não use
endpoint externo: porta efêmera em `127.0.0.1` torna o teste determinístico.

## Contrato da Inventory API

Leia os testes de
[`test_api.py`](../projetos/inventory-api/api/tests/test_api.py),
[`test_service.py`](../projetos/inventory-api/api/tests/test_service.py),
[`test_models.py`](../projetos/inventory-api/api/tests/test_models.py) e
[`test_repositories.py`](../projetos/inventory-api/api/tests/test_repositories.py).

Classifique cada teste como:

- contrato HTTP;
- validação de entrada;
- caso de uso;
- persistência/adaptador;
- resiliência/observabilidade.

Escreva um teste para `GET /products` com cursor inválido e outro para método
não permitido. Verifique `application/problem+json`, request ID e ausência de
detalhe interno.

## Gate de conclusão

- runner termina sem falha; skips estão justificados ou eliminados;
- matriz preenchida sem atribuir proteção inexistente;
- pelo menos dois testes autorais falham antes e passam depois da implementação;
- nenhum teste depende de internet, porta fixa ou `sleep` arbitrário;
- erros não exibem credenciais, traceback ou detalhes do banco.
