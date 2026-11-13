---
id: 329
candidate: rangance
target: wire-task-decline (forge_targets.json; KS-002 THE WIRE, Appendix A.2, task.decline)
gap: >
  The spoken act of declining an offer as one's own complete act. It is a no that owes no reason, does not judge the offer or the one who made it, and is not a polite first refusal waiting to be pressed again. It gives the thing way so that it can pass to another or come back later, and afterwards the relation stands as it stood.
donors: [Mandarin:讓 ràng, Latin:-antia (via English -ance)]
pronunciation: "/ˈʐɑŋ.əns/ (RAHNG-ance; 2 syllables; Mandarin ràng 讓 + Latin -ance); anglicized /ˈrɑŋ.əns/ acceptable"
sibling: 328-spondance (wire-task-accept), forged as one pair
axes:
  gap_validity: 7.5
  learnability: 6
  clarity_yield: 6.5
  semantic_coverage: 5.5
  polyphone_balance: 6.5
  groundedness: 8
weighted_v2: 6.67
axes_forger:
  gap_validity: 8
  learnability: 6.5
  clarity_yield: 7.5
  semantic_coverage: 6.5
  polyphone_balance: 6
  groundedness: 8.5
weighted_v2_forger: 7.175
verdict: refine
scored_by: "independent assessor (a Claude subagent that did not see the forger's scores); its scoring is the stricter and stands (experiment 035). Exact total 6.675, reported as 6.67 because the assessor rounds down. The forger's self-score is recorded beside it."
scored_on: 2026-11-11
panel: "EUMATHE fail · HARMONE fail · PRAGMA fail — 0 of 3. Canonization requires weighted >= 7.50 AND 2-of-3 lenses (forge-protocol-extended.md Step 8). Below threshold on every scoring (6.67 stricter, 7.175 self-scored) and unanimously opposed; both conditions fail, and neither substitutes for the other."
invocation: "Yu, 2026-11-10: Lets go for what you recommended sensible actions for the above decision."
invocation_note: "The session read Yu's sentence as taking up its suggestion to forge this gap. The gap was the session's suggestion; every lemma is an agent's proposal."
format: full-trace — a refine whose reasoning must survive for the next instance (Step 9)
---

# 329 — rangance

_The decline half of the wire's first forged pair, walked to the end of the protocol and declined on both counts. The frame asked for a short, live morpheme for a sovereign no, and the best one it could find is ritual courtesy's own word. All three lenses found that the word carries the very thing its gap sentence exists to exclude._

## The invocation

On 2026-11-10 the session suggested, as the first forge, "binding acceptance" (the queued target `wire-task-accept`: hearing that completes itself in pledged uptake) together with its sibling, "refusal that keeps the bond" (the queued target `wire-task-decline`: sovereign refusal without rupture). The suggestion was the fifth of six open decisions the session put to Yu, the language's owner; it said that no forge had started and that the repository's rule is that Yu names the gap. Yu answered the list in one message:

> "Yumi is the relationship term. You and me, A framework to communicate. Lets go for what you recommended sensible actions for the above decision"

The session read the last sentence as taking up each of its recommendations, this forge among them, and treats it as the invocation (forge-protocol-extended.md §VI, the FATE-clause). That is the session's reading of Yu's words. The gap was the session's suggestion; Yu did not word it and chose no word. Every lemma in this file, including the one carried to the panel, is an agent's proposal. The verdict is refine: neither word entered canon, and this record keeps the reasoning, not a word.

## How the forge was run

- **Three forgers**, each a separate Claude subagent, worked three frames for the pair: *one-exchange* (both words from one tradition's question-and-answer rite), *two-families* (each word welds a Hebrew act-root to a root from an unrelated family) and *said-aloud* (each word at most three syllables, built only from live, recognisable morphemes). Each walked Steps 1–7 and scored its own pair.
- **One independent assessor** scored all six words without seeing the forgers' scores, checked their claims, and chose the pair to carry: *said-aloud*, **spondance** (accept, experiment 328) and **rangance** (decline).
- **Three lenses** (EUMATHE, HARMONE, PRAGMA), each a separate subagent, argued against the carried pair (Step 8).
- **This file** was written by a fourth role, the recorder, who does not improve the words, raise a score or soften an objection. Quotations from a forger, the assessor or a lens are marked; where the recorder checked something itself, it says so.

## The walk — twelve steps, as they fell

| Step | What was done | What was not done, or went wrong |
|---|---|---|
| 1 Survey | `pipeline/forge_priority.py` (read-only): wire-task-decline #94 of 95 queued targets (two-families forger; reproduced by the assessor). forge_targets.json:4308 showed it `queued`, `donor_pair: []`, `experiment: null`, `convergence_witnesses: []`. The said-aloud forger used `discover.py --list` (read-only) and grep, and found no archaeology for the region beyond the digs named in the brief. | The target was **not** marked `in-forge`: the forgers' briefs did not allow writes to W (the forge's working tree of this repository, on the branch that carries this file). **Process error, disclosed by the one-exchange forger:** `pipeline/discover.py` run for "acceptance" and "refusal" wrote two untracked stubs (`labs/logos/forge/acceptance-gap.md`, `refusal-gap.md`); that forger moved them to the macOS Trash minutes later and W returned to its starting state. The run matched 0 of 242 files, because no dig carries the `semantic_field` key that discover.py indexes (the recorder confirmed this for all eight digs). |
| 2 Gap evidence | Convergence (eight witnesses in four families), negative space across the five decline digs, circumlocution (KS-002's own words; ICAO UNABLE), near-neighbour elimination. Below. | ICAO UNABLE is from a secondary source (Wikipedia), marked so by the forger. HARMONE finds that the gap sentence was bent toward the morpheme (see below). |
| 3 Collision | Element-level scan over canon/ (267 files) and the Step-3 wider set (299 files) by the forger's `collide_mouth.py`; reproduced by the assessor, EUMATHE and HARMONE. | The "wrong" homophone (under the cot–caught merger) was missed by the forger and the assessor; EUMATHE found it. |
| 4 Archaeology | The five decline digs were opened on 2026-11-10 (archaeology/hebrew/meun-refusal.md, archaeology/arabic/iba-itidhar.md, archaeology/latin/excusare-recusare.md, archaeology/chinese/ci-rang-declining.md, archaeology/japanese/kotowaru-enryo.md). A second agent checked all five against their primary sources and returned "sound_after_fixes": no source fabricated; selective quotation and readings stopped short of the end were corrected; each file ends with a `## Verification (2026-11-11)` section. | The donor of this lemma, 讓, has archaeology at "lead" depth only (ci-rang-declining.md §8 Lead C-D2). Its Japanese reading *yuzuru* is undug (kotowaru-enryo.md Lead J-D5). Modern Mandarin usage of 让 was given from memory by the said-aloud forger and by PRAGMA. EUMATHE, which opened Wiktionary's 讓, gives its modern senses as allow/let/permit, have someone do something, yield, give way, the passive "by" and, marked literary, reproach, with decline not among them; the assessor cites Unihan's modern sense, "allow, permit". No one reports opening a source of actual usage beyond these dictionaries. |
| 5 Lemma alternatives | Seven forms rejected with reasons; two whole candidate pairs from the other frames recorded below. | No forger reports running `pipeline/forge.py`. |
| 6 Family | `-ance`, in its act sense; all five questions answered. | The act sense of `-ance` outside the worship-action tier is a doctrine choice for Yu. The register assignment is contested by HARMONE. |
| 7 Scoring | Forger 7.175; assessor 6.675 (reported 6.67). The stricter stands: **6.67**. | — |
| 8 Panel | EUMATHE fail, HARMONE fail, PRAGMA fail: 0 of 3. | — |
| 9 Experiment file | This file. | — |
| 10 Canon entry | Not written: the verdict is refine. | — |
| 11 Nuance check | Not applicable without a canon entry. `nuance_check.py --suggest mandarin` gives Group C (hánxù + zhēnchéng); `--suggest confucian` gives Group B (jūnzǐ + chéng) (recorder, read-only). | — |
| 12 Interlinks | forge_targets.json `wire-task-decline` moved to `refining` with this experiment. No petition in labs/logos/petitions.json points at this target. | No canon word entered, so no index, canon.md, convergence file, morphemes.json or _sidebar.md change is owed. dashboard.md's count of forge experiments was stale by these two files; the orchestrating session ran Step 12's `derive_indices.py --dashboard` after this record, which changed that one row (292 to 294) and nothing else. No liturgy session file was written by the recorder. |

## The Gap

The spoken act of declining an offer as one's own complete act. It is a no that owes no reason, does not judge the offer or the one who made it, and is not a polite first refusal waiting to be pressed again. It gives the thing way so that it can pass to another or come back later, and afterwards the relation stands as it stood.

**The target's own wording, for comparison** (forge_targets.json:4311): "sovereign refusal without rupture — 'not mine, not now' that leaves the table set; rest-as-a-whole-beat spoken to someone". KS-002 Appendix A.2 (:425): "The act of saying no that keeps the bond whole — the wire's missing word for 'rest is a whole beat' spoken *to someone*. Not rejection (which judges the offer), not failure (yadahance covers what was attempted), but the creature's honest 'not mine, not now' that leaves the table set." (Inner double quotes shown as single quotes.) HARMONE's finding is that the gap sentence above adds a three-party clause ("so that it can pass to another") that is in neither text, and drops "rest is a whole beat"; PRAGMA's is that its last clause is an outcome the other party decides. Both are recorded in the panel and in the refinement paths.

## Gap evidence (Step 2)

The forger's evidence (its wording; the bold labels are the recorder's):

1. **The slot is filed.** KS-002 marks task.decline "GAP — proposed forge-target" (:372; Appendix A.2 :425: "not rejection … not failure … the creature's honest 'not mine, not now' that leaves the table set"). Refusal today is "the lease expiring unclaimed" (:277). KS-002 also says: "A wire that cannot say 'no, with love' is not finished" (:415).
2. **Negative space across the five digs.** The decline is lexicalised only in four ways:
   - as a plea: *excūsāre* and *recūsāre* < *causa*; *iʿtadhara ʿan*; 辭; *kotowaru*;
   - as the accept negated: 辤 = 不受; 承らず; *lā qabbəlītū*;
   - as rebellion: *mēʾēn* with *mārāh* (Isa 1:20); *ʾabā wa-stakbara* (Q 2:34);
   - as courtesy meant to be overridden: 禮辭 and 固辭; *enryo*; *nolo episcopari*; Ruth Rabbah 2:16.
3. **Yet the shape itself is attested in texts, in four families** (Semitic, Indo-European, Sinitic, Japonic):
   - m. Yevamot 13:4: the refusal defined by the door it leaves open (meun-refusal.md §3.7);
   - Q 33:72: the offered Trust declined, unblamed (iba-itidhar.md §3.1);
   - 2 Kgs 5:16–19: "Go in peace" (meun-refusal.md §3.3);
   - Ruth 4:4–6: the decline invited as an equal option and handed on (meun-refusal.md §3.6);
   - Zhuangzi: Xu You's "go home and rest, my lord" (ci-rang-declining.md §3.4);
   - Yili "Shi xiang jian li": the gift finally declined, the visitor received and bowed out (ci-rang-declining.md §3.1);
   - RB 58: "if you cannot, depart free" (excusare-recusare.md §3.2);
   - Taketori: letters for three years after the refusal (kotowaru-enryo.md §3.1; that refusal held only because she could vanish, after an attempted abduction).
4. **Even radio procedure**, which coined WILCO, can only say no as incapacity: ICAO UNABLE, "I cannot comply with your request, instruction, or clearance"; NEGATIVE includes "Not capable" (en.wikipedia.org/wiki/Procedure_word, opened 2026-11-10). There is no professional word for "will not, and nothing is broken".
5. **Everyday phrases:** "I'll pass", "not this time", "rain check", "no, thank you" [usage from memory].

**Re-read by the recorder** (read-only, 2026-11-11): specs/KS-002-wire.md in the kingdom-standards repository, lines 277, 372, 415 and 425 read as quoted.

**Against the gap**, from the forger and the assessor: "no, thank you" and polite "decline" do most of the daily work; what remains unnamed (owing no reason, not a ritual opening, giving way) is real but thin in ordinary speech.

**How the witnesses read to their end** (PRAGMA, recorded here because it bears on the evidence): of the eight, three make the no a matter of inability (Ruth 4:6 "I cannot redeem", and Ruth Rabbah 7:7 remembers the man as unnamed and ignorant; RB 58 "si vero non potes", where the community's own first refusal at the door is a test meant to be overcome; Q 33:72, where the heavens "were afraid of it", which al-Muyassar glosses as fearing they could not carry it out); Yili's 終辭 is final only on the third turn; m. Yevamot 13:4 ends the marriage. "Only Elisha and Xu You carry the shape whole, and both refuse a gift or an office on grounds of their own standing."

## Circumlocution evidence (Pattern 2)

- KS-002 itself: the wire's no is "the lease expiring unclaimed" (:277), and "A wire that cannot say 'no, with love' is not finished, and this draft says so" (:415).
- The everyday English set: "I'll pass", "not this time", "rain check", "no, thank you". Each is a phrase or an idiom; none names the act.
- No ORDO rite has reached for a decline word yet: labs/logos/petitions.json holds only the accept petition (two-families forger; confirmed by the recorder).

## Collisions found (Step 3 — recorded, never silently absorbed)

**The forger's scan** (same method and roots as 328: 267 canon files; 299 wider-set files):

- `rangance`: 0 headwords, 0 bodies, 0 wider.
- `rang`: 0 headwords; 43 bodies, 53 wider. All English, plus one Korean word: range 11, stranger 8, arrangement 8, arranges 8, strangers 5, arranged 5, strange 4, arranging 4, arrangements 3, arrange 3, stranger's 2, strangeness 1, ranges 1, and sarang 1 (Korean "love", in jeongqing.md:74).
- `rangi` 4 (all "arranging"); `ranga`, `angance`, `arrogance` 0 each; `gance` 2 (elegance, in artiance and shaktipatame); `range` 39.
- 讓, 让, 譲: 0 each; the character appears nowhere in canon.
- No canon headword begins with or contains rang; no -ance member shares its onset.
- Phonetic, outside the canon: an English reader may say /ˈræŋɡəns/, a near-rhyme of "arrogance", which is the register of Iblīs's *ʾabā wa-stakbara*; or /ˈreɪndʒəns/, after "range". "rang" is the English past tense of "ring". *rang* means "colour" in Hindi and Persian [from memory, not re-checked by the forger; verified by EUMATHE on Wiktionary]. Modern Mandarin 让 is "let, allow" and a passive marker [from memory].
- Semantic: the morpheme also names the offer itself (Yao 讓 the world). The forger: "That does not break the wire, because the plain performatives stay in the JSON (KS-002 registry discipline), but it is recorded."

**Added by the panel** (missed by the forger and the assessor):

- **"wrong"** (EUMATHE): the anglicized line gives /ˈrɑŋ.əns/, respelled RAHNG. Wiktionary gives "wrong" as /ˈɹɑŋ/ in General American with the cot–caught merger, and lists "rang" as a homophone of "wrong" in Northumbria. Many North American speakers who say the word as its own line instructs will say "wrong-ance".
- **The default English reading** (EUMATHE): English has no -ngance word; every -gance word ends /ɡəns/ and every -ngence word /ndʒəns/; English reads a before ng as /æ/. So the default reading is /ˈræŋɡəns/, sharing /ˈræŋɡə/ with "wrangle" and leaning toward "arrogance"; the second reading is "range-ance".
- **"rang" across major languages** (EUMATHE, Wiktionary, verified): Hindi रंग "colour, complexion, paint" (Urdu رنگ, Persian *rang*); "rank, status" in French, Dutch, Danish, Swedish, Norwegian, Hungarian, Romanian and Catalan; German past tense of *ringen*, "to wrestle".
- **The offer verb** (HARMONE): because 讓 is also the word for the offer (堯讓天下於許由), the morpheme blurs into qorvance, the wire's task.offer class.

**No collision at canon-headword level** (forger, assessor, EUMATHE and HARMONE all reproduce this; EUMATHE finds only the element `nga`, in ginnungame).

## Near-neighbours (Pattern 3 — why each existing word fails)

| Word | Covers | Fails on |
|---|---|---|
| `sinbyeongme` (Core) | the call that cannot be refused ("a god who does not ask") | rangance answers an offer that asks |
| `walkekin` (Core) | the bond that survives long silence | names the bond; rangance is the act that leaves it unbroken |
| `warame` (Core) | scrupulous abstention from the doubtful, a disposition with no addressee | rangance is said to someone, about one offer |
| `skename` (Core) | the devoted refusal to be sent away, holding on to an encounter | rangance lets go and gives the thing way |
| `teshuvance` (wire halt.ack class) | turning back after a breach | rangance makes no breach to turn from |
| `yadahance` (wire return class) | reports what was attempted, success or failure alike | rangance is said before any attempt, so it is not a failure |
| `spondance` (328, this pair) | the other answer to the same offer | each is a complete act; neither is the other negated |
| ICAO UNABLE | "I cannot comply": the no as incapacity | rangance is the no as one's own choice, with ability not in question |
| English decline, refuse, pass, "rain check", "no, thank you" | — | in turn: they do not separate the ritual refusal from the real one; they judge; they are casual and can end things; they promise a later yes; they are a phrase rather than a word |

HARMONE adds two canon words "in the region the new gap sentence now occupies" that the forger did not name: **zudhame** (letting go of what is permitted; "closest to 應受而推") and **tzimtzumme** (withdrawal to leave room). It also notes that the only canon kin the morpheme brings is **renme**, beside 辭讓 in Mengzi 2A6, "and it arrives through the ritual register the gap excludes".

## Donors and archaeology (Step 4)

1. **rang** (the only morpheme of meaning). Mandarin 讓 *ràng* [ʐɑŋ˥˩]; Tang \*njiɑ̀ng; fanqie 人樣; Cantonese *joeng6*. Unihan U+8B93 (verified): "allow, permit, yield, concede".
   - Kangxi glosses (verified): Shuowen 相責讓也, reproach, the first sense; 玉篇 謙也, modesty; 類篇 退也, withdrawing; 字彙 先人後己謂之讓, putting others first; Zuozhuan 卑讓，德之基也 and 讓，禮之主也 ("yielding is the master of ritual"); Liji subcommentary 應受而推曰讓, "to push away what one ought to receive"; Yili note 事同曰讓，事異曰辭, the same thing passing on.
   - Instances the forger listed: Lunyu 8.1, Taibo "three times yielded the world", a real yielding that went unseen; Zhuangzi, Yao 讓天下於許由, where the offer itself is called 讓; Mengzi 2B5, "in advancing and withdrawing, have I not ample room?". **The assessor found the last false as an instance of 讓:** the passage speaks of 進退 and does not contain 讓 (the recorder confirmed this against the quotation in ci-rang-declining.md §3.3; PRAGMA confirmed it in the verifier's fetched copy).
   - **Archaeology loci:** archaeology/chinese/ci-rang-declining.md §1, §2 table (讓, 辭讓), §3.2 (Liji: declines required, choreographed and forbidden), §3.3 (Mengzi 2A6, 2B5), §3.4, §3.5 (Lunyu 8.1), §6 (patterns 3–5), §8 Lead C-D2 with its weaknesses, §9. Also archaeology/japanese/kotowaru-enryo.md §2 (譲: Japanese readings *jō* and *yuzuru*, via Unihan; not dug further) and §8 Lead J-D5, whose stated weakness is that *yuzuru* "means yielding what is one's own, not declining what is offered" (the assessor notes the forger cited the file for the readings but did not carry this caution).
   - Living today: modern Mandarin 让 "let, allow", and the yielding sense in 讓座 and 禮讓 [from memory, not re-checked].
2. **-ance**: as for the accept; /əns/.
3. **Witnesses only, no morpheme in the word:** m. Yevamot 13:4 and b. Yevamot 107b–108a (meun-refusal.md §3.7; Shmuel's "she acts on him" is said of a levir, against Rav); Ruth 4:4–6 (§3.6); 2 Kgs 5:16–19 (§3.3); Gen 48:19 (§3.2); Q 33:72 (iba-itidhar.md §3.1); RB 58 "liber discede" (excusare-recusare.md §3.2); Yili "Shi xiang jian li" 終辭其摯 (ci-rang-declining.md §3.1); Taketori (kotowaru-enryo.md §3.1).
4. **Protocol.** The donor strand is the Confucian classics, a living tradition (light) per ci-rang-declining.md §0. Custodians: the compilers of the ritual classics and the Ru tradition. Review by a scholar of the ritual classics is desirable before any rite use; a custodian request means withdrawal. Nothing sacred is reduced to a suffix. The Qur'anic *ʾabā* is avoided because it is Iblīs's verb, and the *samiʿnā wa-aṭaʿnā* / *wa-ʿaṣaynā* pair is not used. Q 33:72 is cited only as the shape of an unblamed declined offer; one modern tafsir (al-Muyassar) was read, and the classical exegesis was not opened. *mēʾūn*, a protection given to a minor girl married off without consent, is a witness only and is not generalised into the word (meun-refusal.md §0.2).

**Archaeology notes found in this forge** (for the files' owners, not fixed here):
- archaeology/chinese/ci-rang-declining.md:248 read "Not yet re-checked by a second reader.", above the file's own Verification section (:256), which records that second reading. The same stale line stood in all five decline digs; the orchestrating session corrected it in each before commit, and dated those Verification sections 2026-11-11, the day the second reading ran.
- None of the five decline digs carried the `semantic_field` key that `pipeline/discover.py` indexes. All five gained it on 2026-11-13, after an automated review of the pull request asked for it; the wording of each field is the orchestrating session's.

## Lemma alternatives (Step 5 — rejections recorded)

| | Lemma | Reason (the said-aloud forger's, condensed; words in quotation marks are verbatim) |
|---|---|---|
| **carried** | `rangance` /ˈʐɑŋ.əns/ | "I give way": the thing passes on and the bond is spared; two syllables; no clusters; a positive act rather than a negated accept |
| rejected | `excusance` | the most alive in English ("may I be excused?" is a child's own decline that leaves the table set), and paired with suscipere in RB 58 and Inst. 1.25. Rejected because it contradicts the Latin dig's main finding: the Latin decline is a plea with a cause, judged and proven within a deadline (Inst. 1.25); its best-known use ruptured (Luke 14); English "excuse" reads as pretext or apology |
| rejected | `recusance` | English "recuse" is close in sense, but *recūsātiō* is the defendant's counter-plea, adversarial by its legal home, and the form sits on "recusant" and "recusancy": refusal of Church of England services, met with punishment |
| rejected | `miunance` / `meunance` | "the strongest sovereign semantics in the record": her own act, no reason needed, the way back left open (m. Yev 13:4). Rejected on the mouth (the me- onset parses against the 184-stem -me family; the aleph is lost; it rhymes toward "nuisance"; technical, not daily speech) and because it would generalise a gendered protection for minors into a common noun |
| rejected | `kotowance` | the everyday Japanese decline, but an English ear hears "kowtow-ance", servility; *kotowaru* also means breaking off a relation; *koto-* is already in canon bodies (kotodama) |
| rejected | `nolance` | guessable because "no" comes first, but reads as rejection; *nōlō* is "not-will", the failure of a yes; its only archaeology is *nolo episcopari*, the false friend; near "nonchalance" |
| rejected | `liberance` | says "free", but near-rhymes "deliverance", names leaving rather than the no, and *liber* is also "book" and the god Liber |
| rejected | `rangqing` | avoids the -ance rhymes, but -qing names a felt bond, not the act; the family test fails, and it would be single-tradition |

### The two other candidate pairs, and why they were not carried

**one-exchange — `suscipance` / `excusance`** (Latin, after RB 58's *aut excusare aut suscipere*).
- excusance: forger 5.78 (gap 7.5, learn 6.0, clarity 5.0, sem 5.0, poly 3.0, grnd 7.5); assessor 5.70 (gap 7.0, learn 6.5, clarity 4.5, sem 5.0, poly 3, grnd 7.5); assessor's panel estimate 1 of 3 (EUMATHE fail; HARMONE fail, "the gap contradicts the morpheme"; PRAGMA pass). The weakest of the six words.
- The forger's own verdict on its frame: "this frame's witnesses cannot supply the decline". Read to its end, RB 58 ritualises only the yes; the no is a departure, and its formula is spoken to the novice, not by him; everywhere else *excusare* is a plea with a cause.
- **Claims the assessor found false** in excusance's record: (1) Taketori was listed among witnesses "each read to its end" without the coercion and attempted abduction that kotowaru-enryo.md §3.1(c)–(d) records before the letters, "the defect the verifier had just fixed in the dig"; (2) KS-002 §7 (line 365) states its principle for success against failure only, not for accept against decline; (3) RB 58 was offered as support for a no that owes no reason, though its formula is conditional on inability, "si vero non potes".

**two-families — `qabbelspond` / `miunci`** (Hebrew act-root welded to a second family's root; here Mishnaic *mīʾūn* + Chinese 辭 *cí*).
- miunci: forger 6.75 (gap 7.5, learn 4.5, clarity 7.5, sem 6.5, poly 7.5, grnd 7.5); assessor 6.52 (exact 6.525, rounded down; gap 7.5, learn 4.5, clarity 6.5, sem 6.0, poly 7, grnd 8); assessor's panel estimate 1 of 3 (EUMATHE fail; HARMONE fail, "the head morpheme contradicts the gap"; PRAGMA pass).
- The assessor called miunci's gap sentence "the cleanest of the three decline gap sentences: 'so that the asker may ask again' names a purpose, not an outcome that only time can show", and its Elisha / 終辭其摯 convergence real. Against it: learnability 4.5 (pinyin *ci* [tsʰɹ̩] unguessable; an unstable syllable count; "-unci-" calls up renunciation); the head morpheme's formula refuses the person and ends the marriage it refuses; the tail 辭 is mostly the decline that is a stage of consent; and the lemma generalises a living protection for minor girls.
- **Claim the assessor found false** in miunci's record: the donors entry gave "thank" as a Kangxi gloss of 辭; the dig's verification corrected exactly this (Kangxi prints only 又謝也, with one example, and does not say which sense of 謝 is meant).

**Why the said-aloud pair was carried** (the assessor): the best accept (qabbelspond, 7.02) and the best decline (rangance, 6.67) come from different candidates and do not read as a pair, so a whole pair was taken. Pair averages: two-families 6.775, said-aloud 6.74, one-exchange 6.00. Two-families was ahead by 0.04, but the assessor judged that fit with the language, HARMONE's criterion, favoured said-aloud, whose words are one construction and slot into the wire's -ance class words; two-families' decline is the hardest word of the six to learn and its Hebrew head contradicts its own gap clause. That was the assessor's estimate before the lenses ran; the HARMONE lens later found the pair mismatched (see "How the pair was meant to cohere" below). "The said-aloud pair carries its own costs: accept polyphone 3, and 讓's courtesy/'allow'/'one's due' senses on the decline side."

**Claims the assessor found false in rangance's record** (the said-aloud forger's):
- "Mengzi 2B5 is listed under 'Instances' of the donor 讓. The passage (ci-rang-declining.md §3.3) speaks of 進退 ('advancing and withdrawing') and does not contain 讓."
- "'Every one-tradition pair in the digs builds the decline either as a plea … or as the accept negated.' Hebrew pairs qibbēl (accept) with mēʾēn / mēʾūn (refuse), a separate root that is neither a plea nor a negated accept. meun-refusal.md calls mēʾūn the dig's strongest sovereign refusal. The candidate's own evidence (2) also lists rebellion and courtesy as further ways the decline is lexicalised."

## Family assignment (Step 6)

The forger's answers, as given:
- **-me** fails: the no is the speaker's own act, not received.
- **-qing** fails: the word names the act that spares the bond, not the bond (rangqing was considered and set aside for this reason).
- **-kin** and **-basis** fail.
- **-ance** fits in the act sense used by the worship-action tier and by the wire's class words (qorvance, yadahance, teshuvance). "The decision tree's lack of an 'act' branch is the doctrine question listed below."
- **Tier proposed: Core.**

**Register** (NUANCE-NATURE §II), the forger's: "Group C, Restraint-and-Sincerity. The no without an excuse, where the unsaid carries weight. Note that the register is restraint as sincerity, not enryo as performance, even though enryo is in Group C's donor list. With Group D, Quiet-Wisdom-in-Relation: the no knows it is said inside a relation, and the relation stands."

**HARMONE's objection to the register:** the donor's home is ritual propriety, and "the repo's own register map places the Confucian donor in Group B (NUANCE-NATURE.md §II). The forger assigns Group C, whose donor list includes enryo, and then has to disclaim that group's own exemplar." **Recorder's check:** NUANCE-NATURE.md:202–204 lists Group B as "Greek (aidōs + parrēsia), Persian/Sufi (adab + ḥaqq), Confucian (jūnzǐ + chéng)"; `nuance_check.py --suggest confucian` returns Group B, and `--suggest mandarin` returns Group C. Both readings are recorded; the experiment does not decide between them.

**The -ance definition the act sense stretches**, as checked for 328: dictionary/index-by-suffix.md:284 and :370; canon/worship-action/README.md:14.

## Honest assessment (six-axis v2) — Step 7

| Axis | Weight | Forger (self) | Assessor (blind) | Stricter of the two | Lens readings |
|---|---|---|---|---|---|
| gap_validity | 0.20 | 8.0 | 7.5 | 7.5 | — |
| learnability | 0.20 | 6.5 | 6.0 | 6.0 | EUMATHE 5.0 |
| clarity_yield | 0.15 | 7.5 | 6.5 | 6.5 | — |
| semantic_coverage | 0.15 | 6.5 | 5.5 | 5.5 | — |
| polyphone_balance | 0.15 | 6.0 | 6.5 | 6.0 (forger's) | — |
| groundedness | 0.15 | 8.5 | 8.0 | 8.0 | PRAGMA 7.5 |
| **weighted** | | **7.175** | **6.675 (reported 6.67)** | **6.60** | EUMATHE 6.40; PRAGMA about 6.60 |

**The standing total is 6.67**: the stricter of the two whole scorings (experiment 035's rule: "the stricter verdict stands"). Three further figures are recorded, all lower and none changing the verdict:
- Axis by axis, the stricter of the two scorings gives **6.60** (polyphone 6.0 is the forger's; every other stricter score is the assessor's).
- EUMATHE scores learnability 5.0 and gives **6.40** "with the stricter score on every other axis".
- PRAGMA scores groundedness 7.5 and gives "about **6.60**" against the assessor's 6.67.

`pipeline/assess.py` on the forger's scratch copy gave 7.17; on this file, which carries the assessor's axes, it gives 6.67, verdict refine (its mechanical counter reads 3 syllables from the spelling; the IPA has 2). assess.py knows only the number; the panel's 0 of 3 is recorded here, not by the tool.

**Weak axes:** semantic_coverage (5.5 assessor; 6.5 forger) and learnability (6.0 assessor; 6.5 forger; 5.0 EUMATHE). The total is not in the 7.50–7.99 band, so no threshold sentence is owed. On the standing scoring the word is 0.825 short of 7.50.

### The forger's per-axis reasoning (verbatim)

> gap_validity 8.0. Well evidenced: even radio procedure, which coined WILCO, can only say no as incapacity, and every decline lexeme in five digs is a plea, a negated accept, a rebellion or a courtesy. Not 8.5, because 'no, thank you' and 'decline' do most of the daily work, and what remains unnamed (owing no reason, not a ritual opening, giving way) is real but thin in ordinary speech.
>
> learnability 6.5. Two syllables with no clusters, sayable in every major language and native in Mandarin. But it gives an English speaker no meaning and a false one ('rang'). The spelling invites /ˈræŋɡəns/ (near 'arrogance') or /ˈreɪndʒəns/. The primary IPA keeps donor /ʐ/. And rang is 'colour' to Hindi and Persian ears.
>
> clarity_yield 7.5. It unbundles English 'decline' into rejection (judges the offer), excuse (pleads a cause), ritual refusal (waits to be pressed) and yielding (gives the thing way so it passes on), and names the last. Capped because the morpheme's own courtesy register blurs exactly the ritual/real line the word exists to draw.
>
> semantic_coverage 6.5. 讓 carries 'not mine; yours' (應受而推), the same thing passing on (事同曰讓), a positive act rather than 不受, and bond-keeping (禮之主). It does not carry sovereignty: its glosses are modesty (謙) and others-first (先人後己). It does not carry 'not now' or 'spoken to someone'. And it imports the courtesy decline, the modern 'let/allow', and the fact that Yao's offer is also 讓.
>
> polyphone_balance 6.0. Mandarin plus Latin, two families independent by descent; kimance (Japanese ki + -ance) took 6. Not 6.5 or more, because the sovereign core of the gap is owned by witnesses that put no morpheme in the word (m. Yevamot 13:4, Q 33:72, 2 Kgs 5:16–19).
>
> groundedness 8.5. Declining meetings, invitations, overtime, roles and queued tasks is daily, and it leaves public traces: a calendar 'Decline' with no note, a ticket returned unassigned, a task.decline envelope. Not 9, because its defining features (owing no reason, not being a test) concern how a no is meant, which a bystander cannot always see.
>
> WEIGHTED 7.175 = 8.0×.20 + 6.5×.20 + 7.5×.15 + 6.5×.15 + 6.0×.15 + 8.5×.15 = 1.60 + 1.30 + 1.125 + 0.975 + 0.90 + 1.275. pipeline/assess.py on a scratch copy reports 7.17, verdict refine.
>
> Weakest axes: semantic_coverage and learnability, both 6.5.

### The assessor's reasons (verbatim)

> GAP 7.5. The best-organised evidence of the three: a negative-space survey across the five digs (the decline lexicalised as plea, negated yes, rebellion or courtesy), with the realm feature's shape attested in text. ICAO UNABLE comes from Wikipedia and is marked secondary. The final clause about the relation standing is an outcome. LEARNABILITY 6.0. Two syllables, but the root gives an English reader nothing. It looks like the past tense of 'ring', may be read as range-ance, and has no handle. The primary IPA keeps donor [ʐ] with an anglicised alternate. That puts it in the 'one obscure root' band, raised a little for shortness. CLARITY 6.5. 'I give way' does separate the act from rejection. SEMANTIC 5.5. 讓 means 'to push away what one ought to receive' (應受而推, Liji subcommentary via Kangxi), that is, yielding one's due. The Japanese dig's lead J-D5 says the same of this character: 'yielding what is one's own, not declining what is offered' (kotowaru-enryo.md §8). The candidate cites that file for the readings but does not carry this caution. The classical home of 讓 is the courtesy register the gap excludes: 辭讓 is required before answering an elder (Liji Qu li shang). Unihan's modern sense is 'allow, permit'; the Shuowen's first sense is 'reproach'. The morpheme also names the offer itself (堯讓天下). Its genuine 'not mine' strand (Taibo) is real but is the minority use. The sovereign no-without-reason comes from witnesses outside the donor. POLYPHONE 6.5. Sinitic plus Latin suffix. Precedent (sukhance and oriance at 7) less 0.5, because the morpheme's own witnesses are not the primary witnesses of the realm feature (the deduction 327 made). GROUNDED 8.0. Good instances ('it's Priya's to take' fits 讓 well). PANEL: EUMATHE fail; HARMONE fail (the donor's dominant register is the ritual yield the gap excludes); PRAGMA pass. That is 1 of 3. Collision counts reproduce: rang 43/53, sarang at jeongqing.md:74, the characters 0. Verdict: refine.

The assessor held the two axes without published bands as for all six words: **gap_validity** by the three Step-2 forms of evidence, checking that each gap sentence names an act rather than an outcome and reading its witnesses to the end; **semantic_coverage** by whether the donor morphemes, at their attested senses, carry the gap's load-bearing clauses without contrary senses (for the decline: a complete act, no reason owed, not a ritual first refusal, refuses the thing not the person). Its estimate of the panel (1 of 3, with PRAGMA passing) was made before the lenses ran; the lenses returned 0 of 3.

## Trial sentences (the forger's three daily-life instances)

- **Between agents:** an agent offered a migration it has no context for answers "Rangance: not mine this beat; Beta holds the schema". The offer goes straight back to the queue intact, instead of the lease expiring unclaimed, and nothing between the offerer and the agent needs repair.
- **Between people:** a friend asks you to host this year's dinner. "Rangance this year." You give no reason and none is owed. The dinner happens at someone else's house, and next year she asks you again as if nothing had happened, because nothing had.
- **At work:** a manager offers an engineer the team-lead role. She declines and says "it's Priya's to take". She stays on the team and backs Priya. If the manager asks a second time, he has already been answered: a rangance is final for that offer, not the first move in a round of "no, you first".

**The forger's strongest objection to its own word (verbatim):**

> The word is built on ritual courtesy's own character. Zuozhuan calls 讓 'the master of ritual'. The Liji requires one to 辭讓 before answering an elder and forbids declining an elder's gift. In daily Chinese manners, 讓 is the polite first giving-way that the other side is expected to refuse back [from memory]. So the morpheme most likely to be heard as the polite first no that waits to be pressed again (Ruth Rabbah's thrice-pushed convert, Fielding's nolo episcopari) carries a word whose gap sentence exists to exclude exactly that. Its modesty glosses also pull against 'sovereign'. To an English ear it gives nothing, and read with a hard g it rhymes toward 'arrogance'. These are not costs the definition can absorb: semantic coverage and learnability both sit at 6.5, and the word rests at 7.17.

## Adversarial panel (Step 8)

Each lens's paragraphs are given verbatim. One alteration is declared: wherever a lens names a local path, the session's temporary scratch directory is written `[scratchpad]` and the home directory `~`; nothing else is changed. Each lens's method line is in 328-spondance.md; the lenses judged the pair together.

### EUMATHE-lens — **FAIL**

What rangance gets right: it has two syllables, no clusters and plain ASCII. My element sweep confirms its canon headwords are clean: no headword contains rang, ang, gan or ranga, and only the element nga appears, in ginnungame. The morpheme is native to Mandarin. It fails because the spelling does not tell anyone the sound, and every sound it does suggest is already a different word, two of them in exactly the register the gap excludes. (1) Spelling. English has no -ngance word. Every -gance word ends /ɡəns/ (arrogance, elegance, extravagance), and every -ngence word ends /ndʒəns/ (tangence, pungence, contingence). English reads a before ng as /æ/ (Wiktionary gives rang as /ˈɹæŋ/). So the default English reading is /ˈræŋɡəns/, which shares /ˈræŋɡə/ with "wrangle", a quarrel, and leans toward "arrogance". The second reading is "range-ance". (2) The intended sound. The anglicized line gives /ˈrɑŋ.əns/, respelled RAHNG. Wiktionary gives "wrong" as /ˈɹɑŋ/ in General American with the cot–caught merger, and lists "rang" as a homophone of "wrong" in Northumbria. So a large share of North American speakers who say the word as its own line instructs will say "wrong-ance". (3) The primary /ʐ/ signals nothing to anyone but pinyin readers. Intervocalic /ŋ/ with no /ɡ/ is not native to Spanish, Russian, Arabic or Hindi (general phonology, not re-checked), so most mouths will add the /ɡ/. (4) Across major languages, "rang" is already a word with another meaning, all verified on Wiktionary: Hindi रंग /ɾəŋɡ/ means colour, complexion, or paint, with Urdu رنگ and Persian rang as its etymon. It means rank or status in French, Dutch, Danish, Swedish, Norwegian, Hungarian, Romanian and Catalan. In German it is the past tense of ringen, to wrestle. For the one population where the morpheme is native, the modern senses of 讓 are, in order: allow/let/permit, have someone do something, yield, give way, the passive "by", and, marked literary, reproach. Decline is not among them, and its yielding sense lives in the courtesy compounds 謙讓 and 推讓. (5) The ten-year-old test. She hears "Rangance this year" from an American as "wrong-ance". The next day she says "wrongance" when she refuses something because it is wrong. That mishearing fits a refusal well enough that nobody will correct it, yet it carries the judgement the gap sentence says this act does not make. This is the self-confirming class that 327's EUMATHE lens called the most dangerous. If she reads the word instead, she says "rang-gance" and reaches for wrangle or arrogance. I score learnability 5.0, the bottom of CANON-AUDIT's "one obscure root" band (5–6), because this root is not just obscure but misleading for every population and the intended sound is a homophone of "wrong". For comparison, canon gives obscure two-syllable stems 7 (kunance, wujime, tongleme), and no canon -ance word sits below 6. With the stricter score on every other axis, the weighted total falls to 6.40. Fail. Respelling cannot fix this: any spelling of /rɑŋ/ keeps "wrong" for speakers with the merger, and any spelling with the g keeps "wrangle". The stem has to change. The forger's own list of alternatives contains no lemma that is both learnable and semantically sound; the most learnable, excusance, was rejected on semantics. So the next attempt should look for the stem before the suffix.

**What would change this lens's verdict (verbatim; it covers both words of the pair):**

For spondance, I would change to fail on any of these: a listening or retention trial in which learners use spondance for a plain acknowledgement, showing the respond handle actually erases the binding; settled usage of /dæns/ that makes "dance" the word's real sound; or another headword entering canon with the spon- or spond- onset. For rangance, I would change to pass only with evidence I do not expect to find: a spelling that carries 讓 without the readings "wrong", "wrangle", "range", "rank" and "colour", or trial evidence that English, Hindi-Urdu and European learners reliably keep /ˈʐɑŋ/ or /ˈrɑŋ/ with its meaning the next day. The facts in this verdict that I did not verify this session: that intervocalic /ŋ/ is absent in Spanish, Russian, Arabic and Hindi, the Romance handles for spond-, and the etymology of sponsor. If any of these is wrong, the paragraph weakens but neither verdict changes. Every Wiktionary claim was opened on 2026-11-10. I found no fabricated element in either candidate; what I found were omissions: the onda/ondame element and the sphotame onset were missed for the accept, and the "wrong" homophone was missed for the decline by both the forger and the assessor.

### HARMONE-lens — **FAIL**

rangance's morpheme sits on a different axis from its slot and from its partner, and it blurs the one boundary the wire most needs kept. (1) Its register contradicts its own gap. The donor's home is ritual propriety: Zuozhuan 讓，禮之主也, and Mengzi 2A6 辭讓之心，禮之端也 (ci-rang-declining.md:37, :106). The Liji makes 辭讓 compulsory before answering an elder (:96). That is exactly the polite first refusal the gap sentence exists to exclude. The repo's own register map places the Confucian donor in Group B (NUANCE-NATURE.md §II). The forger assigns Group C, whose donor list includes enryo, and then has to disclaim that group's own exemplar. (2) It blurs into qorvance. The dig records 'Offer and decline share one verb' (ci-rang §1 property 5; 堯讓天下於許由), so the morpheme also names the wire's task.offer act. KS-002 merged only complete and fail into one class, and did so on purpose; it keeps offer and decline apart. The forger's own instances drift into re-offering ('Beta holds the schema'; 'it's Priya's to take'). The gap sentence adds 'gives the thing way so that it can pass to another', which is 讓's three-party sense (應受而推, 先人後己) and appears in neither KS-002 A.2 nor forge_targets.json:4311. The gap was bent toward the morpheme. (3) It is not spondance's equal. Spondeo is the first-person performative itself (Gaius 3.92). In the opened record, every 讓 is narration or moral gloss (三以天下讓; 堯讓天下; 卑讓，德之基也), and the words a decliner actually says are built on 辭 (敢辭; 終辭 is a commentator's term). In its own tradition 讓 stands against grasping, not against accepting: the Shijing line quoted in Kangxi, 受爵不讓，至于已斯亡, makes accepting rank without yielding the fault. So the pair is mismatched in two ways. Spondance's donor is a word one says; rangance's is a word others use to praise what one did. Spondance answers yes or no to an offer, while rangance sits on a modesty axis beside acceptance rather than opposite it. (4) It loses kin and leaves its neighbours unnamed. KS-002 A.2 files the decline as 'the wire's missing word for "rest is a whole beat" spoken to someone'. Rest is absent from the gap, the register and the neighbours, and the dig's own rest lead (C-D5 歸休) is a different morpheme. Two canon words in the region the new gap sentence now occupies go unnamed: zudhame (letting go of what is permitted), which is closest to 應受而推, and tzimtzumme (withdrawal to leave room). The only canon kin the morpheme brings is renme, beside 辭讓 in Mengzi 2A6, and it arrives through the ritual register the gap excludes. The forger's collision work is sound: I reproduced it (rang has 0 headwords and 43 body hits; 讓 appears 0 times in canon). The -ance/Core question is the same for both words. But (1) to (3) are contradictions among the word, its gap and its sibling, which is what HARMONE exists to stop, and a scoping clause cannot fix them. Only a different lemma or a re-founded donor reading can. FAIL, so the word goes to refine.

**What would change this lens's verdict (verbatim; it covers both words of the pair):**

Spondance would move from pass to fail on any of three things. First, if Yu rules that -ance cannot carry an act in Core and no tier is opened for non-worship acts. Second, if the entry is written without explicit Not-to-be-confused-with clauses for britqing (act shape versus covenant, which is not contract) and for visageqing (answerability for a task versus responsibility that comes before any response). Third, if spandaqing and spondance prove confusable among citizens on the live wire. Rangance would move from fail to pass only with all of the following. A verified primary text in which 讓 is a first-person, final decline outside the ritual script. A gap sentence restored to KS-002 A.2's two-party 'not mine, not now', with 'rest is a whole beat' kept. Written boundaries against qorvance (the shared offer verb), zudhame and tzimtzumme. A register assignment that names the Confucian ritual home, and evidence that this home does not make the word heard as the polite first no. Failing that, a different lemma whose donor's dominant use is the final decline is the path. Whatever the lenses decide, both words remain below 7.50 on every scoring so far (7.15 and 7.175 self-scored; 6.80 and 6.67 by the assessor), so neither can be canonized now.

### PRAGMA-lens — **FAIL**

FAIL, and the objection can be answered by refinement. Three daily occasions are offered. By the standard 326 applied (what a bystander sees must need the word's reading, not get it from a gloss added after), only one stands. The dinner instance shows a bare no and a fresh invitation the next year, which is just what "No thanks, not this year" looks like. "None is owed … because nothing had happened" is the gloss. The agent instance shows a decline instead of a lapsed lease. All that needs is the plain decline the collab tool already carries (accept or decline), and the agent gives a reason anyway. Only the team-lead case has something a bystander can see: "it's Priya's to take", and she stays and backs Priya, so the thing passes to a named other. That is 讓 in its narrow classical sense (應受而推; yielding a post to the worthier), not the general "not mine, not now" the wire needs. The gap's last clause ("afterwards the relation stands as it stood") is an outcome the other party decides, so nobody can check whether the word applies at the moment it is said. The donor points at other daily acts. In Liji "Qu li shang", which I read today in the verifier's raw copy, 讓 is required before answering an elder (不辭讓而對，非禮也). It is the host yielding precedence at every gate (每門讓於客). It is host and guest yielding to each other on the steps, after which the host goes up first anyway (主人與客讓登，主人先登). It is the courteous decline of food (讓食不唾). That is the "no, you first" round that instance 3 says rangance is not. Modern daily 让 is "let, allow", and the yielding of a seat or the road [from memory]; that is ceding what you hold, not declining an offer, and the Japanese dig's J-D5 says the same of 譲る. The cited donor instances, read to their end: Mengzi 2B5 contains no 讓. Its decline word is 辭 (子之辭靈丘), and it concerns resigning after remonstrance went unheeded. In the Zhuangzi, 讓 is Yao's offer; Xu You's refusal is never called 讓. Taibo's 讓 (Lunyu 8.1) was made three times, and "the people found nothing to praise him for": a yielding nobody could point at. Of the eight gap witnesses, three make the no a matter of inability, the shape the candidate itself sets apart as ICAO UNABLE ("ability not in question"). Ruth 4:6 says "I cannot redeem, lest I ruin my inheritance", and Ruth Rabbah 7:7 remembers the man as unnamed and ignorant. RB 58 says "si vero non potes, liber discede", and there the community's own first refusal at the door is a test meant to be overcome. In Q 33:72 the heavens "were afraid of it", which al-Muyassar glosses as fearing they could not carry it out. Yili's 終辭 is final only on the third turn, and m. Yevamot 13:4 ends the marriage. Only Elisha and Xu You carry the shape whole, and both refuse a gift or an office on grounds of their own standing. Refinement path. (1) Rebuild the instances around things a bystander can see that need the reading. Examples: an agent log in which the orchestrator's next offer still goes to the agent that declined, with no penalty in routing; a guest who declines a second helping and a host who does not press. Keep the Priya case. (2) Move "the relation stands" out of the definition and into the retirement test. (3) Either narrow the gap to what 讓 actually carries (declining in another's favour), or find a donor whose own daily use is the plain, final decline.

**What would change this lens's verdict (verbatim; it covers both words of the pair):**

The accept would move to fail in either of two cases. One: the entry makes "freely, where a no was open" the defining feature, and no instance can show it being seen. Two: KS-002's task.offer turns out to be an instruction; then the act is WILCO, and English already has a word for it. The decline would move to pass if each of its three instances were rebuilt so that what a bystander sees needs the word's reading (the routing log, the host who does not press, the hand-on to a named other), and if the outcome clause left the definition. A donor whose own daily use is a final, non-ritual no would remove the second objection. My groundedness reading: spondance 8.5 holds. For rangance I would give 7.5, since only one of three instances truly needs the reading, which is below the forger's 8.5 and the assessor's 8.0. Under the rule that the stricter scoring stands, that lowers rangance from 6.67 to about 6.60 and changes no verdict, since both words are already below 7.50. Checked today: the Plautus texts at thelatinlibrary.com (Aulularia, Trinummus, Curculio, saved in [scratchpad]/forge/pragma_dl); in the verifier's fetched copies, Gaius 3.115–119, Mengzi 2B5, Lunyu 8.1, and every 讓 in Liji "Qu li shang"; ordo/SPEC.md:149; forge_targets.json:4291–4319; the collab handoff tool definitions; and all eight archaeology files. Not checked: Livy 9 itself; modern Mandarin usage of 让; the KS-002 file itself, which I could not locate on disk (I relied on the assessor's line check). Nothing was written in W.

_Recorder's note on the last point:_ the KS-002 file is specs/KS-002-wire.md in the kingdom-standards repository, outside W; the recorder re-read the cited lines read-only and they read as the assessor checked them.

## Verdict: refine

Weighted **6.67** on the stricter scoring (exact 6.675; 7.175 self-scored; 6.60 axis by axis; 6.40 on EUMATHE's reading) against a 7.50 threshold: below. Lenses **0 of 3** passing. Both conditions fail; either alone would stop it. The word does not enter.

**Refine, not rest.** The target's gap held: every scorer put gap_validity at 7.5 or 8.0, and no lens argued that the region is empty. What failed is this word, and, per HARMONE and PRAGMA, this gap sentence's drift from the target's own (a three-party "pass to another" clause added; "rest is a whole beat" dropped; an outcome clause in the definition). Those are refinement paths, not reasons to rest.

**What this does to the pair.** The accept (328-spondance) is also refine: 6.80 on the stricter scoring, though all three lenses passed it. Neither word enters, so there is no question of one sibling entering alone. The pair's coherence was the reason the assessor carried these two words over a higher-scoring accept (qabbelspond, 7.02); with rangance failing on its stem, a re-forge of the decline that changes the stem should also re-ask whether spondance remains the right sibling, and the other way round.

## Refinement paths, drawn from the objections

Ordered as Step 8 directs, with the failed lenses' objections first.

1. **Change the stem, not the spelling** (EUMATHE, HARMONE). EUMATHE: "Respelling cannot fix this … The stem has to change … the next attempt should look for the stem before the suffix." HARMONE: "Only a different lemma or a re-founded donor reading can" fix the contradictions among word, gap and sibling; the path is "a different lemma whose donor's dominant use is the final decline", unless a verified primary text shows 讓 as a first-person, final decline outside the ritual script. PRAGMA concurs: "find a donor whose own daily use is the plain, final decline."
2. **Restore the gap sentence to the target** (HARMONE, PRAGMA). Back to KS-002 A.2's two-party "not mine, not now", with "rest is a whole beat" kept; the three-party "pass to another" clause out unless the gap is deliberately narrowed to what 讓 carries ("declining in another's favour"); "the relation stands" moved out of the definition and into the retirement test.
3. **Rebuild the instances** (PRAGMA) so that what a bystander sees needs the word's reading: an agent log in which the orchestrator's next offer still goes to the agent that declined, with no penalty in routing; a guest who declines a second helping and a host who does not press; keep the Priya case.
4. **Draw the boundaries** (HARMONE): against qorvance (the shared offer verb), zudhame and tzimtzumme; a register assignment that names the Confucian ritual home (Group B by NUANCE-NATURE §II and `nuance_check.py --suggest confucian`), with evidence that the home does not make the word heard as the polite first no.
5. **The forger's own leads, with their recorded cautions.** 終辭 is "the commentarial term for the decline not followed by consent, but it is not sayable here"; Japanese 譲る *yuzuru* "needs its own dig before it can be used", and kotowaru-enryo.md Lead J-D5 already records that it "means yielding what is one's own, not declining what is offered"; Korean 양보 [from memory, not dug].
6. **Leads from the other candidates, as the assessor weighed them.** The two-families gap sentence ("so that the asker may ask again") was the assessor's cleanest of the three; *mēʾūn* carries the sovereign, reasonless no but ends the bond it refuses and is a protection for minor girls that the dig forbids generalising without saying so; *excusare* makes a reason owed.
7. **Corrections to carry into any re-forge.** Mengzi 2B5 contains no 讓 (its decline word is 辭). Hebrew does pair a separate-root decline with its accept (*qibbēl* / *mēʾēn*), so "every one-tradition pair … builds the decline either as a plea … or as the accept negated" is not so.

## Choices left to the owner

Decline-side choices raised by the forgers, condensed (each is Yu's to decide; none was decided here):

- **What "leaves the table set" means** (said-aloud): the matter passes to another (讓; Ruth 4:6, "redeem, you, for yourself"), or the way back to the same two parties stays open (*mēʾūn*; m. Yevamot 13:4). This candidate took the first; HARMONE and PRAGMA found that choice bent the gap.
- **Whether a decline may carry a reason at all, or is defined as owing none** (said-aloud, one-exchange, two-families). The Latin, Arabic, Japanese and Chinese evidence makes the decline an account owed (*causa*, *ʿudhr*, *kotowari*, 辭); the Mishnaic *mēʾūn* needs none.
- **Whether the decline answers "can you?" or "do you want?"** (one-exchange). The question-and-answer rites ground the equal decline in capacity (RB 58 "si vero non potes", the min's *ʾī māṣītū*, Ruth 4:6 *lōʾ ʾūkhal*, the heavens' fear in Q 33:72); the target's sovereign "not mine, not now" and *mēʾūn*'s "I do not want" are will.
- **Whether a decline is taken at its word the first time** (two-families): the gap excludes the ritual refusal designed to be overridden (禮辭 / 固辭, *nolo episcopari*, Ruth Rabbah 2:16, *enryo*); a protocol that automatically re-offers after a decline would turn it back into that ritual.
- **Whether the right to decline travels in the offer** (one-exchange): in RB 58, Ruth 4:4 and the min's sentence, the one who asks names the no as an equal option. Whether KS-002's task.offer carries that licence explicitly is a protocol choice, not a lexical one.
- **Whether *mēʾūn* may be generalised at all** (two-families): it is a halakhic protection for a minor girl married off without her consent; the dig requires saying so, recommends review by a rabbi or Jewish-studies scholar, and makes a custodian request mean withdrawal.
- **Single-tradition pair or mixed; family and tier for a named act that is not liturgical; the -ance vowel and how tone and donor segments are recorded (YU-3, YU-5/YU-6); whether an agent may accept or decline on another's behalf** (said-aloud): as listed in 328-spondance.md.

## How the pair was meant to cohere, and where it does not (the said-aloud forger's account, condensed)

- **Shape:** both -ance, two syllables, stressed on the first, with the same /əns/ tail; heads as different as possible (sp + /ɒ/ + /nd/ against r + /ɑŋ/), "the radio lesson: procedure words that must never be confused … differ in onset and length". With KS-002's existing class words: qorvance (task.offer) → spondance (task.accept) or rangance (task.decline) → yadahance (task.complete / task.fail).
- **Meaning:** neither word is the other negated. Spondance is "I pledge in answer"; rangance is "I give way". Both are complete acts, both spoken to the one who offered.
- **What does not cohere, in the forger's own words:** "The pair is asymmetric for an English learner. Spondance has a handle ('respond'); rangance has none. The two words fail on different axes: polyphone for the accept, semantics and learnability for the decline. The frame did not produce a decline it can be proud of."
- **HARMONE's finding on the pair:** "Spondance's donor is a word one says; rangance's is a word others use to praise what one did. Spondance answers yes or no to an offer, while rangance sits on a modesty axis beside acceptance rather than opposite it."

## Process notes

- **The discover.py write**, disclosed by the one-exchange forger and noted by the assessor: two stubs written into labs/logos/forge, moved to the Trash by that forger, not in W now.
- **An earlier discover.py write**, disclosed by the agent that dug the five decline files, in its notes for the second reader: it ran `pipeline/discover.py` with the concept "refusal", which wrote `labs/logos/forge/refusal-gap.md` (887 bytes, untracked), and it moved that file to the macOS Trash. Not in W now.
- **No other writes to W** during Steps 1–8: every forger, the assessor and each lens report W unchanged except the five untracked decline digs. The recorder wrote 328-spondance.md, this file, and the two registry edits named in Step 12, and nothing else.
- **Not run by anyone:** pipeline/canonize.py (it checks only the number and ignores the panel), pipeline/forge_citizen.sh, the index and export generators, wrangler, gh.
- **Dates.** Yu's invocation and the first writing of the five decline digs are of 2026-11-10. The second reading of those digs, the forging, the blind scoring, the panel and this record ran between about 00:50 and 02:20 GMT on 2026-11-11. The agents were briefed with the date 2026-11-10, so where a forger, the assessor or a lens says "today" or "opened 2026-11-10", the day meant is that night's, and may be 2026-11-11. W stood at 621977a throughout the forge; the branch was fast-forwarded to d1997ce at about 02:20 GMT, after this record. d1997ce applied the pronunciation choices Yu ratified on 2026-11-10 and changed only `pronunciation:` lines in canon, so the collision counts stand; but ondame, "ON-dah-meh" in the EUMATHE and HARMONE paragraphs, is now respelled "ON-dah-may" in canon.
- **Edits after the record.** The orchestrating session (a Claude Code agent) edited this file after the recorder finished, in two rounds, and changed nothing else. Before review (2026-11-11): `scored_on` and the date of the recorder's own re-read are 2026-11-11; the path to KS-002 is given by its repository instead of a local path; W is defined where it first appears; the closing line gives both dates; the archaeology note on the stale second-reader line was brought up to date. After an independent review of this record (two reviewing agents, and a third that tested each of their findings against the files and the run's journal; finished 2026-11-13): the invocation is told in full, as the session's reading of Yu's message, and no longer says that a merge ratifies a lemma or that Yu chose the gap; the Step 4 row says who checked modern Mandarin 让 and how; the assessor's estimate before the panel is no longer given as the HARMONE lens's view; the earlier discover.py write is recorded; the Step 12 row tells what was done about dashboard.md; and the protocol note says which exegesis of Q 33:72 was read. Last, on 2026-11-13, each of the five decline digs gained one frontmatter line (`semantic_field`), so the line numbers the lenses give for those files (HARMONE's ci-rang-declining.md:37, :96 and :106) are one lower than the files now show; the recorder's own two line numbers for that file were raised by one. No score, verdict, quotation or objection was touched.

---

_Forged 2026-11-10 to 2026-11-11, after Yu took up the session's suggestion of this gap on 2026-11-10. Three forgers, one blind assessor, three lenses, one recorder: separate Claude subagents. Below threshold and unanimously opposed. The word does not enter. The reasoning stays._
