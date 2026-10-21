# 11 — 802.1X, NAC e port security

802.1X controla acesso por porta com supplicant (cliente), authenticator
(switch/AP) e servidor AAA, frequentemente RADIUS. EAP transporta o método de
autenticação. Certificados de máquina/usuário podem oferecer identidade mais
forte que senha compartilhada.

NAC combina identidade, postura e política para atribuir VLAN, ACL ou papel.
MAB usa MAC como fallback para dispositivos sem supplicant; é identificação
fraca e precisa de restrição/monitoramento.

Port security limita MACs aprendidos e define reação, mas pode quebrar telefone
com PC, dock, virtualização e mobilidade. Ele não substitui 802.1X.

## Alta disponibilidade

Planeje comportamento quando AAA está indisponível: fail-open, fail-closed ou
VLAN crítica conforme risco. Proteja segredo/certificados, sincronize horário e
registre correlação entre sessão, porta e identidade com retenção proporcional.
