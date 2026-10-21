# 16 — Diagnóstico, integridade e reparo

Reparo antes de diagnóstico mistura causas, apaga evidência e pode criar outro
problema. Uma investigação competente define o sintoma, reduz hipóteses com
testes baratos e escolhe a intervenção de menor impacto.

## Objetivos

- escrever uma definição operacional do problema;
- construir hipóteses que possam ser refutadas;
- ordenar coleta e reparo por custo e risco;
- interpretar DISM, SFC e CHKDSK sem tratá-los como ritual;
- usar recuperação e reinstalação apenas quando evidência justificar.

## Definição do problema

“Windows lento” não é um diagnóstico. Pergunte: qual ação demora, desde quando,
em toda execução ou às vezes, para qual conta, por quanto tempo e com qual
impacto? Registre mudanças recentes e o último estado conhecido como bom.

Uma boa definição seria: “ao abrir a fixture de 2 MiB no aplicativo X, entre
14:00 e 14:10 UTC, a janela leva 25 segundos para responder; outros arquivos e
aplicativos abrem em menos de 2 segundos”. Agora existem comparadores e intervalo.

Não confunda reprodução com dano. Use dados sintéticos e uma VM. Se reproduzir
ameaça integridade do sistema ou dados, pare e trabalhe numa cópia.

## Hipóteses e testes

Liste de três a cinco explicações e, para cada uma, evidência esperada, evidência
contrária e teste de baixo impacto. Priorize por probabilidade, impacto e custo
do teste. Atualize a tabela à medida que aprende; não proteja a primeira hipótese.

```text
Hipótese: volume sem espaço suficiente
A favor: poucos GiB livres durante o sintoma
Contra: espaço estável e outro volume apresenta a mesma falha
Teste: consultar Get-Volume e reproduzir com fixture controlada
```

Colete baseline de build, espaço, horário, confiabilidade, eventos do intervalo,
versão/assinatura do componente e contexto da conta. Reiniciar pode ser teste,
mas encerra processos e altera estado; registre antes.

## Ordem de menor impacto

1. confirmar sintoma, alvo, hora e escopo;
2. consultar espaço, build, update e confiabilidade;
3. correlacionar eventos e mudança recente;
4. verificar arquivo, assinatura e configuração documentada;
5. reproduzir com fixture ou outra conta, quando seguro;
6. usar Safe Mode ou inicialização seletiva com plano de retorno;
7. executar ferramenta oficial de integridade indicada;
8. fazer rollback/restauração;
9. reinstalar somente após preservar e testar dados.

## DISM, SFC e CHKDSK

Essas ferramentas respondem perguntas diferentes:

```powershell
DISM.exe /Online /Cleanup-Image /CheckHealth
DISM.exe /Online /Cleanup-Image /ScanHealth
sfc.exe /verifyonly
chkdsk.exe C: /scan
```

`DISM /CheckHealth` consulta se a imagem já foi marcada como corrompida;
`/ScanHealth` examina o Component Store e pode demorar. `/RestoreHealth` tenta
repará-lo e altera estado. SFC verifica arquivos protegidos usando componentes
confiáveis; `/verifyonly` não repara, enquanto `/scannow` pode reparar. CHKDSK
`/scan` faz verificação online de NTFS; opções como `/f` programam ou realizam
correções e podem exigir indisponibilidade.

Não execute os três automaticamente para qualquer sintoma. Faça backup, leia a
ajuda da build, use console elevado apenas quando necessário, guarde código de
saída/log e valide o problema original depois. “A ferramenta concluiu” não prova
que a causa foi resolvida.

## Boot, Safe Mode e WinRE

Windows Recovery Environment oferece Startup Repair, opções de inicialização,
restauração, remoção de atualização, reset e terminal conforme a instalação.
BitLocker pode pedir recovery key. Letras de volume podem mudar. Identifique o
sistema por conteúdo e estrutura antes de operar.

Safe Mode reduz drivers e componentes para diferenciar dependências; não é um
modo para uso permanente. Se o problema desaparece, isso reduz o espaço de
hipóteses, mas ainda não identifica sozinho o culpado.

Para tela azul, registre stop code, horário, build, alteração recente e caminho
do dump, se disponível. Não publique dump: ele pode conter dados. O módulo 09
trata depuração em profundidade.

## Experimento de pouco espaço

No segundo volume descartável, crie uma fixture limitada e mensurável sem
preencher completamente o disco. Registre espaço inicial, aumente o arquivo até
um limiar planejado, observe o alerta de sua função de inventário, remova apenas
a fixture e confirme recuperação. Não execute no volume do sistema e não use um
loop sem limite.

## Relatório de diagnóstico

Inclua definição, impacto, linha do tempo, baseline, hipóteses ordenadas, testes,
resultados, intervenção, rollback e validação independente. Se a causa não for
demonstrada, escreva “causa não confirmada” e entregue próximo teste. Honestidade
é melhor que uma narrativa falsa.

## Exercícios

1. Reescreva três sintomas vagos como definições mensuráveis.
2. Crie uma matriz de hipóteses para aplicativo que não inicia.
3. Explique diferenças entre DISM CheckHealth, ScanHealth e RestoreHealth.
4. Execute apenas verificações compatíveis com uma hipótese e interprete saída.
5. Construa uma árvore de decisão entre Safe Mode, restauração e reinstalação.

## Checklist de domínio

- [ ] Sintoma possui ação, tempo, escopo, frequência e impacto.
- [ ] Toda hipótese tem teste que pode refutá-la.
- [ ] Evidência é coletada antes de reiniciar ou reparar.
- [ ] DISM, SFC e CHKDSK não são usados como receita genérica.
- [ ] Elevação e reparo ocorrem só quando necessários.
- [ ] WinRE e Safe Mode são escolhidos por hipótese e com recovery key disponível.
- [ ] A conclusão admite incerteza quando a causa não foi demonstrada.
