# 18 — VBS, HVCI, Credential Guard e cadeia de confiança

Virtualization-Based Security (VBS) usa recursos do hipervisor para criar fronteiras adicionais dentro do próprio sistema. Hypervisor-Protected Code Integrity (HVCI), exibido ao usuário como Memory Integrity em muitos contextos, fortalece a política de código no kernel. Credential Guard protege categorias específicas de credenciais. São camadas relevantes, mas não equivalem a isolamento absoluto.

## Objetivos

Ao terminar, você deverá conseguir:

- explicar VBS, VTL e secure kernel em nível arquitetural;
- relacionar Secure Boot, TPM, BitLocker, VBS e HVCI;
- distinguir configuração, execução e disponibilidade;
- inventariar estado sem converter ausência de dados em conclusão;
- planejar compatibilidade de drivers antes de habilitar HVCI;
- descrever limites de VM e Sandbox no laboratório.

## Isolamento baseado em virtualização

O hipervisor pode separar regiões chamadas **Virtual Trust Levels** (VTLs). O Windows normal opera no nível comum, enquanto componentes de segurança selecionados operam em um ambiente mais protegido, apoiado pelo secure kernel. O objetivo é tornar mais difícil que comprometimento no kernel comum alcance certos segredos ou decisões de integridade.

VBS depende de uma combinação de hardware, firmware, configuração de boot, virtualização e política do sistema. “Compatível” não significa “em execução”. Do mesmo modo, um valor configurado pode aguardar reinicialização ou falhar por dependência. Relatórios devem separar:

- recurso disponível no hardware e firmware;
- política configurada;
- serviço efetivamente em execução;
- erro ou estado desconhecido.

```powershell
$deviceGuard = Get-CimInstance -ClassName Win32_DeviceGuard `
    -Namespace root\Microsoft\Windows\DeviceGuard

$deviceGuard | Select-Object VirtualizationBasedSecurityStatus,
    SecurityServicesConfigured, SecurityServicesRunning,
    AvailableSecurityProperties, RequiredSecurityProperties

Get-Tpm
Confirm-SecureBootUEFI
```

Arrays numéricos como `SecurityServicesConfigured` precisam ser interpretados conforme documentação da versão. Não assuma que `1` significa simplesmente “seguro”. Se a classe ou cmdlet não existir, capture o erro, versão, edição e tipo de firmware; o estado é `unknown`, não `disabled`.

## HVCI e integridade de código

HVCI move decisões sensíveis de integridade para a fronteira protegida e restringe propriedades de memória usadas por código privilegiado. Drivers precisam obedecer requisitos de assinatura e compatibilidade. Um driver antigo ou mal projetado pode impedir ativação ou causar falhas funcionais.

Antes de um piloto, inventarie drivers, confirme suporte do fabricante, atualize firmware e software por fontes oficiais e tenha caminho de recuperação. Teste periféricos e cenários de suspensão/retomada. Não desative permanentemente Memory Integrity para manter um driver abandonado; substitua ou isole a dependência.

## Credential Guard e limites

Credential Guard isola determinados segredos e operações de autenticação com VBS. Ele reduz exposição de certas credenciais, mas não protege cada token, cookie, chave de aplicativo ou segredo já entregue a um processo. Também não corrige senhas fracas, phishing, sessão desbloqueada ou permissões excessivas.

Em edições e versões recentes, padrões e requisitos podem mudar. Verifique documentação oficial aplicável e política organizacional. O laboratório não tenta extrair credenciais nem testar contornos; apenas observa configuração e explica cobertura.

## Cadeia de confiança

As camadas se complementam:

1. **UEFI Secure Boot** verifica componentes autorizados na sequência inicial de boot;
2. **TPM** oferece armazenamento e medições protegidas usadas por políticas;
3. **BitLocker** protege dados do volume em repouso, inclusive com vínculo a medições;
4. **hipervisor/VBS** cria uma fronteira de execução adicional;
5. **HVCI** fortalece integridade de código privilegiado;
6. **Credential Guard** usa a fronteira para proteger segredos específicos.

BitLocker não valida cada driver; Secure Boot não cifra documentos; VBS não é backup. O desenho só faz sentido quando cada controle é associado à ameaça que cobre e ao que permanece fora do escopo.

## Virtualização aninhada e laboratório

Uma VM pode não expor TPM virtual, Secure Boot ou virtualização aninhada. Documente essas limitações. Windows Sandbox e Hyper-V ajudam a separar fixtures confiáveis e descartáveis, mas não autorizam executar malware. Integração de área de transferência, pastas compartilhadas e rede também atravessa a fronteira; reduza essas integrações conforme o exercício.

O curso usa apenas programas próprios e arquivos artificiais. A VM permanece sem rede quando a prática não exige atualização, e snapshots são feitos antes de alterações de política.

## Exercícios

1. Colete os estados disponíveis e gere tabela com `available`, `configured`, `running` e `unknown`.
2. Desenhe a cadeia Secure Boot → TPM → VBS → HVCI e escreva um limite de cada camada.
3. Crie plano de compatibilidade para habilitar HVCI em um piloto com três periféricos fictícios.
4. Analise quais integrações de uma VM poderiam vazar artefatos para o host.

## Checklist

- [ ] Diferencio capacidade, configuração e execução.
- [ ] Sei por que arrays Device Guard exigem documentação da versão.
- [ ] Não trato VBS ou Credential Guard como proteção universal.
- [ ] Compatibilidade de drivers precede enforcement.
- [ ] O laboratório usa fixtures benignas e fronteiras minimizadas.

