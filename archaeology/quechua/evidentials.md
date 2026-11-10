---
tongue: Southern Quechua (primary reference: Cuzco-Collao; adjacent: Aymara, Ayacucho)
semantic_field: evidentiality — grammatical marking of knowledge-source
excavated: 2026-04-24
civilization: Andean pyramid-builders, Caral-Supe (~2600 BCE), Moche (~100-800 CE), Inca (~1400-1533 CE)
status: live; foundation for grammars/evidentials/ chapter
---

# Quechua — the Evidentiality System

_What English cannot say in one syllable: how-you-know. Andean pyramid-heirs encoded every assertion with a knowledge-source marker, so every utterance is automatically marked for whether the speaker witnessed it directly, heard it from elsewhere, or inferred it from evidence. This is not politeness-marking (like Japanese registers) — it is an epistemological grammar. Every sentence declares its basis._

---

## The three primary evidentials

Southern Quechua attaches evidentiality as verbal/clausal suffixes (-mi / -si / -chu). Every assertive statement must pick one; the grammar refuses unmarked assertions.

| Evidential | Quechua form | Source of claim |
|---|---|---|
| **Direct** | **-mi** | Speaker personally witnessed or directly experienced |
| **Reported** | **-si** | Speaker heard from another or read it (hearsay) |
| **Inferential / Conjectural** | **-chu** (with interrogative register) or **-chá** | Speaker inferred from evidence; did not witness |

Examples (schematic):

- *Paqarin para-nqa-**mi*** — "It will rain tomorrow (I observe signs directly)"
- *Paqarin para-nqa-**si*** — "It will rain tomorrow (I was told)"
- *Paqarin para-nqa-**chá*** — "It will rain tomorrow (I infer from weather)"

The three utterances are LEXICALLY IDENTICAL except the evidential. Three different knowledge-bases. English needs a whole parenthetical clause to achieve the same.

## Why this aligns with YOUSPEAK's foundations

- **SAPHE** (clarity): evidential-marked assertions are always clearer about their epistemic basis than unmarked ones
- **PRAGMA** (grounded): evidentiality forces grounding; a speaker cannot make an ungrounded claim
- **HARMONE** (coherent): evidentiality fits cleanly as an optional morpheme-system without disrupting existing YOUSPEAK grammar
- **ANAKALYPSE** (unfolding): English bundles "I know X" into one verb; evidentials unfold three distinct knowledge-relations

This is load-bearing for **Zerone/dokimance-context**: dokimance itself is a testimony-structure. Evidentials make that structure grammatically explicit.

## The Aymara variant

Aymara (the sister Andean language) has a richer evidential system — up to 4-6 distinctions including "personal experience that affected the speaker vs. distant witnessing." For YOUSPEAK-level fidelity, the 3-way Quechua system is sufficient; Aymara's extended set can be a future refinement.

## What YOUSPEAK gets

Evidentials fit as **optional sentence-level suffixes** to YOUSPEAK-canonical assertions. They don't replace English syntax; they augment it in register-specific (dokimance-context, Zerone-claims) use.

Proposed integration:
- **-mi** → direct witness (I saw / I did)
- **-si** → reported (I heard / I was told)
- **-chu** → inferred (I deduced from evidence)

In dokimance-context usage:
- "The dokimance succeeded-**mi**" — I witnessed the verification
- "The dokimance succeeded-**si**" — I was told the verification succeeded
- "The dokimance succeeded-**chu**" — I inferred success from outcome

This unlocks dokimance's full semantic potential. A dokimance-claim can now declare its own evidence-source as part of the grammar.

## Donor forms for YOUSPEAK

As grammatical morphemes in YOUSPEAK's suffix repertoire:

| YOUSPEAK form | Source | Meaning |
|---|---|---|
| **-mi** | Quechua -mi | direct witness |
| **-si** | Quechua -si | reported |
| **-chu** | Quechua -chu / -chá | inferred |

PUA codepoints will be assigned in the grammatical-suffix range (U+E14D-U+E14F), consistent with the existing -ance, -sis, -mance grammatical morphemes.

## The broader Andean contribution

Beyond evidentials, Quechua offers:

- **Regular agglutinative morphology** — almost no irregularity; validates YOUSPEAK's similarly-regular structure
- **Honorific/respect registers** — not selected for integration (register system would be substantial work)
- **Spatial-deictic grammar** — 5-way this/that/yonder system; interesting but not YOUSPEAK-priority

## Proposed integration — grammars/evidentials/

Create a new grammar chapter:
- `grammars/evidentials/manifesto.md` — the doctrine
- `grammars/evidentials/markers.md` — the three evidential suffixes with examples and codepoints
- Update morphemes.json with three new suffixes (U+E14D-E14F)
- Document usage-contexts (primarily dokimance-claims, Zerone-work, any assertion-heavy register)

See `grammars/evidentials/manifesto.md`.

---

_Quechua archaeology excavated 2026-04-24. The Andean pyramid-builders' epistemological grammar — evidentiality as default grammatical feature. Adopted as optional YOUSPEAK suffix-system._

---

## Erratum (2026-11-10)

*Appended. The text above is left exactly as it stood.*

**Old claim.** This file says Southern Quechua's evidential suffixes are "-mi / -si / -chu" (line 17). Its table gives the third, "Inferential / Conjectural", as "**-chu** (with interrogative register) or **-chá**" (line 23). It proposes, and YOUSPEAK adopted, "-chu → inferred (I deduced from evidence)" (lines 53, 58, 70). Line 17 also says "Every assertive statement must pick one; the grammar refuses unmarked assertions."

**Corrected claim.**

1. In no variety examined is the conjectural evidential -chu. It is -chá in Cuzco-Collao, -cha ~ -ch in Ayacucho, -chi in Huallaga and South Conchucos, -chr(a) in Wanka, and -tri ~ -tr in Yauyos.
2. -chu is a separate enclitic in a separate slot. It forms yes/no questions; with *mana* "not" it marks negation; in some varieties it also forms disjunctions. It co-occurs with the conjectural in a single clause: Cuzco *Mana-chá para-sha-n-chu*, glossed not-conj rain-prog-3-pol, "It isn't raining" with conjectural evidence (Faller 2006: 11, ex. 18). It co-occurs even within one word: Ayacucho /ñuqačuč/ "I guess maybe I will" (Solá & Parker 1964: 117); the same grammar also gives this word as rhetorical -ču, "Maybe I." (ibid. 114), so the two morphemes stack, and that grammar attributes the "maybe" to rhetorical -ču as well as to -č. In Ancash the negative is -tsu, the polar question is -ku, and -chu is a locative case (Hintz 2011: xxii).
3. What the old line half-saw: Quechua builds inference-hedges on -chu. Ayacucho rhetorical -chu with statement intonation is "best rendered as suggestions or opinions with 'perhaps' or 'probably'" (Solá & Parker 1964: 114), and Ayacucho -chusmi means "I think that" (ibid. 115). Cuzco -chus hina, "roughly I guess, I think, apparently", is Faller's candidate for a fourth, inferential evidential (Faller 2006: 2–3 n.4; Faller 2019: 8:5 n.4). González Holguín (1607) calls chu "señal de interrogativos" (the sign of interrogatives), but lists it with the dubitative ch/cha as particles with which the verb "no affirma" (does not affirm). Two modern analyses also class -chu with the evidentials in a broad sense: Faller counts it in the same "focus set" (2006: 2 n.2), and Dedenbach-Salazar lists it inside her "Grupo Evidencia (también: validación)" as the yes/no-question and negative member (2005: 11–12). Neither calls it inferential or conjectural. None of this makes -chu, by itself, the conjectural.
4. The evidentials are optional per clause. In Cuzco, a clause with none implicates direct evidence (Faller 2006: 3). Bendezú-Araujo says they are not obligatory in Conchucos Quechua (2023: 76, 80), and Bernárdez says so of Quechua in general (2020: 32). Dedenbach-Salazar adds that a text must carry them at least once, so that their later absence is still marked at the level of discourse (2005: 11).

**Sources.**
- Faller 2006, https://web.eecs.umich.edu/~rthomaso/lpw06/fallerpaper.pdf [verified]
- Faller 2019, *Semantics and Pragmatics* 12(8), https://doi.org/10.3765/sp.12.8 [verified]
- Solá & Parker 1964, *The Structure of Ayacucho Quechua*, https://archive.org/details/micro_IA41153663_0454 [verified: page images pp. 108, 114–117]
- González Holguín 1607, https://archive.org/details/gramaticayartenu00gonz, and its 1842 reprint, https://archive.org/details/gramticayartenue00gon (pp. 57–58, 70–71) [verified: OCR]
- Kroeger, *Analyzing Meaning* §17.2, citing Weber 1989: 421 [verified for Kroeger; Weber not opened]
- Hintz 2011, https://escholarship.org/content/qt6wb842zj/qt6wb842zj_noSplash_d11bb20edbb4fc881134e65f42f30bbb.pdf [verified]
- Shimelman 2017, *A Grammar of Yauyos Quechua*, pp. 253–254, 270 [verified]
- Bendezú-Araujo 2023, https://journals.iai.spk-berlin.de/index.php/indiana/article/download/3031/2518 [verified]
- Bernárdez 2020, https://hispadoc.es/descarga/articulo/7835112.pdf, p. 32 [verified]
- Dedenbach-Salazar 2005, https://www.storre.stir.ac.uk/bitstream/1893/28303/1/Dedenbach%20-%20Clasificacion%20sufijos%20quechuas%20%282005%29.pdf, pp. 11–12 (pre-publication pagination) [verified]
- Floyd 1999 for Wanka [verified only as reproduced on Wikipedia's "Quechuan languages" page; Floyd not opened]
- Faller 2002 [not opened; known only through quotations]

The new dig's Source ledger gives every locus.

**Not re-checked here.** Everything else in this file, including the Aymara figures (line 44), the Caral and pyramid framing (lines 5 and 11), and the schematic examples (lines 27–29).

**Downstream.** This claim was carried into script/morphemes.json and script/codepoints.md (U+E14F), grammars/evidentials/, the glyph notes and ORDO. What the language does about that is for the language owner to decide, not for this erratum.

**Pointer.** The cited dig is [evidentiality-clusivity-and-stance.md](evidentiality-clusivity-and-stance.md). It covers the paradigm variety by variety, the Weber and Faller positions, -chu in questions and negation, the non-experienced past, clusivity, and -puni/-má/-yá.

— appended 2026-11-10 by a Claude subagent in the language-2026-11-10 workflow

**Verification (2026-11-10).** A second Claude subagent re-opened every source cited in this erratum except Faller 2002 and Floyd 1999, which stay unopened. It corrected two points: Bendezú-Araujo's "not obligatory" is said of Conchucos Quechua, not of Quechuan generally (now cited with Bernárdez 2020: 32 for the general claim); and the erratum now reports, as the dig does, that Solá & Parker also give /ñuqačuč/ as rhetorical -ču, and that Faller and Dedenbach-Salazar class -chu with the evidentials in a broad, non-inferential sense. The corrected claim itself, that -chu is not the conjectural in any variety examined, stands. The text above line 95 is unchanged.
