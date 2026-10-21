# 17 — Framing, tipos, estado e erros

TCP é fluxo de bytes: uma chamada de leitura não corresponde a uma mensagem.
O protocolo precisa delimitar frames por tamanho fixo, delimitador escapado,
length prefix ou formato autocontido. RNP/1 usa header fixo e comprimento.

Campos inteiros usam network byte order (big-endian). O parser valida magic,
versão, flags reservadas, tipo, comprimento máximo e payload antes de alocar ou
decodificar. Nunca confie no comprimento declarado.

Máquina de estados define mensagens legais. No RNP/1: cliente envia HELLO;
servidor responde WELCOME; ambos podem trocar DATA; PING recebe PONG; CLOSE
encerra. Mensagem fora de ordem produz ERROR e fechamento.

## Erros

Separe erro de framing (não é possível continuar), protocolo (tipo/estado
inválido), aplicação (pedido válido falhou) e transporte. Códigos estáveis e
mensagem humana sanitizada ajudam debug. Não reflita payload arbitrário no erro.

Timeout e limite de frames/bytes impedem cliente lento ou infinito. Backpressure
evita que produtor consuma memória sem limite.
