# 17 — Microsoft Defender e mitigações do Windows

Segurança do endpoint é composta por camadas. Microsoft Defender Antivirus, Attack Surface Reduction (ASR), Controlled Folder Access, Exploit Protection e controle de aplicações têm objetivos diferentes. Administrá-los exige inventário, compatibilidade, modo de auditoria quando disponível e rollback planejado. O laboratório observa estados e desenha um piloto; ele não desabilita proteções.

## Objetivos

Ao concluir, você deverá conseguir:

- diferenciar antimalware, redução de superfície e mitigação de exploração;
- explicar DEP, ASLR e CFG em nível conceitual;
- coletar uma linha de base somente leitura;
- desenhar implantação audit → pilot → enforce;
- tratar falsos positivos sem exclusões amplas;
- verificar resultado e registrar exceções com prazo e responsável.

## Camadas e responsabilidades

**Defender Antivirus** inspeciona conteúdo e comportamento conforme recursos e políticas disponíveis. Atualização de inteligência, proteção em tempo real e nuvem são estados diferentes; um único indicador “ativo” não descreve toda a postura.

**Attack Surface Reduction** restringe comportamentos que costumam aumentar risco, como certas cadeias entre documentos e processos. Regras variam por edição e gerenciamento. **Controlled Folder Access** controla escrita de aplicativos em pastas protegidas. **Application Control** decide quais códigos podem executar segundo uma política de confiança. Essas camadas não são intercambiáveis.

**Exploit Protection** aplica mitigações a processos e ao sistema. DEP reduz execução de páginas de dados; ASLR introduz aleatoriedade na localização de imagens e regiões; CFG restringe destinos válidos de chamadas indiretas quando o binário fornece suporte. Nenhuma mitigação isolada elimina vulnerabilidades. Algumas exigem participação da compilação, e políticas agressivas podem quebrar software incompatível.

## Linha de base somente leitura

Em uma VM administrada por você, comandos como estes ajudam a documentar estado:

```powershell
$status = Get-MpComputerStatus
$preferences = Get-MpPreference
$systemMitigations = Get-ProcessMitigation -System
$notepadMitigations = Get-ProcessMitigation -Name notepad.exe

$status | Select-Object AntivirusEnabled, RealTimeProtectionEnabled,
    AntivirusSignatureVersion, AntivirusSignatureLastUpdated
$systemMitigations
$notepadMitigations
```

Disponibilidade e campos variam com versão, edição, provedor instalado e política organizacional. Falha de um comando não deve virar valor `false`; registre `unknown` com o erro e o ambiente. Não publique o inventário completo sem revisar caminhos e detalhes de política.

## Implantação segura

Uma implantação defensiva madura segue estágios:

1. **inventário:** aplicações, versões, proprietários, criticidade e dependências;
2. **linha de base:** política atual, eventos e carga normal;
3. **auditoria:** observar impacto quando o recurso oferece esse modo;
4. **análise:** explicar eventos e separar incompatibilidade de comportamento esperado;
5. **piloto:** aplicar em pequena população representativa e recuperável;
6. **enforcement:** ampliar em ondas com critérios de parada;
7. **verificação:** confirmar telemetria, proteção e funcionalidade;
8. **manutenção:** rever exceções, atualizar software e remover dívida.

Antes de mudar qualquer política, exporte o estado e documente como restaurá-lo. Uma VM snapshot facilita recuperação, mas não substitui saber qual configuração mudou.

## Compatibilidade e falsos positivos

Quando uma aplicação falha, identifique regra, evento, arquivo, versão e cenário. Reproduza em piloto e procure atualização ou correção do software. Se uma exceção for inevitável, limite por aplicativo, regra e escopo; defina justificativa, proprietário, expiração e compensação.

Uma exclusão ampla de diretório cria uma área cega permanente. Desligar proteção para “ver se funciona” mistura diagnóstico com perda de controle e não faz parte deste curso. Use modo de auditoria, eventos e documentação oficial do recurso.

Eventos devem ser interpretados junto à política efetiva. Uma política configurada pode não estar aplicada por conflito, edição ou reinicialização pendente. Colete também versão do Windows e fonte de gerenciamento. Em máquina corporativa, somente administradores autorizados alteram políticas.

## Defesa durante desenvolvimento

Aplicações do curso devem funcionar com proteções normais. Compile com mitigações oferecidas pela toolchain, assine artefatos quando o processo justificar, valide caminhos de DLL, limite permissões e não solicite elevação desnecessária. O melhor tratamento de uma incompatibilidade é corrigir código ou dependência, não ensinar o usuário a abrir exceções.

## Exercícios

1. Gere uma linha de base redigida da VM e marque campos indisponíveis como `unknown`.
2. Escolha uma regra ASR apenas para estudo documental e escreva plano de auditoria, piloto, métricas e rollback.
3. Explique como DEP, ASLR e CFG complementam, mas não corrigem, validação de entrada.
4. Analise um falso positivo hipotético e proponha a exceção mais estreita, com expiração.

## Checklist

- [ ] Distingo as responsabilidades das camadas defensivas.
- [ ] Não desabilito Defender nem crio exclusão ampla no laboratório.
- [ ] Mudanças começam em auditoria/piloto quando possível.
- [ ] Incompatibilidades geram evidência e correção direcionada.
- [ ] Exceções possuem escopo, dono, prazo e controle compensatório.

