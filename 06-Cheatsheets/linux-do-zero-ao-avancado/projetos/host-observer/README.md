# Host Observer — projeto de referência

Host Observer é a implementação de referência do módulo 06. Ele coleta um
snapshot pequeno do host, compara mudanças, grava estado de forma atômica e
pode ser executado por service e timer do systemd. Não envia dados, não abre
porta, não pede privilégio e não modifica configuração do sistema.

O projeto existe para demonstrar integração. Ele não é uma solução de
monitoramento de produção nem deve ser instalado cegamente.

## Contrato

Entrada:

- nenhuma entrada para a coleta;
- dois arquivos chave=valor para comparação;
- lista opcional de chaves voláteis a ignorar.

Saída:

- schema versionado;
- horário UTC;
- release, kernel e arquitetura;
- CPU, tamanho de página e memória total;
- PID 1, filesystem raiz e UID;
- resumo determinístico de campos adicionados, removidos e alterados.

Falha:

- status 2 para argumento ou snapshot inválido;
- status 1 somente quando a opção de falhar por mudança foi pedida;
- arquivo parcial removido no encerramento;
- saída válida anterior não é truncada antes da troca.

## Artefatos usados

| Artefato | Responsabilidade |
|----------|------------------|
| [diagnostico.sh](../../exemplos/diagnostico.sh) | coleta somente leitura |
| [comparar_diagnosticos.py](../../exemplos/comparar_diagnosticos.py) | parsing estrito e diff determinístico |
| [curso-observador](../../exemplos/systemd/curso-observador) | gravação atômica do estado |
| [service](../../exemplos/systemd/curso-observador.service) | identidade e sandbox |
| [timer](../../exemplos/systemd/curso-observador.timer) | execução periódica |
| [testes](../../exemplos/tests/test_examples.sh) | contratos felizes e de erro |

Os arquivos permanecem na pasta de exemplos para evitar duas cópias divergentes
do mesmo código.

## Fluxo

~~~text
timer
  ↓ ativa
service oneshot
  ↓ executa como usuário dinâmico
curso-observador
  ↓ coleta estado pequeno
arquivo temporário no StateDirectory
  ↓ chmod + rename no mesmo filesystem
ultima-execucao.txt

diagnostico.sh → antes.txt
diagnostico.sh → depois.txt
       ↓
comparar_diagnosticos.py → resumo textual ou JSON
~~~

O rename protege leitores contra arquivo parcialmente escrito, desde que
temporário e destino estejam no mesmo filesystem. Isso não torna todo o fluxo
transacional: uma falha antes da troca mantém a versão anterior; uma falha
depois da troca exige observar o novo estado.

## Executar sem instalar

A validação padrão ocorre como usuário comum:

~~~bash
bash ../../testar-curso.sh
~~~

Para uma demonstração isolada:

~~~bash
temp_dir=$(mktemp -d)
STATE_DIRECTORY="$temp_dir" ../../exemplos/systemd/curso-observador
cat "$temp_dir/ultima-execucao.txt"
rm -rf -- "$temp_dir"
~~~

Confirme manualmente que temp_dir não está vazio e pertence ao diretório
temporário antes da remoção ao adaptar o exemplo. A suíte automatizada já
mantém essa barreira.

## Staging da instalação

Não comece copiando para o sistema. Monte primeiro:

~~~text
stage/
├── usr/local/libexec/curso-observador
└── etc/systemd/system/
    ├── curso-observador.service
    └── curso-observador.timer
~~~

Verifique:

1. executável com dono administrativo e sem escrita pelo usuário do serviço;
2. units com modo de leitura apropriado;
3. ExecStart absoluto e correspondente ao staging planejado;
4. service e timer aprovados por systemd-analyze verify;
5. calendário interpretado como esperado;
6. nenhuma variável contém segredo.

O laboratório 03 descreve a instalação opcional em VM. O projeto não fornece
instalador privilegiado justamente para obrigar a revisão do alvo e dos modos.

## Modelo de segurança

A unit usa DynamicUser e StateDirectory: o service manager cria identidade e
diretório de estado para a execução. Os controles de proteção reduzem acesso a
home, dispositivos, módulos, tunables, cgroups e escrita no sistema.

Cada diretiva possui custo de compatibilidade. Se uma futura versão precisar de
dispositivo, home ou syscall adicional, teste a necessidade e libere somente o
recurso específico. Remover toda a sandbox para corrigir uma negação reprova o
projeto.

O snapshot evita hostname, serial, endereço, MAC e conteúdo de processo.
Mesmo assim, release e arquitetura podem ser sensíveis em alguns ambientes;
defina acesso, retenção e finalidade antes de usar fora do laboratório.

## Cenários de teste

### Coleta

- zero argumentos produz todas as chaves obrigatórias;
- argumento inesperado retorna status 2;
- nenhuma chave proibida de identidade aparece;
- números esperados são positivos ou valor unknown explícito.

### Comparação

- timestamps diferentes são ignorados por padrão;
- campo alterado aparece uma vez e em ordem estável;
- campo novo e removido são separados;
- chave duplicada, inválida ou linha sem separador é recusada;
- entrada maior que 1 MiB é recusada;
- modo JSON mantém o mesmo resumo;
- fail-on-change retorna 1 somente quando há diferença relevante.

### Unit

- arquivos passam no verificador;
- usuário dinâmico grava apenas no StateDirectory;
- segunda execução substitui o snapshot completo;
- falha antes do rename não destrói a versão anterior;
- timer perdido durante desligamento segue a política Persistent;
- desligamento não deixa temporário.

## Observabilidade

O serviço registra somente conclusão no journal. O arquivo contém o estado.
Um monitor mínimo verifica:

- resultado da última execução da unit;
- idade de ultima-execucao.txt;
- schema esperado;
- tamanho dentro de limite;
- espaço disponível no filesystem;
- último backup verificado.

Não use o próprio arquivo como única prova de que a unit executou: correlacione
timestamp, status e journal.

## Backup e restauração

O snapshot é derivado e pode ser recriado. Configuração, units, testes e
runbooks são a parte importante. Para o exercício:

1. gere duas versões sintéticas;
2. faça backup com o exemplo versionado;
3. verifique checksum;
4. restaure em árvore vazia;
5. valide units usando caminhos da árvore restaurada;
6. execute coleta sem instalar;
7. compare com o contrato.

Mensure RPO e RTO. Archive no mesmo disco da origem não é cópia independente.

## Extensões permitidas

- saída JSON adicional mantendo compatibilidade;
- teste unitário Python sem dependência externa;
- empacotamento nativo em staging;
- métrica de idade e resultado da unit;
- runbook de atualização e rollback;
- regra MAC mínima para a distro usada.

Não adicione varredura, coleta de credenciais, execução remota, upload ou
descoberta de outros hosts. Ferramentas de segurança pertencem aos módulos 27
em diante, após a base.

## Definição de pronto

- [ ] A suíte local passa sem privilégio.
- [ ] Staging contém somente arquivos declarados.
- [ ] Units são válidas e cada diretiva é explicável.
- [ ] Falha não sobrescreve a última saída válida.
- [ ] Diff é determinístico e recusa entrada malformada.
- [ ] Restore em árvore vazia passa no mesmo teste.
- [ ] Runbooks permitem operação por outra pessoa.
- [ ] Nenhum segredo ou identificador desnecessário é coletado.
