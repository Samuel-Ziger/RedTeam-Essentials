# 36 — Elevação de privilégios em Linux e Windows

Esta etapa ensina a revisar fronteiras de privilégio, identificar configurações
fracas em hosts de laboratório e converter cada achado em hardening, detecção
e teste de regressão.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Administração Linux/Windows, hardening, Red, Blue e Purple Team. |
| Pré-requisitos | Módulos `27`, `28`, `31` e `35`. |
| Tempo estimado | 50–80 horas. |
| Ambiente | VMs locais descartáveis e snapshots conhecidos. |
| Foco | Permissões, serviços, caminhos, credenciais, mitigações e evidência. |
| Evidência final | Matriz de caminhos de privilégio com correção e reteste. |
| Critério de conclusão | Caminhos demonstrados com impacto mínimo, corrigidos e retestados. |

## Conteúdo curricular

- [Privesc Linux e Windows](privesc-linux-windows/README.md)
- [Catálogo de cheatsheets](acervo/LEGADO-CHEATSHEETS.md)
- [Linux: PATH hijacking](acervo/linux/linux_path_hijacking.md)
- [Linux: metodologia moderna](acervo/linux/linux_privesc_modern.md)
- [Linux: fundamentos teóricos](acervo/linux/linux_privesc_teoria.md)
- [Windows: metodologia](acervo/windows/windows_privesc_metodologia.md)
- [Windows: teoria](acervo/windows/windows_privesc_teoria.md)
- [PowerShell de apoio](acervo/windows/powershell_cheatsheet.md)

Próximo: [Módulo 37 — Pós-exploração e movimento lateral](../37-Pos-Exploracao-Movimento-Lateral/README.md).
