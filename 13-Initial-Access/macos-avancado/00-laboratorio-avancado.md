# 00 — Laboratório avançado e fronteiras

Use um Mac de teste suportado com Xcode Command Line Tools, conta padrão e
backup. Separe quatro zonas: sistema observado, fontes versionadas, fixtures
sintéticas e artefatos descartáveis. Nunca use dados reais de TCC, Keychain ou
perfis corporativos.

## Classes de prática

- **L0:** parser/teste offline em qualquer sistema;
- **L1:** consulta read-only no Mac;
- **L2:** compilação e assinatura ad hoc de código próprio;
- **L3:** mudança em VM/Mac descartável com backup;
- **fora do curso:** redução de controles, kext, exploit e coleta pessoal.

Registre arquitetura, versão/build, toolchain e hashes dos fontes. Não use
`sudo` em build. O diretório de saída deve ser temporário e removível.

## Prática

Execute a validação estrutural, testes Python e compile a dylib segura. Entregue
uma matriz que ligue cada lab a risco, contenção, evidência e cleanup.
