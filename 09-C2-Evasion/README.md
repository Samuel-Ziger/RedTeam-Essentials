# 09 - C2 & Evasion (Teoria)

> Conteudo **teorico** sobre Command-and-Control (C2) e tecnicas de evasion modernas. **Nao incluimos exploits ou implants prontos** - apenas conceitos, mapeamento ATT&CK e mitigacoes.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes avançados e equipes purple team. |
| Pré-requisitos | Módulos 00, 05 e 14; laboratório isolado. |
| Tempo estimado | 6 horas de teoria e 4 horas de análise defensiva. |
| Ambiente | Somente laboratório próprio/isolado ou engagement autorizado. |
| Evidência final | Diagrama conceitual, hipótese de detecção e plano de cleanup. |
| Critério de conclusão | Demonstrar o objetivo, explicar limitações e registrar o cleanup. |

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

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [Live - Evasão de defesas com C2](https://www.youtube.com/watch?v=OsYdo9H1tNE) — **Ricardo Longatto**.
2. [SISTEMAS DE C2: O QUE OS ATACANTES UTILIZAM,A EVOLUÇÃO DAS FERRAMTENTAS E PROCEDIMENTOS DE DETECÇÃO](https://www.youtube.com/watch?v=ppxiWMvpJrY) — **SecurityCast**.
3. [Parte 2 - Simulando a técnica do adversário](https://www.youtube.com/watch?v=VrbJUbop6aM) — **CMD & Controle**.
4. [C2 e Beacons: O Segredo das Operações de Ataque Persistente](https://www.youtube.com/watch?v=ql0ijCvO7q8) — **Daniel Donda**.
5. [RTVcron | C2 para Red Team: Uma Introdução Prática com Sliver](https://www.youtube.com/watch?v=qRYYJhaRC6U) — **Red Team Village**.
