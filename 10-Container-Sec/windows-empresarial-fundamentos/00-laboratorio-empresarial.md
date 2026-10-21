# 00 — Laboratório empresarial

Use imagens oficiais evaluation, licenças válidas e VMs sem adaptador de rede.
Prepare dois perfis: Server Core e Desktop Experience, cada um com disco de
sistema, dois discos de dados e snapshot limpo.

## Convenções

- nomes sintéticos, sem dados/credenciais da organização;
- UTC nos relatórios;
- toda mudança com ticket fictício, plano, validação e rollback;
- elevação apenas durante a operação;
- nenhum segredo em script, argumento ou Git;
- ISO, instaladores e módulos com origem/hash registrados.

## Maturidade da mudança

1. observar e exportar baseline;
2. simular com `-WhatIf` ou imagem offline;
3. aplicar em clone;
4. executar testes de saúde;
5. reiniciar quando necessário;
6. validar persistência;
7. reverter e validar novamente.

## Evidência

Registro de console, JSON sanitizado, evento, diferença antes/depois e tempo de
recuperação. Screenshot pode complementar, nunca substituir dados estruturados.

