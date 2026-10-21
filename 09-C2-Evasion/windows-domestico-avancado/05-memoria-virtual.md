# 05 — Memória virtual, commit, working set e faults

“Memória usada” mistura conceitos. Cada processo enxerga espaço virtual; o
sistema mantém compromisso de backing, páginas residentes e cache reutilizável.
Diagnóstico correto liga cada contador à pergunta e observa comportamento no tempo.

## Objetivos

- distinguir endereço virtual, reserva, commit e residência;
- interpretar working set, private bytes e commit do sistema;
- diferenciar soft e hard page faults;
- reconhecer imagem, mapped file, heap, stack e memória privada;
- testar alocação somente numa fixture com limite explícito.

## Espaço virtual por processo

Endereço virtual não é endereço físico. Tabelas de páginas mapeiam intervalos
virtuais para páginas físicas, backing em arquivo ou estado ainda não residente.
Isolamento impede que processos comuns leiam livremente o espaço uns dos outros.

Reserva separa uma faixa de endereços para uso futuro. Commit cria compromisso de
backing para páginas, limitado aproximadamente por RAM e pagefiles, com detalhes
do gerenciador. Tocar páginas pode fazê-las entrar no working set. Liberar exige
seguir a API e granularidade corretas.

Um programa pode reservar grande espaço sem comprometer backing equivalente. Pode
comprometer páginas e ainda não tê-las todas residentes. Portanto “endereço
reservado”, “commit” e “RAM consumida agora” são três medidas diferentes.

## Categorias observadas

- **private:** páginas comprometidas exclusivas do processo;
- **image:** mapeamentos de EXE/DLL com semântica de imagem;
- **mapped file:** conteúdo de arquivo mapeado;
- **heap:** alocador para objetos/blocos, possivelmente vários heaps;
- **stack:** intervalo por thread, com reserva e commit progressivo;
- **shareable/shared:** páginas que podem aparecer em mais de um processo;
- **working set:** páginas residentes atribuídas ao processo naquele instante.

VMMap apresenta essas categorias para um processo próprio. A soma e os nomes são
visões da ferramenta, não uma contabilidade simples de “RAM exclusiva”.

## Commit do sistema

```powershell
Get-Counter '\Memory\Committed Bytes','\Memory\Commit Limit',
  '\Memory\Available MBytes'

Get-Process |
  Sort-Object WorkingSet64 -Descending |
  Select-Object -First 10 Name, Id, WorkingSet64,
    PrivateMemorySize64, VirtualMemorySize64
```

Memória disponível inclui páginas que podem ser reaproveitadas; “livre” isolada
não mede saúde. Cache ocupando RAM pode melhorar desempenho. Pressão aparece em
commit próximo do limite, faults custosos, trimming e impacto observável, não
apenas em um número alto no Task Manager.

Contadores precisam de intervalo. Uma amostra depois do sintoma pode perder o
pico. Registre carga, warm-up e versão da fixture.

## Page faults

Fault ocorre quando a tradução/acesso não está pronto. Pode ser resolvido sem I/O
de disco: página na standby list, copy-on-write ou zero page são exemplos. Hard
fault exige obter backing por caminho mais caro, normalmente armazenamento. Nem
todo fault indica problema; é parte normal da memória sob demanda.

Taxa alta só importa com latência/throughput afetados e contexto de carga. Não
desative pagefile tentando eliminar faults: isso reduz commit limit e pode piorar
confiabilidade.

## Heap, stack e vazamento

Vazamento é memória que permanece alcançada/alocada sem utilidade ao longo de
operações repetidas. Crescimento durante cache warm-up não basta. Defina carga
constante, execute ciclos, force estado comparável quando aplicável e observe
tendência de private bytes/commit.

Stack cresce conforme chamadas e uso local; recursão sem limite pode esgotá-la.
Heap corruption e use-after-free são assuntos de desenvolvimento seguro, mas o
curso não transforma falhas em exploração. A análise termina em causa e correção.

## Experimento de alocação

Crie uma fixture própria com parâmetros `--reserve-mib`, `--commit-mib` e
`--touch`, todos com limite de 256 MiB na VM. Execute primeiro reservando,
depois comprometendo e finalmente tocando páginas. Colete VMMap e contadores
antes/durante/depois. Se não implementar em C, use uma pequena matriz em processo
PowerShell separado e reconheça que runtime/GC adiciona variáveis.

Não use loop ilimitado, não tente provocar paginação extrema e pare se o sistema
ficar sem reserva de segurança. Feche cooperativamente e confirme retorno dos
contadores — sabendo que cache e runtime podem não voltar ao valor exato.

## Exercícios

1. Desenhe virtual → PTE → RAM/backing e marque reserva/commit/residência.
2. Compare working set, private bytes, virtual size e commit do sistema.
3. Explique três faults que não exigem leitura de disco.
4. Planeje um teste que distingue cache legítimo de vazamento.
5. Execute a fixture limitada e produza gráfico com pelo menos dez amostras.

## Checklist de domínio

- [ ] Endereço virtual não é tratado como endereço físico.
- [ ] Reserva, commit e working set são medidas distintas.
- [ ] Memória disponível inclui cache reaproveitável.
- [ ] Page fault não é automaticamente acesso a disco ou erro.
- [ ] Vazamento exige tendência sob carga repetível.
- [ ] Experimento possui teto, critério de parada e processo próprio.
- [ ] Dumps de memória não são necessários para esta prática.
