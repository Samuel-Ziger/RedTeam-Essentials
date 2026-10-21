# Guia de diagnóstico Linux por evidências

Este guia não substitui os capítulos. Ele organiza o raciocínio quando o
sistema não faz o esperado. O objetivo não é colecionar comandos: é localizar
a primeira camada divergente, preservar evidência e aplicar a menor correção
capaz de testar a hipótese.

## 1. O contrato do diagnóstico

Antes de tocar o sistema, escreva:

~~~text
Esperado:
Observado:
Primeira ocorrência:
Frequência:
Usuários e serviços afetados:
Última mudança conhecida:
Janela disponível:
Estado que não pode ser perdido:
Como validar a recuperação:
~~~

“Não funciona”, “está lento” e “caiu” são relatos iniciais, não diagnósticos.
Transforme-os em comportamento mensurável. Exemplo: “a unit termina com status
1 em até dois segundos desde o boot atual; execução manual como meu usuário
funciona”. Essa frase já separa contexto interativo, identidade, ambiente e
supervisão.

## 2. Preserve antes de alterar

Colete horário, release, kernel, boot, identidade, estado da unidade e mensagens
do intervalo relevante. Não reinicie imediatamente: o restart pode eliminar o
processo, descritores, memória, fila e mensagem que explicavam a falha.

~~~bash
date --iso-8601=seconds
cat /etc/os-release
uname -a
id
uptime
systemctl --failed 2>/dev/null || true
journalctl -b -p warning..alert --no-pager 2>/dev/null
~~~

Saneie hostname, serial, endereço, nome de usuário, caminho pessoal, tokens e
conteúdo de aplicação antes de compartilhar. O script
[diagnostico.sh](exemplos/diagnostico.sh) produz um conjunto pequeno, somente
leitura e sem identificadores de rede.

## 3. Escada universal

Percorra nesta ordem:

1. **Escopo:** uma conta, um processo, a VM, todos os hosts?
2. **Tempo:** desde quando, contínuo ou intermitente, ligado a qual mudança?
3. **Estado:** processo, unit, montagem, pacote e configuração efetiva.
4. **Recursos:** CPU, memória, I/O, descritores, tarefas e espaço.
5. **Política:** permissões, ACL, montagem, SELinux/AppArmor, sandbox e sudo.
6. **Dependência:** arquivo, socket local, relógio, dispositivo ou outro serviço.
7. **Hipótese:** uma afirmação que uma observação pode refutar.
8. **Experimento:** menor mudança, em ambiente controlado, com rollback.
9. **Validação:** teste funcional e ausência de regressão.
10. **Prevenção:** monitor, teste, documentação ou mudança de projeto.

Correlação não prova causa. Se a memória aumentou no mesmo horário do erro,
teste se a carga afetada estava pressionada, se houve reclaim, swap ou OOM e se
o sintoma desaparece ao remover a causa proposta.

## 4. Serviço não inicia

Primeiro descubra quem supervisiona o processo e a configuração efetiva.

~~~bash
systemctl status --no-pager app.service
systemctl cat app.service
systemctl show app.service -p User,Group,Environment,WorkingDirectory
journalctl -u app.service -b --no-pager
systemd-analyze verify /caminho/app.service
~~~

Perguntas em sequência:

| Evidência | Hipótese que testa |
|-----------|--------------------|
| código e status de saída | o programa recusou entrada ou foi encerrado |
| usuário, grupo e diretório | o contexto difere do terminal |
| caminho absoluto e arquivo | artefato ausente ou montagem indisponível |
| configuração validada | sintaxe ou semântica inválida |
| permissões e ACL | DAC impede travessia, leitura ou escrita |
| mensagem MAC | SELinux/AppArmor negou uma operação permitida por DAC |
| limites e cgroup | tarefa, memória ou descritor esgotado |
| dependências da unit | ordem ou requisito incorreto |

Não coloque shell, privilégio ou permissão ampla apenas para “ver se funciona”.
Isso altera múltiplas variáveis e pode esconder a causa. Reproduza com a mesma
identidade e ambiente, corrija uma camada e repita o teste funcional.

## 5. Acesso negado

Resolva o caminho inteiro, não apenas o último arquivo.

~~~bash
id
namei -l /caminho/para/objeto
stat /caminho/para/objeto
getfacl /caminho/para/objeto 2>/dev/null || true
findmnt -T /caminho/para/objeto
~~~

Depois verifique contexto MAC, sandbox da unit, namespace e mapeamento de UID.
Uma permissão de leitura no arquivo não ajuda se falta travessia em um diretório.
Escrita no arquivo não concede remoção do nome; essa ação depende do diretório
pai. Dentro de container, o UID exibido pode mapear para outro UID no host.

Critério de encerramento: a identidade necessária realiza somente a operação
prevista, outra identidade continua impedida e a configuração sobrevive à
recriação.

## 6. Disco cheio ou filesystem indisponível

Separe bytes, inodes, montagem e dispositivo:

~~~bash
findmnt -T /caminho
df -hT /caminho
df -ih /caminho
du -xhd1 /caminho 2>/dev/null | sort -h
lsof +L1 2>/dev/null | head
lsblk -f
~~~

Se df e du divergem, investigue arquivo apagado ainda aberto, snapshot,
metadados, blocos reservados ou conteúdo escondido sob outro mount. Não remova
arquivos de log indiscriminadamente. Descubra produtor, retenção e descritor;
prefira rotação ou encerramento coordenado.

Se uma montagem falha, confira identificador persistente, tipo, opção, unit
gerada e log do boot. Não execute reparador em filesystem montado sem que a
documentação permita. Toda formatação ou alteração de camada ocorre somente na
VM descartável e sobre o arquivo-imagem criado no laboratório.

## 7. Pressão de memória

Não use apenas percentual ocupado.

~~~bash
free -h
vmstat 1 5
cat /proc/pressure/memory
grep -E '^(MemAvailable|Swap|Dirty|Slab)' /proc/meminfo
journalctl -k -g 'oom|Out of memory|Killed process' -b 2>/dev/null
~~~

Observe tendência de MemAvailable, swap-in e swap-out, PSI, faults, reclaim e
eventos OOM. Localize processo e cgroup por RSS e PSS. Page cache recuperável
não é vazamento; VIRT não é RAM residente; swap usada sem atividade não prova
thrashing. A correção pode estar na aplicação, no limite, na concorrência, na
capacidade ou na política de memória.

Nunca provoque OOM no host para aprender. Use o exemplo limitado e, quando
necessário, um escopo de usuário com teto pequeno em uma VM.

## 8. Boot falha

Localize a última camada que funcionou:

| Etapa | Evidência | Recuperação típica |
|-------|-----------|--------------------|
| firmware | entrada e disco visíveis | corrigir ordem ou entrada pela console |
| bootloader | menu e artefatos encontrados | escolher entrada anterior |
| kernel | mensagens iniciais | remover parâmetro temporário ou usar fallback |
| initramfs | raiz e volume descobertos | corrigir driver, UUID ou desbloqueio |
| raiz | filesystem montável | verificar camada e integridade offline |
| PID 1 | target alcançado | rescue ou emergency |
| serviço | unit e journal | corrigir dependência/configuração |

Não reinstale bootloader como primeira tentativa. Use o
[laboratório de recuperação](laboratorios/boot-recovery.md), console do
hypervisor e snapshot. Registre a configuração anterior antes de regenerar
initramfs ou entradas.

## 9. Pacote ou atualização quebrou comportamento

Determine origem e arquivos envolvidos:

~~~bash
apt-cache policy PACOTE 2>/dev/null || true
dpkg-query -S /caminho 2>/dev/null || true
dnf info PACOTE 2>/dev/null || true
rpm -qf /caminho 2>/dev/null || true
~~~

Compare release notes, configuração efetiva, arquivos preservados pelo
gerenciador, processos que ainda usam bibliotecas antigas e necessidade de
reboot. Não misture repositórios nem faça downgrade parcial sem plano. Em uma
transação ampla, recupere primeiro a consistência do gerenciador e valide a
aplicação em ambiente de teste.

## 10. Kernel, módulo ou dispositivo

Colete release, linha de boot, mensagens e associação entre dispositivo e
driver.

~~~bash
uname -r
cat /proc/cmdline
journalctl -k -b --no-pager
lspci -nnk 2>/dev/null
lsusb -t 2>/dev/null
lsmod
~~~

Vermagic incompatível, assinatura recusada, firmware ausente e parâmetro
incorreto são hipóteses diferentes. Não remova módulo do disco, console ou
interface de administração. Teste módulo didático somente no clone descartável,
mantenha kernel anterior inicializável e não desative Secure Boot para contornar
um erro que ainda não foi entendido.

## 11. Sessão desktop falha

Separe login, sessão, compositor, aplicativo, portal e dispositivo. Descubra
tipo de sessão e logs do usuário. Teste a aplicação com perfil temporário antes
de apagar configuração pessoal. Uma falha que ocorre em um único usuário aponta
para escopo diferente de uma falha que ocorre antes do login.

Reiniciar toda a máquina é válido quando faz parte do teste, mas não substitui
coleta. Registre o boot anterior porque vários logs relevantes ficam ali.

## 12. Conectividade local

Neste módulo, confirme apenas se o processo abriu o socket local esperado, em
qual endereço, sob qual identidade e unit. Teoria de IP, DNS, roteamento,
firewall, VLAN e VPN pertence aos módulos 14 a 18.

~~~bash
ss -lntup
ss -xl
systemctl status app.service
curl --fail --show-error http://127.0.0.1:8080/health
~~~

Se o processo não escuta, continue no serviço. Se escuta localmente e a falha
está no caminho entre hosts, entregue à trilha de Redes: origem, destino,
horário, socket esperado, resultado local e mensagem exata.

## 13. Pacote de evidências

Uma entrega de diagnóstico contém:

~~~text
incident.md
├── impacto e linha do tempo
├── esperado versus observado
├── versões e escopo
├── hipóteses testadas
├── saídas saneadas
├── causa sustentada pela evidência
├── mudança e rollback
├── validação funcional
└── prevenção e risco residual
~~~

Nomeie arquivos com horário UTC e origem genérica. Inclua os comandos de coleta,
mas nunca chave privada, token, dump irrestrito de ambiente, serial, endereço de
cliente ou core dump sem revisão.

## 14. Checklist de encerramento

- [ ] O sintoma original foi reproduzido ou sua ausência foi registrada.
- [ ] A primeira camada divergente foi identificada por evidência.
- [ ] A correção alterou somente o necessário para testar a hipótese.
- [ ] O teste funcional passou sob a identidade e contexto reais.
- [ ] Reinício, segunda execução e rollback foram avaliados.
- [ ] Logs e evidências foram saneados.
- [ ] Monitoramento ou teste detectaria recorrência.
- [ ] Causa, consequência e risco residual foram documentados separadamente.
