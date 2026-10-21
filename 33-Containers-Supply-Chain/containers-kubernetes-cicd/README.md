# Containers, Kubernetes, CI/CD e supply chain

O percurso segue um artefato desde o código-fonte até sua execução, observando
onde identidade, proveniência, segredos e políticas podem falhar.

## Sequência

1. Estude o [baseline de hardening](hardening-baseline.md).
2. Relacione [caminhos Kubernetes](kubernetes-attack-paths.md)
   aos respectivos controles e sinais.
3. Use [técnicas de escape](docker-escape-techniques.md)
   apenas como modelo de ameaça em ambiente descartável.
4. Execute o [lab de auditoria](labs/README.md) com a
   fixture local e compare a
   [resposta](labs/answers/lab-01-k8s-audit.md).
5. Expanda a análise para
   [CI/CD e supply chain](LEGADO-CICD-SUPPLY-CHAIN.md).

## Entrega

Apresente SBOM ou inventário equivalente, política de imagens, identidade de
workload, tratamento de segredos, gates do pipeline, evidência de auditoria e
procedimento de rollback.
