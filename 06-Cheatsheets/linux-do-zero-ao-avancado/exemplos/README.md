# Exemplos executáveis

Todos os exemplos usam dados sintéticos. O teste automático não pede root,
não toca configuração do host e trabalha em diretório criado por `mktemp`.

| Caminho | Conceito |
|---------|----------|
| `arquivos_seguro.sh` | nomes, links, metadados e iteração com NUL |
| `diagnostico.sh` | coleta somente leitura e saída chave/valor |
| `comparar_diagnosticos.py` | valida e compara dois snapshots sem alterar o host |
| `analisar_logs.awk` | agregação de fluxo textual sintético |
| `backup_versionado.sh` | archive, hash e restauração sem exclusão |
| `c/processos.c` | `fork`, pipe, descritores e `waitpid` |
| `c/memoria.c` | reserva, toque de páginas e page faults |
| `c/syscalls.c` | cópia por `open`, `read`, `write` e `close` |
| `systemd/` | serviço/timer endurecidos, não instalados |
| `kernel/` | módulo mínimo, apenas compilação opcional |

Execute tudo que for seguro:

```bash
bash ../testar-curso.sh
```

Para compilar manualmente:

```bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror c/processos.c -o processos
cc -std=c17 -Wall -Wextra -Wpedantic -Werror c/memoria.c -o memoria
cc -std=c17 -Wall -Wextra -Wpedantic -Werror c/syscalls.c -o syscalls
```

O módulo de kernel exige headers da release em execução. Compilar não o
carrega. `insmod`/`modprobe` não aparecem no executor; se optar pelo laboratório
manual, use a VM descartável e siga `laboratorios/kernel.md`.

Para comparar dois diagnósticos, mantendo diferenças de horário fora do ruído:

~~~bash
./diagnostico.sh > antes.txt
./diagnostico.sh > depois.txt
python3 comparar_diagnosticos.py antes.txt depois.txt
~~~

O comparador limita entradas a 1 MiB, rejeita chaves inválidas ou duplicadas,
ordena o resultado e só retorna status 1 por diferença quando
`--fail-on-change` é solicitado.
