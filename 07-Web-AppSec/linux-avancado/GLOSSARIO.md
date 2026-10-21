# Glossário

- **ABI:** contrato binário entre componentes, incluindo calling convention,
  layout de dados, números de syscall e formato de objetos.
- **acquire/release:** par de operações que ordena publicação e consumo de
  estado entre CPUs segundo um protocolo definido.
- **ASLR:** randomização de endereços de regiões do processo; depende de PIE
  para deslocar o executável principal.
- **backing file:** imagem base da qual um overlay qcow2 depende para ler blocos
  ainda não modificados.
- **bio:** descrição de uma operação sobre setores e páginas entregue à camada
  de bloco.
- **build ID:** identificador que liga um binário ao debug info da mesma build.
- **BTF:** metadados de tipos usados pelo kernel e pelo BPF CO-RE.
- **cgroup v2:** hierarquia unificada que contabiliza e distribui recursos entre
  grupos de processos.
- **completion:** notificação de que uma operação assíncrona terminou; não deve
  ser confundida com readiness.
- **CQE/SQE:** entradas de completion e submission usadas pelos rings do
  io_uring.
- **dentry:** objeto do VFS que associa um nome a um inode no cache de caminhos.
- **DMA:** acesso de dispositivo à memória sem cópia byte a byte pela CPU.
- **EEVDF:** modelo fair que usa elegibilidade, lag e deadline virtual para
  escolher a próxima entidade.
- **ELF:** formato de executáveis, objetos, bibliotecas e core dumps em Linux.
- **folio:** abstração do MM para uma ou mais páginas base gerenciadas juntas.
- **grace period:** intervalo de RCU após o qual leitores anteriores relevantes
  já atravessaram um estado quiescente.
- **hardirq:** contexto imediato de tratamento de interrupção, no qual dormir
  não é permitido.
- **HugeTLB:** pools explícitos de páginas grandes com semântica diferente de
  Transparent Huge Pages.
- **IOMMU:** tradução e proteção de endereços usados por dispositivos.
- **IOVA:** endereço de I/O visto pelo dispositivo antes da tradução da IOMMU.
- **IRQ:** sinal de interrupção de hardware; softirq é trabalho adiado no kernel.
- **KASLR:** randomização do endereço de carga do kernel.
- **Kconfig/kbuild:** linguagem de configuração e sistema de build do kernel.
- **kdump:** mecanismo que transfere a execução para um crash kernel e captura
  vmcore após panic.
- **lag:** diferença entre serviço ideal e recebido por uma entidade fair.
- **LSM:** framework de hooks de segurança usado por SELinux, AppArmor e outros.
- **open file description:** objeto do kernel compartilhável por descritores que
  contém offset e status da abertura.
- **MM:** subsistema de gerenciamento de memória do kernel.
- **NUMA:** arquitetura em que o custo de acesso à memória depende do nó.
- **PIE:** executável position-independent, normalmente ELF `ET_DYN`, que pode
  ser deslocado pelo loader.
- **pidfd:** descritor que representa uma instância de processo sem depender
  apenas de um número PID reutilizável.
- **page fault:** exceção causada por tradução ausente ou acesso incompatível.
- **page cache:** cache de dados de arquivos mantido pelo kernel em RAM.
- **PMU:** contadores de desempenho fornecidos pelo processador.
- **PSI:** métrica de tempo perdido por pressão de CPU, memória ou I/O.
- **RCU:** família de mecanismos para leituras baratas e liberação adiada.
- **readiness:** indicação de que uma operação provavelmente progride sem
  bloquear; não garante conclusão integral.
- **reclaim:** recuperação de páginas para atender novas alocações.
- **RELRO:** endurecimento que torna regiões de relocations somente leitura após
  o trabalho necessário do loader.
- **root hash:** digest raiz de uma Merkle tree; precisa ser autenticado por uma
  cadeia externa para servir como âncora de integridade.
- **scheduler:** subsistema que escolhe qual tarefa executa em cada CPU.
- **seqlock:** protocolo em que writer serializa atualização e reader repete ao
  detectar mudança concorrente.
- **SMP:** sistema com múltiplas CPUs lógicas compartilhando memória.
- **softirq:** contexto de trabalho adiado no kernel, ainda com restrições
  diferentes de uma thread comum.
- **THP:** promoção automática ou orientada de mappings para páginas maiores.
- **TLB:** cache de traduções de endereço virtual para físico.
- **verifier:** analisador do kernel que exige segurança demonstrável dos
  caminhos de um programa BPF antes de carregá-lo.
- **tracepoint:** ponto de instrumentação estável declarado no código do kernel.
- **UKI:** imagem PE única que pode reunir kernel, initrd, linha de comando e metadados.
- **VFS:** camada comum que apresenta operações de arquivo a filesystems distintos.
- **vDSO:** objeto mapeado pelo kernel para certas operações sem transição completa.
- **virtio:** família de dispositivos paravirtualizados para convidados virtuais.
- **VM exit:** retorno de uma vCPU ao hypervisor ou QEMU para tratar evento que
  não continuou diretamente no guest.
- **VMA:** intervalo do espaço virtual com permissões e backing semelhantes.
- **writeback:** envio de páginas sujas do cache para o armazenamento.
