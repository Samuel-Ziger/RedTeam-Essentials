# 05 — Memória virtual, compressão e pressão

Cada processo enxerga um espaço virtual mapeado para memória, arquivos e regiões
compartilhadas. O sistema pode comprimir páginas e usar swap. Resident, virtual,
compressed e purgeable medem coisas diferentes.

```zsh
vm_stat
memory_pressure
footprint PID
vmmap PID
```

Colete apenas de processo próprio. Dumps podem conter tokens, documentos e
segredos. Uma alta alocação virtual não prova vazamento; observe crescimento
retido sob carga repetível e compare gerações.

Jetsam é mais associado a outras plataformas Apple; no Mac, analise memory
pressure, compressor, swap e políticas do processo sem transferir conclusões.

## Prática

Meça um programa de fixture em repouso, carga e recuperação. Explique working
set e por que uma fotografia isolada não estabelece causa.
