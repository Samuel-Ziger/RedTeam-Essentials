# 04 — DISM e servicing offline

DISM monta, consulta e modifica imagens Windows. Offline servicing reduz estado
em execução, mas ordem, applicability e dependências ainda importam.

```powershell
dism.exe /Get-WimInfo /WimFile:C:\Lab\install.wim
dism.exe /Mount-Image /ImageFile:C:\Lab\install.wim /Index:1 /MountDir:C:\Lab\mount /ReadOnly
dism.exe /Image:C:\Lab\mount /Get-Packages
dism.exe /Unmount-Image /MountDir:C:\Lab\mount /Discard
```

Comece read-only. Para mudança, trabalhe em cópia e use `/Commit` somente
depois dos testes. Se houver falha, `/Cleanup-Mountpoints` deve ser aplicado com
entendimento; não apague diretórios de mount manualmente.

## Ordem

Servicing stack/cumulative updates, language/FoD e drivers possuem regras por
release. Consulte a documentação do pacote e verifique `Get-Packages`, logs DISM
e pending actions.

## Drivers

Injete apenas INF assinado e aplicável ao hardware aprovado. Não use `/Recurse`
em depósito descontrolado: aumenta imagem e risco.

## Laboratório

Monte uma WIM de avaliação read-only, inventarie packages/features/drivers e
desmonte com `/Discard`. Registre hashes antes/depois iguais.

