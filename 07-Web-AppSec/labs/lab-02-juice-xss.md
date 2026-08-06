# Lab 02 — OWASP Juice Shop: XSS / DOM

> Lab guiado no Juice Shop local. Foco em challenges educacionais de XSS (reflected, stored, DOM) via Score Board. Sem payloads de ataque a producao.

**Teoria:** [../xss-deep-dive.md](../xss-deep-dive.md)

---

## Pre-requisitos

```bash
cd docker-lab
docker compose up -d
docker compose ps
```

| Item | Valor |
|------|--------|
| URL | http://127.0.0.1:8082 |
| Score Board | Acessivel pela UI do Juice Shop (challenge / menu) |
| Escopo | Somente instancia local `127.0.0.1:8082` |

Ferramentas uteis: navegador com DevTools, Burp (opcional), DOM Invader (Burp Pro, opcional).

---

## Objetivos de aprendizado

1. Navegar o Juice Shop e abrir o **Score Board**.
2. Identificar challenges de XSS / DOM XSS e completar pelo menos **dois** (ou um reflected + um DOM, conforme versao).
3. Classificar o contexto (HTML body, atributo, DOM sink).
4. Documentar no REPORT-TEMPLATE com prova minima (`alert` de lab / flag do challenge), sem roubar sessoes de terceiros.

---

## Parte 0 — Orientacao no Juice Shop

1. Abra http://127.0.0.1:8082
2. Feche o welcome banner se aparecer
3. Localize o **Score Board** (challenge dedicado ou atalho na UI — o path exato varia por versao; use a busca de challenges)
4. No Score Board, filtre por dificuldade / tags relacionadas a:
   - XSS
   - DOM XSS
   - Client-side
5. Leia a descricao de cada challenge — o Juice Shop e **autoexplicativo** por design

> Dica: a propria descoberta do Score Board costuma ser um challenge. Use a busca da aplicacao e hints oficiais do projeto se travar.

---

## Parte 1 — XSS reflected / stored (educacional)

### Metodo geral

1. Escolha um challenge XSS no Score Board e leia o enunciado
2. Encontre o ponto de entrada (busca, feedback, perfil, etc.)
3. Teste um payload **classico de lab** adequado ao contexto, por exemplo:

```html
<img src=x onerror=alert("XSS")>
```

ou, em contextos mais restritos, consulte a secao de contextos em [../xss-deep-dive.md](../xss-deep-dive.md).

4. Confirme o popup / execucao no **seu** browser local
5. Verifique se o Score Board marcou o challenge como resolvido
6. Anote: tipo (reflected vs stored), parametro, contexto de output

### Regras do lab

- Use `alert` / `console.log` apenas na sua instancia local
- Nao configure keyloggers, BeEF ou exfiltracao para hosts externos
- Nao colete dados de outros usuarios reais (no lab local so existem dados de treino)

### Checkpoint

- [ ] Pelo menos um challenge XSS marcado como solved
- [ ] Tipo e contexto identificados
- [ ] Screenshot do Score Board (challenge resolved) + do `alert` (opcional)

---

## Parte 2 — DOM XSS

### Metodo geral

1. Filtre challenges **DOM XSS** no Score Board
2. Abra DevTools → Sources / Elements; procure sinks (`innerHTML`, `document.write`, jQuery `html()`, etc.)
3. Identifique a source (`location.hash`, query string, `localStorage`, etc.)
4. Monte a URL/local de lab que leva o input ate o sink **sem** passar pelo servidor necessariamente
5. Valide com `alert` de lab e marque o challenge

Exemplo conceitual de padrao (nao e o path exato do Juice Shop — descubra no app):

```text
Source: location.search / location.hash
Sink:   element.innerHTML = ...
```

### Checkpoint DOM

- [ ] Sink e source descritos no seu caderno/relatorio
- [ ] Challenge DOM XSS resolvido **ou** tentativa documentada com hipotese clara

---

## Parte 3 — Score Board: trilha sugerida

Ordem educativa tipica (nomes podem variar entre versoes do Juice Shop):

| Ordem | Foco | O que observar |
|-------|------|----------------|
| 1 | Score Board unlock | Como a app esconde features |
| 2 | XSS "simples" / reflected | Input → response |
| 3 | Stored XSS | Persistencia e impacto multi-usuario (lab) |
| 4 | DOM XSS | Sinks no cliente |
| 5 | (Opcional) CSP / bypass leve | So se o challenge existir na sua versao |

Complete no minimo **2 challenges** da trilha XSS/DOM para dar o lab como feito.

---

## Parte 4 — Documentar no REPORT-TEMPLATE

| Campo | Conteudo sugerido |
|-------|-------------------|
| Titulo | DOM/Reflected XSS no Juice Shop (challenge X) |
| Severidade | Media/Alta conforme impacto (sessao, admin) |
| Componente | URL/feature do challenge |
| Passos | Navegacao + input + payload de lab + resultado |
| Evidencia | Score Board "solved" + screenshot do alert |
| Impacto | Execucao de JS no contexto da origem do lab |
| Remediacao | Escape contextual, CSP com nonce, Trusted Types, DOMPurify |
| Referencias | OWASP XSS Prevention; xss-deep-dive do repo |

### Modelo de evidencia

```text
Alvo: http://127.0.0.1:8082 (docker-lab)
Challenge: <nome no Score Board>
Tipo: Reflected | Stored | DOM
Prova: alert de lab + challenge marcado as solved
Payload: <payload minimo usado no lab>
Sem exfiltracao externa.
```

---

## Criterios de sucesso

- [ ] Juice Shop acessivel em `:8082`
- [ ] Score Board utilizado
- [ ] ≥ 2 challenges XSS/DOM resolvidos (ou 1 + analise DOM documentada)
- [ ] Achado(s) no REPORT-TEMPLATE sem dados sensiveis reais
- [ ] Remediacao citada

---

## Encerramento

```bash
cd docker-lab
docker compose down
```

Proximo: [lab-03-vampi-api.md](lab-03-vampi-api.md) · Teoria SSRF: [../ssrf-deep-dive.md](../ssrf-deep-dive.md)

---

## Referencias

- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
- [Juice Shop docs / challenges](https://pwning.owasp-juice.shop/)
- [docker-lab/README.md](../../docker-lab/README.md)
- [../xss-deep-dive.md](../xss-deep-dive.md)
