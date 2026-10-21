# 23 — Projeto final: engenharia de uma frota Mac

Projete uma frota sintética sem conectividade real. O objetivo é integrar
internals, software, política, identidade, telemetria e recuperação.

## Entregáveis

1. matriz de hardware/arquitetura e lifecycle;
2. parser Mach-O e dylib segura com testes;
3. pipeline de build→sign→notarize modelado sem credenciais;
4. catálogo de perfis com ownership e remoção;
5. modelo ADE/MDM/DDM offline e estados de enrollment;
6. identity lifecycle e FileVault escrow conceitual;
7. baseline/drift/exceções com privacidade;
8. anéis de update, telemetria e critérios de parada;
9. resposta a app incompatível e recuperação de dispositivo.

## Defesa oral

Explique quais garantias vêm de XNU, assinatura, Gatekeeper, TCC, MDM e processo
organizacional. Marque tudo que não pode ser implantado antes do módulo de redes.

Reprova se houver segredos, serial real, bypass de controle ou afirmação de
compliance sem evidência efetiva.
