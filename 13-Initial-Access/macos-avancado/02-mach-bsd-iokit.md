# 02 — Mach, BSD e IOKit

Mach fornece tarefas, threads, espaços de endereçamento, ports, mensagens e
agendamento fundamental. BSD fornece modelo de processo Unix, credenciais,
arquivos, sockets e syscalls. IOKit organiza drivers e objetos de I/O.

Uma aplicação pode enxergar PID pelo modelo BSD e task/thread pelo modelo Mach.
Mach ports são capacidades com direitos; não são portas TCP/UDP. Essa distinção
evita misturar IPC local com redes.

Drivers modernos devem preferir DriverKit/System Extensions quando a Apple
oferece a classe necessária. Kexts ampliam impacto no kernel e não fazem parte
dos laboratórios.

## Prática

Classifique dez conceitos entre Mach, BSD, IOKit e user space. Para cada um,
registre a interface pública e o tipo de evidência que comprovaria uma hipótese.
