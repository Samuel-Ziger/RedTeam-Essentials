# 01 — Família, edições, arquitetura e ciclo de suporte

“Windows 11” não identifica completamente um sistema. Compatibilidade e suporte
dependem de produto, edição, versão, build, arquitetura e canal. Misturar esses
conceitos leva a recomendações incorretas e inventários que envelhecem mal.

## Objetivos

- interpretar produto, edição, versão, build e arquitetura separadamente;
- relacionar edição a recursos e licença sem confiar em listas antigas;
- verificar o ciclo de suporte em fonte oficial atual;
- produzir um inventário mínimo, estruturado e sem identificadores;
- distinguir atualização de qualidade, atualização de recursos e upgrade.

## Um identificador em camadas

Windows é uma família construída sobre a arquitetura Windows NT. O nome
comercial comunica geração; a edição, como Home ou Pro, determina direitos e
recursos; a arquitetura indica o conjunto de instruções, normalmente x64 ou
Arm64; a versão representa uma entrega funcional; e a build identifica a linha
dos binários. A revisão da build muda com atualizações cumulativas.

Exemplo abstrato: dois computadores podem exibir “Windows 11”, mas um executar
Home x64 numa versão fora de suporte e o outro Pro Arm64 numa versão atual. Um
aplicativo, driver ou recurso pode funcionar apenas em um deles. Nunca reduza a
ficha técnica ao nome visto na área de trabalho.

```powershell
Get-ComputerInfo |
  Select-Object WindowsProductName, WindowsVersion, OsBuildNumber,
    OsArchitecture

Get-CimInstance -ClassName Win32_OperatingSystem |
  Select-Object Caption, Version, BuildNumber, InstallDate

Get-CimInstance -ClassName SoftwareLicensingProduct |
  Where-Object { $_.PartialProductKey -and $_.Name -like 'Windows*' } |
  Select-Object Name, LicenseStatus
```

Não publique `PartialProductKey`, IDs ou outros campos de licenciamento. A
consulta filtra o objeto relevante, mas a evidência do curso deve manter apenas
nome e estado interpretado.

## Edição não é versão

Home e Pro atendem perfis diferentes; Enterprise e Education usam contratos e
cenários próprios. Recursos como BitLocker gerenciável, virtualização e ingresso
corporativo variam por edição e podem mudar. Em vez de memorizar uma tabela,
transforme a necessidade em requisito e confira a documentação atual: “preciso
de criptografia de volume com esta forma de gerenciamento” é melhor que “preciso
de Pro porque disseram”.

Ativação verifica direitos de uso; não converte hardware incompatível em
compatível, não prolonga suporte e não garante que o sistema esteja atualizado.
Licença OEM, varejo, avaliação e contratos possuem condições distintas. Este
curso não fornece chaves nem procedimentos para contornar ativação.

## Servicing e ciclo de vida

Uma atualização de qualidade normalmente é cumulativa: o pacote recente inclui
correções anteriores aplicáveis. Uma atualização de recursos muda a versão e
pode introduzir capacidades, requisitos e uma nova janela de suporte. Upgrade
também pode significar troca de produto ou edição; contexto é obrigatório.

A Microsoft publica uma página de informações de lançamento com versões,
builds, problemas conhecidos e fim de servicing. A cadência e a duração variam
por edição e podem mudar; por isso o curso não grava uma “versão mais recente”.
Na data do seu estudo, consulte a página oficial, anote a data da consulta e
registre o link ao lado do resultado.

Quatro datas não devem ser confundidas:

- data de instalação local;
- data de publicação da versão;
- data da última atualização instalada;
- fim do suporte daquela versão/edição.

Um equipamento pode ter sido instalado recentemente com uma imagem antiga. A
data local, sozinha, não demonstra suporte.

## Ficha de decisão

Crie uma ficha com: uso pretendido, recursos indispensáveis, edição, versão,
build completa, arquitetura, estado de ativação sanitizado, data de fim de
suporte consultada, URL e data da consulta. Adicione uma coluna “evidência” para
distinguir valor coletado localmente de informação consultada.

Para comparar inventários, exporte objetos em vez de texto formatado:

```powershell
$os = Get-CimInstance Win32_OperatingSystem
[pscustomobject]@{
    Schema = 'rte.windows-version/v1'
    CollectedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    Product = $os.Caption
    Version = $os.Version
    Build = $os.BuildNumber
    Architecture = $os.OSArchitecture
} | ConvertTo-Json
```

`Format-Table` serve para a tela; `ConvertTo-Json` preserva nomes de propriedades
para automação. Ainda assim, um schema precisa de versão para evoluir sem
ambiguidade.

## Falhas de raciocínio comuns

- concluir que o sistema está suportado apenas porque “há updates”;
- recomendar edição por hábito, sem mapear requisitos;
- confundir x64 do sistema com a arquitetura de cada processo;
- tratar build sem revisão como identificação completa de um incidente;
- usar página comunitária antiga como autoridade de ciclo de vida;
- expor chave ou identificador ao compartilhar diagnóstico.

## Exercícios

1. Produza a ficha da VM e cite a fonte oficial do ciclo de suporte.
2. Explique três diferenças possíveis entre duas instalações chamadas Windows 11.
3. Compare a saída de `winver`, `Get-ComputerInfo` e CIM. Quais campos servem
   para humano e quais são melhores para automação?
4. Modele a escolha entre Home e Pro para uma pessoa fictícia usando requisitos,
   sem afirmar recursos que você não verificou.
5. Explique por que uma atualização cumulativa muda a revisão da build, mas não
   necessariamente a versão exibida pelo produto.

## Checklist de domínio

- [ ] Identifico produto, edição, versão, build/revisão e arquitetura.
- [ ] Consulto lifecycle e release health com data e fonte.
- [ ] Não confundo ativação, atualização, compatibilidade e suporte.
- [ ] Escolho edição a partir de requisitos verificados.
- [ ] Meu inventário é estruturado, versionado e sanitizado.
- [ ] Consigo explicar por que “Windows 11 atualizado” é uma afirmação incompleta.
