# ADR-002: estado puro antes do commit e erro explícito

- Status: aceito
- Data: 2026-10-05

## Contexto

Um evento de interface pode produzir estado válido em memória e falhar ao gravar
por quota, permissão ou indisponibilidade do Storage. Confirmar sucesso mesmo
assim cria perda silenciosa após recarregar. Ignorar evento desconhecido também
esconde erro de integração.

## Decisão

- eventos passam por reducer puro e exaustivo;
- reducer rejeita payload, tema, filtro, ID ou tipo de evento inválido;
- `dispatch` mantém o estado anterior até a persistência ser confirmada;
- falha em `save` restaura a referência anterior e renderiza novamente;
- o adapter converte falha do Storage em `StorageError` com operação e causa;
- mensagens para a pessoa não exibem stack trace nem dados do documento;
- importação valida tudo e pede confirmação antes do único commit.

## Consequências

- erro de programação aparece cedo nos testes;
- UI não afirma ter salvo algo que será perdido no reload;
- não há rollback de efeito fora do snapshot nem transação entre chaves;
- eventos novos exigem alteração deliberada do reducer e dos testes;
- diagnóstico consegue separar leitura, escrita e exclusão.

## Alternativas

- persistir antes de calcular: mistura adapter e regra e dificulta apresentar o
  estado proposto;
- manter estado novo após falha: descartado por gerar divergência invisível;
- ignorar eventos desconhecidos: útil em alguns sistemas evolutivos, mas perigoso
  num reducer local fechado;
- capturar toda exceção no domínio: descartado porque falhas inesperadas não são
  equivalentes a erro de entrada.

## Gatilhos de revisão

Se houver múltiplas abas, sincronização remota ou operações assíncronas, adotar
IDs de operação, controle de versão e máquina de estados explícita. O rollback
por referência não resolve concorrência distribuída.
