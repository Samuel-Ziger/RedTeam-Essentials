# 09 - C2 & Evasion (Teoria)

> Conteudo **teorico** sobre Command-and-Control (C2) e tecnicas de evasion modernas. **Nao incluimos exploits ou implants prontos** - apenas conceitos, mapeamento ATT&CK e mitigacoes.

## Sumario

| Documento | Tema |
|-----------|------|
| [c2-overview.md](c2-overview.md) | Visao geral de frameworks C2 (Cobalt Strike, Sliver, Mythic, Havoc, Brute Ratel). |
| [evasion-fundamentals.md](evasion-fundamentals.md) | AMSI, ETW, AV/EDR, sandbox detection, unhooking. |
| [opsec-checklist.md](opsec-checklist.md) | Checklist de OpSec durante engagement (artifacts, logs, beacon traffic). |

## Porque so teoria?

Implementacao real de implants/loaders fica fora do escopo educacional aberto. O foco e:

1. Entender **como o atacante pensa**.
2. Mapear ATT&CK para **defesa**.
3. Preparar conteudo academico/CRTO/OSEP.

## MITRE ATT&CK relevante

- T1071 - Application Layer Protocol (C2)
- T1573 - Encrypted Channel
- T1027 - Obfuscated Files or Information
- T1055 - Process Injection
- T1562 - Impair Defenses
- T1140 - Deobfuscate/Decode Files
- T1497 - Virtualization/Sandbox Evasion

## Ferramentas oficialmente publicas (lab apenas)

- [Sliver](https://github.com/BishopFox/sliver) - open source, BSD-3.
- [Mythic](https://github.com/its-a-feature/Mythic) - open source.
- [Havoc](https://github.com/HavocFramework/Havoc) - open source.
- [Caldera](https://github.com/mitre/caldera) - MITRE oficial, defensivo + ofensivo.

Cobalt Strike, Brute Ratel sao **licenciados** - mencionados para contexto apenas.
