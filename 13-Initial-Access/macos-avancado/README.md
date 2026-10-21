# macOS II — internals, engenharia e administração empresarial

Especialização em Darwin/XNU, Mach, BSD, IOKit, memória, Mach-O, `dyld`,
`launchd`, APFS, assinatura, notarização, sandbox, TCC, observabilidade e gestão
de frota. O foco é engenharia legítima, diagnóstico e defesa.

## Contrato de aprendizagem

| Campo | Definição |
|---|---|
| Nível | Intermediário a avançado |
| Duração | 260–380 horas |
| Pré-requisito | Módulo 12 e fundamentos de C/Python do módulo 00 |
| Ambiente | Mac de teste suportado, Xcode CLT e fixtures offline |
| Evidência | Parser Mach-O, dylib segura, perfis auditados e projeto de frota |
| Conclusão | Explicar internals e projetar gestão defensiva com rastreabilidade |

## Limites

Não há bypass de TCC/SIP/Gatekeeper, injeção, persistência furtiva, roubo de
Keychain, malware ou exploração. MDM, ADE, Platform SSO e serviços de identidade
são modelados offline; APNs, DNS, certificados remotos, VPN, firewall e demais
dependências aguardam o módulo de redes.

## Rota

| # | Capítulo |
|---:|---|
| 00 | [Laboratório avançado](00-laboratorio-avancado.md) |
| 01 | [Darwin e arquitetura XNU](01-darwin-xnu.md) |
| 02 | [Mach, BSD e IOKit](02-mach-bsd-iokit.md) |
| 03 | [arm64, arm64e e binários universais](03-arm64-rosetta-universal.md) |
| 04 | [Processos, threads e IPC](04-processos-threads-ipc.md) |
| 05 | [Memória virtual e pressão](05-memoria-virtual.md) |
| 06 | [Mach-O e load commands](06-mach-o.md) |
| 07 | [`dyld`, dylibs e rpaths](07-dyld-dylibs.md) |
| 08 | [`launchd` e bootstrap domains](08-launchd-dominios.md) |
| 09 | [APFS, snapshots e SSV](09-apfs-internals.md) |
| 10 | [Assinatura e requisitos](10-code-signing.md) |
| 11 | [Notarização, Gatekeeper e quarentena](11-notarizacao-gatekeeper.md) |
| 12 | [Sandbox, Hardened Runtime e entitlements](12-sandbox-hardened-runtime.md) |
| 13 | [TCC e privacidade](13-tcc-privacidade.md) |
| 14 | [System Extensions, DriverKit e Endpoint Security](14-system-extensions.md) |
| 15 | [Unified Logging e signposts](15-unified-logging.md) |
| 16 | [Instruments e performance](16-instruments-performance.md) |
| 17 | [Crash reports e LLDB](17-crash-lldb.md) |
| 18 | [Configuration profiles](18-configuration-profiles.md) |
| 19 | [MDM, ABM e Automated Device Enrollment](19-mdm-abm-ade.md) |
| 20 | [Declarative management e updates](20-ddm-updates.md) |
| 21 | [Identidade, tokens e Platform SSO](21-identidade-tokens-sso.md) |
| 22 | [Baseline, compliance e privacidade](22-baseline-compliance.md) |
| 23 | [Projeto final](23-projeto-final.md) |

## Materiais

- [Laboratórios](laboratorios/README.md)
- [Código Python/C e testes](exemplos/README.md)
- [Glossário](GLOSSARIO.md)
- [Consulta rápida](CHEATSHEET.md)
- [Respostas orientativas](RESPOSTAS.md)
- [Referências](REFERENCIAS.md)
