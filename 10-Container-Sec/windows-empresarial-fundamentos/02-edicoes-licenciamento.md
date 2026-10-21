# 02 — Edições, licenciamento e suporte

Windows Server 2025 oferece opções e canais cujo direito de uso depende do
contrato atual. Standard e Datacenter diferem em virtualização e recursos;
Azure Edition tem cenários específicos. Evaluation é adequada ao laboratório,
não a produção permanente.

## Registre por servidor

- edition, installation option e build;
- canal e datas de suporte;
- modelo de licença e direito de virtualização;
- product owner e workload owner;
- dependências de hardware/firmware;
- plano de upgrade/migração antes do fim de suporte.

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsEditionId,
  OsBuildNumber, OsArchitecture
dism.exe /Online /Get-CurrentEdition
```

Não use ativadores, chaves públicas fora da finalidade documentada ou conversão
de edição sem confirmar caminho suportado e direito contratual.

## Exercício

Compare duas edições na documentação vigente e produza uma decisão rastreável.
Separe capacidade técnica de direito de licenciamento.

