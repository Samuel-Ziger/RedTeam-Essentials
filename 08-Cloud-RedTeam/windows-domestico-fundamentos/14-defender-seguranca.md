# 14 — Segurança do Windows e Microsoft Defender

Segurança local é um conjunto de camadas, não um botão verde. O aplicativo
Segurança do Windows apresenta estados; Microsoft Defender Antivirus é um dos
componentes. Firmware, atualização, reputação, isolamento, conta comum e backup
continuam necessários.

## Objetivos

- interpretar o estado do Defender sem presumir que está ativo;
- diferenciar inteligência, engine, proteção em tempo real e scan;
- explicar SmartScreen, PUA, Controlled Folder Access e Exploit Protection;
- responder a um alerta preservando contexto;
- construir baseline sem malware, exclusões ou desativação.

## Estado observado

```powershell
Get-MpComputerStatus |
  Select-Object AntivirusEnabled, AMServiceEnabled,
    RealTimeProtectionEnabled, BehaviorMonitorEnabled,
    AntivirusSignatureVersion, AntivirusSignatureLastUpdated,
    QuickScanAge, FullScanAge

Get-MpPreference |
  Select-Object PUAProtection, EnableControlledFolderAccess,
    DisableRealtimeMonitoring
```

Propriedades e disponibilidade variam com versão, edição e produto de segurança
registrado. Se outro antivírus gerencia a proteção, Defender pode operar em um
modo diferente. `$false`, `$null`, acesso negado e cmdlet ausente não significam
a mesma coisa. Registre contexto e não tente reconfigurar um produto de terceiros
para fazer a saída “bater”.

Inteligência contém conhecimento de detecção e tem versão/data; engine executa
análises; proteção em tempo real observa atividades conforme configuração; scan
é uma operação pontual. Uma varredura recente não substitui proteção contínua,
e proteção ativa não corrige sistema fora de suporte.

## Camadas locais

- SmartScreen e controles de reputação ajudam na decisão sobre origem e execução;
- proteção contra PUA trata software potencialmente indesejado;
- Controlled Folder Access restringe gravação por aplicativos em pastas protegidas;
- Exploit Protection aplica mitigações de processo/sistema;
- isolamento do núcleo e integridade de memória dependem de hardware e drivers;
- Secure Boot e TPM participam da confiança antes e durante o boot;
- UAC e conta comum limitam mudanças administrativas acidentais.

Nenhuma camada torna seguro executar arquivo desconhecido. Combinação, estado
atualizado e comportamento do usuário reduzem risco.

## Exclusões não são solução rápida

Uma exclusão remove visibilidade ou proteção naquele alvo. Não adicione pasta,
processo ou extensão porque um tutorial mandou. Primeiro valide origem,
assinatura, versão e possível falso positivo por canal do fornecedor. Se houver
necessidade legítima, a exclusão precisa ser mínima, temporária, documentada e
removida; o curso não cria exclusões.

Da mesma forma, não desative proteção para instalar programa. Isso transforma
uma dúvida de compatibilidade em exposição maior e destrói uma camada de
diagnóstico.

## Varredura e resultado

Quick scan verifica áreas mais propensas segundo o produto; full scan tem escopo
maior e custo diferente; custom scan restringe alvo. Escolha por cenário, não
como ritual. No laboratório, uma quick scan pode ser iniciada pela interface ou:

```powershell
Start-MpScan -ScanType QuickScan
```

Registre hora inicial/final, versão da inteligência, resultado e efeito de
desempenho. Não use malware. O arquivo EICAR é uma string de teste reconhecida,
mas este módulo não precisa dela: estado e arquivo nativo assinado são suficientes
para aprender o fluxo sem gerar alertas artificiais.

## Resposta básica a alerta

1. pare a interação e não restaure o item;
2. registre hora, categoria, caminho sanitizado, ação e origem conhecida;
3. preserve o histórico e calcule hash apenas se a política permitir;
4. atualize o produto pelo mecanismo suportado e execute scan adequado;
5. avalie contas, documentos e mudanças no período;
6. restaure dados de fonte conhecida quando necessário;
7. procure suporte especializado se houver impacto ou persistência.

“Quarentena” isola conforme o produto; “removido”, “bloqueado” e “permitido” têm
efeitos distintos. Formatar imediatamente pode destruir evidência e ainda não
responder como a situação ocorreu. Por outro lado, investigação forense completa
não é requisito para toda detecção de PUA doméstica. Classifique impacto.

## Integridade de artefato conhecido

Escolha um executável nativo documentado, obtenha caminho do próprio sistema e
consulte hash e assinatura. Não compare com hash aleatório da internet, pois
builds legítimas diferem. Registre assinatura, versão do arquivo e build do
Windows. O exercício ensina interpretação, não cria uma allowlist universal.

## Exercícios

1. Produza baseline e diferencie ausente, desativado e não consultável.
2. Desenhe as camadas de firmware, sistema, reputação, antivírus, identidade e backup.
3. Explique por que assinatura válida não substitui Defender e vice-versa.
4. Execute quick scan em snapshot e registre métricas e resultado.
5. Escreva um runbook para alerta que não desative proteção nem restaure o item.

## Checklist de domínio

- [ ] Observo engine, inteligência, tempo real e scans separadamente.
- [ ] Não converto erro ou produto terceiro em “Defender desligado”.
- [ ] Entendo a função e o limite de cada camada local.
- [ ] Não crio exclusões nem desativo proteção por conveniência.
- [ ] Laboratório não executa malware nem arquivos desconhecidos.
- [ ] Um alerta preserva contexto antes de ações destrutivas.
- [ ] Baseline contém versão/build e nenhum identificador pessoal.
