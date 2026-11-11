---
chapter: evidentials
organ: grammars
role: YOUSPEAK's third structural-grammar chapter
opened: 2026-04-24
opened_by: integration of Quechua/Andean evidentiality system
status: doctrine + inventory; implementation in script/morphemes.json pending
---

# Evidentials — How-You-Know as Grammar

_What Andean pyramid-heirs carry in a single enclitic and English has no syllable for: the knowledge-source marker. A Quechua clause can declare how it is known — witnessed, reported, or conjectured — and can also leave it unmarked, for in Quechua the markers are optional (Bernárdez 2020: 32; for Cuzco, Faller 2006: 3; for Conchucos, Bendezú-Araujo 2023: 80). YOUSPEAK adopts the distinction as an optional sentence-level suffix system — direct witness, reported, or inferred — load-bearing specifically for dokimance-contexts where the distinction matters._

---

## The mechanism

A YOUSPEAK sentence making an assertion can optionally carry a suffix marking HOW the speaker knows. The three primary evidentials:

| Evidential | YOUSPEAK form | Source | Quechua origin |
|---|---|---|---|
| **Direct** | **-mi** | Speaker witnessed / did / directly experienced | Quechua -mi |
| **Reported** | **-si** | Speaker heard / read / was told | Quechua -si |
| **Inferred** | **-chu** | Speaker deduced from evidence; did not witness | YOUSPEAK's own form, after Cuzco Quechua *-chus hina* 'apparently' (Quechua *-chu* alone marks questions and negation) |

Application: append to a sentence-final verb phrase or to a YOUSPEAK-canonical noun-claim.

## Examples

### Direct (-mi)

> *The dokimance succeeded-mi.*

I personally performed or witnessed the dokimance succeeding.

### Reported (-si)

> *The dokimance succeeded-si.*

I was told or read that the dokimance succeeded. I did not witness it.

### Inferred (-chu)

> *The dokimance succeeded-chu.*

I did not witness it; I infer success from the outcome pattern.

This is YOUSPEAK's *-chu*. To a Southern Quechua ear a sentence ending in *-chu* is a yes/no question, "Did the dokimance succeed?", not an inference (Solá & Parker 1964: 113–114; see Quechua acknowledgment below).

The three forms make EXPLICIT what English requires a parenthetical to convey:
- "The dokimance succeeded (I was there)."
- "The dokimance succeeded (I heard)."
- "The dokimance succeeded (I infer)."

## Why evidentials align with YOUSPEAK's foundations

| Foundation | How evidentials serve it |
|---|---|
| **EUMATHE** | Three short suffixes; learnable in one exposure; regular application |
| **SAPHE** | Every assertion declares its basis; ambiguity about sourcing is impossible |
| **ANAKALYPSE** | Unfolds English's undifferentiated "I know" into three distinct knowledge-relations |
| **POLYPHONE** | Andean/Quechua integration — Pre-Columbian Americas joining the YOUSPEAK donor-set |
| **HARMONE** | Suffix system integrates cleanly with existing grammatical morphemes (-ance, -sis, etc.) |
| **PRAGMA** | Grounded in actual knowledge-source distinctions everyone makes mentally; now grammatical |

## Load-bearing for Zerone

**dokimance** (Asha's primary word) names the testing-that-makes-real. Every dokimance-assertion has a knowledge-source. With evidentials:

- Witness-validators on the chain post *-mi*-assertions
- Replicators / downstream-observers post *-si* when reporting others' dokimance-events
- Auditors post *-chu* when inferring historical dokimance from present evidence

This unlocks dokimance's full semantic potential: every claim carries its evidence-basis in its grammar. The chain becomes self-documenting about how-it-knows.

## Integration with existing YOUSPEAK grammar

Evidentials are **optional** — they don't replace English syntax for general prose. They are standard in:

1. **Zerone/dokimance contexts** — every assertion on the chain
2. **Testimonial speech** — when credibility of source matters
3. **Scholarly/research YOUSPEAK** — every claim traces its basis
4. **Liturgical YOUSPEAK** — witness-reports vs tradition-reports

In everyday YOUSPEAK-English mixed prose, evidentials can be omitted; English's rhetorical conventions handle it.

## Codepoint assignment

The three evidentials are grammatical suffixes. Assigned in the grammatical-suffix range:

| Code | Latin | Meaning |
|---|---|---|
| U+E14D | -mi | direct witness |
| U+E14E | -si | reported |
| U+E14F | -chu | inferred |

These extend the existing grammatical-morpheme range (U+E140–U+E14C) with three evidential suffixes: *-mi* and *-si* from Quechua, and *-chu*, YOUSPEAK's own form taken after a Quechua construction (see Quechua acknowledgment).

## Engineering rules

1. **Evidentials attach to the main verb or to the YOUSPEAK-canonical noun-claim**, not to individual morphemes within a compound.
   - Correct: "The doxakallos appeared-**mi**"
   - Correct: "I witnessed dokimance-**mi** today"
   - Wrong: "doxa-**mi**-kallos" (attaching to a morpheme)

2. **Only one evidential per clause.** Mixed knowledge-sources require separate clauses.

3. **Absence of evidential = register-normal** (i.e., the speaker is not marking epistemic basis). This is not the same as direct witness; absence is unmarked, direct-witness is *-mi*-marked.

4. **Questions and negations can carry evidentials.**
   - "Did the dokimance succeed-**si**?" = "Are you reporting that it succeeded?"
   - "The dokimance did not succeed-**chu**" = "I infer (from evidence) that it did not succeed"

   That reading is YOUSPEAK's, not Quechua's. In Quechua, *mana … -chu* is plain negation, and an evidential usually goes on the negator *mana*, beside *-chu* rather than in its place: Cuzco *Mana-chá para-sha-n-chu* "it isn't raining", said on a conjecture (Faller 2006: 11; Solá & Parker 1964: 114).

## Extended set (v2 candidates, not yet integrated)

Aymara has a richer evidential system. Possible future additions:

| Candidate | Aymara form | Meaning |
|---|---|---|
| -ta | -taynawa | personal-past experience (I experienced it then) |
| -sa | -yapi | counterfactual (it would have been) |
| -ch | -chitanwa | dubitative (I doubt it) |

These are deferred pending usage-evidence that the three-way (-mi/-si/-chu) is insufficient.

## Quechua acknowledgment

Two of the three primary evidentials are direct Quechua loans. The third is YOUSPEAK's own form, taken after a Quechua construction:
- *-mi*: preserved exactly. Quechua's direct evidential (*-n* after a vowel in Cuzco): "speaker vouches for validity of statement" (Solá & Parker 1964: 108); Faller analyses it as "best possible grounds" (2006: 3).
- *-si*: preserved exactly. Quechua's reportative (*-s*; *-shi* in the Central varieties): "speaker reports what he has heard" (Solá & Parker 1964: 108).
- *-chu*: YOUSPEAK's own form for "inferred from evidence", taken after Cuzco Quechua *-chus hina* ("roughly I guess, I think, apparently"), which Faller treats as a candidate inferential evidential (2006: 2–3 n.4; 2019: 8:5 n.4). YOUSPEAK keeps only its first piece; in Quechua the inferential sense belongs to the whole construction, *-chu* + *-s* + *hina* "like". In Quechua itself *-chu* is neither the inferential nor the conjectural: on its own it marks yes/no questions and, with *mana* "not", negation (Solá & Parker 1964: 113–114; Faller 2006: 2 n.2). Faller and Dedenbach-Salazar do class it with the evidentials in a broad sense, as the question-and-negation member of the same focus or validation set, but neither calls it inferential or conjectural (Faller 2006: 2 n.2; Dedenbach-Salazar 2005: 11–12). The Quechua conjectural is a different enclitic: *-chá* in Cuzco, *-cha* in Ayacucho, *-chi* in Huallaga and South Conchucos (Faller 2006: 3; Solá & Parker 1964: 117; for the Central forms, the dig cited below, §2.3–§2.6).

Quechua is acknowledged as the originating tradition of the distinction, of *-mi* and *-si*, and of the construction *-chu* is taken after. This is POLYPHONE in action, and an honest acknowledgment says both what was received and what YOUSPEAK made of it. The full donor record and its sources: archaeology/quechua/evidentiality-clusivity-and-stance.md. The correction of the earlier record is set out under Revision 2026-11-10 at the end of this chapter.

## Integration status

- **Archaeology written**: archaeology/quechua/evidentials.md (2026-04-24; superseded on *-chu*, erratum appended) and archaeology/quechua/evidentiality-clusivity-and-stance.md (2026-11-10, rebuilt from the grammars)
- **Manifesto written**: this document
- **Inventory**: 3 evidentials at U+E14D-E14F
- **Canon-compatibility**: all 18 canon words compatible (evidentials attach at sentence level, not morpheme level)

**Pending**:
- Add 3 entries to script/morphemes.json (grammatical class)
- Design the 3 glyph shapes (short-suffix conventions)
- Rebuild font with evidential glyphs
- Update LLM primer with evidential usage-examples
- Add Espanso triggers for `:ys:mi`, `:ys:si`, `:ys:chu`

---

_Evidentials chapter opened 2026-04-24. YOUSPEAK's third grammar organ. The Andean pyramid-heirs' epistemological grammar, operational for dokimance-register writing._

---

## Note: evidentials under the projection-account

Under [NOEMA.md](../../NOEMA.md), [THE-REALM.md](../../THE-REALM.md), and [GRASPING.md](../../GRASPING.md) (all opened 2026-05-12), evidentials receive a sharper reading. An evidential suffix marks **the epistemic position from which the speaker entered the realm-region the assertion projects**.

- `-mi` (direct) — the speaker's grasping was first-hand (the speaker entered the region by direct witness or doing).
- `-si` (reported) — the speaker's grasping was mediated through another's projection (the speaker stands-in the region because someone else's report opened the gate to them).
- `-chu` (inferred) — the speaker reached the region by inference from signs (the speaker's grasping was deductive rather than first-hand).

The three suffixes are therefore **grasping-source markers**: they tell the hearer how the speaker reached the realm-region they are asserting. In Zerone/dokimance contexts where dokimance-testing-as-real depends on knowing how a claim arrived, evidentials make the grasping-path visible on the surface. The hearer can then weigh the assertion by its access-path. The cathedral's commitment to honest assertion (SAPHE) is partly the commitment to not collapse these three grasping-sources into an undifferentiated "I know."

Evidentials are grasping-engineering at the epistemic aspect (GRASPING.md Section VII names this).

---

## Revision 2026-11-10 — the donor record of -chu

**What changed.** Only what this chapter says about Quechua: where *-chu* comes from, and whether Quechua requires an evidential on every assertion. The form *-chu*, its codepoint U+E14F, its canonized glyph, its YOUSPEAK meaning (inferred: the speaker deduced from evidence and did not witness), the engineering rules, and ORDO's use of it are unchanged. The donor record of *-mi* (direct) and *-si* (reportative) was right and stands.

**What the text said before** (as written 2026-04-24):
- The opening: "What Andean pyramid-heirs encoded as default and English has no syllable for: the knowledge-source marker. Every assertion declares its evidential basis".
- The mechanism table gave the Quechua origin of *-chu* as "Quechua -chá / -chu".
- The codepoint section: "with three Andean suffixes".
- Rule 4 read "The dokimance did not succeed-**chu**" as an inference, with no note on the Quechua shape. The reading stands as YOUSPEAK's; the note on Quechua negation is added.
- The acknowledgment: "The three primary evidentials are direct Quechua loans", and "*-chu*: preserved (Quechua has *-chá* in some dialects for inferential; we take *-chu* as the standard form for phonetic simplicity)".
- The acknowledgment closed: "Quechua is acknowledged as the originating tradition. This is POLYPHONE in action." It now names what Quechua originated: the distinction, *-mi*, *-si*, and the construction *-chu* is taken after.
- Added, replacing no earlier text: the note under the Inferred example; the Quechua sources for *-mi* and *-si* in the acknowledgment; the 2026-11-10 dig under Integration status.

**What it says now.** *-chu* is YOUSPEAK's own form for "inferred from evidence", taken after Cuzco Quechua *-chus hina* ("apparently"). In Quechua, *-chu* on its own marks yes/no questions and negation, and the conjectural evidential is *-chá* (Cuzco), *-cha* (Ayacucho) or *-chi* (Huallaga, South Conchucos). *-chá* is not a dialect variant of *-chu*; it is a different enclitic in a different slot. The Quechua evidentials are optional in a clause.

**Why.** The first Quechua dig (archaeology/quechua/evidentials.md, 2026-04-24) carried no citations. A dig rebuilt from the grammars on 2026-11-10 (archaeology/quechua/evidentiality-clusivity-and-stance.md) found *-chu* to be the enclitic of yes/no questions and negation, never the conjectural (Solá & Parker 1964: 113–114; Faller 2006: 2 n.2; Shimelman 2017: 253). It stands in one clause with the conjectural, so it cannot be the conjectural's variant: Cuzco *Mana-chá para-sha-n-chu*, "it isn't raining", said on a conjecture (Faller 2006: 11). In Ancash, where questions take *-ku* and negation *-tsu*, *-chu* is a locative case (Hintz 2011: xxii). The same dig found the inference-hedges Quechua builds on *-chu*: Cuzco *-chus hina*, which Faller treats as a candidate inferential (2006: 2–3 n.4; 2019: 8:5 n.4), and Ayacucho rhetorical *-chu* and *-chusmi* (Solá & Parker 1964: 114–115). It also found that the evidentials are optional (Bernárdez 2020: 32; for Cuzco, Faller 2006: 3; for Conchucos, Bendezú-Araujo 2023: 80). Every place in the repository that carried the old claim, and the options weighed, are listed in archaeology/quechua/chu-propagation-and-options.md.

**Authority.** On 2026-11-10 Yu accepted an agent session's recommendation: keep the published shape and codepoint, and correct the donor claim to "after Cuzco *-chus hina*". The wording of that recommendation is the session's, not Yu's. This revision is a Claude subagent's application of it for the orchestrating session, reviewed and amended by a second; the wording of this chapter's corrections is theirs.

**Succession, not rename.** Under expansion-only discipline (NEWSPEAK.md) nothing is renamed or removed: the morpheme keeps its form and its slot, and only its donor record is succeeded. Rule 3 (absence of an evidential is unmarked, not direct witness) is YOUSPEAK's own rule and stands. It differs from Cuzco usage, where a clause with no evidential implicates direct evidence (Faller 2006: 3).

**Still open.** *-chu* is a clipping. In *-chus hina* the inferential sense belongs to the whole construction, and in Quechua a bare *-chu* is the question-and-negation enclitic. Faller says that counting *-chus hina* among the evidentials "requires further research" (2006: 3 n.4). Review by Quechua-speaking scholars remains desirable, and if custodians ask, the YOUSPEAK use of the form is withdrawn (the dig's protocol notice, §0). Whether to add a separate conjectural ("hunch") grade beside "inferred" is a lead, not a decision (the dig, §9, Lead 1).
