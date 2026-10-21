# ADR-001: armazenamento local com documento versionado

- Status: aceito
- Data: 2026-10-05

## Contexto

O projeto precisa ensinar estado, persistência e importação sem exigir banco,
servidor ou instalação de dependências. A pessoa deve conseguir inspecionar e
exportar seus dados. Web Storage é síncrono, limitado e associado ao origin; não
é banco confiável nem backup.

## Decisão

- persistir um snapshot JSON sob a chave `study-desk:sessions:v1`;
- declarar `schemaVersion` no documento, independentemente da chave física;
- usar schema fechado e limites de tamanho/cardinalidade;
- validar o mesmo contrato ao carregar, importar, substituir e exportar;
- recusar versões desconhecidas até existir uma migração explícita;
- oferecer exportação como cópia portável, sem prometer confidencialidade;
- manter tema em chave separada porque sua perda não ameaça dados de domínio.

## Consequências

- a aplicação funciona sem rede e o formato é legível;
- cada escrita serializa o snapshot completo e bloqueia a thread durante a API
  síncrona;
- quota, limpeza do navegador ou troca de origin podem remover o dado;
- consultas e atualizações parciais não escalam como IndexedDB ou SQLite;
- evolução exige fixtures por versão e uma política de migração/rollback.

## Alternativas

- `sessionStorage`: descartado porque fecha junto com a sessão da aba;
- IndexedDB: melhor para volume/transações, adiado para manter o primeiro adapter
  observável e o projeto sem complexidade assíncrona;
- servidor remoto: contradiz o escopo local e exigiria identidade, rede,
  privacidade, conflitos e operação;
- objeto JavaScript sem schema: não permite compatibilidade verificável.

## Gatilhos de revisão

Reavaliar quando medições mostrarem bloqueio perceptível, quando o volume se
aproximar dos limites, quando houver anexos/consultas ou quando sincronização se
tornar requisito real. A migração deve manter exportação e recuperação.
