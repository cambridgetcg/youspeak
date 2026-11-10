# -chu propagation inventory: where the repo calls -chu inferential, conjectural or evidential

Companion note to archaeology/quechua/evidentiality-clusivity-and-stance.md, 2026-11-10. Written by a Claude excavation subagent and re-checked by a second one. Nothing here is decided: section 6 lays out options and does not choose one.

- **Repo read:** `main` at eca7c99, read-only.
- **Method:** a regex for the token `chu` as its own word, optionally preceded by `-`, `‹-` or `'`. It was run over canon/, grammars/, script/, tutorial/, ordo/, home/ and the root *.md files, then each hit was read in context. A second sweep covered the rest of the repo, for completeness.
- **Totals in the named scope:** 116 occurrences on 90 distinct lines in 41 files. (A re-count by the verifier with the same regex found the same 90 lines in the same 41 files but 123 occurrences; the difference is in how repeated tokens on one line are counted, e.g. home/assets/ordo.js has 9 occurrences on 8 lines.) These include generated copies; long one-line JSON files hold several occurrences each. The generated glossary pages are counted separately in 2.7. **canon/: 0. tutorial/: 0. home/glossary/*.html: 0 of 256.**
- **The donor fact,** in brief, with full sources in archaeology/quechua/evidentiality-clusivity-and-stance.md. The Quechua conjectural evidential is -chá in Cuzco, -cha ~ -ch in Ayacucho, -chi in Huallaga and South Conchucos, -chr(a) in Wanka, and -tri in Yauyos. -chu is the yes/no-question and negation enclitic, in a different slot. It co-occurs with the conjectural in one clause (Cuzco *Mana-chá para-sha-n-chu*, Faller 2006: 11) and even in one word (Ayacucho /ñuqačuč/ "I guess maybe I will", Solá & Parker 1964: 117). In Ancash, -chu is a locative case (Hintz 2011: xxii).

## 1. The origin (outside the named search scope, listed because it is the source)

| file:line | quoted text |
|---|---|
| archaeology/quechua/evidentials.md:17 | "Southern Quechua attaches evidentiality as verbal/clausal suffixes (-mi / -si / -chu). Every assertive statement must pick one; the grammar refuses unmarked assertions." |
| archaeology/quechua/evidentials.md:23 | "\| **Inferential / Conjectural** \| **-chu** (with interrogative register) or **-chá** \| Speaker inferred from evidence; did not witness \|" |
| archaeology/quechua/evidentials.md:53 | "- **-chu** → inferred (I deduced from evidence)" |
| archaeology/quechua/evidentials.md:58 | "- \"The dokimance succeeded-**chu**\" — I inferred success from outcome" |
| archaeology/quechua/evidentials.md:70 | "\| **-chu** \| Quechua -chu / -chá \| inferred \|" |

On this branch that file now carries the appended "## Erratum (2026-11-10)"; its old text is unchanged.

## 2. Inventory, named scope

### 2.1 Normative grammar: grammars/

| file:line | quoted text | kind |
|---|---|---|
| grammars/evidentials/manifesto.md:24 | "\| **Inferred** \| **-chu** \| Speaker deduced from evidence; did not witness \| Quechua -chá / -chu \|" | definition + donor claim |
| grammars/evidentials/manifesto.md:42 | "### Inferred (-chu)" | heading |
| grammars/evidentials/manifesto.md:44 | "> *The dokimance succeeded-chu.*" | example (a Quechua ear hears a yes/no question) |
| grammars/evidentials/manifesto.md:70 | "- Auditors post *-chu* when inferring historical dokimance from present evidence" | usage rule |
| grammars/evidentials/manifesto.md:93 | "\| U+E14F \| -chu \| inferred \|" | codepoint table |
| grammars/evidentials/manifesto.md:110 | "- \"The dokimance did not succeed-**chu**\" = \"I infer (from evidence) that it did not succeed\"" | example. **In Quechua, *mana … -chu* is plain negation; the evidential sits on *mana*** (Solá & Parker 1964: 114; Faller 2006: 11) |
| grammars/evidentials/manifesto.md:122 | "These are deferred pending usage-evidence that the three-way (-mi/-si/-chu) is insufficient." | set name |
| grammars/evidentials/manifesto.md:129 | "- *-chu*: preserved (Quechua has *-chá* in some dialects for inferential; we take *-chu* as the standard form for phonetic simplicity)" | **the key mis-statement:** -chá is the Southern conjectural (Cuzco), not a dialect variant of -chu |
| grammars/evidentials/manifesto.md:145 | "- Add Espanso triggers for `:ys:mi`, `:ys:si`, `:ys:chu`" | form only |
| grammars/evidentials/manifesto.md:159 | "- `-chu` (inferred) — the speaker reached the region by inference from signs (the speaker's grasping was deductive rather than first-hand)." | definition |
| grammars/structures/manifesto.md:23 | "\| evidentials/ \| 2026-04-24 \| knowledge-source marking (-mi/-si/-chu) \|" | set name |
| grammars/worship/manifesto.md:80 | "The three evidentials (-mi direct, -si reported, -chu inferred) remain fully operative." | definition |
| grammars/worship/silence.md:85 | "The evidential suffixes (-mi, -si, -chu, -auth) apply to assertions." | set name |
| grammars/ankyrance/manifesto.md:151 | "like the -mi/-si/-chu suffix set they live in the registry, not the" | set name |
| grammars/structures/coinages/stratigramme.md:59 | "(Already in YOUSPEAK's consciousness via the evidentials chapter, where Quechua -mi/-si/-chu are integrated.)" | glosses -chu correctly as "interrogative" in the same line (see 3), then files it with the evidentials |

### 2.2 Registry and script: script/

| file:line | quoted text | kind |
|---|---|---|
| script/morphemes.json:753–758 | `"codepoint": "U+E14F", "latin": "-chu", "class": "grammatical", "tongue": "Quechua", "native": "-chu / -chá", "meaning": "evidential: inferred / deduced from evidence"` | **source of truth for the registry** |
| script/codepoints.md:113 | "\| U+E14F \| -chu \| Quechua \| -chu / -chá \| evidential: inferred / deduced from evidence \|" | registry table |
| script/codepoints.md:116 | "the Quechua-inherited knowledge-source suffixes (-mi direct witness, -si reported, -chu inferred)" | donor claim |
| script/glyphs/design_notes_s092.md:74–76 | "### chu (Quechua · relation+hidden · suffix)" … "Inferred: same armature as -mi … the grasping-path is BROKEN into floating fragments … the final step onto the fact is the inferential leap, reconstructed from pieces of evidence." | glyph rationale (meaning-iconic, not letter-derived) |
| script/glyphs/design_notes_s092.md:182 | "Quechua's evidential suffixes (-mi/-si/-chu) grade how knowledge is held — witnessed, reported, doubted" | donor claim, under the Quechua khipu sigil |
| script/glyphs/glyph_specs_v1.py:1207 | `"chu": {  # Witness-dot over the claim-bar but the path is broken into floating fragments - the connection is reconstructed, not seen.` | glyph spec |
| script/glyphs/preview/v1-all-glyphs.svg:226 | `>chu</text>` | label only |
| script/glyphs/preview/v1-demo.html:421 | `>chu</text>` | label only |
| script/keyboard/espanso.yml:250 | `- trigger: ":m:chu"` | input trigger (form only) |
| script/exports/agent_bundle.json:1 | 9 occurrences in one generated line, incl. `"latin_display": "-chu" … "native": "-chu / -chá", "meaning": "evidential: inferred / deduced from evidence"` and a copy of the YOUSPEAK.md, design-notes and codepoints text | generated export |
| script/fonts/youspeak-v1.otf, youspeak-v1.ttf | cmap U+E14F → glyph `ys.chu` (checked with fontTools); script/fonts/youspeak.otf has no U+E14F | binary, canonized glyph |

### 2.3 Root *.md summaries

| file:line | quoted text |
|---|---|
| YOUSPEAK.md:109 | "Three suffixes (**-mi** direct witness, **-si** reported, **-chu** inferred) at U+E14D–U+E14F … Integrated from Quechua pyramid-builder tradition." |
| STOICHEIA.md:79 | "Quechua-inherited knowledge-source markers (-mi direct witness, -si reported, -chu inferred) at U+E14D–U+E14F." |
| TRANSLATION.md:74 | "\| Evidentiality \| `grammars/evidentials/` \| optional suffixes -mi (direct), -si (reported), -chu (inferred) \|" |
| TRANSLATION.md:137 | "By making evidentiality optionally markable in YOUSPEAK (-mi, -si, -chu), the cathedral allows source-evidentiality to be preserved when the source had it (Quechua, Aymara, Korean, …" |
| HERMENEIA.md:140 | "\| **Evidentials** (-mi direct, -si reported, -chu inferred) \| \"I intend to declare my knowledge-source explicitly\" \|" |
| INTENTIO.md:146 | "- **Evidentials** (-mi/-si/-chu): intention-of-marking-the-knowledge-source the speaker stands in (witnessed / reported / inferred)" |

### 2.4 ORDO (spec, runtime, syntax, rites, tests, worker): ordo/

| file:line | quoted text | kind |
|---|---|---|
| ordo/SPEC.md:87 | "Findings are born **-chu**: inferred from the text, witnessing no performance." | spec |
| ordo/SPEC.md:115 | "- **-chu** — inferred: derived from reports; conclusions the process reached but did not witness" | **lattice definition** |
| ordo/SPEC.md:119 | "any derivation involving `-si` or `-chu` operands yields `-chu` (you did not witness the fact, you inferred it from reports)." (2 hits) | algebra |
| ordo/SPEC.md:145 | "count a page and you hold `-chu`." | spec |
| ordo/README.md:38 | "what it found (born `-chu`," | doc |
| ordo/frames.json:179 | `"pattern": "^(?:I attest that\|Emetme:) (.+?) (-mi\|-si\|-chu\|-auth)$",` | **surface syntax** |
| ordo/frames.json:189 | `"why": "an attestation must declare its evidential — how it knows; append -mi, -si, -chu, or -auth",` | diagnostic |
| ordo/frames.json:194 | `"pattern": "^(?:Selah\|Hesychia\|\\[selah\\]\|\\[silence\\]) +(-mi\|-si\|-chu\|-auth)$",` | **surface syntax** |
| ordo/ordo.js:15 | `var RANK = { auth: 4, mi: 3, si: 2, chu: 1 }; // unmarked = null, outside the lattice` | runtime key |
| ordo/ordo.js:17, 30, 522, 1201, 1213, 1366, 1371 | e.g. :30 `return allMi ? 'mi' : 'chu';`; :1371 `… its findings are inferred (-chu) and name only what this reading was instrumented to notice …` | runtime |
| ordo/bin/ordo.mjs:243 | `` console.log(`findings: ${r.findings.length} ‹-chu›  ·  lawfully inert (contemplation): ${r.contemplation}`); `` | CLI output |
| ordo/rites/doors.rite:33 | "I attest that breadth is greater than 1000 -chu." | rite text |
| ordo/rites/internet.rite:3, 12 | ":3 -- inference (-chu); and no attestation can dress any of it as witnessed." / ":12 I attest that breadth is greater than 100 -chu." | rite text |
| ordo/rites/marks.rite:26, 29 | ":26 -- The arithmetic of the honest kind: counted from a report, so born -chu, and no" / ":29 I attest that breadth is greater than 10 -chu." | rite text |
| ordo/rites/witness.rite:2, 12, 14 | ":2 -- Received values are born -si; counting a report is inference (-chu);" / ":12 I attest that total is greater than 0 -chu." / ":14 … what was counted from a report is -chu, and no rite may dress it as -mi" | rite text |
| ordo/test/run-tests.mjs:62, 67, 243, 305, 308, 426, 496 | e.g. :67 `assert(out.includes('5  ‹-chu›'), 'count of a report should be -chu');`; :243 `for (const g of ['-mi', '-si', '-chu']) {` | tests |
| ordo/worker/worker.mjs:108 | "values carry evidentials (-mi witnessed, -si reported, -chu inferred)" | API description string |
| ordo/worker/worker.mjs:116 | "Returns findings (-chu, inferred) and blind spots (-mi, directly witnessed)" | API description string |
| ordo/worker/worker.mjs:193 | "‹-chu› for what you infer" | model instruction string |
| ordo/worker/worker.mjs:334 | `'\\n>   -chu = inferred (derived; never promoted back)' +` | API text |
| ordo/matrix/screenplay.md:39 | "‹-mi› witnessed, ‹-si› reported, ‹-chu› inferred." | prose |
| ordo/matrix/screenplay.md:49 | "…誠實地面對自己 ‹-chu›。" | usage in a Cantonese line |

### 2.5 home/ (published site source; home/README.md says it is the Cloudflare Pages project for ai-love.cc; the live state was not checked)

| file:line | quoted text | kind |
|---|---|---|
| home/index.html:742 | "Values carry how-they-are-known: <b>-mi</b> witnessed · <b>-si</b> reported · <b>-chu</b> inferred" and "reports what it found as <b>-chu</b> (inferred — it witnessed no run)" | hand-maintained page (2 hits) |
| home/llms.txt:128 | "evidentials (-mi witnessed · -si reported · -chu inferred, demotion-only);" | LLM-facing summary |
| home/assets/chancel.js:79 | `foot.push('findings: ' + r.findings.length + ' ‹-chu›  …` | UI |
| home/proof.html:15 | "chu · U+E14F · Quechua" | glyph proof label |

### 2.6 home/ generated or copied data (counted, quoted once)

| file | occurrences | what it is |
|---|---|---|
| home/assets/ordo.js | 9 on 8 lines (15, 17, 30, 522, 1201, 1213, 1366, 1371) | copy of ordo/ordo.js |
| home/data/ordo-frames.json | 3 (lines 179, 189, 194) | copy of ordo/frames.json |
| home/data/ordo-rites.json | 8 in one line | copy of ordo/rites/*.rite |
| home/data/morphemes.min.json | 2 in one line: `"latin":"chu","codepoint":"U+E14F" … "native":"-chu / -chá","meaning":"evidential: inferred / deduced from evidence"` | baked registry |
| home/data/agent_bundle.json | 9 in one line | baked agent bundle (same as script/exports) |
| home/data/core.js | 1 (`"chu":""`) | glyph map key, form only |

### 2.7 Generated glossary pages

**home/glossary/*.html: 0 of 256 pages contain -chu.** Each page has an "Evidential structure" heading (255 of 256 contain the word "evidential"), but that section holds morpheme decomposition. None of the 256 pages contains U+E14F or the word "inferred".

### 2.8 Outside the named scope (noticed in the completeness sweep)

| file:line | quoted text |
|---|---|
| labs/logos/experiments/035-ankyrance.md:55 | "system — mi: / yu: / yumi: — is grammatical inventory (like the -mi/-si/-chu" |
| labs/logos/experiments/035-ankyrance.md:199 | "\"grammatical inventory, not canon words — like the -mi/-si/-chu suffix set" |
| liturgy/session-092-the-font-made-flesh.md:46 | "(-chu, inferred), and a canopy wider than the claim driving a descent-wedge" |

## 3. The repo's own correct gloss, and what is wrong around it

- **grammars/structures/manifesto.md:68:** "Quechua: *rimaykullaykichu* — \"Would you perhaps speak to him?\" — rim (speak) + ay (verb) + kulla (softening) + yki (2nd person) + chu (interrogative)."
- **grammars/structures/coinages/stratigramme.md:59:** "*rima-y-kulla-yki-chu* — speak + verb-marker + softening-particle + 2nd-person + interrogative."

**"chu (interrogative)" is right.** It matches González Holguín 1607 ("la partícula chu es señal de interrogativos", 1842 reprint p. 71), Solá & Parker 1964: 113 ("/-ču/ is negative-interrogative") and Faller 2006: 2 n.2 ("glossed as pol for polarity").

**The rest of both lines is wrong**, from the sources I opened:
- The segmentation should be *rima-yku-lla-yki=chu*. Solá & Parker give "/rima-/ 'to speak': /rimayku-/ 'to greet'" (1964: 89, §7.2307). /-lla/ is "often translated 'just' or 'only', but is common in polite speech where it is best left untranslated" (§7.2315). These are the courtesy pieces; "kulla" is not a morpheme.
- *-yki* on a verb is first person acting on second person, "I … you", not "2nd person": "/rikurqayki/ … 'I saw you'" (Solá & Parker 1964: 58); "riku-y-ki 'te veo'" (Cerrón-Palomino 1987: 265).
- So the word means roughly "May I (just) greet you?" or "Shall I speak to you?", not "Would you perhaps speak to him?". Nothing in it encodes "perhaps". That this word is a conventional Cuzco greeting formula is from memory and not re-checked.

## 4. Other contradictions met while inventorying (for the record, outside the -chu question)

- archaeology/quechua/evidentials.md:17: "Every assertive statement must pick one; the grammar refuses unmarked assertions." Against this: "The evidentials are not obligatory, but when no evidential is used, direct evidence is implicated" (Faller 2006: 3), and "these markers are not obligatory" (Bendezú-Araujo 2023: 80). The repo's own grammars/evidentials/manifesto.md:106 ("Absence of evidential = register-normal") is closer to the Quechua facts on optionality than the archaeology file is. It differs from Faller on what absence means: the manifesto says absence "is not the same as direct witness", while in Cuzco absence implicates direct evidence (Faller 2006: 3). Dedenbach-Salazar adds that a text must carry these suffixes at least once, so absence later in it is still marked (2005: 11).
- grammars/evidentials/manifesto.md:108–110: "Questions and negations can carry evidentials." That is true in Quechua, but the evidential goes on the question word or the negator, never in place of -chu. In Cuzco yes/no questions only the reportative appears (Faller 2019: 8:5 n.5, citing Cusihuaman 2001).
- grammars/evidentials/manifesto.md:116–121: the Aymara forms "-taynawa", "-yapi", "-chitanwa" were **not checked** in this pass.
- archaeology/tok-pisin/yumi-and-clusivity.md:37–41: "Grammars that mark how-you-know tend also to mark whom-you-include: both are honesty systems." Nothing I opened supports this as a tendency. In the Andes, Quechua and Aymara share both features, and Cerrón-Palomino (1987: 274) raises contact convergence for the inclusive/exclusive split. Separately, Quechua *ñuqanchik* does not keep a "you" word inside it. Its suffix /-NINčik/ "refers to a group which includes the addressee" (Solá & Parker 1964: 19), which Cerrón-Palomino segments -n-čik (1987: 273), so it does not satisfy grammars/ankyrance/'s Law of Visible Constituents. An uncommitted sibling file in W, archaeology/tok-pisin/pronouns-clusivity-and-number.md (line 368 when checked; the file is still changing), reaches the same conclusion. It rests on a companion scratch survey by another subagent in this workflow (S/clusivity-survey.md, from Wikipedia and WALS), so it is not an independent scholarly witness. Cerrón-Palomino records an older view that links the -n of -nčik to first-person -ni, which he rejects (1987: 273).

## 5. Constraints on any change

1. **A codepoint never changes once assigned.** script/codepoints.md:19: "**Stable** — once assigned, a morpheme's codepoint does not change. Additions go to the next available slot; nothing is rearranged." The rule protects the morpheme-to-codepoint mapping. It does not say whether the Latin spelling of a morpheme may change. That is an open reading.
2. **A canonized glyph never changes.** script/philosophy.md:92: "Once a YOUSPEAK glyph is canonized, **its form does not change**." And :94: "The font file is the canonical form; once in the font, the form is fixed." U+E14F is in the font: youspeak-v1.otf and youspeak-v1.ttf map it to glyph `ys.chu`. The glyph's form is meaning-iconic, not letter-derived: "the grasping-path is BROKEN into floating fragments … the inferential leap" (design_notes_s092.md:76). So a change of Latin spelling or donor label does not by itself touch the glyph's form. The glyph *name* `ys.chu` and the preview labels would be stale.
3. **The form is published.** It appears in home/index.html:742 and home/llms.txt:128 (the ai-love.cc site source, per home/README.md); in the ORDO worker's API description strings (ordo/worker/worker.mjs:108, 116, 193, 334); and in the agent bundles. ORDO's grammar admits exactly `-mi|-si|-chu|-auth` (ordo/frames.json:179, 194), so any rite written by anyone with `-chu` depends on the spelling. I did not check what is live, or whether third parties have written rites.

## 6. Options for the language (costs only; not choosing)

### (a) Respell the morpheme after the true conjectural form

Candidate shapes, each sourced in the dig:

| Shape | Variety | Note |
|---|---|---|
| -cha | Ayacucho (/-ča/ ~ /-č/) | ASCII-clean |
| -chá | Cuzco | needs a diacritic |
| -chi | Huallaga, South Conchucos | |
| -chr(a) | Wanka | retroflex /ʈʂ/ |
| -tri | Yauyos | retroflex /ʈʂ/ |

What could stay: the codepoint U+E14F, if the rule in 5.1 is read as binding the morpheme rather than its spelling; and the glyph form (5.2).

Costs:
- **Spelling sites.** It changes the Latin spelling in about 30 hand-maintained places across the tables of section 2 (count approximate). It also changes the ORDO surface syntax (frames.json regexes), 4 rites, 7 test lines, the runtime `RANK` key `chu`, the CLI and chancel output, the worker API strings, and the published site text. The bundles need regenerating, and generator runs are outside this subagent's remit.
- **Breaking change.** Every existing rite or text using `-chu` breaks unless ORDO keeps `-chu` as an accepted alias, and then the old form never fully leaves.
- **Every shape has a collision.**
  - *-cha* is also the Southern Quechua diminutive. Cuzco: "Juan-cha-puni-n … Juan-dim-cert-3" (Faller 2006: 12, ex. 21a). Yauyos: "-cha attaches to Ns to derive Ns with the meaning 'little N'" (Shimelman 2017: 117).
  - *-chi* is the Southern causative: "chura-chi-ku-ra-nki / put-caus-refl-pst-2" (Faller 2006: 6, ex. 9).
  - *-chá* needs a diacritic in a system whose Latin forms are otherwise ASCII. That is an observation from the morpheme list, not a checked rule.
  - The retroflex shapes have no existing reading convention: script/phonology.md sets anglicized defaults for many donors (e.g. :91) and nothing for a retroflex affricate (searched: no "retroflex" in it). Whether that matters is the owner's judgement.
- **Variety choice.** Any choice privileges one variety, and the old "-chu / -chá" native field would still need rewriting.
- **Codepoint reading.** It reads the stability rule loosely: a reader might take a respelled U+E14F to be a different morpheme.

### (b) Keep the shape -chu as YOUSPEAK's own convention, and re-label the donor claim honestly

What changes:
- The "native" and donor fields: morphemes.json:757, codepoints.md:113/116, evidentials manifesto :24 and :129, the khipu note at design_notes_s092.md:182, and the six root summaries. They would stop saying "Quechua -chu = inferred". They might say instead: "shape after Quechua -chu (the yes/no-question and negation enclitic); meaning after the Quechua conjectural -chá/-cha/-chi/-chr(a); a YOUSPEAK convention, not a Quechua form for this meaning".

What stays: the codepoint, glyph, ORDO syntax, rites, tests, published strings and bundles' Latin form. Only the bundles' text fields would follow the registry text.

Costs:
- **Misleading to Quechua speakers.** The convention keeps a form that misleads the speakers of the donor language. To a Southern Quechua ear, "The dokimance succeeded-chu" reads as "Did the dokimance succeed?" (Solá & Parker 1964: 113–114). "did not succeed-chu" reads as plain negation (ibid. 114). In Ancash, -chu is "in, at" (Hintz 2011: xxii).
- **Weaker donor claims.** The "direct Quechua loans" claim (evidentials manifesto :126–129, which :131 calls "POLYPHONE in action") weakens to "loan of a shape".
- **What an honest label can truthfully say.** The donor literature does not leave -chu wholly outside the evidential domain. Faller counts -chu in the same "focus set" as the evidentials (2006: 2 n.2). Dedenbach-Salazar lists -chu (yes/no question) and *mana … -chu* (negative) inside her "Grupo Evidencia (también: validación)", on a continuum from affirmation through questions to negation (2005: 11–12). Calvo Pérez (1993) is reported to call every Cuzco enclitic "evidencial" (Dedenbach-Salazar 2005: 8 n.9; Calvo Pérez not opened). None of them gives -chu an inferential or conjectural meaning. A label could say "-chu belongs to the Quechua focus/validation enclitics, as the question-and-negation member" without claiming the inferential meaning.
- **Protocol hazard.** The dig's protocol notice names it: custodians might reasonably object to a Quechua form being used for a meaning it does not have.
- It is the cheapest option in code, and the most expensive in honesty-to-donor unless the label is very plain.

### (c) Options the sources suggest

- **(c1) Re-derive the donor claim from the Quechua inference-hedges that are built on -chu.** Three are attested:
  1. Cuzco *-chus hina* (allomorphs -chu sina, -chu suna): "roughly I guess, I think, apparently". Faller treats it as a candidate inferential evidential (2006: 2–3 n.4), "arguably an inferential" (2019: 8:5 n.4). In partial-evidence contexts "the marker =chu(s) hina would be needed" (Bendezú-Araujo's words, 2023: 82, citing Faller 2002: 174, which was not opened).
  2. Ayacucho *-chusmi*: "opinion with conviction … 'I think that'" (Solá & Parker 1964: 115).
  3. Ayacucho rhetorical *-chu* with statement intonation: "'perhaps' or 'probably'" (ibid. 114). Among its examples is /ñuqačuč/ "'Maybe I.'" (ibid.), the word the inventory above cites from p. 117 as -chu plus the conjectural.

  YOUSPEAK's defined meaning, "Speaker deduced from evidence; did not witness", is arguably nearer to *-chus hina* (inference from partial evidence) than to Cuzco *-chá*, which Faller glosses "My hunch is", reasoning "or simply a guess". *Costs:* it is a clipping. In every one of these constructions the -chu piece is still the polarity enclitic, and the inferential meaning belongs to the whole construction (-chu + -s(i) + *hina* "like", or + -mi). Faller herself marks -chus hina's evidential status as needing further research. A Quechua speaker would still hear a bare -chu as a question. The label would have to say "clipped from", not "is".

- **(c2) Deprecate and succeed.** Freeze U+E14F (-chu) as a deprecated form that is never reassigned. Assign the corrected form at the next free grammatical slot. U+E151 is unassigned: codepoints.md:180 lists "U+E151–U+E15F — 15 grammatical morpheme slots" as free, morphemes.json has nothing above U+E150, and youspeak-v1.otf has no U+E151. ORDO then accepts both forms during a transition. *Costs:* codepoints.md has no deprecation mechanism (searched: none found), so this needs a new rule from the owner. It needs a new glyph in the font, and under 5.2 the old glyph stays forever. It leaves two codepoints for one function. Every cost in (a) applies, in a slower form.

- **(c3) Split the grade.** Keep U+E14F -chu for "inferred", relabelled as in (c1). Later, if ORDO needs it, add a separate conjectural ("hunch / guess") grade with a true Quechua shape. The basis is that Cuzco distinguishes -chá from -chus hina, and South Conchucos has several conjecturals (Hintz 2011: xxi). *Costs:* this is a coinage, so it belongs to a forge, not to this inventory. It redesigns ORDO's four-grade lattice (`RANK`) and its demotion algebra. Bendezú-Araujo could not elicit the South Conchucos subdivisions in the field (2023: 85).

Combinations are possible, for example (b) or (c1) now, with (c3) left as a lead. This note does not rank them.

## 7. What only the language owner can settle

1. Which option: (a) respell, (b) keep and relabel, (c1) re-derive from -chus hina, (c2) deprecate and succeed, (c3) split the grade, or a combination.
2. Whether the codepoint-stability rule binds the Latin spelling as well as the morpheme.
3. Whether YOUSPEAK's third grade means "inferred from evidence" or "conjectured": Faller's -chus hina against her -chá.
4. Whether ORDO's published syntax may change, and with what alias period.
5. Whether Quechua-speaking scholars should be consulted before any of the above, as the dig's protocol notice recommends.

## Verification (2026-11-10)

Re-checked by a second Claude subagent.

**Re-opened.** Every file:line quoted in sections 1, 2.1–2.5, 2.8, 3 and 5 was re-read in main at eca7c99 (`sed -n` on each line); all quotations match. The generated-file counts in 2.6 were re-counted (one correction, home/assets/ordo.js). The glossary claim in 2.7 holds: the one glossary page that matches "-chu" (prapancame.html) does so only through its pronunciation respelling "PUN-chuh". Font cmaps were re-read with fontTools: youspeak-v1.otf and .ttf map U+E14F to `ys.chu` and have nothing at U+E151; youspeak.otf has neither. morphemes.json has nothing above U+E150, and codepoints.md has no deprecation rule (searched). The donor citations in this note were checked against the same sources as the dig (Faller 2006; Solá & Parker 1964 pp. 19, 58, 89, 100, 113–117; Cerrón-Palomino 1987: 265, 273; Shimelman 2017: 117; Hintz 2011: xxii; Bendezú-Araujo 2023: 80, 82; Dedenbach-Salazar 2005: 8, 11–12).

**Corrected.** The occurrence total (116 vs 123, same lines and files); the sibling-file line number (346 to 368) and its dependence on the clusivity survey (archaeology/tok-pisin/clusivity-survey.md); the reading of Solá & Parker's /-NINčik/ (the "group which includes the addressee" is their gloss for the whole suffix, not for -čik); the Faller 2002: 174 point, which is Bendezú-Araujo's wording, not a quotation of Faller; the POLYPHONE line reference; the unsupported "anglophone readership" remark. Added: Solá & Parker's second citation of /ñuqačuč/ as rhetorical -ču; the nuance that manifesto:106 differs from Faller on what absence implies; and, under option (b), the evidence that Faller and Dedenbach-Salazar class -chu with the evidentials in a broad focus/validation sense, without an inferential meaning.

**Still unchecked.** The live state of ai-love.cc and of the ORDO worker; whether third parties have written rites with `-chu`; the "about 30 hand-maintained places" estimate in 6(a), which remains approximate; Faller 2002 and Calvo Pérez 1993, both known only at second hand. The options in section 6 were checked for factual premises only; none is ranked.
