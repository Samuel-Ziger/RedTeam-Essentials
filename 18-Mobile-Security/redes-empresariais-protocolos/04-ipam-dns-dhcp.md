# 04 — IPAM, DNS e DHCP empresariais

IPAM mantém blocos, prefixos, endereços, VRFs, VLANs, status, dono e reserva.
Ele deve ser fonte autoritativa e integrar DNS/DHCP, evitando planilhas paralelas.
Alocação hierárquica por região/site/função permite sumarização e crescimento.

DNS empresarial separa recursão, autoridade, zonas internas/externas, views
quando indispensáveis, DNSSEC, logs e gestão de mudança. Split-horizon adiciona
complexidade e deve ter testes. Transfers e updates exigem autenticação/allowlist.

DHCP usa pares redundantes conforme implementação e relay por segmento. Controle
de DHCP não autorizado em switches reduz servidores rogue; registre Option 82
somente com privacidade/finalidade. Monitore pool, conflitos, latência e leases.

## DDI

DNS, DHCP e IPAM formam DDI. Mudança atômica e reconciliação evitam que IPAM
diga “livre” enquanto DNS ou DHCP ainda utiliza o endereço.
