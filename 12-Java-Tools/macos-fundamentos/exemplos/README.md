# Exemplos executáveis

## Baseline local

`Get-RteMacBaseline.py` executa somente consultas conhecidas, sem shell, e não
coleta serial, UUID, contas ou rede. No macOS:

```zsh
python3 Get-RteMacBaseline.py --pretty
```

Em qualquer sistema, o modo fixture permite estudar e testar a transformação:

```bash
python3 Get-RteMacBaseline.py --fixture fixtures/mac-command-output.json --pretty
```

## Backup didático

`Backup-RteFixture.py` exige origem existente e destino novo, recusa destino
dentro da origem, suporta dry-run e gera manifesto SHA-256.

```bash
python3 Backup-RteFixture.py ORIGEM DESTINO --dry-run
python3 Backup-RteFixture.py ORIGEM DESTINO
python3 Backup-RteFixture.py --verify DESTINO
```

Ele demonstra o contrato; Time Machine continua sendo a solução apropriada para
backup geral do Mac. Rode os testes com:

```bash
python3 -m unittest discover -s tests -v
```
