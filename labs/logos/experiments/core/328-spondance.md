---
id: 328
candidate: spondance
target: wire-task-accept (forge_targets.json; KS-002 THE WIRE, Appendix A.1, task.accept)
gap: >
  The spoken act by which someone who has heard an offer of work answers it so that the answer itself binds them. The hearing ends as a pledge, given freely where a no was open; from then on the work is theirs to answer for.
donors: [Latin:spondeō (spondēre), Latin:-antia (via English -ance)]
pronunciation: "/ˈspɒn.dəns/ (SPON-dance; 2 syllables; Latin spondeo + Latin -ance)"
sibling: 329-rangance (wire-task-decline), forged as one pair
axes:
  gap_validity: 7.5
  learnability: 7
  clarity_yield: 7
  semantic_coverage: 7.5
  polyphone_balance: 3
  groundedness: 8.5
weighted_v2: 6.8
axes_forger:
  gap_validity: 8
  learnability: 7.5
  clarity_yield: 8
  semantic_coverage: 7.5
  polyphone_balance: 3
  groundedness: 8.5
weighted_v2_forger: 7.15
verdict: refine
scored_by: "independent assessor (a Claude subagent that did not see the forger's scores); its scoring is the stricter and stands (experiment 035). The forger's self-score is recorded beside it."
scored_on: 2026-11-11
panel: "EUMATHE pass · HARMONE pass · PRAGMA pass — 3 of 3. Canonization requires weighted >= 7.50 AND 2-of-3 lenses (forge-protocol-extended.md Step 8). The lenses pass; the weighted total (6.80 stricter, 7.15 self-scored) does not. Both conditions are required."
invocation: "Yu, 2026-11-10: Lets go for what you recommended sensible actions for the above decision."
invocation_note: "The session read Yu's sentence as taking up its suggestion to forge this gap. The gap was the session's suggestion; every lemma is an agent's proposal."
format: full-trace — a refine whose reasoning must survive for the next instance (Step 9)
---

# 328 — spondance

_The accept half of the wire's first forged pair, walked to the end of the protocol and declined on the number. All three lenses passed it. The score did not: a Latin stem with a Latin suffix takes polyphone 3, and no other axis can make up the 0.70 it is short._

## The invocation

On 2026-11-10 the session suggested, as the first forge, "binding acceptance" (the queued target `wire-task-accept`: hearing that completes itself in pledged uptake) together with its sibling, "refusal that keeps the bond" (the queued target `wire-task-decline`: sovereign refusal without rupture). The suggestion was the fifth of six open decisions the session put to Yu, the language's owner; it said that no forge had started and that the repository's rule is that Yu names the gap. Yu answered the list in one message:

> "Yumi is the relationship term. You and me, A framework to communicate. Lets go for what you recommended sensible actions for the above decision"

The session read the last sentence as taking up each of its recommendations, this forge among them, and treats it as the invocation (forge-protocol-extended.md §VI, the FATE-clause). That is the session's reading of Yu's words. The gap was the session's suggestion; Yu did not word it and chose no word. Every lemma in this file, including the one carried to the panel, is an agent's proposal. The verdict is refine: neither word entered canon, and this record keeps the reasoning, not a word.

## How the forge was run

- **Three forgers**, each a separate Claude subagent, worked three frames for the pair: *one-exchange* (both words from one tradition's question-and-answer rite), *two-families* (each word welds a Hebrew act-root to a root from an unrelated family), and *said-aloud* (each word at most three syllables, built only from live, recognisable morphemes). Each walked Steps 1–7 and scored its own pair.
- **One independent assessor** scored all six words without seeing the forgers' scores, checked their claims, and chose the pair to carry. It chose *said-aloud*: **spondance** (accept) and **rangance** (decline, experiment 329).
- **Three lenses** (EUMATHE, HARMONE, PRAGMA), each a separate subagent, argued against the carried pair (Step 8).
- **This file** was written by a fourth role, the recorder, who does not improve the words, raise a score or soften an objection. Where the record quotes a forger, the assessor or a lens, it says so; where the recorder checked something itself, it says that too.

## The walk — twelve steps, as they fell

| Step | What was done | What was not done, or went wrong |
|---|---|---|
| 1 Survey | `pipeline/forge_priority.py` (read-only) placed wire-task-accept #91 and wire-task-decline #94 of 95 queued targets (two-families forger; reproduced by the assessor). forge_targets.json:4291 and :4308 showed both `queued`, `experiment: null`, `convergence_witnesses: []`. The said-aloud forger used only `discover.py --list` (read-only) and grep, and found no archaeology for the region beyond the eight digs named in the brief. | The target was **not** marked `in-forge`: the forgers' briefs did not allow writes to W (the forge's working tree of this repository, on the branch that carries this file). **Process error, disclosed by the one-exchange forger:** it ran `pipeline/discover.py <concept>` for "acceptance" and "refusal" without first checking whether it writes. It does: it wrote two untracked stubs, `labs/logos/forge/acceptance-gap.md` and `refusal-gap.md`, which that forger moved to the macOS Trash minutes later, returning W to its starting state. The run matched 0 of 242 files, because none of the digs carries the `semantic_field` key that discover.py indexes (the recorder confirmed: none of the eight files has the key). |
| 2 Gap evidence | All three forms: convergence (four families attest a binding answer), circumlocution (a rite reached for the word; radio procedure coined one), near-neighbour elimination (canon and English). Below. | The WILCO and ICAO evidence is from a secondary source (Wikipedia), marked so by the forger. |
| 3 Collision | Element-level scan over canon/ (267 files) and the Step-3 wider set (299 files) by the forger's `collide_mouth.py`; reproduced independently by the assessor, EUMATHE and HARMONE. | The forger's scan missed the element `onda` (the stem of the Core headword ondame) and the sphotame onset; EUMATHE found both, HARMONE found ondame. |
| 4 Archaeology | Donor files open and second-read: archaeology/latin/suscipere.md, archaeology/hebrew/naaseh-venishma.md, archaeology/hebrew/uptake-convergence-notes.md, each with a `## Verification (2026-11-10)` section. | Read during the forge in fetched copies but **not in any archaeology file when the forge ran** (since added by the 2026-11-11 erratum in suscipere.md, after this record): Gaius 3.102, 3.105, 3.115–119; RB 29; the Plautine betrothal scenes as PRAGMA read them (suscipere.md names Trin., Aul. and Curc. only as Lewis & Short quotes them, "Plautus not opened"). The Digest and Livy 9 remain known only as Lewis & Short quotes them. |
| 5 Lemma alternatives | Seven forms rejected with reasons; two whole candidate pairs from the other frames recorded below. | No forger reports running `pipeline/forge.py`. |
| 6 Family | `-ance`, in its act sense; all five questions answered. | The act sense of `-ance` outside the worship-action tier is a doctrine choice for Yu, not settled here. |
| 7 Scoring | Forger 7.15; assessor 6.80. The stricter stands: **6.80**. | — |
| 8 Panel | EUMATHE pass, HARMONE pass, PRAGMA pass: 3 of 3. | — |
| 9 Experiment file | This file. | — |
| 10 Canon entry | Not written: the verdict is refine. | — |
| 11 Nuance check | Not applicable without a canon entry. `pipeline/nuance_check.py --suggest latin` returns Group A (verecundia + sinceritas) (assessor; re-run by the recorder). | — |
| 12 Interlinks | forge_targets.json `wire-task-accept` moved to `refining` with this experiment; the `qabalance` petition in labs/logos/petitions.json, whose standing target this is, has the outcome added to its note. labs/logos/forge/qabalance-gap.md:8–9 reads "status queued" and says "The target's status is Yu's to move"; the move to refining made here under Step 12 therefore stands only if Yu merges this record, and a dated note added at the end of that file by the orchestrating session says so. | No canon word entered, so no index, canon.md, convergence file, morphemes.json or _sidebar.md change is owed. dashboard.md's count of forge experiments was stale by these two files; the orchestrating session ran Step 12's `derive_indices.py --dashboard` after this record, which changed that one row (292 to 294) and nothing else. No liturgy session file was written by the recorder. |

## The Gap

The spoken act by which someone who has heard an offer of work answers it so that the answer itself binds them. The hearing ends as a pledge, given freely where a no was open; from then on the work is theirs to answer for.

## Gap evidence (Step 2)

The forger's evidence (its wording; the bold labels are the recorder's):

1. **The slot is filed.** KS-002 marks `task.accept` as "GAP — proposed forge-target" (KS-002-wire.md:371; Appendix A.1, :423). It says that until the word is forged, "acceptance is implicit in the JetStream ack … This is honest but mute" (:277). ORDO borrows shemme for reception with the declared caveat that "the act-word is a standing wire GAP" (ordo/SPEC.md:59), and lists the five wire GAPs as remaining commissions (:161).
2. **Circumlocution.** A rite reaches for a word that does not exist: "Let reply be qabalance" (ordo/rites/petition.rite:12), logged in labs/logos/petitions.json and labs/logos/forge/qabalance-gap.md. Everyday English says it only in phrases: "I'm on it", "leave it with me", "consider it done" [usage from memory].
3. **Convergence.** The binding answer to an offer (shape 3 in archaeology/hebrew/uptake-convergence-notes.md §1) is attested in four families independent by descent (§2–3): Semitic (Ex 24:7, which Onkelos renders *naʿbēd u-nqabbēl*; Est 9:27 *qibbēl ʿal*), Indo-European (Gaius 3.92 DARI SPONDES? SPONDEO; Sanskrit *pratijñā*; Greek *homologeō*), Sinitic (諾, 應承) and Japonic (承る). If Sinitic–Japonic written contact is discounted, the count is three plus one.
4. **A profession had to coin a word for it.** Radio procedure's WILCO is "I have Received your signal, understand it, and will comply", and "since the meaning of ROGER is included in that of WILCO, the two prowords are never used together" (ACP 125(F), as quoted at en.wikipedia.org/wiki/Procedure_word, opened 2026-11-10; the primary was not opened). That is hearing completed in uptake, lexicalised. It also names compliance with an instruction, whereas KS-002 says "A task offer is not a command".

**Checked by the assessor:** KS-002 lines 277, 371 and 423; ordo/SPEC.md lines 59 and 161; forge_targets.json lines 4291 and 4308. **Re-read by the recorder** (read-only, 2026-11-11), because PRAGMA could not locate the file: specs/KS-002-wire.md in the kingdom-standards repository, lines 277, 365, 371, 372, 415, 423 and 425 read as the forgers and the assessor quote them.

**Against the gap**, from the forger and the assessor: English "accept (an offer)" and "take on" already cover much of the region, and WILCO lexicalises a close neighbour in procedural speech. What remains unnamed is narrower: an answer to a declinable offer, in general speech, that binds the one who gives it.

## Witnesses (Pattern 1 — convergence)

From archaeology/hebrew/uptake-convergence-notes.md §2–3, counted there, not scored:

| Family | Witness | Locus | Independence |
|---|---|---|---|
| Semitic | *naʿăśeh wə-nišmāʿ*; Onkelos *naʿbēd u-nqabbēl*; *qibbēl … ʿal* | Ex 24:7; Onkelos Ex 24:7, Dt 5:24; Est 9:23, 27 (naaseh-venishma.md §1, §3.1, §3.5) | the anchor |
| Indo-European | *Spondēsne? — Spondeō*; *pratijñā*; *homologeō* | Gaius 3.92–93; MW s.v. pratijñā; LSJ s.v. ὁμολογέω (suscipere.md §3) | Roman stipulatio independent of Semitic |
| Sinitic | 諾 *nuò* (the yes that binds; Shiji 100, Ji Bu's one 諾); 應承 | Kangxi s.v. 諾; Wiktionary 應承 | independent |
| Japonic | 承る *uketamawaru*, NKD sense 3 | kotobank 承る | independent by descent; heavy written contact with Sinitic |

The decisive Latin witness, for this lemma, is Gaius 3.92: the obligation is made "by question and answer", and the one who will be bound speaks second, repeating the verb of the question. Dig. 45.1.1, as Lewis & Short quotes it: *stipulatio non potest confici, nisi utroque loquente*.

## Circumlocution evidence (Pattern 2)

- ordo/rites/petition.rite:12, "Let reply be qabalance.", and the rite's own comment: "This rite reaches for a word the canon does not have: the volitional act of ACCEPTING what is offered". Filed as usage evidence for this target in labs/logos/petitions.json (`standing_target: wire-task-accept`) and labs/logos/forge/qabalance-gap.md.
- KS-002 itself, at :277: until the word exists, acceptance is "implicit in the JetStream ack". The wire speaks the act only as a transport detail.
- Radio procedure's WILCO (above): a working profession coined a word for hearing completed in uptake, though for compliance with an instruction rather than the taking-up of an offer.

## Collisions found (Step 3 — recorded, never silently absorbed)

**The forger's scan** (element-level substring search, case-folded, diacritics stripped, over canon/ — 267 files, headword stems plus `word:`/`candidate:` fields and bodies — and the wider set labs/logos/experiments, dictionary, DICTIONARY.md, canon.md, script/morphemes.json — 299 files):

- `spondance`: 0 headwords, 0 canon bodies, 0 wider-set files.
- `spond`: 0 headwords; 33 canon bodies, 43 wider. Every hit is English: responds 10, correspondence 8, corresponds 5, respond 4, responding 4, responded 3, corresponding 2, despondency 1 (nepsisme), responder 1 (paqduqing, "recipient-and-responder").
- `spon`: 0 headwords; 92 bodies, 120 wider. Mostly "response" (58); also spontaneous 3.
- `pond`: 0 headwords (ponome contains "pon", not "pond"); 33 bodies.
- `sponde`: 13 bodies, including despondency (nepsisme) and phase-correspondence (tinaime).
- `spons`: 72 bodies, including responsibility (kittume, visageqing).
- `dance`: 22 bodies: dance 15, dancers 4, guidance 2, avoidance 2, epanodance 1, attendance 1, accordance 1, abundance 1. The dance register is live in katsintawime, lilame, liturgiame, hastame and rasame.
- `ondan` 0; `ndance` 2 (attendance in kimance, abundance in yvymarame); `spondee` 0; `despond` 1 (nepsisme).
- `ndence`: 1 headword, candence (a -ndence tail rhyme); 24 bodies.
- **Phonetic collision, in canon, recorded and scored in learnability:** spandaqing /ˈspʌn.dʌ.tɕʰiŋ/ (SPUN-duh-ching), a Core headword linked from 11 canon files. It and spondance /ˈspɒn.dəns/ differ by one vowel over their first two syllables.
- Outside the canon: the -spondence tail of correspondence and despondence; medical spondyl- [from memory]; English "spondee"; initial sp- needs an added vowel in Spanish, Arabic, Persian and Japanese.
- Register: the English handle "respond" points to "answer", the right neighbourhood but not "pledge".

**Added by the panel** (the forger's scan did not catch these):

- **ondame** (EUMATHE, HARMONE): `onda` is the stem of the Core headword ondame /ˈɔn.dɑː.meɪ/. The forger searched `ondan` and `pond` but not `onda`, `ond` or `nda`. HARMONE judges the overlap to be in spelling only.
- **sphotame** (EUMATHE): /ˈspoʊ.tə.meɪ/, on the same hearing-to-answer arc as shemme and this word. With spandaqing, three sp-vowel-dental words to keep apart.
- **spandaqing is a live citizen's name** (HARMONE): agent.json in the cambridgetcg/citizen-spandaqing repository, outside W; its task subject on the wire is `kingdom.citizen.spandaqing.task`, so "spandaqing: spondance" is a real utterance there.
- **Spelling and sound** (EUMATHE): the respelling "SPON-dance" spells "dance", and the repo's one earlier -dance coinage, epanodance, wrote /dæns/ (labs/logos/experiments/core/247-epanodance.md:81). The system word list (/usr/share/dict/words) has 15 forms in -spondenc- (EUMATHE's paragraph says 16) and none in -spondance, so a hearer will write "spondence".

**No collision at canon-headword level** for the lemma or any element (forger, assessor, EUMATHE and HARMONE all reproduce this).

## Near-neighbours (Pattern 3 — why each existing word fails)

| Word | Covers | Fails on |
|---|---|---|
| `shemme` (Core, 7.65) — the nearest | receptive hearing as a state that "arrives or it doesn't", pre-volitional | spondance is the volitional answer that turns that hearing into a bond |
| `qorvance` (worship-action; the wire's task.offer class) | the offerer drawing near through what is brought | spondance is the receiver's answer to it |
| `yadahance` (the wire's return class) | acknowledges at the end what was done or failed | spondance opens the loop that yadahance closes |
| `sabrme` (Core) | patient self-binding kept up under pressure after a course is taken | spondance is the single moment of binding, in answer to another |
| `britqing` (Core) | the standing, felt covenant bond | spondance is one act that can begin a bond; it is not the bond (HARMONE's objection to this line is below) |
| `paqduqing` (Core) | mutual custodial care between Creator and created | a relation, not the act of taking on one piece of work |
| WILCO (English radio procedure) | received, understood, will comply; said only by the addressee of an instruction | spondance answers an offer that could have been declined |
| English accept, obey, promise, undertake, consent (naaseh-venishma.md §5) | — | in turn: acceptance without the answer, compliance without freedom, a pledge without having heard anything, bureaucratic, and permission for another's act |

HARMONE adds three canon relations the forger did not resolve: **britqing** (its entry says the Sinai covenant "is not contract", while spondance takes its only morpheme from the model Roman verbal contract), **visageqing** (responsibility "before any deliberation", against the forger's "responsibility starts in a response") and **xeniame** (spondeo was the formula a non-citizen could not speak). See the HARMONE paragraph.

## Donors and archaeology (Step 4)

1. **spond-** (the only morpheme of meaning). Latin *spondeō, spondēre, spopondī, spōnsum* [ˈspɔndɛ.oː]: "promise solemnly, bind or pledge oneself; in contract law the answer spondeo to spondes?; become surety; betroth" (L&S s.v. spondeo, verified).
   - DARI SPONDES? SPONDEO: the party who will be bound speaks second, repeating the question's verb (Gaius *Inst.* 3.92).
   - Reserved to Roman citizens, and "cannot even be properly translated into Greek, although it is said to be formed from a Greek word" (3.93).
   - *stipulatio non potest confici, nisi utroque loquente* (Dig. 45.1.1, via L&S).
   - Betrothal: *Spondēsne? Spondeō* (Plautus, via L&S; the plays were read by PRAGMA, see its paragraph).
   - The Caudine sponsio, repudiated by the people (Livy 9, via L&S).
   - Etymology: "akin with σπένδω, to pour out [a libation]; cf. σπονδαί, league" (L&S).
   - **Archaeology loci:** archaeology/latin/suscipere.md §1 (property 4), §2 table (rows spondeō, Spondēsne, spōnsiō, spōnsus/spōnsa), §3 (Gaius 3.92–94, the Digest definitions, the Caudine Forks), §4, §8 Lead L2, §9; archaeology/hebrew/uptake-convergence-notes.md §2.2 (the Spondēsne row: "shape 3, exact … independent of Semitic"), §3, §5 Lead A2, §6.
2. **The English handle** (evidence for the mouth, not donor evidence): respond < Latin *respondeō* < *re-* + *spondeō* "promise"; responsible < *responsus* < *respondeō* (both verified 2026-11-10 at en.wiktionary.org, a secondary source). Sponsor and spouse as descendants: from memory, not re-checked.
3. **-ance**: Latin *-antia* via English; the formalized family (script/suffix_families.json; dictionary/index-by-suffix.md), sounded /əns/ per script/phonology.md, "For future forges".
4. **Witnesses only, no morpheme in the word:** Ex 24:7 with Onkelos *nəqabbēl* (naaseh-venishma.md §1, §3.1); m. Berakhot 2:2 (§3.4); 承る (uptake-convergence-notes.md §2.3); 諾, 應承 (§2.4); RB 58 *promissio* (suscipere.md §3).
5. **Protocol.** The donor strand, Roman law, is a closed corpus with no custodians. Said aloud rather than stripped: the pledge once had a libation under it, and its binding force was a citizen's privilege. The living liturgical and scriptural witnesses are not reduced to a suffix: the Benedictine and Ignatian *Suscipe*, the Rabbinic *naʿăśeh wə-nišmāʿ* and *qabbālat ʿōl*, and the Qur'anic *samiʿnā wa-aṭaʿnā*. The s-m-ʿ pair and its polemical twin (Q 2:93, 4:46; uptake-convergence-notes.md §5) are not used. Breadth is honestly low: one Latin stem plus a Latin suffix.

**Archaeology debts found in this forge** (for the files' owners, not fixed by this forge; errata dated 2026-11-11, appended to suscipere.md and uptake-convergence-notes.md after this record, take up both):
- Gaius 3.102 (a non-matching answer leaves the stipulation void), 3.105 (each party "must hear", *exaudire debet*), 3.115–117 (the *sponsor* as surety for another's debt) and RB 29 (*spondeat … recipiatur*) were read in fetched copies but are not in archaeology/latin/suscipere.md.
- The assessor found that suscipere.md §9 ("not binding per L&S") and uptake-convergence-notes.md §5 Lead A3 ("voluntary, not binding") overread Lewis & Short, which distinguishes voluntary (*suscipio*) from obligated (*recipio*) undertaking and does not say that the voluntary one fails to bind.

## Lemma alternatives (Step 5 — rejections recorded)

| | Lemma | Reason (the said-aloud forger's, condensed; words in quotation marks are verbatim) |
|---|---|---|
| **carried** | `spondance` /ˈspɒn.dəns/ | the free answer that binds once given; two syllables; an English handle in "respond" |
| rejected | `kablance` /ˈkɑːb.ləns/ (q-b-l + -ance) | The tradition's own act-word and the best semantic fit: the Targum renders "we will hear" as "we will accept", and Semitic plus Latin gives two families (polyphone about 7, semantic coverage about 8). Rejected on the mouth: the English ear hears Kabbalah (in 17 canon files; the forger wrote 24, which is the count for the string `kab`) and Kabul; Arabic *qabl* means "before"; Rabbinic Qal *qābal* means "complain"; the canon reads q as /tɕʰ/ in -qing; both living traditions guard q-b-l formulas; it would be another Hebrew-stem -ance (the forger wrote "the seventh"; the assessor counted eight already, so "the ninth"); and it near-rhymes with palance. **Honest note recorded by the forger:** "with learnability 6.0–6.5 it would land at about 7.45–7.55, likely above spondance. The frame trades it away; that is recorded, not hidden." |
| rejected | `suscipance` | L&S and Cicero (Verr. 2.2.1) make suscipere the voluntary uptake (the forger wrote "that does not bind"; the assessor found that an overreading, see below). English hears "susceptible" first. The liturgical *Suscipe* is the offerer's plea, qorvance's side. |
| rejected | `recipance` | binding acceptance of what is entrusted, but no hearing in it and a prior duty assumed (*fidei commissum*), where a wire offer can be declined; English "recipient" sounds passive |
| rejected | `sponsance` | heard as "response", and names the pledged result rather than the act |
| rejected | `spondeo` (unsuffixed) | a loan, not a coinage (the SAPHE relabelling fault); leaves the wire's -ance cluster |
| rejected | `yingance` / `chengance` / a 諾 form | "ying" is the common misspelling of "yin"; *cheng* collides with the planned chengme (canon/core/ihsanme.md:69; INTENTION.md:173); 諾 *nuò* sounds like "no", fatal for an accept |
| rejected | `ukeance` | in English martial-arts usage the *uke* is the partner who receives the technique, and in fandom slang the passive partner: a register collision for a volitional act |

### The two other candidate pairs, and why they were not carried

**one-exchange — `suscipance` / `excusance`** (Latin stems after RB 58's *aut excusare aut suscipere*).
- suscipance: forger 6.03 (gap 7.0, learn 5.5, clarity 6.5, sem 6.0, poly 3.0, grnd 8.0); assessor 6.30 (gap 7.5, learn 6.0, clarity 6.0, sem 6.5, poly 3, grnd 8.5); assessor's panel estimate EUMATHE fail, HARMONE fail, PRAGMA pass (1 of 3).
- The forger's own finding: the frame holds for the accept word and fails for the decline word; read to its end, RB 58 holds the equality in right but not in rite (the yes is promised, written, laid on the altar and sung; the no has no words, and "si vero non potes, liber discede" is said to the novice, not by him).
- Assessor's reason for not carrying it: weakest pair (average 6.00); suscipere does not carry "the answer itself binds" (suscipere.md §1 property 4 puts the binding answer in spondere/stipulatio); the *Suscipe* register belongs to qorvance.

**two-families — `qabbelspond` / `miunci`** (Hebrew act-root welded to a second family's root).
- qabbelspond: forger 6.85 (gap 7.0, learn 5.5, clarity 7.0, sem 7.0, poly 7.0, grnd 8.0); assessor **7.02** (exact 7.025, rounded down; gap 7.5, learn 5.5, clarity 6.5, sem 7.5, poly 7, grnd 8.5); assessor's panel estimate 2 of 3 (EUMATHE fail; HARMONE pass with objection; PRAGMA pass).
- **qabbelspond is the highest-scoring accept of the three candidates**, above spondance (6.80). The assessor records that it "holds the strongest accept semantics".
- Assessor's reason for carrying the said-aloud pair instead: the two best words (qabbelspond, rangance) come from different candidates and do not read as a pair, so a whole pair was taken. Pair averages: two-families 6.775, said-aloud 6.74, one-exchange 6.00. Two-families was ahead by 0.04, but the assessor judged that fit with the language, HARMONE's criterion, favoured said-aloud: spondance and rangance are one construction and slot into the wire's -ance class words; the two-families pair shares no visible element, its decline (miunci) is the hardest word of the six to learn (4.5), and its Hebrew head contradicts its own gap clause. That was the assessor's estimate before the lenses ran. The HARMONE lens later found the pair mismatched: "Spondance's donor is a word one says; rangance's is a word others use to praise what one did" (329-rangance.md).
- The assessor's recommendation, recorded: carry the said-aloud pair forward "as a slightly lower-scoring pair that coheres", and record that qabbelspond's semantics support "the candidate's own refinement path 1, which is to bring q-b-l into the accept, ideally in a shape that keeps the -ance sibling form."

**Claims the assessor checked and found false**, across the accept words:
- spondance's forger: "suscipere is, for L&S and for Cicero (Verr. 2.2.1), the voluntary uptake that does not bind." L&S distinguishes voluntary from obligated undertaking; it does not say the undertaking fails to bind (Cicero's *suscepi causam* commits him; RB 58's *suscipere* leads straight into a binding promise). The overreading was inherited from suscipere.md §9 and uptake-convergence-notes.md A3.
- spondance's forger: "kablance … would be the seventh Hebrew-stem -ance." The canon already has eight (qorvance, yadahance, teshuvance, kipporance, palance, qinance, hallance, kunance); it would be the ninth.
- suscipance and qabbelspond: none found.

## Family assignment (Step 6)

The forger's answers, as given:
- **-me** fails. The binding is made by the speaker's own answer, not received; the received state that comes before it is shemme.
- **-qing** fails. The word names the act, not the bond the act creates; britqing holds the covenant bond.
- **-kin** and **-basis** plainly fail.
- **-ance** fits only in its act sense. dictionary/index-by-suffix.md defines -ance as "perceptible quality", and its decision tree has no branch for an act. But 8 of its 16 members are named acts (the worship-action tier), and the wire's own class words are -ance acts: qorvance for task.offer, yadahance for task.complete and task.fail, teshuvance for halt.ack.
- **Tier proposed: Core**, since this is a daily, non-liturgical act. "That stretches Core -ance from 'stance' to 'act', which is a doctrine choice."

**Recorder's check of the two texts this turns on:** dictionary/index-by-suffix.md:284 ("*-ance* names the *perceptible quality* — what you can notice") and :370 (the decision tree's only -ance branch is "a perceptible quality / state you can notice?"); canon/worship-action/README.md:14 ("Core Canon words name states, qualities, and ontological conditions"). Both read as the forger and HARMONE report.

**Register** (NUANCE-NATURE §II), the forger's: Group B, Respect-and-Bold-Speech (the yes said plainly to the asker; Shiji 100's one 諾 from Ji Bu), with Group A, Modesty-and-Truth (Sforno's "so that they would know what they were accepting"). `nuance_check.py --suggest latin` gives Group A (verecundia + sinceritas) for the donor tongue.

## Honest assessment (six-axis v2) — Step 7

| Axis | Weight | Forger (self) | Assessor (blind) | Stricter |
|---|---|---|---|---|
| gap_validity | 0.20 | 8.0 | 7.5 | 7.5 |
| learnability | 0.20 | 7.5 | 7.0 | 7.0 |
| clarity_yield | 0.15 | 8.0 | 7.0 | 7.0 |
| semantic_coverage | 0.15 | 7.5 | 7.5 | 7.5 |
| polyphone_balance | 0.15 | 3.0 | 3.0 | 3.0 |
| groundedness | 0.15 | 8.5 | 8.5 | 8.5 |
| **weighted** | | **7.15** | **6.80** | **6.80 — stands** |

The assessor's scoring is stricter on every axis where the two differ, so the axis-by-axis minimum and the assessor's total coincide at **6.80**. The lenses' axis readings do not lower it further: EUMATHE scores learnability 7.0 ("That matches the assessor"), PRAGMA holds groundedness 8.5. `pipeline/assess.py` on the forger's scratch copy gave 7.15; on this file (which carries the standing axes) it gives 6.8, verdict refine (its mechanical counter reads 3 syllables from the spelling; the IPA has 2). assess.py knows only the number; the panel's 3 of 3 is recorded here, not by the tool.

**Weak axis:** polyphone_balance 3.0, by both scorers. The total is not in the 7.50–7.99 band, so no threshold sentence is owed; the weak axis is named anyway. On the stricter scoring the word is 0.70 short; reaching 7.50 on that axis alone would need polyphone 7.67, which a Latin-only word cannot honestly have (CANON-AUDIT band "3-4: single donor-tradition with one auxiliary"; precedents candence 3, veriseem 3, dokimance 4).

### The forger's per-axis reasoning (verbatim)

> gap_validity 8.0. The act is unnamed in canon (shemme is a state, and KS-002 marks the slot GAP), and four families attest a binding answer to an offer. Not 8.5, because radio procedure already lexicalises hear-understand-comply as WILCO, so what remains unnamed is narrower: an answer to a declinable offer, in general rather than procedural speech.
>
> learnability 7.5. Two syllables, plain ASCII, initial stress, and a real English handle (respond < respondeō < re- + spondeō 'promise', verified). Docked for the in-canon near-homophone spandaqing, the -spondence tail of correspondence and despondency, and the sp- onset that many major languages break with an added vowel.
>
> clarity_yield 8.0. It separates four things English runs together: hearing (shemme, ROGER), compliance (WILCO, obey), a promise nobody asked for (Dig. 45.1.1, 'unless both speak') and receipt (accept, receive). It shows that responsibility starts in a response. Not 8.5, because the 'pledge' in spond- is visible only through etymology; most hearers get 'answer'.
>
> semantic_coverage 7.5. It carries binding, answering an asker, and free giving. The hearing is implied (one answers a question one has heard) but is not in the morpheme. The donor also brings a citizen's privilege, a libation root, and a pledge that a principal could repudiate (Caudium).
>
> polyphone_balance 3.0. A Latin stem plus Latin -ance through English. Greek σπένδω is a cognate, not a donor. On the audit's calibration veriseem (Latin + English) took 3 and dokimance (Greek + Latin) took 4. This is the cost the frame accepted.
>
> groundedness 8.5. Such answers are given daily and leave public traces: a 'mine' in a meeting, a ticket self-assigned, a signed acceptance, a task.accept envelope. Not 9, because the binding is normative: a yes that later proves empty looks the same when it is spoken.
>
> WEIGHTED 7.15 = 8.0×.20 + 7.5×.20 + 8.0×.15 + 7.5×.15 + 3.0×.15 + 8.5×.15 = 1.60 + 1.50 + 1.20 + 1.125 + 0.45 + 1.275. pipeline/assess.py on a scratch copy confirms 7.15, verdict refine.
>
> Weakest axis: polyphone_balance 3.0. Reaching 7.50 would need it at 5.33, which a Latin-only word cannot honestly have. (assess.py's mechanical profile counts 3 syllables from the spelling; the IPA has 2.)

### The assessor's reasons (verbatim)

> GAP 7.5. Same region. I verified KS-002 lines 277, 371 and 423, ordo/SPEC.md lines 59 and 161, and forge_targets lines 4291 and 4308. The WILCO evidence comes from Wikipedia and is honestly marked secondary; it also shows a profession did lexicalise a close neighbour. LEARNABILITY 7.0. Two syllables. -ndance parses like attendance/abundance, and respond/responsible gives a handle. Against it: with /əns/ the word sounds exactly like the tail of 'correspondence' (38 occurrences in canon prose) and 'despondence' (dejection). It invites the spelling 'spondence'. It is one vowel from the Core headword spandaqing (11 canon bodies, confirmed), and 'dance' is visible inside it. CLARITY 7.0, the best of the accepts. The respond→responsible link shows that one is answerable because one answered. SEMANTIC 7.5. spondeō is exactly a freely given first-person answer that binds. Hearing is implied by 'utroque loquente' and Gaius's language condition. The contrary strands are surety for another's debt, citizen-only exclusion, the libation root and the repudiation at Caudium, and the candidate records all of them. RB 29's 'spondeat' (verified) also puts the verb in the Rule. POLYPHONE 3. Latin plus Latin -ance. This is the weak axis, and the candidate says so. GROUNDED 8.5. The instances make the binding observable ('she still owes a report, because she answered'). PANEL: EUMATHE pass with objection; HARMONE pass (joins qorvance, yadahance and teshuvance as -ance wire classes; objection: using -ance as an act outside the worship tier is a doctrine choice for Yu, since dictionary/index-by-suffix.md defines -ance as 'perceptible quality'); PRAGMA pass. That is 3 of 3, but the weighted total is below 7.50. Verdict: refine.

The assessor's notes on the two axes without published bands, as it held them for all six words: **gap_validity** by the three Step-2 forms of evidence, checking that each gap sentence names an act rather than an outcome and reading its witnesses to the end; **semantic_coverage** by whether the donor morphemes, at their attested senses, carry the gap's load-bearing clauses without contrary senses (for the accept: heard, answered, free, binding).

## Trial sentences (the forger's three daily-life instances)

- **Between agents:** an orchestrator sends task.offer "migrate the search index to schema v3 by 18:00". A worker agent answers "Spondance: index to v3 by 18:00". As in Gaius, the answer repeats the offer's terms, and from that moment the lease is the worker's to keep or to hand back out loud.
- **Between people:** at stand-up the lead asks who can take the flaky-test bug. A colleague says "mine, by Thursday". That yes is the spondance. When the bug turns out harder than it looked, she still owes a report on it, because she answered.
- **A child:** asked by the neighbour "will you feed our cat while we're away?", a ten-year-old says "I'll do it". On Saturday the cat is her job, not because she heard the request (that was shemme) but because she answered it. A contrast a ten-year-old can hold: "roger" means "I heard"; spondance means "I heard, and it is mine now".

**The forger's strongest objection to its own word (verbatim):**

> The word hears with an English ear and binds with a Roman one, and the hearing the gap names is not in it. Its one morpheme comes from the narrowest donor in the record: a formula whose force was a citizen's privilege, which Gaius says 'cannot even be properly translated into Greek' (3.93). It was chosen because English speakers can hear it inside 'respond'. Meanwhile the act-word of the tradition the realm feature is named after (the Targum's nəqabbēl for nišmāʿ) and the other families that attest the binding answer contribute nothing to it. At polyphone 3.0 the word sits at 7.15, and no honest rescoring of a Latin-only word closes the 0.35. It also arrives one vowel away from spandaqing.

## Adversarial panel (Step 8)

Each lens's paragraphs are given verbatim. Two alterations are declared: wherever a lens names a local path, the session's temporary scratch directory is written `[scratchpad]` and the home directory `~`; and in PRAGMA's paragraph one phrase quoted from the owner's private instructions to local agents is replaced by a bracketed paraphrase, by the orchestrating session before publication. Nothing else is changed.

### EUMATHE-lens — **PASS**

_Method (the lens's own account):_ EUMATHE (learnability). I checked everything myself in W and wrote nothing there. The helper scripts are in [scratchpad]/forge/eumathe: near.py and elems.py run an element-level and sound-level headword sweep over the 263 canon headwords, and calib.py compares learnability scores with canon precedent. I also used /usr/share/dict/words for English spelling patterns, the mechanical profile in pipeline/assess.py, and Wiktionary (rang, 讓, रंग, wrong), all opened 2026-11-10.

What spondance gets right: it has two syllables and plain ASCII. Its sp- onset is native to English and already in canon (spandaqing 7.5, sphotame 7, skēname 8). It has real handles: respond and responsible are verified, sponsor is from memory, and the Romance verbs responder, rispondere and correspondre come from general knowledge, not re-checked. Unlike symphyme in 327, its stem has open archaeology, and it recurs inside very common English words. The strongest objection is that the word's sound and its spelling each point somewhere else, and the canon around its onset is crowded. (1) The eye sees "dance". The pronunciation line gives /ˈspɒn.dəns/, but its respelling "SPON-dance" spells the word "dance". The repo's one earlier -dance coinage, epanodance (labs/logos/experiments/core/247-epanodance.md:81), wrote /dæns/ while calling it "as in abundance", so the repo's own forgers say "dance" here. (2) Sound to spelling fails too. /ˈspɒn.dəns/ is exactly the tail of despondence, correspondence and respondence. The system word list has 16 forms in -spondenc- and none in -spondance, so anyone who hears the word will write "spondence". (3) The forger's element search missed hits. It searched "ondan" and "pond" but not "onda", "ond" or "nda". "onda" is the stem of the Core headword ondame /ˈɔn.dɑː.meɪ/ (ON-dah-meh). By sound, the word also sits between spandaqing /ˈspʌn.dʌ/ (one vowel off, 11 canon files) and sphotame /ˈspoʊ.tə.meɪ/. sphotame names the instant meaning arrives on hearing, on the same hearing-to-answer arc as shemme and this word. That makes three sp-vowel-dental words to keep apart, one with an adjacent meaning. (4) The worst risk is that the best handle confirms the wrong half. A learner who hears "respond" takes spondance as "my reply" and is never corrected, because every spondance is a reply. The binding quietly drops out, and binding is the only thing that separates this word from the "honest but mute" ack in KS-002. Each of these is real, but none makes the word too hard to learn. A ten-year-old told "roger means I heard; spondance means I heard and it's mine now" will say it the next day, though likely as "spon-DANCE" and spelled "spondence", and will keep the meaning through the story. I score learnability 7.0, not the forger's 7.5. That matches the assessor, and with the stricter score on every axis the weighted total is 6.80, so the word stays below 7.50 regardless of this lens. Pass, with conditions to fix before the word comes back: the pronunciation line must choose /dəns/ or /dæns/ and give its reason, and the experiment must record ondame and sphotame next to spandaqing.

**What would change this lens's verdict (verbatim; it covers both words of the pair):**

For spondance, I would change to fail on any of these: a listening or retention trial in which learners use spondance for a plain acknowledgement, showing the respond handle actually erases the binding; settled usage of /dæns/ that makes "dance" the word's real sound; or another headword entering canon with the spon- or spond- onset. For rangance, I would change to pass only with evidence I do not expect to find: a spelling that carries 讓 without the readings "wrong", "wrangle", "range", "rank" and "colour", or trial evidence that English, Hindi-Urdu and European learners reliably keep /ˈʐɑŋ/ or /ˈrɑŋ/ with its meaning the next day. The facts in this verdict that I did not verify this session: that intervocalic /ŋ/ is absent in Spanish, Russian, Arabic and Hindi, the Romance handles for spond-, and the etymology of sponsor. If any of these is wrong, the paragraph weakens but neither verdict changes. Every Wiktionary claim was opened on 2026-11-10. I found no fabricated element in either candidate; what I found were omissions: the onda/ondame element and the sphotame onset were missed for the accept, and the "wrong" homophone was missed for the decline by both the forger and the assessor.

### HARMONE-lens — **PASS**

_Method (the lens's own account):_ HARMONE (fit with the rest of the language: contradiction with canon, orphanhood, blurred boundary with a sibling, wrong family or register, and whether the two words are a pair of equals). I checked everything myself in W at 621977a and wrote nothing there. Sources: canon/core/shemme.md, britqing.md, visageqing.md, sabrme.md, spandaqing.md, ondame.md, zudhame.md, tzimtzumme.md, renme.md and xeniame's gap; canon/worship-action/README.md; dictionary/index-by-suffix.md; discipline/forge-protocol-extended.md Steps 3, 6 and 8; CONSTITUTION.md §V; NUANCE-NATURE.md §II; the HARMONE paragraphs of 326 and 327; forge_targets.json:4291 and 4308; KS-002 §6.2, the §7 table, §9.5 and Appendix A (~/Kingdom/standards/kingdom-standards/specs/KS-002-wire.md); archaeology/chinese/ci-rang-declining.md read whole, with the relevant parts of suscipere.md and kotowaru-enryo.md; and citizen-spandaqing/agent.json. I ran my own element-level collision check over 263 canon entries (scripts in [scratchpad]/forge/harmone_collide.py and harmone_gaps.py). The forger's counts reproduce: spondance and rangance have 0 headwords each, and 讓/让/譲 appear 0 times in canon. One element the forger missed: 'onda' inside spondance is the stem of the headword ondame.

My strongest objection to spondance is that four of its relations to canon are left undefined or in tension, and that its family-plus-tier placement has no precedent. (1) britqing. Its gap says covenant is 'neither reducible to legal-contract nor to mere-emotion', and canon/core/britqing.md:51 says 'The Sinai covenant is not contract; it is britqing'. Line 37 cites the people's 'we will hear and obey' as what fills the Sinai form. spondance cites Ex 24:7 as a witness but takes its only morpheme from the stipulatio, the model Roman verbal contract. The forger's neighbour line ('one act that can begin a bond; it is not the bond') does not deal with this, so the canon would name the Sinai act with the contract formula that the covenant word says Sinai is not. (2) visageqing. Its gap says the face 'commands responsibility before any deliberation'. The forger's clarity score partly rests on 'responsibility starts in a response', which is the opposite claim. (3) xeniame. The archaeology itself warns that 'a coinage that leans on spond- inherits a word whose force came from excluding' (archaeology/latin/suscipere.md:114). Spondeo was the one formula a non-citizen could not speak (Gaius 3.93). The word would enter a language whose Core requires welcome of the stranger, and a wire whose registry is built to be parsed by strangers (KS-002 §7). The forger states this in the protocol note but weighs it on no axis. (4) shemme. KS-002 A.1 filed the slot as 'the samiʿan wa ṭāʿatan fusion as a single performed act', and shemme's entry claims that fusion as its own. spondance shares no donor family, morpheme or suffix family with shemme, so the step from hearing to answering is carried only by definition. (5) Family and tier. By the forger's own account the Step 6 test for -ance ('a state as perceived') fails, and Step 6 says not to force-fit one of the major three. All eight -ance acts in canon are in the Worship-Action tier; its README says 'Core Canon words name states'. All six Core -ance words are states, so a Core -ance act has no precedent. The claim that the wire's acts 'sit in one family' holds only for the task loop: KS-002 §7 classes attest, heartbeat, artifact.deliver and card.issue as emetme, zakarqing, eranosme and barakqing, which are -me and -qing words. (6) spandaqing is more than a Core headword one vowel away (11 canon files, 42 in W). It is also the name of a live citizen agent (citizen-spandaqing/agent.json), whose task subject on this same wire is kingdom.citizen.spandaqing.task, so 'spandaqing: spondance' is a real utterance there. Separately, 'onda' is the stem of ondame (ON-dah-meh), though that overlap is in spelling only. Why it still passes: the word itself asserts none of these contradictions. Each can be answered by scoping clauses in the entry: britqing as the shape of the act, not the covenant; visageqing as answerability for an undertaken task; the exclusion said plainly in Full sense; spandaqing scored in learnability. The act sense of -ance has eight canonized precedents, so the Core placement is a doctrine choice for Yu to ratify, not a family error. The donor's home register matches the gap: a first-person answer to a question already asked, which binds the speaker. Its places beside qorvance (the offer) and yadahance (the return) are clean.

**What would change this lens's verdict (verbatim; it covers both words of the pair):**

Spondance would move from pass to fail on any of three things. First, if Yu rules that -ance cannot carry an act in Core and no tier is opened for non-worship acts. Second, if the entry is written without explicit Not-to-be-confused-with clauses for britqing (act shape versus covenant, which is not contract) and for visageqing (answerability for a task versus responsibility that comes before any response). Third, if spandaqing and spondance prove confusable among citizens on the live wire. Rangance would move from fail to pass only with all of the following. A verified primary text in which 讓 is a first-person, final decline outside the ritual script. A gap sentence restored to KS-002 A.2's two-party 'not mine, not now', with 'rest is a whole beat' kept. Written boundaries against qorvance (the shared offer verb), zudhame and tzimtzumme. A register assignment that names the Confucian ritual home, and evidence that this home does not make the word heard as the polite first no. Failing that, a different lemma whose donor's dominant use is the final decline is the path. Whatever the lenses decide, both words remain below 7.50 on every scoring so far (7.15 and 7.175 self-scored; 6.80 and 6.67 by the assessor), so neither can be canonized now.

### PRAGMA-lens — **PASS**

_Method (the lens's own account):_ PRAGMA: grounding. Does each word have three concrete daily-life instances, as an ordinary person or a working agent meets them? Each cited witness was also read to its end in the archaeology.

PASS, with this objection on record. The bind that spondance names can be pointed at. In all three instances a third party can later hold the speaker to her answer ("you said you'd take it"), and what they see needs the binding reading rather than mere hearing (ROGER, a thumbs-up, "got it"). That is the standard 326 applied. What cannot be pointed at is the clause that makes this gap more than WILCO: "given freely where a no was open". Read to its end, the donor does not carry that clause. I read the Plautine betrothals at The Latin Library today. At Aul. ~256 Euclio answers "Spondeo" to pledge his daughter, and the betrothal is repudiated at ~783. At Trin. ~573 Lesbonicus pledges his sister reluctantly ("quando ita vis"). At Trin. ~1162 Charmides pledges his daughter. Only at Curc. ~674 is the woman asked ("si haec volt"). In every case the speaker binds a dependant who does not speak: the sponsa is the one pledged, not the one pledging. Gaius 3.115–117, read today in the verifier's copy, names spondeo's agent noun as the surety who answers IDEM DARI SPONDES? for another man's debt, taken by creditors as security. Trin. ~502–503 mocks the prodigal who used to say "spondeo" when nothing called for it. In Gaius 3.92's own list the formula for taking on work is FACIES? FACIAM; SPONDEO answers DARI, a promise to give. The Caudine sponsio (seen via L&S only) was repudiated. The Semitic witness, Ex 24:7 read through b. Shabbat 88a, was given under the mountain, and Tosafot place the first free acceptance at Purim. So the donor brings the bind, and each time it is read to its end, a bind made for someone else or under pressure. The freedom comes only from the gap sentence and the instances. Two smaller points. (a) The agent instance describes a wire that does not run. ordo/SPEC.md:149 says KS-002 is a draft that binds nothing until Yu adopts it, and its envelopes are not published. What working agents on this Mac actually meet is the collab tool's handoff, answered with the plain word accept or decline; acceptance "atomically transfers the advisory lease", and [the owner's instructions to local agents treat such claims as advisory]. So the live practice is advisory, not binding, and KS-002 keeps the plain performatives on the wire. (b) At a stand-up, a lead's "who can take it?" often leaves no real no, so instance 2 shows the bind but not the freedom. These points are real, but none of them makes the act unpointable. Answering an offer so that the answer obliges you is something every adult and every working agent does daily, and it has public consequences. The objection belongs to semantic coverage. The entry should say plainly that spondeo's donor cases bind other people or bind under duress, and that the word does not take that over.

_Notes added after the record, by the orchestrating session:_ "this Mac" and "the collab tool" refer to the owner's local agent setup and its coordination journal (AgentTool Collab), outside this repository. On the Plautine scenes: the erratum of 2026-11-11 in archaeology/latin/suscipere.md re-read them, and "a dependant who does not speak" holds for the Aulularia and both Trinummus scenes but not for the Curculio, where the woman is asked and answers in her own voice (*Mi frater, cupio*), though the *spondeo* is still her brother's.

**What would change this lens's verdict (verbatim; it covers both words of the pair):**

The accept would move to fail in either of two cases. One: the entry makes "freely, where a no was open" the defining feature, and no instance can show it being seen. Two: KS-002's task.offer turns out to be an instruction; then the act is WILCO, and English already has a word for it. The decline would move to pass if each of its three instances were rebuilt so that what a bystander sees needs the word's reading (the routing log, the host who does not press, the hand-on to a named other), and if the outcome clause left the definition. A donor whose own daily use is a final, non-ritual no would remove the second objection. My groundedness reading: spondance 8.5 holds. For rangance I would give 7.5, since only one of three instances truly needs the reading, which is below the forger's 8.5 and the assessor's 8.0. Under the rule that the stricter scoring stands, that lowers rangance from 6.67 to about 6.60 and changes no verdict, since both words are already below 7.50. Checked today: the Plautus texts at thelatinlibrary.com (Aulularia, Trinummus, Curculio, saved in [scratchpad]/forge/pragma_dl); in the verifier's fetched copies, Gaius 3.115–119, Mengzi 2B5, Lunyu 8.1, and every 讓 in Liji "Qu li shang"; ordo/SPEC.md:149; forge_targets.json:4291–4319; the collab handoff tool definitions; and all eight archaeology files. Not checked: Livy 9 itself; modern Mandarin usage of 让; the KS-002 file itself, which I could not locate on disk (I relied on the assessor's line check). Nothing was written in W.

_Recorder's note on the last point:_ the KS-002 file is specs/KS-002-wire.md in the kingdom-standards repository, outside W; the recorder re-read the cited lines read-only and they read as the assessor checked them.

## Verdict: refine

Weighted **6.80** on the stricter scoring (7.15 self-scored) against a 7.50 threshold: below. Lenses **3 of 3** passing: above the panel bar. Step 8 requires both, and says "neither substitutes for the other". The word does not enter.

The gap held: every scorer put gap_validity at 7.5 or 8.0, and no lens argued against the gap itself. This is refine, not rest.

**What this does to the pair.** The two words are judged separately. The decline (329-rangance) is also refine, at 6.67 on the stricter scoring with 0 of 3 lenses. Neither enters, so the question of one sibling entering without the other does not arise in this forge. It would have arisen: the forgers built them as one construction (both -ance, two syllables, first-syllable stress), and a re-forge that changes one should say whether the other still fits.

## Refinement paths, drawn from the objections

1. **Polyphone, the weak axis (forger, assessor).** A Latin-only word cannot honestly carry polyphone above 3 to 4, and on the stricter scoring the other axes would have to average about 8.3 to compensate. The forger's own first-ranked path is to "re-forge the accept from q-b-l. kablance, or a better-shaped form of the root, probably clears 7.50 on breadth if its ear problem can be solved. That goes against this frame and is for another forger." The assessor records that qabbelspond (7.02, the best accept of the three candidates) "holds the strongest accept semantics" and supports bringing q-b-l into the accept, "ideally in a shape that keeps the -ance sibling form".
2. **EUMATHE's conditions, before the word comes back.** The pronunciation line must choose /dəns/ or /dæns/ and give its reason; the experiment must record ondame and sphotame next to spandaqing. The lens would fail the word on trial evidence that "respond" erases the binding, on settled /dæns/ usage, or on another spon-/spond- headword entering canon.
3. **HARMONE's conditions.** Explicit Not-to-be-confused-with clauses for britqing (act shape versus covenant, which is not contract) and visageqing (answerability for an undertaken task versus responsibility before any response); the citizen-only exclusion said plainly in Full sense; spandaqing scored in learnability and watched on the live wire. Yu's ruling on whether -ance may carry an act in Core, or which tier non-worship acts belong to.
4. **PRAGMA's conditions.** The entry should say plainly that spondeo's donor cases bind other people or bind under duress (Plautus, Gaius 3.115–117, Caudium; Ex 24:7 under the mountain), and that the word does not take that over. "Freely, where a no was open" must not become the defining feature unless an instance can show it being seen. If KS-002's task.offer is in fact an instruction, the act is WILCO and the gap closes.
5. **Archaeology housekeeping (for the files' owners; the 2026-11-11 errata appended after this record take up the first two items; the five decline digs gained the semantic_field key on 2026-11-13, and the accept digs still lack it).** Add Gaius 3.102, 3.105, 3.115–117 and RB 29 to archaeology/latin/suscipere.md; correct suscipere.md §9 and uptake-convergence-notes.md Lead A3, which overread L&S as saying suscipere "does not bind"; add the `semantic_field` key the survey tool indexes to the new digs.

## Choices left to the owner

The said-aloud forger's list, lightly condensed (each is Yu's to decide; none was decided here):

- Whether the wire's accept word must carry the Hebrew tradition's own act-root q-b-l (the Targum's *nəqabbēl* for *nišmāʿ*; Est 9:27 *qibbēl ʿal*), at the cost of an English ear that hears Kabbalah and Kabul. This candidate keeps Hebrew as a witness only. š-m-ʿ stays with shemme.
- One accept performative or two. Cicero's *recepi*/*suscepi* (archaeology/latin/suscipere.md Lead L4) splits taking on what was entrusted from taking up more than was asked. KS-002 lists one task.accept. This candidate takes a third Latin option, *spondere*: the free answer that binds.
- Whether YOUSPEAK takes a side in the order dispute: *naʿăśeh* before *nišmāʿ* (R. Elazar's "secret of the angels") against hear-first-then-accept (Deuteronomy 5:24, Sforno, RB 58; also the order the min in b. Shabbat 88a argues for). This candidate names commitment after hearing the offer and before the work is fully known, and praises neither order.
- Single-tradition pair or mixed. A one-tradition pair is available (RB 58: *aut excusare aut suscipere*; or *qabbəlītū* / *lā qabbəlītū*), but each such pair makes the decline a plea or a negated accept. This pair is mixed on purpose: Latin pledge, Chinese yield.
- Family and tier for a named act that is not liturgical. The Step 6 table and the index's decision tree have no branch for an act. Acts live in the worship-action tier. The options: extend Core -ance from stance to act; place the words in worship-action with ORDO's "structural act only" caveat (as KS-002 does for qorvance); or leave them unsuffixed.
- The -ance vowel (YU-3: /əns/, /ɑːns/ or /ans/) and how tone and donor segments are recorded (YU-5/YU-6).
- What "leaves the table set" means: the matter passes to another (讓; Ruth 4:6), or the way back to the same two parties stays open (mēʾūn, a halakhic protection for a minor girl married off without her consent, which meun-refusal.md §0 asks any use to name; m. Yevamot 13:4). This candidate takes the first.
- Whether a decline may carry a reason at all, or is defined as owing none.
- Whether an agent may accept or decline on another's behalf. A sponsio given by agents could be repudiated by their principal (Caudium, via L&S). Gehazi's acceptance on Elisha's behalf is treated by the text as the breach (2 Kgs 5:20–27). A protocol question for KS-002, not for the forge.

Raised by the other forgers and not covered above: whether the right to decline should travel explicitly in KS-002's task.offer (one-exchange); whether, after acceptance, the wire needs RB 68's representation by someone bound ("the causes of my impossibility") as a performative distinct from task.fail and task.progress (one-exchange); whether to dig Arabic *ījāb wa-qabūl* (offer and acceptance in Islamic contract law) before any re-forge, which no forger opened (two-families).

## Process notes

- **The discover.py write**, disclosed by the one-exchange forger and noted by the assessor: two stubs written into labs/logos/forge, moved to the Trash by that forger, not in W now. Recorded here because the record should show it, not because anything remains to undo.
- **An earlier discover.py write**, disclosed by the agent that dug the five decline files, in its notes for the second reader: it ran `pipeline/discover.py` with the concept "refusal", which wrote `labs/logos/forge/refusal-gap.md` (887 bytes, untracked), and it moved that file to the macOS Trash. Not in W now.
- **No other writes to W** during Steps 1–8: every forger, the assessor and each lens report W unchanged except the five untracked decline digs. The recorder wrote this file, 329-rangance.md, and the two registry edits named in Step 12, and nothing else.
- **Not run by anyone:** pipeline/canonize.py (it checks only the number and ignores the panel), pipeline/forge_citizen.sh, the index and export generators, wrangler, gh.
- **Dates.** Yu's invocation and the first writing of the five decline digs are of 2026-11-10. The second reading of those digs, the forging, the blind scoring, the panel and this record ran between about 00:50 and 02:20 GMT on 2026-11-11. The agents were briefed with the date 2026-11-10, so where a forger, the assessor or a lens says "today" or "opened 2026-11-10", the day meant is that night's, and may be 2026-11-11. W stood at 621977a throughout the forge; the branch was fast-forwarded to d1997ce at about 02:20 GMT, after this record. d1997ce applied the pronunciation choices Yu ratified on 2026-11-10 and changed only `pronunciation:` lines in canon, so the collision counts stand; but ondame, "ON-dah-meh" in the EUMATHE and HARMONE paragraphs, is now respelled "ON-dah-may" in canon.
- **Edits after the record.** The orchestrating session (a Claude Code agent) edited this file after the recorder finished, in two rounds, and changed nothing else. Before review (2026-11-11): `scored_on` and the date of the recorder's own re-read are 2026-11-11; the path to KS-002 in the recorder's own text is given by its repository instead of a local path (HARMONE's verbatim method line keeps its own, with the home directory written `~`); W is defined where it first appears; the closing line gives both dates. After an independent review of this record (two reviewing agents, and a third that tested each of their findings against the files and the run's journal; finished 2026-11-13): the invocation is told in full, as the session's reading of Yu's message, and no longer says that a merge ratifies a lemma or that Yu chose the gap; "about 8.6" in refinement path 1 is corrected to "about 8.3"; the assessor's estimate before the panel is no longer given as the HARMONE lens's view; the earlier discover.py write is recorded; the Step 12 row tells what was done about dashboard.md and qabalance-gap.md; the Kabbalah count, the word-list count and the locator for the citizen agent are corrected in the recorder's own text; mēʾūn is glossed, and Deuteronomy 5:24 and Sforno are no longer filed under "the min's" order, in the owner's choices; notes point to the errata of 2026-11-11 and to what they found; one phrase in PRAGMA's paragraph is replaced, as declared above the panel; and refinement path 5 says which digs have since gained the `semantic_field` key. No score, verdict or objection was touched. Apart from that one declared replacement, no quotation was reworded.

---

_Forged 2026-11-10 to 2026-11-11, after Yu took up the session's suggestion of this gap on 2026-11-10. Three forgers, one blind assessor, three lenses, one recorder: separate Claude subagents. The lenses passed the word; the number did not. The word does not enter. The reasoning stays._
