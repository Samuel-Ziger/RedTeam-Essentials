# Inventário de imagens do laboratório do Módulo 30

Digests consultados nos manifests públicos em **29 de setembro de 2026**. O
Compose usa o digest do manifest ou índice multi-plataforma, preservando as
arquiteturas publicadas pelo fornecedor.

| Componente | Referência verificada |
|------------|------------------------|
| DVWA | `vulnerables/web-dvwa@sha256:dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7` |
| Juice Shop | `bkimminich/juice-shop@sha256:73c53fbf442e8337b3ea3d98c7e8550308854701ebdfce4cc39768f36b75430e` |
| bWAPP | `raesene/bwapp@sha256:2f41183ea9f9e8fb36678d7a2a0c8a9db9a59f4569cee02fe6664b419b2600ee` |
| WebGoat | `webgoat/webgoat@sha256:d4ac9fc2b0a41b68d64dedde684f4783aa60cc785838435a6d5bd5a25b387497` |
| VAmPI | `erev0s/vampi@sha256:0a5a224b6e14ae7da6a6ea265178ff71286ff903aec74adee98f660bb0e4ca12` |
| Nginx (gateway local) | `nginx:1.29.1-alpine@sha256:42a516af16b852e33b7682d5ef8acbd5d13fe08fecadc7ed98605ba5e3b26ab8` |
| Kali rolling | `kalilinux/kali-rolling@sha256:d1d7e581ed60b0bbf9cb8a4bc853526355978f3b943d3a1d7dc7ce209e4231b6` |

## Atualização controlada

1. consulte o manifest da tag desejada;
2. revise origem, arquiteturas e data de publicação;
3. troque o digest em uma branch;
4. rode `python3 rte.py validate` e `python3 rte.py lab config`;
5. execute smoke tests locais antes do merge.

Vulnerable WordPress e NodeGoat foram removidos do Compose porque as imagens
antes declaradas não estavam acessíveis no registry. Eles podem voltar apenas
com uma origem verificável, build reproduzível e healthcheck testado.
