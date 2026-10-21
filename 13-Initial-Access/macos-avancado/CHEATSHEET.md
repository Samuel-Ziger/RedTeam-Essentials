# Consulta rápida

```zsh
uname -a
file binario
lipo -info binario
otool -hv binario
otool -L binario
dyld_info -dependents binario
codesign --display --verbose=4 binario
codesign --verify --deep --strict --verbose=4 Aplicativo.app
spctl --assess --type execute --verbose=4 Aplicativo.app
plutil -lint perfil.mobileconfig
profiles show -type configuration
log show --last 5m --style compact --predicate 'subsystem == "com.example.rte"'
sample PID 5 -file amostra.txt
```

Perguntas de revisão:

1. Qual camada tomou a decisão observada?
2. Qual identidade e qual code requirement estão em uso?
3. O dado é fato, inferência ou ausência de telemetria?
4. A mudança é local, por perfil, declarativa ou dependente de serviço?
5. Qual é a reversão e como a pós-condição será provada?

Nunca use `csrutil disable`, desative Gatekeeper ou remova atributos de
quarentena como atalho de diagnóstico.
