# 09 — Aplicativos, pacotes, origem e ciclo de vida

Instalar software modifica mais do que uma pasta. Um pacote pode registrar
componentes, serviços, tarefas, associações e dependências. Administração segura
preserva procedência, registra mudanças e testa remoção ou rollback.

## Objetivos

- distinguir EXE, MSI, MSIX, Store e catálogo `winget`;
- avaliar origem, assinatura, hash, versão e licença;
- reconhecer escopo por usuário e por máquina;
- construir um plano de instalação e desinstalação verificável;
- evitar atalhos perigosos como DLLs avulsas e “packs” desconhecidos.

## Formato não é procedência

MSI é um pacote consumido pelo Windows Installer e possui modelo próprio de
produto, componentes, instalação e reparo. MSIX adiciona identidade de pacote e
um modelo mais controlado. EXE é apenas um formato executável: o instalador pode
implementar qualquer lógica. Microsoft Store é uma experiência de distribuição;
`winget` é um cliente que consulta fontes e manifests. Nenhum formato, sozinho,
garante qualidade ou adequação.

Antes de instalar, responda:

- quem é o editor e qual é a página oficial?
- qual produto, versão, arquitetura e canal estão sendo escolhidos?
- o artefato possui assinatura válida e hash publicado?
- qual licença permite este uso?
- instala para o usuário ou para toda a máquina?
- adiciona serviços, tarefas, drivers, inicialização ou associações?
- como exportar dados e voltar à versão anterior?

## Assinatura e hash

```powershell
$installer = 'C:\RTE-Lab\pacotes\fixture.exe'
Get-FileHash -LiteralPath $installer -Algorithm SHA256
Get-AuthenticodeSignature -FilePath $installer |
  Select-Object Status, StatusMessage, Path, TimeStamperCertificate,
    SignerCertificate
```

Não execute a fixture. Um `NotSigned` demonstra apenas ausência de assinatura
Authenticode reconhecida. `Valid` indica que a assinatura e cadeia foram
validadas no contexto atual; ainda não afirma que o programa é livre de falhas,
necessário ou licenciado. Hash só é útil para procedência quando comparado a um
valor obtido por canal independente e confiável.

Certificados expiram, podem ser revogados e usam timestamp. Documente o status
observado e a hora, sem reduzir tudo a um booleano.

## Inventário de software

```powershell
winget list
Get-AppxPackage |
  Select-Object Name, Publisher, Architecture, Version, PackageFullName
```

A cobertura varia: aplicativos portáteis, instaladores antigos ou produtos por
outros mecanismos podem não aparecer da mesma maneira. Evite usar
`Win32_Product` como inventário geral: a consulta pode ser lenta e acionar
consistência/reparo de pacotes MSI. Compare Settings, `winget list` e dados do
próprio aplicativo, registrando limitações.

Não conecte a VM apenas para executar uma consulta de catálogo. Se a atividade
exigir obtenção ou atualização, faça isso numa janela controlada, por fonte
oficial, e retorne ao estado local do curso.

## Plano de mudança

Crie snapshot, registre versão atual, dados do usuário, processos relacionados,
espaço livre e método de desinstalação. Leia todas as opções do instalador. Uma
instalação “para todos” costuma exigir elevação e altera estado de máquina; uma
instalação por usuário fica no perfil, mas não é automaticamente mais segura.

Não aceite componentes adicionais por inércia. Integração de shell, associação
de arquivos e inicialização têm impacto visível. Reinicie somente quando
solicitado ou quando o plano exigir, e valide depois: aplicação abre, arquivo de
fixture é preservado, versão é a esperada, não há erro no intervalo e o sistema
continua protegido.

## Atualização, reparo e remoção

Atualização pode migrar formato de dados; rollback do binário não garante que a
versão antiga leia o estado novo. Exporte documentos e configurações antes.
“Repair” de MSI tenta restaurar componentes registrados, não corrige qualquer
problema do Windows.

Use o desinstalador registrado. Remover o programa pode preservar preferências e
documentos no perfil; isso pode ser intencional. Não apague diretórios residuais
até identificar proprietário, conteúdo e necessidade de recuperação. Serviços
ou tarefas remanescentes devem ser avaliados pela documentação do fornecedor,
não excluídos no impulso.

Baixar uma DLL de um site genérico para resolver mensagem de dependência perde
versão, arquitetura, assinatura e contrato de servicing. Reinstale o runtime ou
aplicativo pelo fornecedor e diagnostique a causa.

## Prática controlada

Selecione um aplicativo pequeno já presente na VM ou um pacote oficial
previamente arquivado. Documente editor, versão, assinatura, hash, arquitetura,
escopo, dados e rollback. Faça baseline de processos e inicialização. Instale ou
repare após snapshot, valide a função com arquivo sintético, desinstale e compare
o estado. Não remova componentes do Windows.

## Exercícios

1. Compare EXE, MSI, MSIX, Store e `winget` sem declarar um vencedor universal.
2. Explique precisamente o que assinatura válida e hash igual demonstram.
3. Faça um checklist de instalação que inclua dados e rollback.
4. Compare três fontes de inventário e documente objetos ausentes.
5. Explique por que “apagar a pasta” raramente é desinstalação correta.

## Checklist de domínio

- [ ] Formato de pacote e procedência são conceitos separados.
- [ ] Verifico editor, versão, arquitetura, licença, assinatura e origem.
- [ ] Sei se a mudança é por usuário ou por máquina.
- [ ] Registro dados, integrações e método de rollback antes de instalar.
- [ ] Não uso `Win32_Product` como inventário rotineiro.
- [ ] Não baixo DLL ou driver avulso para corrigir dependência.
- [ ] Valido instalação e remoção por função e evidência, não apenas por ícone.
