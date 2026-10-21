# 00 — Laboratório avançado, dados e método causal

Ferramentas de internals observam memória, stacks, caminhos, argumentos e eventos
que podem conter informação sensível. Este módulo exige um laboratório mais
rigoroso que o anterior: toda captura tem pergunta, limite, retenção e cleanup.

## Objetivos

- preparar uma VM reproduzível para compilação, tracing e depuração;
- classificar a sensibilidade de traces, dumps, símbolos e logs;
- criar baselines de ferramenta, sistema e proteções;
- formular hipóteses causais antes de capturar;
- impedir que introspecção legítima alcance processos ou dados de terceiros.

## Topologia e perfis

Use clone da VM concluída no módulo 08, Windows 11 x64 suportado, conta cotidiana
comum, elevação separada, dois discos e adaptador desconectado durante as práticas.
Antes de desconectar, obtenha de fontes oficiais Visual Studio Build Tools,
Windows SDK, WinDbg, Windows Performance Toolkit e Sysinternals. Preserve URL,
versão, assinatura e hash dos instaladores autorizados.

Crie quatro snapshots:

- `09-base`: sistema atualizado, ferramentas verificadas e sem dados de prática;
- `09-dev`: compilador, SDK e símbolos das próprias fixtures;
- `09-trace`: espaço livre dimensionado para ETL e dumps pequenos;
- `09-final`: clone no qual outra pessoa reproduzirá o diagnóstico.

Não use perfil pessoal, navegador autenticado ou documentos reais. As únicas
aplicações-alvo são as compiladas em `exemplos/` ou processos nativos usados
somente para consultas não invasivas.

## Classes de artefato

| Artefato | Pode conter | Controle mínimo |
|---|---|---|
| inventário | build, versões, configuração | seleção de campos e sanitização |
| trace ETL/PML | caminhos, comandos, atividade de processos | filtro, janela curta, acesso local |
| dump mínimo | stack, registradores, partes de memória | processo próprio, retenção curta |
| dump completo | grande parte do espaço do processo | evitado neste curso |
| PDB/símbolos | nomes, tipos e caminhos de build | apenas projeto próprio |
| logs WER | exceção, módulo e contexto | pasta isolada e cleanup validado |

Dump não é “só diagnóstico”: memória pode carregar conteúdo e segredos. Não
publique, envie a serviços externos ou mantenha indefinidamente. O laboratório
usa mini dump de fixture sem credenciais.

## Método de experimento

```text
sintoma → modelo do subsistema → hipótese → sinal previsto → captura mínima
        → análise → teste discriminador → mudança única → nova captura
        → comparação → retenção/cleanup
```

Comece pelo modelo. Se a hipótese é carga insegura de DLL, a evidência deve
mostrar caminho e resultado do loader da fixture; um trace geral de CPU não
responde. Se o problema é latência, uma captura sem janela de reprodução mistura
atividade irrelevante.

Defina antecipadamente:

1. processo e arquivo autorizados;
2. provider/categoria/contador necessário;
3. início e fim da captura;
4. volume máximo e espaço livre mínimo;
5. campos que serão sanitizados;
6. critério de sucesso, interrupção e exclusão.

## Baseline técnica

```powershell
Get-ComputerInfo |
  Select-Object WindowsProductName, WindowsVersion, OsBuildNumber,
    OsArchitecture, HyperVisorPresent

Get-ProcessMitigation -System

Get-CimInstance Win32_DeviceGuard |
  Select-Object VirtualizationBasedSecurityStatus,
    SecurityServicesConfigured, SecurityServicesRunning
```

Registre também versões de WinDbg, WPR/WPA, Sysinternals, compilador e SDK. A
ausência de cmdlet, acesso negado, `$null`, recurso não suportado e valor `False`
são estados diferentes. Não force uma ferramenta a executar elevada apenas para
preencher uma coluna sem relação com a hipótese.

## Símbolos e reprodutibilidade

Para código próprio, preserve fonte, comando de build, arquitetura, executável,
DLL e PDB da mesma compilação. Símbolo de outra build produz nomes ou linhas
incorretos. O identificador verificável é o conjunto exato, não o nome do arquivo.

Símbolos públicos da Microsoft podem ser obtidos em uma fase controlada e
armazenados em cache conforme termos aplicáveis. As práticas devem continuar
funcionando com símbolos apenas das fixtures; não dependem de conectividade.

## Critérios de parada

Interrompa se o processo-alvo não for seu, o filtro abranger o sistema por tempo
indefinido, o disco cair abaixo da reserva, um dump puder conter dados reais, a
ferramenta pedir redução de proteção ou o resultado exigir técnica ofensiva.
Acesso negado é evidência de fronteira, não convite para contorno.

## Exercícios

1. Desenhe os quatro perfis e o caminho de promoção entre snapshots.
2. Classifique inventário, PML, ETL, mini dump, full dump e PDB por sensibilidade.
3. Escreva um plano de captura de 30 segundos com tamanho e cleanup.
4. Produza baseline das ferramentas e explique três estados “desconhecidos”.
5. Peça a outra pessoa para decidir, apenas pelo plano, quando deve parar.

## Checklist de domínio

- [ ] Todas as ferramentas têm origem, versão, assinatura e hash registrados.
- [ ] A VM não contém conta ou documento pessoal.
- [ ] Dumps e traces têm alvo, duração, tamanho e retenção definidos.
- [ ] A hipótese prevê um sinal que pode ser refutado.
- [ ] Somente fixtures e processos próprios recebem captura detalhada.
- [ ] Símbolos, binários e fonte pertencem à mesma build.
- [ ] O cleanup é verificado por inventário, não apenas declarado.
