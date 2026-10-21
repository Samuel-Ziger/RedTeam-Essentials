# RNP/1 — Rede Notification Protocol, versão didática 1

## Status e escopo

RNP/1 é um protocolo binário didático para trocar pequenas notificações entre
dois processos confiáveis. Ele ensina framing, validação, estado e versionamento.
Não fornece autenticação nem confidencialidade e **MUST NOT** ser usado em rede
não confiável ou em produção.

As palavras MUST, MUST NOT, SHOULD e MAY são interpretadas conforme RFC 2119/8174.

## Transporte e byte order

RNP/1 opera sobre fluxo de bytes confiável e ordenado. A implementação de curso
usa sockets locais. Todos os inteiros multibyte usam network byte order
(big-endian). Receptores MUST aceitar fragmentação arbitrária do fluxo e MUST
NOT assumir que uma leitura equivale a um frame.

## Frame

Header fixo de 12 bytes:

| Offset | Tamanho | Campo | Regra |
|---:|---:|---|---|
| 0 | 4 | Magic | ASCII `RNP1` |
| 4 | 1 | Version | `1` |
| 5 | 1 | Type | registro abaixo |
| 6 | 1 | Flags | `0`; outros valores são erro |
| 7 | 1 | Reserved | `0`; outros valores são erro |
| 8 | 4 | Length | bytes de payload, máximo 4096 |
| 12 | Length | Payload | significado por tipo |

## Tipos

| Valor | Nome | Payload |
|---:|---|---|
| 1 | HELLO | nome UTF-8, 1–64 bytes |
| 2 | WELCOME | texto UTF-8, 1–128 bytes |
| 3 | DATA | bytes opacos, 0–4096 bytes |
| 4 | PING | token opaco, 0–32 bytes |
| 5 | PONG | cópia exata do token PING |
| 6 | CLOSE | razão UTF-8, 0–128 bytes |
| 7 | ERROR | código `uint16` + mensagem UTF-8 até 256 bytes |

Payload textual MUST ser UTF-8 válido, sem NUL. O receptor MUST rejeitar tipo
desconhecido, comprimento acima do limite, flags/reserved não zero, magic ou
versão incompatível. O protocolo não tenta ressincronizar após header inválido.

## Máquina de estados

1. cliente conectado MUST enviar exatamente um HELLO;
2. servidor em `WAIT_HELLO` aceita HELLO e responde WELCOME, entrando `OPEN`;
3. em `OPEN`, DATA é entregue; PING gera PONG com mesmo payload;
4. CLOSE recebe CLOSE e ambos encerram;
5. qualquer tipo inválido para o estado gera ERROR `1001` e encerramento;
6. erro de framing encerra imediatamente; responder pode ser inseguro se o
   limite do frame não foi estabelecido.

O servidor SHOULD limitar conexão a 100 frames e 1 MiB acumulado, e SHOULD usar
timeout inativo. A implementação didática limita cada payload e deixa limites de
sessão para o chamador.

## Erros registrados

- `1001`: mensagem inválida para o estado;
- `1002`: payload semanticamente inválido;
- `1003`: recurso/limite excedido;
- `1999`: erro interno sanitizado.

## Versionamento e extensões

Uma nova versão incompatível MUST alterar `Version`. Tipos 128–255 ficam
reservados para experimentos privados e ainda são rejeitados por RNP/1 puro.
Flags só podem ganhar significado em especificação que defina negociação; o
receptor v1 não deve ignorá-las.

## Vetor de teste

HELLO com payload ASCII `lab`:

```text
52 4e 50 31  01 01 00 00  00 00 00 03  6c 61 62
 R  N  P  1  v1 type flags  length=3       lab
```

## Considerações de segurança

O parser valida limites antes de aguardar/alocar payload. Mensagens de erro não
incluem dados arbitrários. Uma versão real SHOULD operar sobre TLS 1.3, definir
identidade/autorização, proteção contra replay, rate limits, privacy e audit.
TLS não corrige parser sem limites nem estado incorreto.
