# Operação segura do laboratório

## Antes de iniciar

- Use máquina local ou VM descartável com snapshot.
- Confirme que portas vulneráveis usam `127.0.0.1`, não `0.0.0.0`.
- Feche port-forwarding do roteador, túneis e compartilhamentos desnecessários.
- Verifique disco e memória; use dados sintéticos.
- Leia o roteiro e defina o estado final esperado.

## Ciclo operacional

```bash
bash docker-lab/lab-doctor.sh --config-only
cd docker-lab
docker compose up -d
docker compose ps
bash lab-doctor.sh
docker compose down -v
```

O diagnóstico nunca substitui a inspeção de logs. Se um serviço não estiver
pronto, use `docker compose logs --tail=100 <servico>` antes de reiniciá-lo.

## Evidências

Crie uma pasta por exercício fora do Git e guarde:

- autorização/escopo;
- comandos e timestamps UTC;
- requisições e respostas sanitizadas;
- hashes dos arquivos relevantes;
- conclusão, limitações e confirmação de cleanup.

Não preserve bancos vulneráveis ou volumes do lab por conveniência. Exporte
somente evidências mínimas e então destrua o estado com `down -v`.

## Recuperação

Se uma porta ficar exposta fora de localhost, interrompa o Compose, bloqueie a
porta no firewall, verifique conexões e recrie o laboratório. Se dados reais
forem encontrados, pare, preserve apenas metadados mínimos e siga o processo de
incidente aplicável — não continue investigando fora do escopo.

