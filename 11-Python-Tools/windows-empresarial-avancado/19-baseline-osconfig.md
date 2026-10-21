# 19 — Security baseline, OSConfig e exceções

Windows Server 2025 inclui caminhos de baseline/OSConfig que devem ser avaliados
contra role e compatibilidade. Security Compliance Toolkit fornece artefatos
para plataformas suportadas. A fonte oficial evolui: fixe versão e data.

## Processo

1. associe servidor/endpoint a perfil;
2. importe baseline como referência versionada;
3. transforme settings em controles com IDs;
4. avalie current × desired sem mutação;
5. classifique incompatibilidade por workload;
6. pilote e teste operações/recuperação;
7. aplique por autoridade única;
8. monitore drift;
9. revise a cada release.

## Exceção

Precisa de controle, valor divergente, motivo, risco, compensação, owner,
approver, início, expiração e evidência. Exceção sem prazo é baseline paralelo.

## Exercício

Mapeie dez settings de uma baseline oficial atual a um perfil fictício. Não
importe/aplique pacote no host; use comparador offline e tabletop.

