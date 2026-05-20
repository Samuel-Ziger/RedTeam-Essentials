# Evasion Fundamentals (Teoria)

> Conteudo educacional. Foco em **entender** mecanismos de defesa modernos e suas falhas conceituais. **Nao apresentamos payloads prontos**.

---

## 1. Camadas de defesa em endpoint Windows

```
   User-mode .NET  ---> AMSI -> Defender
       |
   Win32 API
       |
   ntdll!Nt*  --- syscalls --->  Kernel  -> EDR (callback PsSetCreateProcessNotifyRoutineEx, kernel hooks)
                                     |
                                     -> ETW (kernel + tenant events)
```

Cada camada e um ponto onde a defesa pode observar. Evasion estuda **onde introduzir codigo sem disparar telemetria**.

---

## 2. AMSI (Antimalware Scan Interface)

API que permite ao Defender/AV inspecionar **conteudo dinamico** antes da execucao (`PowerShell -Command "..."`, .NET assembly via `Assembly.Load`, Office macros).

### Como funciona

Antes de avaliar o script, PowerShell chama `AmsiScanBuffer(buffer, length)`. Se o engine retorna `AMSI_RESULT_DETECTED`, execucao e abortada.

### Bypasses publicos (citados em pesquisa)

- **Memory patching:** modificar `AmsiScanBuffer` em `amsi.dll` para sempre retornar limpo.
- **Provider unhook:** desregistrar provider AV via COM.
- **Hardware breakpoints:** detour via Vectored Exception Handler.

### Deteccao

- Event Log "Microsoft-Windows-PowerShell/Operational" EID 4100/4104.
- Defender AntimalwareEvent 1116 com `Amsi:` na descricao.
- AMSI Logger (PowerShell module open source) salva todo buffer scanned.

---

## 3. ETW (Event Tracing for Windows)

Sistema de tracing kernel/user-mode. Fontes principais para defesa:

- `Microsoft-Windows-Threat-Intelligence` (TI) - mostra alocacoes RW/RX, image loads sem disk.
- `Microsoft-Windows-DotNETRuntime` - .NET load, assembly resolve.
- `Microsoft-Windows-Kernel-Process` - process creation, handles.

### Bypasses

- **ETW patching:** zero out `EtwEventWrite` no proprio processo.
- **Provider disable:** chamar `EnableTraceEx2(... DISABLE)`.

Cada bypass deixa rastro - patching da DLL e detectavel por integrity check.

---

## 4. EDR (Endpoint Detection & Response)

EDRs modernos (CrowdStrike, SentinelOne, Defender ATP, etc.) usam:

1. **User-mode hooks** em ntdll (DLL injection ou IAT hook).
2. **Kernel callbacks** (`PsSet*NotifyRoutine`, `CmRegisterCallback`).
3. **ETW Threat-Intelligence subscriptions**.
4. **Behavioral analytics** na nuvem (telemetria correlacionada).

### Unhooking

Reescrever bytes hookados em `ntdll.dll` com copia limpa de disco. Funciona apenas para hooks user-mode.

### Direct/Indirect Syscalls

Em vez de chamar `NtAllocateVirtualMemory` (hookable), copiar o `syscall stub` e executa-lo diretamente. Tecnica popular: **Hell's Gate / Halo's Gate / Tartarus' Gate**.

EDR contra-medidas:
- Kernel callbacks ainda veem a chamada.
- Anti-instrumentation no proprio EDR (TamperProtect).
- Machine learning sobre sequence de syscalls.

---

## 5. Sandbox / VM Detection

Heuristicas:

- CPU count baixo.
- RAM < 4 GB.
- Username `John Doe`, `sandbox`, `cuckoo`.
- Registry: VMware/VBox keys.
- Macroscopic timing (sleep skipping detection).
- Mouse activity ausente.
- Recent files vazios.

Modernos analistas defendem com **bare-metal sandboxes** + **decoy artifacts** para reverter cada heuristica.

---

## 6. Process Injection (T1055)

Variantes:

- **DLL injection** (LoadLibrary in remote process).
- **Process Hollowing.**
- **Reflective DLL Loading.**
- **APC injection** (`QueueUserAPC` + alertable thread).
- **Early Bird APC.**
- **Module Stomping.**
- **Process Doppelganging / Ghosting.**

Trade-off: mais simples = mais detectado. EDR observa `OpenProcess + WriteProcessMemory + CreateRemoteThread`.

---

## 7. Living-Off-The-Land (LOLBins / GTFOBins)

Em vez de droppar binario, usar utilitarios assinados:

- Windows: `mshta`, `regsvr32`, `rundll32`, `wmic`, `certutil`, `bitsadmin`.
- Linux: `awk`, `find`, `python3` (GTFOBins).
- macOS: `osascript`, `sw_vers`, `mdfind`.

Defesa: AppLocker/WDAC com signers; tagging via ETW; restricoes em script hosts.

---

## 8. Maturity Levels (Atacante)

| Nivel | Operacoes |
|-------|-----------|
| 0 - Script kiddie | Powershell raw, Metasploit out-of-the-box. |
| 1 - Junior pentest | Obfuscacao basica (Invoke-Obfuscation), AV evasion publico. |
| 2 - Mid red team | C2 com profile custom, AMSI/ETW bypass dinamico. |
| 3 - Senior | Loader proprio em C++, syscalls indiretos, anti-EDR especifico. |
| 4 - APT-tier | Drivers assinados, bypass de Secure Boot, supply-chain. |

---

## 9. Defesa pratica

Apos entender as tecnicas, ajude o blue team:

- Habilitar PowerShell Script Block Logging.
- Habilitar Module Logging + Transcription.
- Sysmon com config Olaf Hartong / SwiftOnSecurity.
- WDAC ou Applocker em mode bloqueio para LOLbins.
- EDR com tamper protection ativa.
- Threat hunt periodico (RITA, Velociraptor, KAPE).
- Treinar SOC com Atomic Red Team / Caldera.

---

## Referencias

- [Maldev Academy](https://maldevacademy.com/) (pago, conceitual).
- [Red Team Notes do ired.team](https://www.ired.team/).
- [Atomic Red Team](https://atomicredteam.io/) - emulacao defensiva.
- [LOLBAS](https://lolbas-project.github.io/), [GTFOBins](https://gtfobins.github.io/).
