# Tiantai lemma notes: shapes on the Chinese reading, and an element-level collision check

Companion notes. They accompany
`archaeology/chinese/tiantai-yinian-sanqian.md`.
Written 2026-11-10 by a Claude Opus 5.5 subagent. **No scores are proposed anywhere in this file.**
Grep target: main at `eca7c99` (2026-11-10), directory `canon/`,
267 `.md` files: 263 entries and 4 READMEs (canon/, core/, mathema/, worship-action/). The root index `canon.md` is checked only where noted.

Experiment 326 asked for one thing above all: grep *elements*, not just the compound (326:218).
That is done in part 2.

---

## 1. Candidate lemma shapes on the Chinese reading

Each shape gets its IPA, its syllable count, what it keeps, what it loses, and its attestation.
Mandarin IPA for 一念三千 and the homophones comes from the Wiktionary pages opened this session.
Mandarin IPA for other morphemes is derived by the standard pinyin-to-IPA correspondence [from memory].
The -me tail is given as the canon writes it, /meɪ/.

| # | Shape (ASCII file / display) | IPA (Mandarin-faithful; then the canon-style anglicized guess) | Syl. | Keeps | Loses or risks | Attestation of the Chinese |
|---|---|---|---|---|---|---|
| A | `yiniansanqianme` / *yinian-sanqianme* (display could also be tone-marked *yīniàn-sānqiānme*, or hyphenated at the suffix seam, *yiniansanqian-me*) | [i³⁵ ni̯ɛn⁵¹ sän⁵⁵ t͡ɕʰi̯ɛn⁵⁵] + /meɪ/; anglicized ≈ /ˌiː.njɛn.sɑːnˈtʃjɛn.meɪ/ | 5 | the whole label: moment + inventory | tone loss (part 3); the q problem (part 2.6); "-ian" eye-parse (part 2.3); anglophone recognition of "ichinen sanzen" | Zhanran's label; first attested in his commentaries (T1912 fasc. 5 ×7; T1717; T1927; T1719). Not in Zhiyi |
| B | `sanqianme` | [sän⁵⁵ t͡ɕʰi̯ɛn⁵⁵] + /meɪ/ | 3 | the inventory; attested Tiantai shorthand 「並以三千而為指南」 (T1912 296a08–09); DDB s.v. 三千 | **the moment, which is the gap's pole**; collides in Chinese Buddhist usage with 三千(大千世界), the trichiliocosm (1000³ worlds), which is a different number and a cosmology; 三遷 is a full homophone | attested as shorthand, Zhanran onward |
| C | `jusanqianme` (具三千 "is endowed with the three thousand") | [t͡ɕy⁵¹ sän⁵⁵ t͡ɕʰi̯ɛn⁵⁵] + /meɪ/; anglicized ≈ /dʒuː.sɑːn.tʃjɛn.meɪ/ | 4 | Zhiyi's own verb-phrase, 「即具三千」 (T1911 54a08–09) | 具 is the containment verb whose 橫 reading Zhiyi refuses at the ultimate level and re-admits only as expedient (dig §3.2); it is a verb phrase, not a nominal term; 326 already flagged the 即具 misreading; English hears "ju" as /dʒuː/ | Zhiyi (as a phrase, not a term) |
| D | `sanqianzaiyinianme` (此三千在一念心, minus 此 and 心) | [sän⁵⁵ t͡ɕʰi̯ɛn⁵⁵ t͡sai̯⁵¹ i³⁵ ni̯ɛn⁵¹] + /meɪ/ | 6 | the only shape that is literally Zhiyi's clause (T1911 54a07–08) | length (EUMATHE); 在 "is in" is a locative-containment verb, worse than 具 for a region defined by 非橫 | Zhiyi |
| E | `yinianxinme` (一念心) | [i³⁵ ni̯ɛn⁵¹ ɕin⁵⁵] + /meɪ/ | 4 | Zhiyi's term for the moment (54a08, 54b20) | the whole inventory; generic | Zhiyi |
| F | Middle Chinese-based, e.g. from Baxter *'jit nemH sam tshen* | /ʔiɪt̚ nemᴴ sɑm t͡sʰen/ (Zhengzhang) | — | closeness to Zhanran's own Tang pronunciation | a reconstruction, not a living reading; no speech community; noted only so the option is on record | — |
| G | Cantonese-based, *jat nim saam cin* | /jɐt̚⁵ niːm²² saːm⁵⁵ t͡sʰiːn⁵⁵/ | — | a living reading with final stops | no canon precedent for a Cantonese donor morpheme: `grep -rli cantonese canon` hits only `canon/slipsooth.md`, which reports a Cantonese anecdote and its phonology but takes no Cantonese morpheme into a lemma [checked by the verifier, 2026-11-10]; no reason to prefer it over Mandarin for a Sui-Tang text | — |

Two notes that bear on any shape:

- **The forge record already gives two different IPA for shape A.** 326:124 has `/ˌiː.njɛnˈsɑːn.tɕʰjɛn.meɪ/` (stress on *san*), and 326:191 has `/ˌjiː.njɛn.sɑnˈtɕʰjɛn.meɪ/` (stress on *qian*). Whoever re-forges should settle one.
- **Any shape from the label is Zhanran's, not Zhiyi's** (dig §3.3). C, D and E are Zhiyi's words but not his terms. The gap-sentence has to absorb the dig's §3.2 (refusal at the ultimate, re-admission as expedient) before *any* shape is scored. Otherwise the shape inherits a selectively quoted source.

---

## 2. Element-level collision check against canon/

Method: `grep -rniw` (whole word, case-insensitive) and `grep -rni` (substring) over `canon/`. Also a match
against the 267 lemma file-names. Run 2026-11-10. Hits are reported with file:line.

### 2.1 `yinian` (and yi-nian, yīniàn, yíniàn, Wade-Giles i-nien)

- Whole word: **0**. Substring: **0**. Lemma names: **0**.

### 2.2 `yi` (and yī)

- Whole word: **0**.
- Lemma-name substrings: `canon/core/chayimme.md` (Hebrew *chayim*, /xaˈjiːm.meɪ/ at :5) and `canon/core/ereckappayime.md` (/…pɑː.ji.meɪ/ at :5). The latter already ends in the syllable sequence /ji.meɪ/. That is no collision for shape A, but it would be for any short *yi-me* form.

### 2.3 `nian` (and niàn, Wade-Giles nien)

- Whole word: **0**. Lemma names: **0**.
- Substring: **103 lines**, every one inside an English word in -nian(s). The commonest, counted as occurrences (`grep -rnio '[a-z-]*nian[a-z]*'`, re-counted by the verifier; the earlier figures here did not match any count): armenian 33, babylonian 16 (plus neo-babylonian 2), augustinian 16, plotinian 13, eleusinian 9, iranian 6, indo-iranian 6. Also romanian, athenian, thessalonians, lithuanian, bergsonian, wittgensteinian, riemannian, pyrrhonian, kuhnian, hamiltonian and avestan-iranian. Files include `canon/core/maatme.md`, `canon/core/shinjinme.md`, `canon/core/hanme.md`, `canon/core/balagme.md`, `canon/worship-action/yadahance.md` and `canon/dokimance.md`; the full list comes from `grep -rli nian canon`.
- **Hazard (an observation, not a score):** in a corpus this full of -ian adjectives, *yinian* reads to an English eye as an adjective, "Yin-ian", parsed as *yin* + *-ian*. *Yin* is already in the corpus (2.8).

### 2.4 `sanqian` (and san-qian, sānqiān)

- Whole word: **0**. Substring: **0**. Lemma names: **0**.

### 2.5 `san`

- Whole word: **4 lines**.
  - `canon/core/ihsanme.md`:5 (pronunciation /ˈiː.sɑn.meɪ/, the syllable of Arabic *iḥsān*).
  - `canon/core/sankofame.md`:5 (pronunciation /sɑn.ˈkɔ.fa.meɪ/).
  - `canon/core/sankofame.md`:25 and :73, where **Twi *san* "return" is a recorded morpheme**: 「Twi san "return" + kɔ "go" + fa "take/fetch"」.
- Lemma names: `ihsanme`, `sankofame`.
- So "san" is not free in the canon. It is a glossed donor morpheme meaning "return" in one entry, and a word-initial *san-* syllable in a 4-syllable -me lemma. Shapes A and B would put a second, unrelated *san* beside it.
- Substring "san" is ubiquitous in English (thousand, Sanskrit…) and was not counted.

### 2.6 `qian` (and qiān, Wade-Giles ch'ien / chien)

- Whole word: **0**. Substring: **0**. Lemma names: **0**.
- **But the letter q is already contested in the canon.** This is the near-homophone class at issue:
  - **The `-qing` suffix**, the felt-bond family (`dictionary/index-by-suffix.md`:23, :235: "35 members", Mandarin 情). The 35 files are 34 in `canon/core/` and 1 in `canon/mathema/`; `allostasisqing` stands in both. *qian* and *qing* differ by one vowel and the nasal (/i̯ɛn/ against /iŋ/). Spelled, they are q-i-a-n against q-i-n-g. A reader scanning for family markers sees *-qi-* and expects *-qing*.
  - **The canon renders its own -qing onset three ways** (first `pronunciation:` field of each of the 35 files):
    - aspirated /tɕʰ/ in **20**;
    - unaspirated /tɕ/ in **8**: `barakqing`, `darshanqing`, `hayatqing`, `jeongqing` (/t͡ɕʌŋˈt͡ɕɪŋ/ at :5), `kinqing` (/ˈkɪn.tɕɪŋ/ at :8, "with Mandarin q as /tɕ/"), `natsarqing`, `panimqing`, `zakarqing`;
    - English /tʃ/ in **7**: `britqing`, `danaqing`, `ifeqing`, `mahabbahqing`, `paqduqing`, `syzygyqing`, `tarabqing`.

    Mandarin 情 *qíng* is /t͡ɕʰiŋ³⁵/, aspirated [verified: Wiktionary 情]. So `kinqing`:8's statement that Mandarin q is /tɕ/ is wrong; /tɕ/ is pinyin *j*. A *qian* lemma would inherit a q the canon has not settled.
  - **`script/morphemes.json`:454** registers *qing* (U+E126, Mandarin 情, used_in `kinqing`).
  - **`canon/worship-action/qinance.md`** (Hebrew *qinah*, -ance family) spells Hebrew qof with q. The file has no pronunciation field at all. So the canon has q for /k/ (qinance) beside q for /tɕʰ/ (most -qing), and *qinance* begins with the same three letters as *qin-g*.
  - **`canon/core/wakanme.md`:150** has Chinese *qi* (氣) as a whole word; *san-qi-an* contains it.

### 2.7 `sanzen`, `ichinen`, `nen`, `zen` (for completeness, on the Japanese reading)

- `sanzen` whole word: **6 lines**: `canon/core/satorime.md`:59, :63, :88, :98; `canon/core/daigome.md`:75; `canon/core/kenshome.md`:38. Root `canon.md`:33 and :38 also carry it. These match experiment 326's list.
- `ichinen`, `nen`: **0**.
- `zen`: 51 lines in 15 files (Zen Buddhism). This is the reason the Japanese reading's tail is hazardous.

### 2.8 `yin`, `qi`, `ju`, `zai`, `xin`, and the CJK characters

- `yin` whole word: **8 lines**. Seven are yin-yang: `canon/core/syzygyqing.md`:76; `canon/core/ngünecheme.md`:16, :82; `canon/core/chiasmqing.md`:38; `canon/core/wujime.md`:36, :39, :85. The eighth, `canon/core/tengrime.md`:57, is the Mongolian genitive in "Möngke Tngri-yin küčündür", not yin-yang (corrected by the verifier). This is the other half of the "Yin-ian" eye-parse in 2.3.
- `qi`: 1 line (`canon/core/wakanme.md`:150).
- `ju`, `zai`, `xin`: 0 whole word. `ju` appears inside the lemma names `tjukurpame` and `wahdatwujudme` only.
- 一念, 三千, 念, 千, 三: **0**. 一: 1 line, inside a Cantonese quotation (`canon/slipsooth.md`:37, 「一代傳一代」), unrelated.
- Tiantai, Zhiyi, Zhanran, Nichiren, Tendai, Saichō, 天台, 智顗, 湛然, 摩訶止觀: **0** in `canon/`.

### 2.9 Canon precedent for Mandarin donors

All four Mandarin-donor -me lemmas are toneless in their file names and pronunciation fields:

- `canon/core/daome.md`:5 /daʊ.meɪ/;
- `canon/core/renme.md`:5 /ˈʐən.meɪ/;
- `canon/core/wujime.md`:6 /ˈwuː.dʒi.meɪ/ (the prose writes *wújí* with tones);
- `canon/core/tongleme.md`:5 /ˈtɒŋ.le.meɪ/.

So the house convention already accepts tone loss. Part 3 records what that costs here specifically.

---

## 3. Tone loss in romanization — a real cost, recorded, not scored

1. **The label's own tones are not its spoken tones.** The citation form is yī-niàn sān-qiān (tones 1-4-1-1). Mandarin sandhi turns 一 before a fourth tone into a second tone, so it is spoken *yíniàn* [i³⁵ ni̯ɛn⁵¹] [verified: Wiktionary 一, sandhi note]. A tone-marked display (*yīniàn*) shows the citation form, not what is said. A toneless display hides both.
2. **Toneless *yinian* is several words.**
   - 疑念 *yíniàn* "doubt; suspicion" is /i³⁵ ni̯ɛn⁵¹/. That is **identical, tones included, to spoken 一念** [verified: Wiktionary 疑念]. A Mandarin listener can hear "a doubting thought" where the lemma means "one thought-moment".
   - 意念 *yìniàn* "thought, notion, will, ideation" is /i⁵¹⁻⁵³ ni̯ɛn⁵¹/ [verified: Wiktionary 意念]. Toneless, it is the same string, and it is a near-synonym of the intended sense, which makes the confusion easy rather than absurd.
3. **Toneless *sanqian* is several words.**
   - 三遷 *sānqiān* "(literary) to move house multiple times" is /sän⁵⁵ t͡ɕʰi̯ɛn⁵⁵/, **identical, tones included, to 三千** [verified: Wiktionary 三遷].
   - 散錢 *sǎnqián* "loose change; small sum of money" is /sän²¹⁴⁻²¹ t͡ɕʰi̯ɛn³⁵/ [verified: Wiktionary 散錢].
4. **What is lost is the thing tone carries in the donor.** In Mandarin, tones are lexical: toneless *yinian sanqian* is a string a Mandarin reader must guess back from, the same failure 326's EUMATHE lens found for Mandarin readers of *ichinen-sanzen*. The cathedral's convention (2.9) is toneless, so a Chinese-reading lemma would be legible to its anglophone readers *and* opaque to the donor's own speech community. That trade should be named in any entry, not assumed.
5. **On the Japanese side the reading has its own homophones.** *ichinen* is also 一年 "a year" ([it͡ɕinẽ̞ɴ], verified: Wiktionary 一年, Japanese). *sanzen* is also 参禅 "Zen meditation; consultation with the abbot" [verified: Wiktionary 参禅]. Moving to the Chinese reading trades the 参禅 collision for the 疑念 / 三遷 homophones and the q problem. It does not reach a collision-free form.

---

## 4. What this file does not do

- It proposes no scores and no family assignment.
- It does not decide between shapes. The choice between a faithful-but-opaque Chinese form and a recognizable-but-colliding Japanese form is a doctrine call; see the questions in the structured report.
- It did not re-verify experiment 326's external witnesses (Anaxagoras, Leibniz, hitkallelut, Whitehead), nor 326's line T1911 51c08–11.

---

## Verification (2026-11-10)

A second Claude Opus 5.5 subagent re-ran the checks in this file against main at `eca7c99`, using its own greps.

**Confirmed:**
- **Zero hits** for yinian, sanqian, qian, ichinen and nen (whole word), and for 一念, 三千, 念, 千, 三, Tiantai, Zhiyi, Zhanran, Nichiren, Tendai and Saichō.
- **`san`**: 4 whole-word lines, in ihsanme:5 and sankofame:5, :25, :73. The Twi gloss "return" is at :25 and :73.
- **`sanzen`**: 6 lines in canon: satorime:59, :63, :88, :98; daigome:75; kenshome:38. Also canon.md:33 and :38.
- **`qi`**: wakanme:150.
- **`一`**: slipsooth.md:37.
- **Lemma-name substrings** for yi, san and ju.
- **The -qing family:**
  - 35 files (34 in core, 1 in mathema; allostasisqing is in both).
  - Onsets: 20 aspirated, 8 unaspirated, 7 /tʃ/.
  - kinqing:8 and jeongqing:5.
  - index-by-suffix.md:23 and :235.
  - morphemes.json:453–454 (U+E126, used_in kinqing).
  - qinance has no pronunciation field.
- **The four Mandarin-donor -me lemmas and their pronunciation lines.** The verifier checked the frontmatter of every -me lemma that mentions Chinese; the others name Chinese only as resonance.
- **326's IPA at :124 and :191.**
- **Wiktionary forms and IPA** for 一 (sandhi note), 疑念, 意念, 三遷, 散錢, 情, 一年 and 参禅.

**Corrected:**
- **File count:** 267 is the number of `.md` files, of which 263 are entries and 4 are READMEs.
- **The -nian breakdown:** the earlier per-word figures matched no count and have been replaced with occurrence counts. The total of 103 lines stands.
- **`yin`:** tengrime:57 is a Mongolian genitive, not yin-yang.
- **Shape D IPA:** 在 gets its tie bar, [t͡sai̯⁵¹].
- **Shape G:** the Cantonese-precedent question is now checked.

**Unchecked:** the anglicized canon-style IPA guesses in part 1 are proposals, not attestations, and were not checked. Nothing here was scored.
