# 16 — Vazamentos de DNS, IPv6 e WebRTC

“Vazamento” significa que um fluxo saiu por caminho diferente do declarado pelo
modelo. Para diagnosticar, primeiro defina o comportamento esperado.

## DNS

Uma VPN de túnel completo pode definir resolvedor no túnel. Interfaces com
prioridades incorretas, fallback do sistema ou aplicativos com resolvedor
próprio podem usar outro caminho. Split DNS corporativo pode ser intencional;
documente zonas e fallback.

## IPv6

Se o túnel cobre apenas IPv4 e o sistema mantém rota IPv6 externa, destinos
podem ser alcançados fora do túnel. Soluções corretas são suportar IPv6 de ponta
a ponta ou bloquear explicitamente o protocolo enquanto o túnel estiver ativo.
Desativação indiscriminada não substitui projeto e pode quebrar redes modernas.

## WebRTC

Comunicações em tempo real usam mecanismos de descoberta e travessia de NAT.
Navegadores modernos aplicam proteções, mas política, versão e permissões
importam. Teste apenas o próprio navegador e interprete endereços candidatos
com contexto; um endereço privado não é exposição direta à internet.

## Fail-open e fail-closed

Quando o túnel cai, o sistema pode restaurar a rota comum. Um kill switch busca
bloquear esse fallback, mas pode interromper DNS, atualizações e administração.
Defina exceções mínimas e um rollback fora de banda antes de ativá-lo.

## Prática segura

Crie uma matriz de testes para túnel ativo, reinício, troca de Wi-Fi e queda do
gateway. Registre resultado esperado para IPv4, IPv6 e DNS sem consultar alvos
de terceiros além de serviços públicos que você conscientemente escolheu.

