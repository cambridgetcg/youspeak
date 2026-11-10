---
name: phonology-reconciliation-2026-11
role: script-organ proposal (reconciling session, unratified)
opened: 2026-11-10
revised: 2026-11-10 (adversarial review integrated; silent-word lines added as IX)
companions: phonology.md, phonology-audit.md, tools/check_pronunciation.py
status: proposal — changes nothing in canon; no ruling here is in force
---

# YOUSPEAK pronunciation: a reconciliation proposal

> **Status.** This is a proposal, not a decision. Agent sessions wrote it on 2026-11-10, after
> Yu asked for the pronunciation work to be taken further, and revised it the same day after an
> adversarial review (X.8 records what that review changed). It changes nothing in canon. No
> entry, tutorial, primer, dictionary or voice file was edited to produce it, and no generator
> or voice tool was run. Each ruling below takes effect only when it is ratified. Until then,
> `script/phonology.md` and `script/phonology-audit.md` (both 2026-06-09) remain the record.
> Agents wrote those two documents as well; neither is a decision by Yu. The three documents
> together are evidence for a decision, not the decision. The one file outside this document
> that the work touched is the checker, `script/tools/check_pronunciation.py`, on this branch:
> four counting bugs found by the review were fixed there (X.8). It reads canon and writes
> nothing.

## How to read this

**What it does.** The 2026-06-09 audit recorded 49 inconsistencies and left each one to "a
future reconciling session". This is that session's proposal. It describes what the corpus
actually does (sections I to VI), proposes a ruling for every recorded finding (VII), tests one
structural idea (VIII), proposes lines for the twelve words that have none (IX), and lists what
stays open (X).

**What it rests on.**
- The 263 entry files under `canon/`, read today through `script/tools/check_pronunciation.py`
  (this branch). The checker found 255 words: 243 carry a `pronunciation:` line and 12 do not.
  Eight mathema words exist as two files.
- `script/phonology.md` and `script/phonology-audit.md`.
- The four other places the sound is written down: `PRIMER.md`, `tutorial/01` to `03`,
  `DICTIONARY.md`, and `pipeline/voice/forged.json`.
- Sources about donor languages opened today by this session, its silent-words drafting pass
  and its review pass. They are listed at the end of X, and each claim carries a tag:
  - `[verified: URL]`: the page was opened today and says this. The fetch tool returns a
    model's reading of the page, so quoted wording is close but not guaranteed letter for
    letter; re-check the quotes a row rests on before ratifying it.
  - `[from memory: not re-checked]`: the claim comes from general knowledge and needs checking
    before anyone relies on it.
  - `[canon: path]`: a fact about the corpus itself.

The ruling table works directly from `phonology-audit.md`'s 49 findings, each re-checked against
today's canon, and from the checker's current report.

**Words used here.** Each term is explained where it first appears. The ones used most:
- *IPA*: the International Phonetic Alphabet, one symbol per sound. Slashes `/…/` mark the
  intended sound. Square brackets `[…]` mark how something is actually said aloud.
- *Respelling*: the reader-friendly spelling in each line, such as `KOO-nance`. The syllable in
  capitals carries the stress.
- *Donor*: the language a stem is borrowed from.
- *Anglicized*: reshaped to the sounds English speakers already make.

**Dispositions in VII.**
- **HEAL**: a plain error, with the corrected line given. A row can heal the plain part and
  point to a YU choice for the part that is not plain; both are then named.
- **HONOR**: a deliberate exception that keeps faith with the donor, with the reason.
- **YU-n**: a choice of doctrine for Yu, with the options and their costs. There are six, all
  gathered in VII.E.
- **CLOSED**: resolved since the audit, or never true.
- A **†** marks a HEAL whose donor fact comes from memory and should be checked before the line
  is applied.
- **interim** marks a line whose stress follows its own respelling because the donor has no
  word stress to keep. The notation repair is plain; which syllable is stressed waits for YU-4
  (VII.0).

---

## I. What the corpus contains

### I.1 Where sound is written down

A *phoneme* is a sound that a language treats as one unit. The canon records sound in one
frontmatter line per entry:

    pronunciation: /IPA/ (RESPELLING; N syllables; notes); anglicized /…/ acceptable

Today 243 of 255 words carry this line. Nineteen lines also offer an alternate form, usually an
anglicized one. Nine lines quote other IPA in their notes (a donor form or a single sound);
those are glosses, not alternates. Four other records write the same words, and they disagree with canon and with
each other:

| Record | Words it pronounces | Differ from canon | How they differ |
|---|---|---|---|
| `tutorial/01`–`03` | 14 | 13, plus 1 that canon leaves silent | Teaches -me as /mɛ/ and -ance as /ɑːns/; different syllable counts and stress |
| `PRIMER.md` | 16 | 9 | Stress (doxomme /dɒksˈɒm/, paqduqing /pɑːkˈduː/), -ance as /ɑːns/, respellings |
| `DICTIONARY.md` | 18 (respellings only) | 5 | dokimance `dok-I-mance` against canon `DOK-i-mance`; candence, complerescence, nyamame, verisleight spelled differently |
| `pipeline/voice/forged.json` | 26 | 2 differ, 12 are drafts for silent words | alayame, kinhme; never written back to canon |

`[canon: records compared word by word on 2026-11-10]`

### I.2 Consonants

Several kinds of consonant appear below:
- A *stop* blocks the air completely and then releases it (p, t, k).
- A *fricative* lets air hiss through a narrow gap (f, s, sh).
- An *affricate* is a stop released into a fricative, heard as one sound. The "ch" in *church*
  is one.
- A *nasal* sends air through the nose (m, n, and "ng" /ŋ/).
- *Aspiration* is a puff of breath after a stop. It is written ʰ.

The counts are tokens in the 243 main IPA lines, then the number of words. Five spellings of the
same sound are merged: ɡ with ASCII g, tʃ with t͡ʃ, dʒ with d͡ʒ, tɕ with t͡ɕ, and ts with t͡s. The
46 symbols written in the corpus thus come to 41 sounds.

Marks in the table:
- **‡** means the sound comes almost entirely from a suffix.
- *Italic* means the sound is donor-marginal: found in four or fewer words, or confined to one or
  two donors.

| | Lips | Teeth and gum ridge | Behind the ridge | Hard palate | Soft palate | Back of mouth, throat |
|---|---|---|---|---|---|---|
| **Stops** | p 32/30 · b 21/20 · *bʱ 1* | t 72/63 · d 45/44 | | | k 71/65 · ɡ 21/20 · *kʰ 2* · *kʷ 1* | *q 3* · *ʔ 2* |
| **Affricates** | | *ts 3/2* · *tɬ 1* | tʃ 15/15 · dʒ 13/13 · tɕʰ‡ 19/19 · tɕ 9/8 (8‡) | | | |
| **Fricatives** | f 15 · v 14 | θ 14 · *ð 1* · s 93/74 · z 14 | ʃ 21 · *ʒ 1* · *ɕ 2* · *ʐ 1* | | *x 4* | *ʁ 1* · *ħ 1* · h 24/22 |
| **Nasals** | m 239/195 (180‡) | n 99/88 | | | ŋ 41/40 (34‡) | |
| **Liquids** (l and r sounds) | | l 48/47 · r 71/67 · *ɾ 2* · *ɹ 1* · *r̩ 2* | | | | |
| **Glides** (vowel-like consonants) | w 14/13 | | | j 21/21 | | |

Some symbols need a word:
- **tɕʰ and tɕ** are *alveolo-palatal* affricates, made with the tongue blade just behind the gum
  ridge. Mandarin pinyin *q* is [tɕʰ], "similar to the ch in English punchy"
  [verified: https://en.wikipedia.org/wiki/Pinyin].
- **q** is a *uvular* stop, made further back than k.
- **ħ** is a *pharyngeal* fricative, made in the throat. It is Arabic ح.
- **ʔ** is a *glottal stop*, the catch in English "uh-oh".
- **r̩** is a *syllabic* r, an r that carries a syllable by itself with no vowel.
- **ɾ** is a tap, the quick r of Japanese and Spanish *pero*.
- **ʁ** is a voiced uvular fricative, like a French r.

### I.3 Vowels

A *diphthong* is a vowel that glides from one position to another, as in "day" /eɪ/. The length
mark ː makes a vowel long. *Schwa*, /ə/, is the weak "uh" of English *about*.

| | Front | Central | Back |
|---|---|---|---|
| **Close** (tongue high) | i 57 · iː 31 · ɪ 73 | *ɨ 1* | u 12 · uː 18 · ʊ 16 |
| **Close-mid** | e 8 · *eː 2* · *øː 1* | ə 82 | o 7 · *oː 1* |
| **Open-mid** | ɛ 33 · *ɛː 1* · *œ 2* · *œː 1* | ʌ 41 · ɜː 5 | *ɔ 3* · ɔː 9 |
| **Open** (tongue low) | æ 28 · a 38 · *aː 2* | | ɑ 20 · ɑː 62 · ɒ 32 |

| Diphthong | Tokens / words |
|---|---|
| eɪ | 188 / 179 (178 are the -me suffix) |
| oʊ | 28 / 27 |
| aɪ | 18 / 18 |
| aʊ | 5 / 5 |
| ɔɪ | *1 / 1* |

`[canon: script/tools/check_pronunciation.py --inventory, 2026-11-10]`

### I.4 Core and donor-marginal

In this proposal a sound counts as **core** when it appears in the stems of at least ten words
drawn from at least five donor labels. Suffix syllables are left out of that count, so a sound
cannot be core just because a suffix repeats it.

- **Core consonants (20):** p b t d k ɡ m n l r s z f v h j w ʃ θ dʒ.
  - tʃ and ŋ are also core. Each comes just under the line in stems (9 and 8 words) and is
    heard in every qing word besides.
- **Suffix-only:** tɕʰ, the sound of -qing. It appears in no stem at all.
- **Neither:** tɕ, the unaspirated Korean ㅈ in jeongqing's stem. Eight of its nine tokens are
  qing written without aspiration (VII.A4), so it fits no group. 20 core consonants, tʃ and ŋ,
  tɕʰ, and the 17 marginal ones below make 40 of the 41 sounds; tɕ is the 41st.
- **Core vowels (17):** ə ɪ i iː a ɑ ɑː ʌ ɛ æ ɒ u uː ʊ eɪ oʊ aɪ.
- **Middle** (5 to 9 words): ɔː e o aʊ ɜː.
- **Donor-marginal consonants:**

  | Sound | Words |
  |---|---|
  | x | barzakhqing, chayimme, halakhame, nextlame |
  | q | damqme, hopiqatsime, qorbme |
  | ts | kintsugime, tzimtzumme |
  | kʰ | kherme, sukhance |
  | ʔ | kinhme, warame (in warame it stands for Arabic ʿayn, which is /ʕ/: VII.D7) |
  | ɾ | satorime, yvymarame |
  | ɕ | sinbyeongme, sinmyeongme |
  | r̩ | sabrme, shukrme |
  | bʱ | bhaktime |
  | ħ | hayatqing |
  | kʷ | kwothme |
  | ɹ | oriance |
  | ʐ | renme |
  | tɬ | tlamatisme |
  | ʒ | visageqing |
  | ʁ | voghbme |
  | ð | zudhame |

- **Donor-marginal vowels:**

  | Sound | Words |
  |---|---|
  | ɔ | autopoieme, ondame, sankofame |
  | eː | devekutqing, emetme |
  | aː | hayatqing, maname |
  | œ | orlogme, ragnarokme |
  | ɛː | aletheme |
  | oː | hotepme |
  | ɨ | ngünecheme |
  | øː | noetherme |
  | œː | orlogme |
  | ɔɪ | autopoieme |

  Each sits in one to three words, usually from one donor.

The core set is close to what an English speaker already has. The marginal set is where the
donor-faithful policy shows: 17 consonants and 10 vowels, each kept in the main line for one to
four words.

### I.5 The vowels are two systems written side by side

Read plainly, the vowel table mixes two transcription habits:

- **English-reference symbols:** ɪ ɛ æ ʌ ɒ ʊ ə iː uː ɑː ɔː ɜː, with eɪ oʊ aɪ aʊ. These are the
  symbols a British-English dictionary uses. Here the length mark is part of the vowel's name.
  /iː/ is the vowel of "see", not "a long i".
- **Cardinal symbols:** a e i o u, with eː aː oː. These are the plain five-vowel symbols used for
  Spanish, Japanese or Hebrew. Here the length mark means the donor's vowel really is longer.

So the length mark means two different things in one corpus. The same donor vowel lands in
either system depending on which entry wrote it:

| Donor vowel | Written in the corpus as | Examples |
|---|---|---|
| Hebrew and Arabic *a* | /a/, /ɑ/, /ɑː/, /ʌ/, /aː/ | barakqing /baˈrak/, barzakhqing /ˈbɑːr/, hadaratme /hʌ/, hayatqing /jaːt/ |
| Sanskrit short *a* | /ʌ/, /ɑː/, /ə/ | hastame /ˈhʌs.tʌ/, tapasme /ˈtɑː.pɑːs/, yantrame /trə/ |

English-reference symbols are the majority in every month's entries. The cardinal share is
higher in July than in April, though it dips from May to June. Counting stem vowels written
a, e, o, eː, aː, oː against ɑː ʌ æ ɒ ɛ ɔː eɪ oʊ:

| Entries from | Cardinal tokens |
|---|---|
| April | 5 of 60 |
| May | 18 of 94 |
| June | 13 of 80 |
| July | 19 of 61 |

The corpus is a mixture here, and this proposal does not pretend otherwise. VIII and YU-6 offer a
way to give each system its own line.

---

## II. Spelling to sound

The written word keeps each donor's own spelling, so a letter's sound depends on where the stem
came from. A *digraph* is two letters for one sound, as in "sh". The counts below cover stem
letters only; the suffix letters are treated in II.5. The letter-to-sound pairings come from the
checker's alignment, which is approximate, and each example was confirmed against its line.
A digraph read as one sound (th as /t/, kh as /k/) is counted under the digraph in II.3, not
under its letters. `[canon: check_pronunciation.py --inventory, as fixed on this branch (X.8)]`

### II.1 Letters with one reading

The spelling tells the reader the sound for these letters:

| Letter | Sound | Count |
|---|---|---|
| b | /b/ | 19 of 19 |
| d | /d/ | 45 of 45 |
| f | /f/ | 9 of 9 |
| k | /k/ | 43 of 43 |
| l | /l/ | 43 of 43 |
| m | /m/ | 56 of 56 |
| n | /n/ | 83 of 83 |
| p | /p/ | 31 of 31 |
| v | /v/ | 14 of 14 |
| w | /w/ | 14 of 14 |
| z | /z/ | 7 of 7 |
| sh | /ʃ/ | 15 of 15 |

### II.2 Letters with several readings

| Letter | Default (most frequent) | Donor-conditioned readings, with counts and examples | Does the spelling tell? |
|---|---|---|---|
| **a** (231) | none clear | Six values in common use:<br>/ɑː/ 61: artiance, agapeme<br>/ə/ 47: athaumasma<br>/ʌ/ 37: hastame (Sanskrit 15 of them)<br>/a/ 37: barakqing (Hebrew 11, Arabic 5)<br>/æ/ 23: candence (Greek 14)<br>/ɑ/ 20: balagme<br>Also /eɪ/ 2, /aː/ 2, /aɪ/ 1, silent 1 (tawbame) | No |
| **e** (81) | /ɛ/ 33: autoxenia | /ə/ 16: devekutqing<br>/eɪ/ 8: agapeme (Greek ē)<br>/iː/ 7: heurekin (Greek ē)<br>/e/ 6: tongleme<br>/ɪ/ 3, /eː/ 2 (Hebrew), silent 3<br>/ɛː/ 1 (aletheme), /ɜː/ 1 (eternalme), /i/ 1 (eucatastrophe) | No |
| **i** (103) | /ɪ/ 40 | /i/ 36: agnime<br>/iː/ 20: chayimme<br>/aɪ/ 4: pime, artiance (English habit)<br>/ɜː/ 2: firstnessqing<br>silent 1: prehensionme | Partly |
| **o** (86) | /ɒ/ 32: anagnoristasis (Greek 21) | /oʊ/ 27: alohame<br>/ə/ 9: concrescenceme<br>/o/ 7: kobame, hozhome<br>/ɔː/ 4: morphame<br>/ɔ/ 2: ondame<br>/œ/ 2 and /œː/ 1, in orlogme and ragnarokme: Modern Icelandic ö. Old Norse ǫ was a back vowel [ɒ] (*Ragnarǫk* [ˈrɑɣnɑˌrɒk] [verified: https://en.wikipedia.org/wiki/Ragnar%C3%B6k]); orlogme's second vowel is the same ǫ [from memory: not re-checked]<br>/oː/ 1: hotepme<br>/ɜː/ 1: godelme | No |
| **u** (43) | /uː/ 15 or /ʊ/ 15 | /u/ 11: guthme, fulgurme<br>/ɨ/ 1: ngünecheme (the headword writes ü)<br>/ɜː/ 1: liturgiame | No. The respelling OO is used for both /uː/ and /ʊ/ (chulme `CHOOL` /tʃʊl/) |
| **y** (27) | consonant /j/ 16: alayame, hayatqing | Vowel in Greek: /ɪ/ and /i/ syzygyqing, /aɪ/ myesisme. freenergyme's /i/ is the y of English *energy*<br>Norse y: /ɪ/ in yggdrasilme, whose own note gives the donor's front rounded /y/<br>Guaraní y: /ɪ/ in yvymarame | Only before a vowel |
| **c** (13) | /k/ 7: candence | /tʃ/ 3: catuskotime, prapancame (Sanskrit c, which is /tɕ/ [verified: https://en.wikipedia.org/wiki/Sanskrit_phonology]); wiconime (the canon spells *wičoni*, but the Lakota word is *wičhóni* [verified: https://en.wiktionary.org/wiki/wičhóni], with aspirated čh [tʃʰ]: "Aspirates are written with ⟨h⟩" [verified: https://en.wikipedia.org/wiki/Lakota_language])<br>/s/ or silent in -scence: complerescence | No |
| **g** (26) | /ɡ/ 20: agapeme (4 of them typed as ASCII g) | /dʒ/ 5: algiadoxame, freenergyme (English habit before i, e, y)<br>/ʒ/ 1: visageqing | Partly, by the English rule "soft g before e, i" |
| **h** (30) | /h/ 24 | Silent 5: ihsanme, kinhme, mahabbahqing, wahyqing, and the h of -tahv- in humahukhtahvarshtame. The h of th, ph and kh read as a plain stop belongs to those digraphs (II.3)<br>/ħ/ 1: hayatqing | No |
| **j** (11) | /dʒ/ 8: drujme, jivame | /j/ 1: heimrekjame (Gothic)<br>/tɕ/ 1: jeongqing (Korean ㅈ, "unaspirated" [verified: https://en.wikipedia.org/wiki/Revised_Romanization_of_Korean])<br>Inside tj in tjukurpame: the Pitjantjatjara palatal stop [verified: https://en.wikipedia.org/wiki/Pitjantjatjara_dialect], written /tʃ/ | Partly |
| **q** in a stem (7 lines) | none | /k/ 4: faqrme, koyaanisqatsime, paqduqing, shawqame<br>/q/ 3: damqme, hopiqatsime, qorbme | No, and see II.5 |
| **r** (81) | /r/ 71 | Silent 4, English non-rhotic: eternalme, firstnessqing, liturgiame, thirdnessqing<br>/r̩/ 2: sabrme, shukrme<br>/ɾ/ 2: satorime, yvymarame<br>/ɹ/ 1: oriance<br>/ʐ/ 1: renme (Mandarin r) | Mostly |
| **s** (70) | /s/ 57 | /ʃ/ 6: Sanskrit ś and ṣ written s (sunyatame, vimarsame, asraya-paravrttime, catuskotime), Old Persian š (vasname), English -sion (prehensionme)<br>/z/ 5: daseinqing, chiasmqing, visageqing, hailsme, jinsme. The last two are English habit, not the donor: Gothic final -s and Arabic sīn are /s/ [from memory: not re-checked]<br>/ɕ/ 2: Korean sin- | No |
| **t** (64) | /t/ 63 | Inside tj 1 | Yes |
| **x** (10) | /ks/ 9 (all Greek) | /x/ 1: nextlame, which is wrong for the donor (VII.D2) | Yes for Greek |

### II.3 Digraphs and letter pairs

| Spelling | Readings in the corpus | Does the spelling tell? |
|---|---|---|
| **ch** (8) | /tʃ/ 4: anamcharame, chulme, ngünecheme, pachame<br>/k/ 3, Greek χ: chiasmqing, eucharistime, prosocheme<br>/x/ 1, Hebrew ḥet: chayimme<br>The Old Irish *ch* of anamcharame is /x/ in the donor (broad ch = /x/ [verified: https://en.wikipedia.org/wiki/Irish_orthography]), so its /tʃ/ is an error (VII.B7) | No |
| **th** (17) | /θ/ 14: Greek (ethosme), Gothic þ (guthme), Welsh (hiraethqing), Hebrew via English (sabbathme), English (slipsooth), Nuer (kwothme)<br>/t/ 3: noetherme (German), shamathaqing (Sanskrit aspirate *th*), aletheme (Greek θ, whose own respelling says `theh`: VII.D5)<br>Classical Greek θ was an aspirated /tʰ/ before it became a fricative [verified: https://en.wikipedia.org/wiki/Ancient_Greek_phonology] | No |
| **ph** (5) | /f/ 4, Greek: morphame<br>/p/ 1: sphotame (Sanskrit *ph*, an aspirated p; the entry flags its English-Indological reading) | No |
| **kh** (5) | /x/ 2: barzakhqing (Arabic), halakhame (Hebrew)<br>/kʰ/ 2: kherme (Egyptian), sukhance (Sanskrit). Egyptian ḫ is conventionally a fricative, not an aspirated stop [from memory: not re-checked], so kherme's /kʰ/ needs a check<br>/k/ 1: humahukhtahvarshtame (Avestan). Avestan x is /x/ [verified: https://en.wikipedia.org/wiki/Avestan_alphabet], so this /k/ is a donor error (VII.B9) | No |
| **bh** (1) | /bʱ/ bhaktime: breathy b, Sanskrit | Yes |
| **dh** (1) | /ð/ zudhame, the voiced "th" of "this". The donor is Arabic *zuhd* (X) | No |
| **zh** (1) | /z.h/ hozhome. Navajo zh is [ʒ] [verified: https://en.wikipedia.org/wiki/Navajo_phonology], so this is an error (VII.D1) | No |
| **gh** (2) | /ʁ/ voghbme (Armenian); silent in verisleight (English *sleight*) | No |
| **tl** (3) | /tɬ/, one sound, in tlamatisme<br>/t.l/ split in nextlame<br>teotlme has no line<br>Nahuatl tl is a single lateral affricate [verified: https://en.wikipedia.org/wiki/Classical_Nahuatl] | No |
| **ts, tz** (7) | One affricate /ts/: kintsugime, tzimtzumme<br>Split /t.s/ across a syllable break: hopiqatsime, koyaanisqatsime, katsintawime, jiritsume, natsarqing<br>Hopi ts is one affricate [verified: https://en.wikipedia.org/wiki/Hopi_language]; so is Japanese [ts] before u [verified: https://en.wikipedia.org/wiki/Japanese_phonology]<br>The two notations are close but not the same: an English /t/ before a syllable break is often unreleased or glottalized [from memory: not re-checked], and jiritsume's /rit.su/ closes a syllable that is open in Japanese *ji-ri-tsu* | Yes for the sound; the notation drifts |
| **kw** (1) | /kʷ/ kwothme, a k with lip rounding | Yes |
| **ny** (2) | /nj/ nyamame, sunyatame | Yes |
| **ck** (1) | /k/ ereckappayime | Yes |
| **Doubled consonants**<br>bb, kk, ll, mm, nn, pp, ss, tt, gg | One sound in sabbathme, tikkunme, kallodoxa, ginnungame<br>Two sounds split across a syllable in mahabbahqing /b.b/, kittume /t.t/, tawakkulme /k.k/, ereckappayime /p.p/<br>A *geminate* (a consonant held twice as long) is real in Arabic, Akkadian and older Hebrew [from memory: not re-checked]; the corpus writes it both ways | No |
| **aa** (2) | One long vowel /ɑː/: koyaanisqatsime (Hopi writes long vowels double [verified: https://en.wikipedia.org/wiki/Hopi_language])<br>Two syllables /ɑː.ɑ/: maatme (Egyptian *maat*)<br>Two vowels across the suffix boundary: panimaance | No |
| **ee** (2) | /iː/: veriseem, freenergyme | Yes |
| **oo** (2) | /oʊ/: manidoome (Ojibwe)<br>/uː/: slipsooth (English) | No |
| **ae** (2) | /aɪ/: hiraethqing (Welsh), saeculme (classical Latin) | Yes |
| **ai** (4) | /aɪ/: daigome, hailsme, tinaime, wairuaqing | Yes |
| **au** (8) | /aʊ/ 4: athaumasma, hauqing, landauerme, mauriqing<br>/ɔː/ 3: autoxenia, autopistme (English auto-), waurdme (Gothic)<br>/ɔ/ 1: autopoieme | No |
| **aw** (5) | /ɔː/ 2: shawqame, tawbame (Arabic *aw* read as English "law")<br>/aw/ 1: mugawme<br>a + w 2: tawakkulme, katsintawime | No |
| **ay** (7) | /aɪ/ 1: aynime (Aymara)<br>/aɪ/ and then /j/ 1: alayame (VII.C5)<br>a + consonant y 5: asraya-paravrttime, ayanme, chayimme, ereckappayime, hayatqing | Only before a vowel |
| **ng** (8) | /ŋ/ 7: jeongqing, songlineme, tengrime… It also starts a word in ngünecheme, where English speakers do not expect it.<br>/n.ɡ/ 1: ginnungame, although its own donor note writes /ŋɡ/ | Mostly |
| **ei** (4) | /aɪ/ 4: daseinqing, eikonme, heimrekjame, verisleight | Yes |
| **eo** (5) | /ʌ/ 3, Korean eo: jeongqing, sinbyeongme, sinmyeongme. Korean 벽 *byeok* is [pjʌk̚] [verified: https://en.wikipedia.org/wiki/Revised_Romanization_of_Korean]<br>Two vowels: theobasis /iː.oʊ/; teotlme has no line | No |
| **eu** (4) | /ju/, /jʊ/ or /juː/, all Greek: heurekin, eurekame, eucharistime, eucatastrophe | Yes for the sound; the length drifts |
| **oe** (4) | /øː/: noetherme (German ö)<br>Two vowels: noemame /oʊ.eɪ/, noesisme /oʊ.iː/, zoeme /oʊ.iː/ (Greek) | No |
| **oi** (1) | /ɔɪ/: autopoieme | Yes |
| **ia, ua, ue** | Always two syllables (*hiatus*: two vowels side by side, each its own syllable): xeniame, liturgiame, wairuaqing, landauerme | Yes |

### II.4 Marks in the headword

The `word:` field keeps marks that the file name drops. Eighteen headwords carry them:
- Length marks over a vowel: ālayame, kenshōme, manāme, skēname, kuṇḍalinīqing.
- Indic letters ṇ ḍ ś ñ: kuṇḍalinīqing, tiṇaime, śūnyatame, vimarśame, prapañcame.
- Front rounded vowels ü and ö: ngünecheme, örlögme, ragnarökme.
- þ: guþme. š: vašnāme. ḥ: waḥdat-al-wujūdme.
- Yoruba marks: àṣẹme.
- The **apostrophe**: ch'ulme, k'inhme.

The IPA follows these marks only sometimes:
- **ö** is kept as /œ/ in örlögme and ragnarökme.
- **ō** becomes the English diphthong /oʊ/ in kenshōme.
- **The apostrophe** gets two treatments. In ch'ulme it is dropped (/ˈtʃʊl/). In k'inhme it
  becomes a glottal stop after the k (/kʔɪn/). In Mayan spelling the apostrophe marks an
  *ejective*, a consonant popped out with the throat closed [from memory: not re-checked].
  `forged.json` writes kinhme with the ejective sign, as /ˈkʼiːn/. Spelling alone does not tell
  the reader what the apostrophe does.

### II.5 The suffix letters

Two suffix spellings work against what an English reader will do with them.

- **The -e of -me is never silent.** 109 of the 184 -me words end in vowel + m + e:

  | Ending | Words |
  |---|---|
  | -ame | 64 |
  | -ime | 20 |
  | -eme | 12 |
  | -ome | 8 |
  | -ume | 4 |
  | -yme | 1 |

  That is exactly the English "silent e" pattern of *came, time, theme, home, fume*. A reader
  who has not been taught otherwise will meet several words as English look-alikes:
  - *kame* as "came"
  - *ashame* as "a shame"
  - *dalime* as "da-lime"
  - *emime* as "e-mime"
  - *hozhome* as "hozh-home"

  Each word then loses a syllable. Nothing in the spelling signals the extra syllable.
  `[canon: count over canon slugs, 2026-11-10]`
- **q means two unrelated things.** In the suffix **-qing** it is the Mandarin sound [tɕʰ], close
  to English "ch". In a stem it is /k/ or /q/. *paqduqing* holds both: PAQ is /k/, and -qing is
  "ching".

### II.6 What this section shows

Only twelve spellings tell the reader the sound outright: the eleven letters and sh in II.1.
Every vowel letter and most digraphs depend on the donor. The Constitution's EUMATHE test asks
whether an untrained reader can "pronounce it out loud without hesitation", and it rules out
"ambiguous phoneme sequences" `[canon: CONSTITUTION.md §I]`. The spelling cannot pass that test
by itself, because it was never designed to. POLYPHONIA asks that each path's own gift be
received `[canon: POLYPHONIA.md §VIII]`, and keeping donor spellings is how the corpus has done
that. The tension between the two foundations is real. The respelling is the layer that carries
the reader across, and it is also where much of the inconsistency lives (VII).

---

## III. Syllable shapes and sound combinations

A *syllable* has three parts:
- the *onset*: the consonants before the vowel;
- the *nucleus*: the vowel, or a syllabic consonant;
- the *coda*: the consonants after the vowel.

A *cluster* is two or more consonants in a row. The counts below follow the syllable dots and
stress marks that each line itself writes. The 243 lines hold 822 pieces between those marks:
- 813 pieces hold exactly one vowel (or syllabic consonant). These are the syllables counted
  below.
- 6 pieces are undotted lumps holding 15 vowels between them: autopistme /ɔːtə/, ifeqing
  /iːfɛtʃɪŋ/, manidoome /mænɪ/, noesisme /iːsɪs/, nommome /nɒməmeɪ/, nyamame /njɑːməmeɪ/. Only
  their first onset is counted (nyamame's /nj/).
- 3 pieces hold no vowel: autoxenia /k/, damqme /q/, asraya-paravrttime /rt/.

The lumps and the empty pieces are notation errors, healed in VII.

**Shapes attested.** C stands for a consonant and V for a vowel.

| Shape | Count | Example |
|---|---|---|
| CV | 452 (56%) | the *me* of every -me word |
| CVC | 216 (27%) | *kuːn* in tikkunme |
| V | 55 | the *a* of ahavame |
| VC | 38 | the *ɪn* of indrajalame |
| CCV | 17 | *friː* in freenergyme |
| CVCC | 15 | *dəns* in candence |
| CCVC | 12 | *drʊdʒ* in drujme |
| VCC | 7 | *əns* in oriance |
| CCCV | 1 | *strɒ* in metastrophesis |

Simple syllables, with at most one consonant on each side, make up 761 of 813 (93.6%). 41 of
the 243 words begin with a vowel.

**Onset clusters (31).** All but six are kinds English also allows. The six are **ks**
(xeniame), **kʔ** (kinhme), and a consonant + /j/ before a vowel other than /uː/: **nj** in
nyamame and sunyatame, **bj** in sinbyeongme, **mj** in sinmyeongme. English puts a consonant
before /j/ only "before /uː/ or its modified/reduced forms", as in *pure, tube, cute*
[verified: https://en.wikipedia.org/wiki/English_phonology]. The rest are a consonant followed
by r, l or w, heurekin's /hj/ before /u/, or s followed by p, t or k.

| Cluster | Count | Examples |
|---|---|---|
| dr | 3 | drujme, indrajalame, yggdrasilme |
| pr | 3 | prapancame, prehensionme, prosocheme |
| st | 2 | allostasisqing, anagnoristasis |
| pl | 2 | complerescence, diplosemy |
| fr | 2 | frashame, freenergyme |
| nj | 2 | nyamame, sunyatame |
| sp | 2 | spandaqing, sphotame |
| tr | 2 | eucatastrophe, yantrame |
| sl | 2 | slipsooth, verisleight |
| ʃr | 1 | asraya-paravrttime |
| br | 1 | britqing |
| kr | 1 | concrescenceme |
| ɡl | 1 | glossame |
| hj | 1 | heurekin |
| bj | 1 | sinbyeongme |
| mj | 1 | sinmyeongme |
| sk | 1 | skename |
| str | 1 | metastrophesis |
| ks | 1 | xeniame (autoxenia writes it once more, broken; VII.B10) |
| kʔ | 1 | kinhme |

Outside the clusters, **ŋ** also starts a word once (ngünecheme), which English never does.

**Coda clusters (22).**

| Cluster | Count | Examples |
|---|---|---|
| ns | 11 | every -ance and -mance |
| st | 2 | autopistme, firstnessqing |
| lz | 1 | hailsme |
| rʃ | 1 | humahukhtahvarshtame |
| nz | 1 | jinsme |
| lk | 1 | molkme |
| xt | 1 | nextlame |
| rb | 1 | qorbme |
| nd | 1 | secondnessqing |
| ʁb | 1 | voghbme |
| rd | 1 | waurdme |

**Three consonants in a row across a syllable break.** Most of these happen where a stem that
ends in two consonants meets -me:

| Junction | Words |
|---|---|
| r-b-m | qorbme |
| ʁ-b-m | voghbme |
| m-q-m | damqme |
| l-k-m | molkme |
| r-d-m | waurdme |
| s-t-m | autopistme |
| l-z-m | hailsme |
| n-z-m | jinsme |
| n-s-m | concrescenceme |

Others sit inside stems: str, mpl, ndr, ntr, ɡdr, nkr, xtl, rʃt, ndn, stn, nbj, nmj. Four
consonants run together once, v-r-t-t in asraya-paravrttime, and this is only because its
syllabic ṛ is not written as a nucleus.

**Syllabic consonants and vowel-less pieces.** Two words make r a syllable: sabrme /ˈsɑb.r̩.meɪ/
and shukrme /ˈʃʊk.r̩.meɪ/. A third word of the same Arabic shape takes a different road: faqrme
inserts a schwa, /ˈfɑk.rə.meɪ/. Inserting a vowel to break up a cluster is called *epenthesis*.
So one donor shape (consonant, vowel, consonant, r) gets two treatments; VII.B16 refers the
choice to YU-6. Three lines leave a piece between dots with no vowel at all: /k/ in autoxenia,
/q/ in damqme, /rt/ in asraya-paravrttime. These are notation errors (VII.B).

**Proposed template for new coinages.** It is descriptive of what 93.6% of syllables already
do, and existing words are not reshaped:

> (C)(C)V(C)(C), where:
> - a two-consonant onset is a consonant followed by r, l or w, or by j only before /uː/
>   (s + l included), or s followed by p, t or k;
> - a two-consonant coda is a nasal or liquid followed by s, z, t or d, or s followed by t;
> - three consonants in a row across the stem + suffix junction are avoided. Where a donor
>   stem forces them (qorb-, voghb-, damq-), the said-aloud form shows the vowel speakers will
>   insert, as faqrme already does.

---

## IV. Stress

*Stress* is the extra force on one syllable, as in English *baNAna*. The *primary* stress is
the strongest and is written ˈ. A *secondary* stress is weaker and is written ˌ.

**The stated rule.** `phonology.md` "For future forges" and §4 state it: a suffix takes no
stress, and the stem keeps the stress it has in its donor. `[canon: script/phonology.md:26-28]`

**How well the corpus keeps the first half.**
- 231 of the 243 lines carry exactly one primary mark. Of the other 12, eight carry none and four
  carry two. All twelve are listed in VII.B.
- Of the 231, the suffix is unstressed in 228. The three exceptions are jeongqing, kinhme and
  muditaqing.

Where the primary stress falls, counted back from the end of the word:

| Position | Lines |
|---|---|
| Last syllable | 3, the three exceptions |
| Next-to-last | 78 |
| Third from the end | 132 |
| Fourth from the end | 14 |
| Fifth from the end | 4 |

Third from the end is the commonest landing place. That is simply a stress on the stem's
second-to-last syllable followed by a one-syllable suffix: *ˈBIN-doo-may*, *a-ˈHAH-va-meh*.

**How well it keeps the second half.** This can be checked only where the donor's stress is
known. This session could verify the donor fact for thirteen words:

| Word | Donor stress (source) | Canon IPA | Canon respelling |
|---|---|---|---|
| emetme | Hebrew *emét*, last syllable. Modern /(ʔ)eˈmet/, Tiberian /ʔɛ̆ˈmɛθ/ [verified: https://en.wiktionary.org/wiki/אמת] | first syllable: no | `EH-met`: no |
| devekutqing | Hebrew *dvekút*, last syllable [verified: https://en.wiktionary.org/wiki/דבקות] | second: no | `deh-VEH-koot`: no |
| shevirame | Hebrew *shvirá*, last syllable [verified: https://en.wiktionary.org/wiki/שבירה] | second: no | `sheh-VEER-uh`: no |
| andemame | Hebrew *dmamá* /dmaˈma/, last syllable [verified: https://en.wiktionary.org/wiki/דממה] | on *mɑː*: yes | `an-DEM-ah`: no |
| ihsanme | Arabic: "If the final syllable is superheavy, stress it" [verified: https://en.wikipedia.org/wiki/Arabic_phonology]. Here that means *iḥ-SĀN* | first: no | `EE-san`: no |
| warame | Arabic, same rules: a two-syllable word without a superheavy final syllable is stressed on the first [verified: same page]. So *WA-raʿ* | second: no | `wa-RAH`: no |
| mandalame | Sanskrit *máṇḍala*, and English /ˈmʌn.də.lə/: first syllable in both [verified: https://en.wiktionary.org/wiki/mandala] | second: no | `mun-DAH`: no |
| wiconime | Lakota stress "generally the vowel of the second syllable", marked with an acute [verified: https://en.wikipedia.org/wiki/Lakota_language]. *wičhóni* [verified: https://en.wiktionary.org/wiki/wičhóni] | first: no | `wee-CHOH`: yes |
| wakanme | Lakota, same rule. The entry's own donor form is *wakȟáŋ* | second: yes | `wa-KAN`: yes |
| aynime, pachame | Aymara: "Stress is usually on the second-to-last syllable" [verified: https://en.wikipedia.org/wiki/Aymara_language], so *AY-ni*, *PA-cha* | second: no (both) | `AY-nee`: yes · `pa-CHA`: no |
| teyoliame | Classical Nahuatl: "Stress generally falls on the penultimate syllable" [verified: https://en.wikipedia.org/wiki/Classical_Nahuatl], so *te-yo-LI-a* | none marked | `teh-YOH`: no |
| ngünecheme | Mapuche: a closed last syllable takes the stress [verified: https://en.wikipedia.org/wiki/Mapuche_language], so *Ngüne-CHEN* | second: no | `ngü-ne-CHE`: yes |

Of these thirteen, the IPA line keeps the donor's stress in two (andemame, wakanme). The
respelling keeps it in four (wakanme, wiconime, aynime, ngünecheme). Most of the other donor
stresses the audit questioned could not be checked today and are marked † in VII.

**Where the rule says nothing.** Many donors have no stress to keep:
- Mandarin, Cantonese and Yoruba mark words with *tone* (see VI).
- Japanese has a *pitch accent*, a fall in pitch after a given syllable: "a pitch accent system
  in which the position or absence of a pitch drop may determine the meaning of a word"
  [verified: https://en.wikipedia.org/wiki/Japanese_phonology].
- Korean has no word stress [from memory: not re-checked].
- For Sumerian, Akkadian, Hittite, Hurrian and Etruscan, nobody knows the stress
  [from memory: not re-checked].

For all of these, the corpus has used English habit without saying so, and not one habit:
- first-syllable stress in emime, ifeqing and oriance (Yoruba), and in daigome's respelling;
- second-syllable stress in the respellings of sinbyeongme and sinmyeongme (Korean), whose IPA
  marks nothing;
- no stress at all in satorime, whose respelling caps nothing.

The stated rule needs a clause for this case. That clause is part of YU-4. Until YU-4 rules,
VII gives these lines the stress their own respelling shows (marked *interim*), so that each
line has exactly one primary.

**Compounds.** Lines with two primary marks belong to multi-word donors: anamcharame,
asraya-paravrttime, humahukhtahvarshtame, doxakallos. Two primaries in one word is a plain
notation error, and VII heals it. Which element takes the primary is not plain. The only
precedent is one Greek word, kallodoxa, which puts the secondary on the first part and the
primary on the last. VII uses that as a *proposed house compound pattern* and refers the choice
to YU-4: Irish puts stress on the first syllable [from memory: not re-checked], and Sanskrit
*parāvṛtti* may stress *vṛt* by the classical heavy-syllable rule [from memory: not
re-checked]. The canon respellings capitalize every element.

---

## V. The suffixes

### V.1 -me

**What the corpus does.** 184 words take -me. 180 carry a line.

| Record | Form |
|---|---|
| `phonology.md` "For future forges" (normative, lightly held) | /meɪ/ respelled "meh" `[canon: script/phonology.md:28]` |
| Canon IPA | /meɪ/ in 178, /me/ in 2 (ngünecheme, satorime), /mɛ/ in none |
| Canon respelling | `may` 126, `meh` 51, `me` 3 (agapeme, eternalme, ngünecheme) |
| Tutorial 01 | "The `-me` ending is always: /mɛ/ — the vowel as in "bed," not "me" as in "me myself."" |
| PRIMER | IPA /meɪ/ with respelling `meh` (kimme `KEE-meh`, shemme `SHEM-meh`) |

The respelling has drifted over time:

| Month entered | Words | `meh` | `may` | `me` |
|---|---|---|---|---|
| April | 20 | 14 | 5 | 1 |
| May | 56 | 29 | 27 | 0 |
| June | 60 | 5 | 54 | 1 |
| July | 44 | 3 | 40 | 1 |

When the audit was written the split was 42 `meh`, 31 `may`, 1 `me`. So the only record that
states a rule for the respelling names `meh`, and 126 lines today depart from it.
`[canon: frontmatter lines; tutorial/01-the-me-family.md:144; PRIMER.md:90,96]`

**The donor.** Sumerian 𒈨, transliterated *me* [verified: https://en.wikipedia.org/wiki/Me_(mythology)].
The cuneiform script "clearly distinguishes" only the vowels /a e i u/. Nobody heard Sumerian;
it is known "through the filter of Akkadian phonology". Scholars who posit long vowels "do not
consider it possible to reconstruct the length of the vowels in most Sumerian words" [verified:
https://en.wikipedia.org/wiki/Sumerian_language]. So the conventional reading is /me/: a
front, mid, plain vowel, with no glide and no known length. The tutorial's "likely /me/ or /mɛ/"
is fair; the script cannot decide between the two.

**Ease for English speakers.**
- /meɪ/ is native English: *may*, *day*.
- A pure final [e] is not an English vowel in that position. English speakers tend to say it as
  [eɪ] [from memory: not re-checked].
- English *checked* vowels (ɪ ɛ æ ɒ ʊ ʌ) "commonly stand only in stressed closed syllables". The
  exceptions are "mostly in interjections", and *eh* and *meh* are among them [verified:
  https://en.wikipedia.org/wiki/Checked_and_free_vowels]. So `meh` is sayable. But it is an
  interjection shape, and the suffix is always unstressed. Unstressed final vowels in English
  drift toward /ə/ [from memory: not re-checked], so /mɛ/ risks becoming /mə/. That is already
  the sound of the -ma suffix (athaumasma /mə/) and of the weak stem vowel before -me in 24
  words (mathemame /ˈmæθ.ə.mə.meɪ/ would become "MATH-uh-muh-muh").
- The respelling `me` invites /miː/ or a silent e (II.5).

**Ease for others.** Five or six vowel qualities is the commonest inventory size in the world:
287 of 564 languages, or 50.9% [verified: https://wals.info/chapter/2]. Speakers of such languages
(Spanish, Italian, Japanese, Swahili and many more [from memory: not re-checked]) have /e/ and
no /eɪ/ glide. For them /me/ is the easy form, /meɪ/ is an English accent, and /mɛ/ against /me/
is a difference many of them do not make.

**Options (YU-1).**

| Option | What it means | Cost |
|---|---|---|
| A. /meɪ/ "may" everywhere | Keep the canon IPA; make all respellings `may` | 51 `meh` and 3 `me` respellings change. The tutorial 01 note and PRIMER respellings change. It reverses the stated normative respelling "meh" (phonology.md:28), from which 126 `may` lines already depart. The record goes on stating an English diphthong as the sound of a Sumerian syllable. |
| B. /me/ in the IPA, `may` as the respelling | Record the donor vowel; accept [meɪ] from English speakers and [me] from others as both right | All 178 /meɪ/ lines change (one mechanical replacement), and 54 respellings as in A. The respelling `may` likewise reverses phonology.md:28's "meh", from which 126 lines already depart. The respelling still steers English readers to [meɪ]. This fits VIII's two-line record exactly. Tutorial 01 changes from /mɛ/ to /me/. |
| C. /mɛ/ "meh" everywhere, as the tutorials teach | Follow the teaching material | All 178 IPA lines, 126 `may` and 3 `me` respellings change, and so does PRIMER. It keeps phonology.md:28's respelling "meh" but changes its IPA /meɪ/; 126 lines depart from that respelling today. There is a risk of reduction to /mə/, the -ma sound. English *meh* also carries a shrug, a register cost for a suffix that names received ordinance [from memory: not re-checked]. |
| D. Free variation | Write one canonical form and declare [meɪ ~ me ~ mɛ] all acceptable | The respelling layer cannot write "any of these", and the voice pipeline must pick one anyway. |

This proposal sets out the options and does not decree one.

### V.2 qing

**What the corpus does.** 34 words carry a line:

| Form | Words |
|---|---|
| /tɕʰiŋ/ | 17 |
| /t͡ɕɪŋ/ | 7 |
| /tʃɪŋ/ | 7 (britqing, danaqing, ifeqing, mahabbahqing, paqduqing, syzygyqing, tarabqing) |
| /tɕʰɪŋ/ | 2 |
| /tɕɪŋ/ | 1 |

- The respelling is `ching` in all 34.
- Four entries also offer /kɪŋ/ "-king" as acceptable (barakqing, hayatqing, natsarqing,
  zakarqing).
- kinqing offers `KIN-ting`.
- Tutorial 02 teaches /tɕɪŋ/ and calls /kɪŋ/ "acceptable" in casual speech.
  `[canon: tutorial/02-the-qing-family.md:118]`

**The donor.** Mandarin 情 *qíng*. Pinyin q is [tɕʰ]; the final -ing is [iŋ]; the acute marks the
second, rising tone [verified: https://en.wikipedia.org/wiki/Pinyin]. So the donor form is
[tɕʰiŋ] with a rising tone. The /t͡ɕɪŋ/, /tɕʰɪŋ/ and /tɕɪŋ/ lines are notation drift around that
one target, and VII heals them. The 7 /tʃɪŋ/ lines are a different thing: an English form
promoted to the main line.

**Ease.** English speakers already say [tʃɪŋ] ("ching"). [tɕʰ] is "similar to the ch in English
*punchy*" (same source). How many English listeners hear the difference was not checked.
/kɪŋ/ is easy,
but it costs two things:
- It is one consonant away from the **-kin** suffix /kɪn/. `suffix_families.json` defines qing
  and -kin *against each other* (felt-bond against bond-class). `[canon: script/suffix_families.json]`
- It is the English word *king*.

**Options (YU-2).**

| Option | Cost |
|---|---|
| A. Donor /tɕʰiŋ/ in every main line, /tʃɪŋ/ "acceptable" (the stated policy) | 7 main lines change; 10 notation heals |
| B. English /tʃɪŋ/ in every main line, donor form in the notes | 27 lines change, and the stated donor-first policy is reversed for the commonest donor sound |
| C. Two lines (VIII): donor /tɕʰiŋ/, said aloud [tʃɪŋ] | The new record field |

A separate question under YU-2: may /kɪŋ/ remain "acceptable"? Dropping it costs four alternates
and a sentence in tutorial 02. Keeping it costs the qing/-kin contrast in casual speech.

### V.3 -ance and -mance

**What the corpus does.** Canon has /əns/ in 7 of 8 lines: artiance, candence, complerescence,
melamance, oriance, panimaance, sukhance. kunance has /ans/, and lists /əns/ as its own alternate.
The 8 silent worship-action words all have /əns/ drafts in `forged.json`. The other records
differ:

| Record | Form | Words |
|---|---|---|
| Tutorial 03 | /ɑːns/ | sukhance, kimance, oriance, panimaance |
| PRIMER | /ɑːns/ | kimance, panimaance |
| PRIMER | /əns/ | oriance, sukhance |

`[canon: tutorial/03-ance-and-kin.md:38,53,68,83; PRIMER.md:84,130,138,144]`

**The donor.** Latin *-antia* reached YOUSPEAK through English *-ance* `[canon:
script/suffix_families.json]`. Latin had a full /a/ there [from memory: not re-checked]. English
unstressed *-ance* is /əns/, as in *distance* and *balance* [from memory: not re-checked].

**Ease.** English readers say /əns/ without being taught. Readers of other languages, reading
letter by letter, will say /ans/ or a French-style nasal [from memory: not re-checked].

**Options (YU-3).**

| Option | Cost |
|---|---|
| A. /əns/ (status quo) | kunance, tutorial 03 and PRIMER change |
| B. /ɑːns/, as the tutorials teach | The 6 canon -ance lines and the 8 drafts change. The -ence words candence and complerescence keep /əns/ unless the ruling names them. It gains a full, audible vowel. |
| C. Two lines: donor /ans/, said aloud /əns/ | The new record field |

**-mance.** The two -mance words (kimance, dokimance) both read /mæns/. PRIMER gives kimance
/mɑːns/. `suffix_families.json` declares no -mance family. melamance is spelled -mance but
declares -ance, and is sounded /əns/, because its m belongs to the stem *melammu*. So the
/mæns/ against /əns/ contrast is a fact about two words, not a family rule. It is recorded here
and needs no ruling.

### V.4 The small families

| Family | Corpus | Status |
|---|---|---|
| -kin | /kɪn/ in 2 of 2 (heurekin, walkekin) | Uncontested. Tutorial 03 differs only in walkekin's stem vowel. |
| -sis | /sɪs/ in 2 of 2, stress on the syllable before | Uncontested |
| -phanes | /fæn.iːz/ in 2 of 2 | The two members flip their stress (VII.A34) |
| -ma | /mə/ in 1 (athaumasma) | Uncontested; see V.1 on why -me should not reduce into it |
| -y | /i/ in 1 (diplosemy) | Respelled `my`, which reads /maɪ/ (VII.B32) |
| -basis | /bæs.ɪs/ in 1 (theobasis, filled in since the audit) | PRIMER gives /bɑːsɪs/ |

---

## VI. Tone and length

*Tone* is pitch that changes a word's meaning. In Yoruba, *ó bẹ* said on a high, a mid and a low
pitch means "jumped", "is forward" and "asks for pardon" [verified:
https://en.wikipedia.org/wiki/Yoruba_language]. *Vowel length* is holding a vowel longer, where
that can change a word.

### VI.1 How tone donors have been flattened

**Mandarin.**
- Every qing word comes from 情 *qíng*, with a rising tone [verified:
  https://en.wikipedia.org/wiki/Pinyin]. None of the 34 lines marks it.
- daome comes from 道 *dào*, whose IPA is [tâʊ], a falling tone [verified:
  https://en.wikipedia.org/wiki/Tao]. Its main line is the English /daʊ/. The donor form survives
  only as a "scholarly alt" /tâʊ.meɪ/, the only tone mark in the whole corpus.
- Pinyin d is the unaspirated [t] seen in that IPA, so /daʊ/ is also the English reading of the
  letter.
- renme keeps Mandarin r as /ʐ/ but drops *rén*'s tone [from memory: not re-checked].
- wujime writes *wújí* with its tones in the entry, then gives /ˈwuː.dʒi/ with English stress.
  `[canon: canon/core/wujime.md]`

**Yoruba.** Yoruba has three level tones. Acute marks high, grave marks low, and mid is unmarked
[verified: https://en.wikipedia.org/wiki/Yoruba_language]. Reading the canon's own donor
spellings by that rule:

| Word | Donor | Tones | Canon line | Stress |
|---|---|---|---|---|
| ifeqing | *ìfẹ́* | low–high | /ˈiːfɛtʃɪŋ/ | first syllable |
| emime | *èmí* | low–high | /ˈeɪ.miː.meɪ/ | first |
| oriance | *orí* | mid–high | /ˈɔː.ɹi.əns/ | first |
| aseme | *àṣẹ* | low–mid | no line; the `forged.json` draft is /a.ˈʃɛ.meɪ/ | second |

In all three canon lines the English stress lands on the first syllable, while the high tone sits
on the second. Tone has not been turned into stress; stress was simply put first.

There is also a small factual slip. aseme's own body says the ẹ of *àṣẹ* is "also low tone", and
`forged.json` repeats it. But ẹ carries no mark, which by the spelling rule means mid tone.
`[canon: canon/core/aseme.md:166; pipeline/voice/forged.json]`

**Cantonese.** No canon word draws its sound from Cantonese. The only Cantonese in canon is the
founding story of slipsooth, whose donors are English `[canon: canon/slipsooth.md]`. There is
nothing flattened to report.

**Vedic.** Vedic Sanskrit had a *pitch accent*: *udātta* "raised", *anudātta* "not raised", and
*svarita*, a falling pitch [verified: https://en.wikipedia.org/wiki/Vedic_accent]. "The above
system of accent disappeared completely at some point during the classical stage" [verified:
https://en.wikipedia.org/wiki/Sanskrit_phonology]. rtame, from *ṛta*, is the one entry labelled
Vedic. Its line /ˈrɪ.tɑː/ records no accent. It reads the syllabic ṛ as "ri", in the Hindi way,
and lengthens the final short a.

**Others flattened without comment.**
- Navajo has high and low tone [verified: https://en.wikipedia.org/wiki/Navajo_phonology]; see
  hozhome, from *hózhǫ́*.
- Third Mesa Hopi has tone on long vowels [verified: https://en.wikipedia.org/wiki/Hopi_language].
- Japanese has pitch accent (IV).

### VI.2 How length has been handled

The length mark ː does two jobs (I.5):
- **English vowel names:** /iː uː ɑː ɔː ɜː/, in 125 tokens.
- **Donor length:** /eː aː oː øː œː ɛː/, in 8 tokens.

Donor length is kept in some entries:
- Sanskrit ā against a in hastame (the audit shows this does not hold across the corpus).
- Polynesian *manā* in maname /naː/. Whether the donor vowel is long was not checked: Māori and
  Hawaiian *mana* may have short vowels and initial stress [from memory: not re-checked].
- Arabic *ḥayāt* in hayatqing /jaːt/.
- Hopi aa in koyaanisqatsime.

It is dropped in others:
- kenshōme becomes /ʃoʊ/.
- ihsanme drops the long ā of إحسان.
- ginnungame keeps its long n only in a note.

Hebrew is marked long in two words (emetme, devekutqing). Yet Modern Hebrew vowel length "is
non-contrastive" [verified: https://en.wikipedia.org/wiki/Modern_Hebrew_phonology], and the
corpus otherwise follows Modern Hebrew stress.

### VI.3 Policy options (YU-5)

| Option | Cost |
|---|---|
| A. Flatten openly | No tone or donor length in any line, and phonology.md says so in one sentence. Cheapest. It loses something POLYPHONIA names as each path's unique gift, most where tone carries meaning (Yoruba, Mandarin). |
| B. Record tone and length in the donor line only (VIII) | The said-aloud line stays flat and English-friendly. Each tone word needs a sourced donor form. daome's [tâʊ] is the model. |
| C. Map tone onto stress where a rule exists | For example, stress the syllable the donor gives a high tone (*ì-FẸ́*, *è-MÍ*, *o-RÍ*). This gives the said-aloud stress a principle, where today it has only habit. Mandarin monosyllables gain nothing. It is a new convention and needs testing on speakers. |
| D. Mark tone in the main line, as daome's alt does | Hardest for readers. It contradicts EUMATHE's "without hesitation". |

---

## VII. The ruling table

### VII.0 How the table was built

There are four parts:
- **A.** The audit's 49 findings, in its own order and cited by its line number. Each was
  re-checked against today's line. Two citations turned out to be misquotes: ubuntume and drujme
  already read /ʊ/ at the audit's own commit `10a4f7b` and at its parent.
- **B.** The checker's current findings on words the audit never saw. Most of these words entered
  canon after 2026-06-09.
- **C.** The four other records.
- **D.** Six errors this session found while writing II and IV.

A corrected line gives the whole frontmatter value. Three things are left untouched in it:
- the -me vowel and its respelling code (`may` or `meh`), which wait for YU-1;
- a qing main form of /tʃɪŋ/, and the "-king" alternates, which wait for YU-2;
- -ance /əns/ against /ɑːns/, which waits for YU-3.

Notation used in the healed lines follows the majority practice:
- Affricates are written without a tie bar, as 47 of the 60 affricate tokens already are. The
  syllable dot already tells /ts/ (one sound) from /t.s/ (two).
- A stress mark replaces the syllable dot rather than sitting beside it, as in 220 of 243
  lines.

Three working rules decide what counts as a plain HEAL:
- **The stated donor-segment policy.** `phonology.md` "For future forges" says "donor-marked
  segments preserved in the primary IPA with an anglicized alternate offered, never the
  reverse" `[canon: script/phonology.md:29-30]`, and its §3 names Arabic ḥā /ħ/ and Semitic
  qoph /q/ among them. A line that drops such a segment is healed toward it, with the plain
  sound as the alternate (A9, A12c, D3, D4, D7). A departure that someone wants kept is
  recorded as a stated exception, not healed.
- **The Hebrew default.** The corpus's Hebrew follows Modern Hebrew in stress, vowel length and
  ח (A18, A27, A36). The HONOR in A12a and the Hebrew silent words (IX) rest on that default;
  if YU-4 chooses a Tiberian-style Hebrew instead, they move together.
- **The interim stress rule.** Where the donor has no word stress to keep (Japanese pitch
  accent, Korean, Yoruba and Mandarin tone), the healed line puts its one primary where its
  own respelling does, and the row says *interim*. Which syllable is right is YU-4's no-stress
  clause. Where the donor has stress but this session could not verify it for the word, the
  row is a HEAL † instead: the donor fact exists and needs checking.

### VII.A The 49 findings of 2026-06-09

| # | Audit line | Words | Today | Disposition | Corrected line, reason, or options |
|---|---|---|---|---|---|
| A1 | L19 | britqing, danaqing, ifeqing, mahabbahqing, paqduqing, syzygyqing, and tarabqing since | open, 7 words | **YU-2** | Whether the main line carries donor /tɕʰiŋ/ or English /tʃɪŋ/. Options in V.2. |
| A2 | L20 | jeongqing | open | **HONOR** | The entry gives its reason: *jeong* and *qing* share the character 情, and "double-character 情情 resonance" is the point of the word. Stressing the second 情 makes the doubling audible. If Yu wants the suffix rule without exception, the line would be /ˈtɕʌŋ.tɕʰiŋ/ (JUNG-ching). The suffix notation is healed under A4. |
| A3 | L21 | kunance | open | **YU-3** | If YU-3 keeps /əns/, the line becomes `/ˈkuː.nəns/ (KOO-nunce; 2 syllables; Hebrew kûn + Latin -ance)`. That is its own listed alternate promoted. |
| A4 | L22 | barakqing, darshanqing, hayatqing, jeongqing, natsarqing, panimqing, zakarqing (/t͡ɕɪŋ/); hiraethqing, muditaqing (/tɕʰɪŋ/); kinqing (/tɕɪŋ/) | open, 10 words | **HEAL** | The donor is [tɕʰiŋ] (V.2), so every donor-faithful line writes /tɕʰiŋ/. Lines are in VII.A4 below. |
| A5 | L23 | the -me respelling split | open, 126 `may` / 51 `meh` / 3 `me` | **YU-1** | Once YU-1 is decided, every respelling is mechanically set to the chosen code. |
| A6 | L24 | agapeme | open | **HEAL** | `/əˈɡɑː.peɪ.meɪ/ (uh-GAH-pay-may; 4 syllables)`. The stem syllable `pe` becomes `pay`. The final `may` is a placeholder: the suffix takes whichever code YU-1 chooses, like every other -me line. |
| A7 | L25 | doxomme, kimme, panimqing, sukhance, theobasis | **CLOSED** | — | All five now carry real lines. PRIMER and the tutorials still disagree with four of them (C2, C3). |
| A8 | L29 | ubuntume | **CLOSED** (misquote) | — | The audit quoted /uˈbʌn/. The line read /uˈbʊn.tuː.meɪ/ at `10a4f7b` and before it. The respelling's OO is the house code for both /ʊ/ and /uː/. What remains is the general mixture of vowel systems (A14, YU-6). Zulu is [ùɓúntʼù] [verified: https://en.wikipedia.org/wiki/Ubuntu_philosophy]. |
| A9a | L30 | ihsanme | open | **HEAL** | `/ɪħˈsɑːn.meɪ/ (ih-SAHN-meh; 3 syllables; Arabic iḥsān + Sumerian me); anglicized /ɪhˈsɑːn.meɪ/ acceptable`. Restores ḥ, which is /ħ/ [verified: https://en.wikipedia.org/wiki/Arabic_phonology]. Restores the long ā that the entry's own إحسان writes with alif. Moves stress to the superheavy final syllable (also A39). This follows the stated policy: donor sound in the main line, anglicized form as alternate. |
| A9b | L30 | mahabbahqing | open | **HEAL** | `/məˈħɑb.bɑ.tʃɪŋ/ (ma-HAB-bah-ching; 4 syllables; Arabic maḥabbah + Mandarin qing); anglicized /məˈhɑb.bɑ.tʃɪŋ/ acceptable`. The entry writes محبة, with ح. The /tʃɪŋ/ waits for YU-2. |
| A9c | L30 (same case, not cited) | rahmame, hadaratme, wahdatwujudme | open | **HEAL** | The audit named three ḥ words; the corpus has six. hayatqing already writes /ħ/, and these three write /h/ for the ḥ their own donor fields spell (`[canon: canon/core/rahmame.md, hadaratme.md, wahdatwujudme.md]`). Without them the heal would leave ḥ as /h/ in half the corpus.<br>rahmame: `/ˈraħ.mɑ.meɪ/ (RAH-ma-may; 3 syllables; Arabic raḥma + Sumerian me); anglicized /ˈrah.mɑ.meɪ/ acceptable`.<br>hadaratme: `/ħʌˈdˤɑː.rʌt.meɪ/ (huh-DAH-rut-may; 4 syllables; Arabic ḥaḍarāt + Sumerian me); anglicized /hʌˈdɑː.rʌt.meɪ/ acceptable`. ḍ is restored with ḥ (A9d).<br>wahdatwujudme: `/ˌwʌħ.dʌt.ʌl.wʊˈdʒuːd.meɪ/ (wuh-dat-al-woo-JOOD-may; 6 syllables; Arabic waḥdat al-wujūd + Sumerian me); anglicized /ˌwʌh.dʌt.ʌl.wʊˈdʒuːd.meɪ/ acceptable`. |
| A9d | — (not in the audit) | ridame, tarabqing; hadaratme (A9c); sabrme (B16) | open | **HEAL** | The same policy reaches the Arabic emphatics: ص /sˤ/, ض /dˤ/, ط /tˤ/ [verified: https://en.wikipedia.org/wiki/Arabic_phonology]. No line writes one today, though the entries spell them (riḍā, ṭarab, ḥaḍarāt, ṣabr).<br>ridame: `/rɪˈdˤɑː.meɪ/ (rih-DAH-may; 3 syllables; Arabic riḍā + Sumerian me); anglicized /rɪˈdɑː.meɪ/ acceptable`.<br>tarabqing: `/ˈtˤɑː.rʌb.tʃɪŋ/ (TAH-rub-ching; 3 syllables; Arabic ṭarab + Mandarin qing); anglicized /ˈtɑː.rʌb.tʃɪŋ/ acceptable`. The /tʃɪŋ/ waits for YU-2.<br>ayanme is not healed: its entry records dropping the ʿayn of *aʿyān* as a deliberate naturalization loss `[canon: canon/core/ayanme.md:51]`, so its line follows its spelling. If Yu would rather keep §3's list to the segments it names (ḥā, qoph), this row is withdrawn and the emphatics are recorded as a stated exception. |
| A10 | L31 | visageqing | open | **HEAL** | `/viˈzɑːʒ.tɕʰiŋ/ (vi-ZAHZH-ching; 3 syllables)`. The respelling now matches its own IPA's /z/. |
| A11 | L32 | the qing transcriptions | open | **YU-2** with A4 | The same matter as A1 and A4. |
| A12a | L33 | tikkunme, devekutqing (/k/ for qof); qinance and qorvance (IX) | open | **HONOR** | "The [k] allophone merged with /q/ into SIH /k/" in Modern Hebrew [verified: https://en.wikipedia.org/wiki/Modern_Hebrew_phonology], and the corpus's Hebrew follows Modern Hebrew in stress, length and ח (VII.0). §3's "Semitic qoph → uvular /q/" was read off qorbme, whose donor is Proto-Semitic *q-r-b*, not Hebrew `[canon: canon/core/qorbme.md:19]`; qorbme keeps /q/. The q-spelled Hebrew silent words take /k/ with a Tiberian-style /q/ alternate (IX). This HONOR rests on YU-4's Hebrew default: if YU-4 chooses a Tiberian-style Hebrew, these four words move to /q/ together. |
| A12b | L33 | barakqing; zakarqing | open | **YU-6** | The audit misnamed the letter: ברך has kaf, not qof, so /q/ is not at issue. But this kaf is spirantized (*berékh, berákh, barákh*, romanized with kh [verified: https://en.wiktionary.org/wiki/ברך]; kaf's fricative allophone is /χ/ in Modern Hebrew [verified: https://en.wikipedia.org/wiki/Modern_Hebrew_phonology]). So /k/ follows the YOUSPEAK spelling and Strong's transliteration "barak", not the donor. zakarqing (זכר *zakhár*) is the same case [from memory: not re-checked]. Whether a k-spelled spirantized kaf is /k/ or /χ/ goes with halakhame's /χ/ (A27). This was CLOSED in the first draft; the review showed it is not. |
| A12c | L33 | paqduqing | open | **HEAL** † | `/ˈpɑːq.duː.tʃɪŋ/ (PAHK-doo-ching; 3 syllables; Akkadian paqdu + Mandarin qing); anglicized /ˈpɑːk.duː.tʃɪŋ/ acceptable`. The word spells q, and the stated policy keeps marked donor sounds in the main line. Akkadian q as a marked "emphatic" sound is [from memory: not re-checked]. The respelling `PAQ` cannot be read by an English reader; `PAHK` can. |
| A13a | L34 | mandalame | open | **HEAL** | `/ˈmʌn.dʌ.lʌ.meɪ/ (MUN-duh-luh-may; 4 syllables)`. Sanskrit *máṇḍala* and English /ˈmʌn.də.lə/ both stress the first syllable [verified: https://en.wiktionary.org/wiki/mandala]. This also removes an invented long /ɑː/ (A38). |
| A13b | L34 | rtame, jivame, tapasme; margame's alternate | open | **HEAL** | An unstressed short Sanskrit a written /ɑː/ matches no tradition this proposal offers: neither a reconstructed [ɐ] nor English-Indological /ə/ (English *mandala* /ˈmʌn.də.lə/ [verified: https://en.wiktionary.org/wiki/mandala]).<br>rtame: `/ˈrɪ.tʌ.meɪ/ (RIH-tuh-meh; 3 syllables)`.<br>jivame: `/ˈdʒiː.vʌ.meɪ/ (JEE-vuh-meh; 3 syllables)`.<br>tapasme: `/ˈtɑː.pʌs.meɪ/ (TAH-pus-meh; 3 syllables)`.<br>margame: `/ˈmɑːr.ɡə.meɪ/ (MAR-guh-meh; 3 syllables; Sanskrit-style alt /ˈmɑːr.ɡʌ.meɪ/ MAR-guh-meh)`. Its main line and alternate now differ only in /ə/ against /ʌ/, which A13c leaves to YU-4.<br>shamathaqing's stressed /ɑː/ is handled with its stress (A38e). |
| A13c | L34 | hastame, spandaqing, rasame; silame | open | **YU-4** | Left to YU-4: the stressed Sanskrit a (/ʌ/ in hastame and spandaqing, /ɑː/ in tapasme and rasame) and /ʌ/ against /ə/ for the unstressed one. Sanskrit short a sits close to English /ʌ/ [from memory: not re-checked]. silame is in the audit's list, but its donor is Inuit *sila*, not Sanskrit `[canon: canon/core/silame.md]`; its /ʌ/ goes with the same choice only by analogy. |
| A14 | L35 | the Hebrew and Arabic *a* written five ways | open | **YU-6** | Two vowel systems in one line (I.5). |
| A15 | L36 | heurekin, eurekame, noesisme, noemame, zoeme, agapeme, morphame | open | **YU-4** | Classical Attic η was /ɛː/; Koine moved it toward /i/ [verified: https://en.wikipedia.org/wiki/Ancient_Greek_phonology]. English-scholarly readings use both /iː/ and /eɪ/. The question is which tradition, and then one reading per root (heurēka). |
| A16 | L37 | allostasisqing /steɪ/, anagnoristasis /stæs/ | open | **YU-4** | One morpheme should have one reading. Which one follows the YU-4 tradition choice. |
| A17 | L38 | autopistme, autopoieme | open | **HEAL** | autopistme: `/ˌɔː.toʊˈpɪst.meɪ/ (aw-toh-PIST-meh; 4 syllables)`.<br>autopoieme: `/ˌɔː.toʊ.pɔɪˈeɪ.meɪ/ (aw-toh-poy-AY-may; 5 syllables)`.<br>autoxenia already has /ˌɔː.toʊ/, so this makes 3 of 3 agree. It also heals A41 and A48 for these two words. |
| A18 | L39 | emetme, shemme, devekutqing (Hebrew e length) | open | **HEAL** | Drop ː on the Hebrew e, since Modern Hebrew length is non-contrastive [verified: https://en.wikipedia.org/wiki/Modern_Hebrew_phonology]. The lines are under A36. shemme /ˈʃɛm.meɪ/ needs no change. |
| A19 | L40 | sabbathme | open | **HEAL** | `/ˈsæb.əθ.meɪ/ (SAB-uth-may; 3 syllables)`. The house code reads `SAB` as /æ/. English *sabbath* has /æ/ [from memory: not re-checked]. |
| A20 | L41 | ethosme | open | **HEAL** | `/ˈɛθ.ɒs.meɪ/ (ETH-os-may; 3 syllables)`. This heals the respelling (`ohs` against /ɒ/), which is what the audit found. The vowel itself is a separate YU-4 question: ἦθος has η, and /ɛ/ fits neither Attic /ɛː/ nor English *ethos* /ˈiːθɒs/ [from memory: not re-checked]; it goes with A15. |
| A21 | L42 | anagnoristasis | open | **HEAL** | `/ˌæn.əɡ.nɒr.ɪˈstæs.ɪs/ (an-ag-nor-i-STAS-is; 6 syllables)`. This also fixes the ASCII g (B22) and adds the missing count (B32). |
| A22 | L43 | tjukurpame (respelling) | open | **HEAL** | The respelling `chuh` becomes `choo`. The full line is A38b's: `/ˈtʃʊ.kʊr.pə.meɪ/ (CHOO-koor-puh-may; 4 syllables)`. |
| A23 | L44 | noetherme | open | **HEAL** | `/ˈnøː.tər.meɪ/ (NUR-ter-may; 3 syllables; German Noether, ö as /øː/); anglicized /ˈnɜː.tər.meɪ/ acceptable`. The anglicized vowel moves from the respelling into a declared alternate, as policy asks. |
| A24 | L45 | molkme, ondame, hotepme, eikonme, penthosme | open | **YU-6** | The o written in two systems. |
| A25 | L46 | britqing, tzimtzumme, tikkunme, rigpame, xeniame, duyuktame, walkekin | open | **YU-6** | Cardinal and English short vowels mixed. |
| A26 | L47 | natsarqing, tzimtzumme (tsade) | open | **HEAL** (notation only) | natsarqing: `/naˈtsar.tɕʰiŋ/ (nat-SAR-ching; 3 syllables; Hebrew natsar + Mandarin qing); anglicized /natˈsar.kɪŋ/ acceptable`.<br>tzimtzumme: under A28.<br>Said aloud, nothing changes. |
| A27 | L48 | chayimme, halakhame | open | **HEAL** | chayimme: `/χaˈjiːm.meɪ/ (chai-YEEM-meh; 3 syllables; Hebrew chet /χ/); anglicized /haɪˈiːm.meɪ/ (high-EEM-meh) acceptable`.<br>halakhame: `/ha.laˈχa.meɪ/ (ha-la-KHA-meh; 4 syllables; softer alt /ha.laˈha.meɪ/ ha-la-HA-meh)`.<br>In Modern Hebrew ח "has merged with /x/ … into /χ/" [verified: https://en.wikipedia.org/wiki/Modern_Hebrew_phonology], which is what chayimme's note already says. barzakhqing (Arabic) keeps /x/. |
| A28 | L49 | jivame, tjukurpame, pachame, tzimtzumme, and the seven /t͡ɕ/ (A4) | open | **HEAL** (notation only) | jivame: under A13b, whose line also drops the tie bar.<br>tzimtzumme: `/tsimˈtsum.meɪ/ (tsim-TSUM-may; 3 syllables)`.<br>tjukurpame: A22.<br>pachame: D6. |
| A29 | L50 | oriance | open | **HEAL** | `/ˈoʊ.ri.əns/ (OH-ree-ance; 3 syllables; Yoruba orí + Latin -ance)`. ɹ becomes r, as in every other line. /ɔː/ becomes /oʊ/: orí has a plain o, and "The oral /e, o/ are close-mid [e, o]", while the dotted ọ is the open [ɔ] [verified: https://en.wikipedia.org/wiki/Yoruba_language]. The line's own respelling OH is /oʊ/ in the house code (ponome `POH` /poʊ/, alohame `LOH` /loʊ/). |
| A30 | L51 | daome (the one tone mark) | open | **YU-5** | See VI. |
| A31 | L52 | nommome, nyamame | open | **HEAL** | nommome: `/ˈnɒm.oʊ.meɪ/ (NOM-mo-may; 3 syllables)`.<br>nyamame: `/ˈnjɑː.mɑː.meɪ/ (NYAH-mah-may; 3 syllables)`.<br>The full stem vowel is in the respelling, in DICTIONARY (`NYAH-mah-may`), in tutorial 01, and, by the audit's report, in the donors. This also adds the dots (A41). |
| A32 | L56 | wiconime | open | **HEAL** | `/wiːˈtʃoʊ.niː.meɪ/ (wee-CHOH-nee-meh; 4 syllables)`. Lakota stresses the second syllable (IV). |
| A33 | L57 | jeongqing | open | **HONOR** | As A2. |
| A34 | L58 | kallophanes, orthophanes | open | **HEAL** | kallophanes: `/ˌkæl.oʊˈfæn.iːz/ (kal-lo-PHAN-ees; 4 syllables)`. Both respellings already stress PHAN. kallodoxa has the same /ˌkæl.oʊˈ/ pattern. orthophanes gains its count: `(or-tho-PHAN-ees; 4 syllables)`. This aligns the IPA with the two respellings and with phonology.md §1's "-PHAN-ees". English classical practice would instead stress the syllable before *-phanes* and reduce *-phan-* (*Aristophanes*) [from memory: not re-checked]; that tradition question belongs to YU-4. |
| A35 | L59 | artiance | open | **HONOR** | `ar-TI-ance` with /aɪ/ is an English-habit reading by analogy with *defiance* and *reliance*. `phonology.md` §2 (line 70) records it as such, and canon and DICTIONARY agree. English *-iance* has /aɪ/ only where the base verb ends in stressed -y (*defy, rely*); after another base it is /i.əns/ (*variance, radiance*) [from memory: not re-checked]. artiance has no such base, so this is a kept habit, not an English rule. Its three donor stems do not share one stress: Latin *ars, artis*, Greek *ártios*, Greek *aretḗ*. It needs only its count, `(ar-TI-ance; 3 syllables)` (B32). |
| A36 | L60 | emetme, devekutqing, shevirame | open | **HEAL** | emetme: `/ɛˈmɛt.meɪ/ (eh-MET-meh; 3 syllables)`. The note "emet-stress on first syllable from Hebrew" is removed: Modern and Tiberian Hebrew both stress the last syllable [verified: https://en.wiktionary.org/wiki/אמת].<br>devekutqing: `/də.vɛˈkuːt.tɕʰiŋ/ (deh-veh-KOOT-ching; 4 syllables)`, from *dvekút* [verified: https://en.wiktionary.org/wiki/דבקות].<br>shevirame: `/ʃə.viːˈrɑː.meɪ/ (sheh-vee-RAH-may; 4 syllables)`, from *shvirá* [verified: https://en.wiktionary.org/wiki/שבירה]. |
| A37 | L61 | eranosme, zoeme, palamasme | open | **YU-4** | English-scholarly or donor stress for Greek. |
| A38a | L62 | mandalame | open | **HEAL** | As A13a. |
| A38b | L62 | tjukurpame | open | **HEAL** † | `/ˈtʃʊ.kʊr.pə.meɪ/ (CHOO-koor-puh-may; 4 syllables)`. Initial stress in Pitjantjatjara is [from memory: not re-checked]. The only evidence seen today is the language name transcribed [ˈpɪɟanɟaɟaɾa], with no rule stated [verified: https://en.wikipedia.org/wiki/Pitjantjatjara_dialect]. |
| A38c | L62 | wairuaqing | open | **HEAL** † | `/ˈwaɪ.ru.ʌ.tɕʰiŋ/ (WHY-roo-uh-ching; 4 syllables)`. Māori stress on the *wai-* diphthong is [from memory: not re-checked]; the part of the Māori article read today stated no rule. |
| A38d | L62 | darshanqing | open | **HEAL** † | `/ˈdar.ʃan.tɕʰiŋ/ (DAR-shan-ching; 3 syllables; Sanskrit darshan + Mandarin qing)`. Initial stress in *darśan* is [from memory: not re-checked]. Wiktionary gives no English IPA [verified: https://en.wiktionary.org/wiki/darshan]. |
| A38e | L62 | shamathaqing | open | **HEAL** † | `/ˈʃʌ.mʌ.tʌ.tɕʰiŋ/ (SHUH-muh-tuh-ching; 4 syllables; Sanskrit śamatha + Mandarin qing)`. Sanskrit has a stress tradition, so this is the same case as darshanqing (A38d), not a no-stress donor. The classical rule (stress a heavy second-to-last syllable, otherwise the one before) [from memory: not re-checked] gives *ŚA-ma-tha*, as it gives *DAR-śa-na*. The second a is then unstressed, and the long /ɑː/ goes with the stress (A13b). The entry's donor label is Tibetan; the stem is the Sanskrit word `[canon: canon/core/shamathaqing.md:18,20]`. In the first draft this row was YU-4. |
| A39 | L63 | ihsanme (stress) | open | **HEAL** | As A9a. |
| A40 | L64 | visageqing | open | **HEAL** | As A10. |
| A41 | L65 | ifeqing, nommome, nyamame, autopistme, noesisme (missing dots) | open | **HEAL** | ifeqing: `/ˈiː.fɛ.tʃɪŋ/ (EE-feh-ching; 3 syllables)`. The respelling `I` read as EYE, so it becomes `EE`.<br>noesisme: `/noʊˈiː.sɪs.meɪ/ (no-EE-sis-meh; 4 syllables; alternative /noʊˈɛ.sɪs.meɪ/ no-EH-sis-meh)`. The label "classical-Greek-style" is dropped: νόησις is accented on νό- [from memory: not re-checked], which neither form follows.<br>The other three are under A31 and A17. |
| A42 | L66 | daome, duyuktame | open | **HEAL** | daome: `/ˈdaʊ.meɪ/ (DOW-meh; 2 syllables; scholarly alt /tâʊ.meɪ/ TAU-meh)`.<br>duyuktame: `/duˈjuk.ta.meɪ/ (doo-YOOK-tah-may; 4 syllables)`. |
| A43 | L67 | doxakallos | open | **HEAL** (one primary) + **YU-4** (which element) | `/ˌdɒk.səˈkæl.ɒs/ (dox-a-KAL-los; 4 syllables)`. Two primaries is a plain error. Putting the primary on the last element follows its mirror word kallodoxa: the proposed house compound pattern (IV), which YU-4 decides. |
| A44 | L68 | britqing (count) | open | **HEAL** | `/ˈbrit.tʃɪŋ/ (BRIT-ching; 2 syllables)`. The qing form waits for YU-2. |
| A45 | L69 | ahavame | open | **HEAL** | `/a.haˈvɑː.meɪ/ (ah-hah-VAH-meh; 4 syllables; Hebrew ahavá + Sumerian me)`. The audit found only the hedged count, but the first draft's heal kept the stress on HAH, against the donor: *ahavá*, Modern /ʔa.haˈva/, Tiberian /ʔa.hăˈvɔː/, final stress in both [verified: https://en.wiktionary.org/wiki/אהבה]. A36's logic for emetme, devekutqing and shevirame applies. The pretonic /a/ follows barakqing, zakarqing and halakhame. |
| A46 | L70 | the -me respelling | open | **YU-1** | As A5. |
| A47 | L71 | walkekin | open | **HEAL** | `/ˈwɑl.kə.kɪn/ (WAL-kuh-kin; 3 syllables)` |
| A48 | L72 | 7 lines, and 23 lines today, writing a dot beside a stress mark | open | **HEAL** (notation only) | The dot goes and the mark stays. Lines are in VII.A48 below. |
| A49 | L73 | noetherme | open | **HEAL** | As A23. |

**VII.A4: the ten qing lines** (notation only; the respelling is unchanged)

| Word | Corrected line |
|---|---|
| barakqing | `/baˈrak.tɕʰiŋ/ (bah-RAHK-ching; 3 syllables; Hebrew barak + Mandarin qing); anglicized /baˈrak.kɪŋ/ (bah-RAHK-king) acceptable` |
| darshanqing | `/darˈʃan.tɕʰiŋ/ (dar-SHAN-ching; 3 syllables; Sanskrit darshan + Mandarin qing)`. Its stress is a separate question (A38d). |
| hayatqing | `/ħaˈjaːt.tɕʰiŋ/ (hah-YAHT-ching; 3 syllables); anglicized /haˈjaːt.kɪŋ/` |
| jeongqing | `/tɕʌŋˈtɕʰiŋ/ (jung-CHING; 2 syllables; Korean jeong + Mandarin qing; double-character 情情 resonance); anglicized /dʒʌŋˈtɕʰiŋ/ acceptable`. Korean ㅈ stays the unaspirated /tɕ/. |
| natsarqing | as A26 |
| panimqing | `/paˈniːm.tɕʰiŋ/ (pah-NEEM-ching; 3 syllables)` |
| zakarqing | `/zaˈkar.tɕʰiŋ/ (zah-KAR-ching; 3 syllables; Hebrew zakar + Mandarin qing); anglicized /zaˈkar.kɪŋ/ (zah-KAR-king) acceptable` |
| hiraethqing | `/ˈhɪr.aɪθ.tɕʰiŋ/ (HEER-ighth-ching; 3 syllables; Welsh ae as /aɪ/); anglicized /ˈhɪər.ɛθ.tʃɪŋ/ acceptable` |
| muditaqing | as B21 |
| kinqing | `/ˈkɪn.tɕʰiŋ/ (KIN-ching; 2 syllables; Mandarin q as /tɕʰ/; English approximation "KIN-ting" acceptable)` |

**VII.A48: a stress mark replaces the dot** (IPA only; the rest of each line is unchanged
unless another row heals it)

| Word | Corrected IPA | Word | Corrected IPA |
|---|---|---|---|
| complerescence | /ˌkɒm.pləˈrɛs.əns/ | kumarme | /kʊˈmɑːr.meɪ/ |
| eternalme | /ɪˈtɜː.nəl.meɪ/ | liturgiame | /lɪˈtɜː.dʒi.ə.meɪ/ |
| katsintawime | /kat.sinˈta.wi.meɪ/ | mugawme | /muˈɡaw.meɪ/ |
| sankofame | /sɑnˈkɔ.fa.meɪ/ | tinaime | /tɪˈnaɪ.meɪ/ |
| wakanme | /waˈkɑn.meɪ/ | yvymarame | /ɪ.vɪ.mɑˈɾɑ.meɪ/ |

The other thirteen are healed in their own rows: agapeme (A6), ahavame (A45), anamcharame (B7),
autopoieme (A17), aynime (B24), halakhame (A27), hopiqatsime (D3), kobame (B26),
koyaanisqatsime (B14), mahabbahqing (A9b), pachame (D6), warame (D7) and doxakallos (A43).

### VII.B The checker's findings since the audit

| # | Words | Finding | Disposition | Corrected line or reason |
|---|---|---|---|---|
| B1 | daigome | no primary stress; ASCII g | **HEAL** (notation), interim stress | `/ˈdaɪ.ɡoʊ.meɪ/ (DYE-goh-may; 3 syllables; Japanese 大悟 + Sumerian 𒈨)`. Japanese has pitch accent, not stress (IV). The respelling and the first-syllable option of YU-4 agree here. |
| B2 | kwothme | no primary stress | **HEAL** † | `/ˈkʷoθ.meɪ/ (KWOTH-may; 2 syllables; Nuer kwoth + Sumerian me)`. The stress is certain (one stem syllable); the † is for the th, which in Nuer may be a dental stop rather than /θ/ (X.5). |
| B3 | satorime | no primary stress; respelling caps nothing | **HEAL** (notation), interim stress † | `/saˈto.ɾi.me/ (sah-TOH-ree-may; 4 syllables; Japanese 悟り + Sumerian 𒈨)`. Japanese has pitch accent, not stress. The respelling caps nothing, so the interim stress follows English *satori* [from memory: not re-checked]. YU-4's first-syllable option would give `/ˈsa.to.ɾi.me/ (SAH-toh-ree-may)`. The /me/ waits for YU-1. |
| B4 | sinbyeongme | no primary stress | **HEAL** (notation), interim stress | `/ɕinˈbjʌŋ.meɪ/ (sin-BYONG-may; 3 syllables; Korean sinbyeong + Sumerian me)`. Follows the respelling. Korean has no word stress (IV); YU-4's first-syllable option would give `/ˈɕin.bjʌŋ.meɪ/ (SIN-byong-may)`. |
| B5 | sinmyeongme | no primary stress | **HEAL** (notation), interim stress | `/ɕinˈmjʌŋ.meɪ/ (sin-MYONG-may; 3 syllables)`. As B4; the first-syllable option is `/ˈɕin.mjʌŋ.meɪ/ (SIN-myong-may)`. |
| B6 | teyoliame | no primary stress | **HEAL** | `/tɛ.joʊˈli.ɑ.meɪ/ (teh-yoh-LEE-ah-meh; 5 syllables; Nahuatl yōlia + Sumerian me)`. Nahuatl stresses the second-to-last syllable (IV), counted over the stem *yōlia*, as the stated rule keeps the stem's own stress; IX applies the same reading to teotlme. That *ia* is two syllables in *yōlia* is [from memory: not re-checked]. |
| B7 | anamcharame | two primaries; IPA letter in respelling; ch | **HEAL** (one primary; ch) + **YU-4** (which element) | `/ˌan.əmˈxa.rɑ.meɪ/ (an-um-KHAR-ah-may; 5 syllables; Old Irish anam chara + Sumerian me); anglicized /ˌan.əmˈka.rɑ.meɪ/ (an-um-KAR-ah-may) acceptable`. Irish broad ch is /x/ [verified: https://en.wikipedia.org/wiki/Irish_orthography]; the Old Irish value is [from memory: not re-checked]. /tʃ/ fits neither the Irish nor the common English *anam cara*. The primary on the last element is the proposed house compound pattern (IV). Irish first-syllable stress [from memory: not re-checked] would give `/ˈan.əmˌxa.rɑ.meɪ/ (AN-um-khar-ah-may)`. |
| B8 | asraya-paravrttime | two primaries; vowel-less /rt/; count | **HEAL** (one primary; syllabic ṛ; count) + **YU-4** (which element and syllable) | `/ʌˌʃra.jʌ.pʌˈrɑː.vr̩t.ti.meɪ/ (uh-shrah-yuh-puh-RAH-vrit-tee-may; 8 syllables; Sanskrit āśraya-parāvṛtti + Sumerian me)`. Sanskrit ṛ is a vowel-like syllabic r [from memory: not re-checked], so *vṛt* is a syllable, and the total is 8, not 7. The primary follows the canon respelling's RAH under the proposed house compound pattern. By the classical rule a heavy second-to-last syllable takes the stress, so *parāvṛtti* may stress *vṛt* [from memory: not re-checked]: `/ʌˌʃra.jʌ.pʌ.rɑːˈvr̩t.ti.meɪ/ (uh-shrah-yuh-puh-rah-VRIT-tee-may)`. |
| B9 | humahukhtahvarshtame | two primaries; secondary capped; kh as /k/ | **HEAL** (one primary; x) + **YU-4** (which element) | `/ˌhu.məˌhʊx.təˈvɑːrʃ.tə.meɪ/ (hoo-muh-hookh-tuh-VARSH-tuh-may; 7 syllables; Avestan humata-hūxta-xᵛaršta + Sumerian me); anglicized /ˌhu.məˌhʊk.təˈvɑːrʃ.tə.meɪ/ acceptable`. Avestan x is /x/ and xᵛ is /xʷ/ [verified: https://en.wikipedia.org/wiki/Avestan_alphabet]; that the words are *hūxta* and *xᵛaršta* is [from memory: not re-checked]. The canon /k/ for kh was a donor error (II.3). The primary on the last element is the proposed house compound pattern. |
| B10 | autoxenia | vowel-less /k/ | **HEAL** | `/ˌɔː.toʊˈksɛ.ni.ə/ (aw-toh-KSEH-nee-ah; 5 syllables)`. This follows the respelling and xeniame's /ks/ onset. The /ks/ onset is a choice: `/ˌɔː.toʊkˈsɛ.ni.ə/ (aw-tohk-SEH-nee-ah)` keeps the original dot and III's template. |
| B11 | algiadoxame | count 5 against IPA 6; `gi` reads as hard g | **HEAL** | `/ˌæl.dʒi.əˈdɒk.sə.meɪ/ (al-jee-uh-DOK-suh-may; 6 syllables)` |
| B12 | doxalgiame | count 4 against IPA 5 | **HEAL** | `/dɒkˈsæl.dʒi.ə.meɪ/ (dok-SAL-jee-uh-may; 5 syllables)`. Its root doxalgia is /dɒkˈsæl.dʒi.ə/, 4 syllables, plus -me. |
| B13 | ereckappayime | count 5 against IPA 6 | **HEAL** † | `/ˌɛr.ɛkˈɑp.pɑː.ji.meɪ/ (er-ek-AHP-pah-yee-may; 6 syllables)`. This fixes the count only. It re-issues two donor questions without settling them: the Hebrew dual *-áyim* would put the stress on *pa*, not *ap* [from memory: not re-checked], and *erekh*'s final kaf is spirantized, which Modern Hebrew says as /χ/ [verified: https://en.wikipedia.org/wiki/Modern_Hebrew_phonology] (as A12b). |
| B14 | koyaanisqatsime | count 5 against IPA 6; secondary capped | **HEAL** | `/koʊˈjɑː.nɪsˌqɑːt.si.meɪ/ (ko-YAH-nis-kaht-see-may; 6 syllables; Hopi koyaanisqatsi, q = [k̠] + Sumerian me); anglicized /koʊˈjɑː.nɪsˌkɑːt.si.meɪ/ acceptable`. The /q/ is D3's. |
| B15 | damqme | vowel-less /q/ | **HEAL** | `/ˈdæmq.meɪ/ (DAMK-may; 2 syllables; Akkadian damqu + Sumerian me)`. This keeps the declared count and the donor consonant. If YU-6 chooses epenthesis for B16, damqme would follow as `/ˈdæm.qə.meɪ/`. |
| B16 | sabrme, shukrme; faqrme (D4) | count 2 against syllabic r 3; the same donor shape treated two ways (III) | **YU-6** | One rule for all three. The donor-against-said-aloud split is exactly YU-6's question, so both line sets are given:<br>(a) Main line follows the donor, as the stated policy asks; the said-aloud form is the alternate:<br>sabrme `/ˈsˤɑbr.meɪ/ (SABR-meh; 2 syllables; Arabic ṣabr + Sumerian me); anglicized /ˈsɑ.bər.meɪ/ (SAH-ber-meh) acceptable`<br>shukrme `/ˈʃʊkr.meɪ/ (SHUKR-meh; 2 syllables; Arabic shukr + Sumerian me); anglicized /ˈʃʊ.kər.meɪ/ (SHOO-ker-meh) acceptable`<br>faqrme `/ˈfɑqr.meɪ/ (FAHKR-may; 2 syllables; Arabic faqr + Sumerian me); anglicized /ˈfɑk.rə.meɪ/ (FAK-ruh-may) acceptable`<br>(b) Epenthesis in all three main lines, donor consonants kept:<br>sabrme `/ˈsˤɑ.bər.meɪ/ (SAH-ber-meh; 3 syllables)`; shukrme `/ˈʃʊ.kər.meɪ/ (SHOO-ker-meh; 3 syllables)`; faqrme `/ˈfɑq.rə.meɪ/ (FAHK-ruh-may; 3 syllables)`.<br>(a) creates the codas /br/, /kr/ and /qr/, which III's template rejects for new coinages; the template does not reshape existing words. ṣ is /sˤ/ (A9d). The first draft healed sabrme and shukrme toward (a) and faqrme toward (b); the review caught the contradiction. |
| B17 | songlineme | count 4 against IPA 3 | **HEAL** | `/ˈsɒŋ.laɪn.meɪ/ (SONG-line-may; 3 syllables; English songline + Sumerian me)` |
| B18 | thirdnessqing, secondnessqing | count; ə in the respelling | **HEAL** | thirdnessqing: `/ˈθɜːd.nəs.tɕʰiŋ/ (THURD-nus-ching; 3 syllables)`.<br>secondnessqing: `/ˈsɛk.ənd.nəs.tɕʰiŋ/ (SEK-und-nus-ching; 4 syllables)`. |
| B19 | manidoome | missing dot; IPA stress against respelling | **HEAL** † | `/ˈmæn.ɪ.doʊ.meɪ/ (MAN-i-doh-may; 4 syllables)`. Follows the respelling and English *manitou* [from memory: not re-checked]. Ojibwe stress was not checked. The canon IPA's primary on /doʊ/ may be the form faithful to Ojibwe, where long vowels attract stress [from memory: not re-checked]; if so, heal the respelling instead (`man-i-DOH-may`). |
| B20 | kinhme | suffix stressed | **HEAL** (stress only) | `/ˈkʔɪn.meɪ/ (K'IN-may; 2 syllables; glottal stop preserved)`. Stress goes back to the stem, as in the rule. Vowel length and the ejective notation wait for YU-6 (D8); `forged.json` and the voice already say /ˈkʼiːn/, with an ejective and a long vowel. IX defers to the same ruling. |
| B21 | muditaqing | suffix stressed | **HEAL** † | `/ˈmuː.di.tɑː.tɕʰiŋ/ (MOO-dee-tah-ching; 4 syllables)`. Pali has a stress tradition, so this is a † HEAL, not an interim one. Pali initial stress is [from memory: not re-checked]. |
| B22 | ginnungame, ragnarokme, voghbme, yggdrasilme | ASCII g | **HEAL** (notation; ragnarokme's vowel) | ginnungame: `/ˈɡɪn.ʊn.ɡɑː.meɪ/ (GIN-un-gah-may; 4 syllables; Old Norse /ˈɡinːuŋɡɑp/ with long n and back a)`.<br>ragnarokme: `/ˈraɡ.na.rɒk.meɪ/ (RAG-na-rok-may; 4 syllables; Old Norse Ragnarǫk [ˈrɑɣnɑˌrɒk]); anglicized /ˈræɡ.nə.rɒk.meɪ/ acceptable`. Old Norse ǫ was back [verified: https://en.wikipedia.org/wiki/Ragnar%C3%B6k]; the canon /œ/ is the Modern Icelandic *ö*. If Yu prefers the headword's *ö*, keep /œ/ and label the note "Modern Icelandic ragnarök".<br>voghbme: `/ˈvoʁb.meɪ/ (VOGH-bmay; 2 syllables; Armenian gh = voiced velar/uvular fricative); anglicized /ˈvoɡb.meɪ/ (VOG-bmay) acceptable`.<br>yggdrasilme: `/ˈɪɡ.drə.sɪl.meɪ/ (IG-druh-sil-may; 4 syllables; anglicized /ˈɪɡ.drə.sɪl.meɪ/; Old Norse /ˈyɡˌdrasil/ with front-rounded y)`. Its main line equals its own "anglicized" alternate, and the donor form sits only in a note: the reverse of the stated order (phonology.md:29-30), with no flag. Promoting the donor form goes with YU-6. |
| B23 | andemame | respelling stress | **HEAL** | `/ˌæn.dɛˈmɑː.meɪ/ (an-deh-MAH-may; 4 syllables)`. The IPA already follows Hebrew *dmamá* (IV). |
| B24 | aynime | IPA stress | **HEAL** | `/ˈaɪ.ni.meɪ/ (AY-nee-may; 3 syllables; Aymara ayni + Sumerian me)`. Aymara stresses the second-to-last syllable (IV). |
| B25 | dalime | IPA stress | **HEAL** † | `/ˈdɑː.liː.meɪ/ (DAH-lee-may; 3 syllables; Georgian/Svan Dali stress preserved in compound, Sumerian -me suffix)`. The entry claims to keep the donor stress, and its respelling stresses DAH. Georgian stress was not checked [from memory: not re-checked]. |
| B26 | kobame | IPA stress | **HEAL** † | `/koˈba.meɪ/ (ko-BA-may; 3 syllables; Basque koba + me)`. The respelling is healed, not the IPA: for Standard Basque, Euskaltzaindia recommends a weak, high-pitched stress on the second syllable of a phrase [verified: https://en.wikipedia.org/wiki/Basque_language, "Stress and pitch"], which the canon IPA already has. The † is for dialect variation: central and eastern dialects have "a marked stress ... with varying patterns" (same source). The first draft healed the IPA toward the respelling and would have lost this. |
| B27 | melamance | respelling stress | **HEAL** † | `/mɛˈlæm.əns/ (meh-LAM-ance; 3 syllables)`. Akkadian *melammu* stressed on its heavy second-to-last syllable is [from memory: not re-checked]. |
| B28 | ngünecheme | IPA stress | **HEAL** | `/ŋɨ.neˈtʃe.me/ (ngü-ne-CHE-me; 4 syllables; Mapuche Ngünechen + Sumerian me)`. Mapuche stresses a closed last syllable, *-chen* (IV). ü is the central vowel the cited page writes /ɘ/; "Traditionally, /ɘ/ has been described as a close central vowel", and it is near-close [ɨ̞] when unstressed [verified: https://en.wikipedia.org/wiki/Mapuche_language], so /ɨ/ fits this unstressed ü. The /me/ and the `me` respelling wait for YU-1. |
| B29 | skename | IPA against respelling, in stress and vowel | **YU-4** | Greek σκηνή has its accent on the last syllable [from memory: not re-checked]; English *skene* stresses the first. Which tradition decides. |
| B30 | shannonme | the two files differ | **HEAL** | Both files: `/ˈʃæn.ən.meɪ/ (SHAN-un-may; 3 syllables)`. `un` is the house code for /ə/. |
| B31 | doxapothos | respelling caps a secondary | **HEAL** | `/ˌdɒk.səˈpɒθ.ɒs/ (dox-a-POTH-os; 4 syllables)` |
| B32 | 21 lines without a count | note | **HEAL** | Add the count, which agrees with the IPA in every case:<br>anagnoristasis 6 (A21), artiance 3, athaumasma 4, candence 2, complerescence 4, doxapothos 4, kimance 2, kinqing 2, oriance 3, walkekin 3, diplosemy 4, dokimance 3, doxakallos 4, doxalgia 4, kallodoxa 4, kallophanes 4, metastrophesis 5, orthophanes 4, slipsooth 2, synophora 4, verisleight 3.<br>Two respellings fix themselves at the same time: diplosemy `dip-LOH-suh-mee` (`my` read /maɪ/) and synophora `si-NOF-uh-ruh` (`sy` read /saɪ/). |
| B33 | tarabqing /tʃɪŋ/; satorime, ngünecheme /me/ | suffix variants in new words | **YU-2**, **YU-1** | They join A1 and A5. hiraethqing and muditaqing are notation only (A4). |

### VII.C The other four records

| # | Record | Finding | Disposition | Action |
|---|---|---|---|---|
| C1 | Tutorials 01–03, suffix teaching | -me /mɛ/, -ance /ɑːns/, qing /tɕɪŋ/ with casual /kɪŋ/ | **YU-1**, **YU-3**, **YU-2** | After each ruling, the tutorial notes are rewritten to match canon. Teaching follows the record. |
| C2 | Tutorial per-word IPA | All 13 words that canon also records differ: maatme has 2 syllables against 3, panimaance has 3 against 4 with stress on the suffix, britqing, walkekin and others | **HEAL** | Align with canon once the rulings land. |
| C3 | PRIMER | 9 of 16 differ: doxomme /dɒksˈɒm/, paqduqing /pɑːkˈduː/, theobasis /θiːoʊˈbɑːsɪs/, -ance /ɑːns/, respellings | **HEAL** | Align with canon. |
| C4 | DICTIONARY, and dokimance in canon | 5 of 18 respellings differ. Canon dokimance also has IPA /ˈdoʊ/ against its own respelling `DOK`. | **HEAL** | Align DICTIONARY with canon. Canon dokimance: `/ˈdɒk.ɪ.mæns/ (DOK-i-mance; 3 syllables)`. Greek δόκιμος has a short o [from memory: not re-checked]; respelling, DICTIONARY and the Greek agree on it. |
| C5 | `forged.json`: alayame | Canon /ɑːˈlaɪ.jʌ/ reads *ay* both as /aɪ/ and as /j/ | **HEAL** † | `/ˈɑː.lʌ.jʌ.meɪ/ (AH-luh-yuh-may; 4 syllables)`. This is the `forged.json` form, *ā-la-ya*. Initial stress on *ālaya* is [from memory: not re-checked]. |
| C6 | `forged.json`: 12 drafts | Drafts for the 12 silent words | → IX | |

### VII.D Errors found while writing this proposal

| # | Words | Finding | Disposition | Corrected line |
|---|---|---|---|---|
| D1 | hozhome | Navajo *zh* is [ʒ] [verified: https://en.wikipedia.org/wiki/Navajo_phonology]; the line splits it into /z.h/ | **HEAL** | `/ˈhoʊ.ʒoʊ.meɪ/ (HOH-zhoh-may; 3 syllables)` |
| D2 | nextlame | Classical Nahuatl x is /ʃ/ and tl is one sound /tɬ/, and stress falls on the second-to-last syllable [verified: https://en.wikipedia.org/wiki/Classical_Nahuatl]; the line has /x/ and /t.l/ | **HEAL** | `/ˈnɛʃ.tɬɑː.meɪ/ (NESH-tlah-meh; 3 syllables; Nahuatl nextla); anglicized /ˈnɛʃ.tlɑː.meɪ/ acceptable` |
| D3 | hopiqatsime against koyaanisqatsime | One Hopi morpheme, *qatsi*, is /q/ in one line and /k/ in the other. Hopi ⟨q⟩ is a separate phoneme, a "voiceless pre-uvular plosive" /k̠/, which contrasts with ⟨kya⟩ in native words; both differ from the ⟨ka⟩ of loans [verified: https://en.wikipedia.org/wiki/Hopi_language]. Both respellings say `KAHT`. | **HEAL** | `/ho.piˈqɑːt.si.meɪ/ (ho-pi-KAHT-see-may; 5 syllables; Hopi hopiqatsi, q = [k̠] + Sumerian me); anglicized /ho.piˈkɑːt.si.meɪ/ acceptable`, and the same for koyaanisqatsime (B14). /q/ is the house approximation of the backed [k̠]; /k̠/ itself would also do. The marked sound stays in the main line, as the stated policy asks (VII.0). The first draft healed toward /k/, the opposite direction to A12c and D4. If /k/ is preferred, record it as a stated exception, not a HEAL. |
| D4 | faqrme; shawqame | Its own note gives Arabic /ˈfaq.r/; its IPA has /k/. shawqame (Arabic *shawq*, شوق) writes qāf as /k/ too. | **HEAL** (q) + **YU-6** (faqrme's epenthesis, B16) | faqrme: lines in B16; both options keep /q/.<br>shawqame: `/ˈʃɔːq.ə.meɪ/ (SHAWK-a-may; 3 syllables; Arabic shawq + Sumerian me); anglicized /ˈʃɔːk.ə.meɪ/ acceptable`. ق is /q/ [verified: https://en.wikipedia.org/wiki/Arabic_phonology]. With paqduqing (A12c), damqme and qorbme, every q-spelled stem from Arabic or Akkadian then writes /q/. |
| D5 | aletheme | The IPA reads θ as /t/ while its respelling says `theh`. | **YU-4** | The line is coherently Attic, not a slip: /a/, η as /ɛː/, /e/, and θ as /t/, since Classical θ was an aspirated stop, written /tʰ/, which became a fricative "in Attic Koine around the first century AD" [verified: https://en.wikipedia.org/wiki/Ancient_Greek_phonology]. The respelling `theh` and the IPA /t/ record that split between two traditions. Options:<br>Attic: `/aˈlɛː.tʰe.meɪ/ (a-LEH-teh-may; 4 syllables)`.<br>English-scholarly: θ as /θ/ with the English vowel values that go with it (η as /iː/ or /eɪ/, as A15 asks), written once YU-4 picks the Greek tradition. No sourced English form of the word was found today.<br>The first draft's /aˈlɛː.θe/ mixed a Koine consonant into Attic vowels. |
| D6 | pachame | Aymara stresses the second-to-last syllable [verified: https://en.wikipedia.org/wiki/Aymara_language]; the line stresses *-cha* | **HEAL** | `/ˈpa.tʃa.meɪ/ (PAH-chah-may; 3 syllables; Aymara pacha + Sumerian me)` |
| D7 | warame | Arabic *waraʿ* has two syllables and no superheavy final, so the first is stressed: "Otherwise, if the word has only two syllables, stress the first one" [verified rule: https://en.wikipedia.org/wiki/Arabic_phonology; applying it to this word is this session's reading]. The line also writes ʿayn as ʔ, but ع is /ʕ/, a voiced pharyngeal fricative; ʔ is hamza (same source). | **HEAL** | `/ˈwa.raʕ.meɪ/ (WA-rah-may; 3 syllables; Arabic waraʿ + Sumerian me); anglicized /ˈwɑː.rɑː.meɪ/ acceptable` |
| D8 | ch'ulme, k'inhme | The apostrophe is dropped in one and a glottal stop in the other; Mayan ejectives (II.4) | **YU-6** | The ejective belongs in a donor line. The said-aloud forms /ˈtʃʊl/ and /ˈkɪn/ are what readers will say. |

### VII.E The choices for Yu

Six choices of doctrine. Everything else in the table is either a plain repair or a reasoned
exception. YU-4 and YU-6 each hold several smaller questions; they are listed so that each can
be answered on its own.

| | Question | Options and what each costs |
|---|---|---|
| **YU-1** | The -me vowel and its respelling | **A** /meɪ/ "may": 54 respellings change (51 `meh`, 3 `me`); reverses the stated normative respelling "meh" (phonology.md:28), from which 126 `may` lines already depart; the record states an English glide as Sumerian.<br>**B** /me/ with `may`: 178 IPA lines change mechanically, and the same 54 respellings; the respelling likewise reverses phonology.md:28 (126 lines already do); donor-faithful and easiest worldwide; English speakers still say [meɪ].<br>**C** /mɛ/ "meh", as the tutorials teach: 178 IPA lines and 129 respellings change; keeps phonology.md:28's respelling "meh" but not its IPA /meɪ/; risks reduction to the -ma sound.<br>**D** Free variation: cannot be written in the respelling. (V.1) |
| **YU-2** | qing's main form; whether "-king" stays | **A** Donor /tɕʰiŋ/ everywhere, /tʃɪŋ/ acceptable: 7 lines change.<br>**B** English /tʃɪŋ/ everywhere: 27 lines change, and the donor-first policy is reversed.<br>**C** Two lines (VIII).<br>Keeping "-king" blurs the qing/-kin contrast; dropping it changes 4 alternates and tutorial 02. (V.2) |
| **YU-3** | -ance as /əns/, /ɑːns/ or /ans/ | **A** /əns/: 1 canon line (kunance), tutorial 03 and PRIMER change; the 8 silent -ance words (IX) are drafted this way.<br>**B** /ɑːns/: 6 canon lines and the 8 IX lines change; a fuller vowel.<br>**C** Two lines, donor /ans/ and said /əns/. (V.3) |
| **YU-4** | Which tradition stands for a donor that has several; what to do when a donor has no stress; how compounds are stressed | **4a. Tradition.** Greek can be Classical (η /ɛː/, θ /tʰ/) or English-scholarly (η /iː/ or /eɪ/, θ /θ/): A15, A16, A20 (vowel), A34 (-phanes stress), A37, B29, D5 aletheme, and epiclance in IX. Sanskrit can be reconstructed or English-Indological: A13c (the stressed a, and /ʌ/ against /ə/). Hebrew can be Modern (final stress, no length, qof /k/) or Tiberian-style (qof /q/, length): the proposed default is Modern, which A12a, A18, A36 and the IX Hebrew words already assume. Latin can be classical or ecclesiastical.<br>**A** Each entry names its tradition. Costs a field and a check.<br>**B** One default per donor: Modern Hebrew, Classical or English-scholarly Greek, and so on. Costs roughly 20 lines (the rows just named). A Tiberian Hebrew default would also move tikkunme, devekutqing, qinance and qorvance to /q/.<br>**C** Donor line reconstructed, said-aloud line English-scholarly (VIII).<br>**4b. Donors with no word stress** (tone, pitch accent, Korean): B1 daigome, B3 satorime, B4 sinbyeongme, B5 sinmyeongme, and hanme and aseme in IX. Options:<br>(i) Follow the respelling as forged. This is the interim rule (VII.0): no line beyond the notation repair changes, but there is no principle behind the choice.<br>(ii) First syllable of the stem. satorime, sinbyeongme, sinmyeongme and aseme change; daigome and hanme do not. Matches the Yoruba lines (ifeqing, emime, oriance).<br>(iii) Follow the tone, where YU-5 C is adopted. Needs sourced tone for each word; Korean and Japanese gain nothing from it.<br>**4c. Compounds.** One primary is a plain repair; which element takes it is not. A43 doxakallos, B7 anamcharame, B8 asraya-paravrttime, B9 humahukhtahvarshtame. Options: (i) the proposed house pattern, primary on the last element, from one Greek word (kallodoxa): the healed lines as given; (ii) each donor's own rule, so Irish first syllable (B7) and Sanskrit heavy syllable (B8 on *vṛt*), both [from memory: not re-checked], with lines shown in their rows. |
| **YU-5** | Tone and donor length | **A** Flatten openly.<br>**B** Donor line only.<br>**C** Map tone to stress.<br>**D** Mark tone in the main line. (VI.3) |
| **YU-6** | The shape of the record, and the places where donor and said-aloud forms compete for one slot | **A** One line with alternates, as now. The two vowel systems (A14, A24, A25) then need one system chosen for all 243 lines: a large rewrite either way. Each split below also needs its own answer.<br>**B** Two lines, donor-faithful and said aloud (VIII). The mixture becomes two honest layers; the cost is a new field and the tools that read it. Each split below then dissolves.<br>The splits:<br>• B16: sabrme, shukrme, faqrme (and damqme by analogy): donor coda (a) or inserted vowel (b) in the main line; both line sets are in B16.<br>• A12b: barakqing, zakarqing: a k-spelled, spirantized kaf as /k/ (spelling) or /χ/ (donor, as halakhame).<br>• D8 and B20: ch'ulme, kinhme: whether the main line writes the ejective kʼ and Yucatec length (/ˈkʼiːn/, as `forged.json` and the voice already do).<br>• yggdrasilme (B22): its main line is its own anglicized form; promoting the donor form would follow the stated order. |

### VII.F Tally

| Disposition | Rows | Rows in A | Rows in B | Rows in C | Rows in D |
|---|---|---|---|---|---|
| HEAL | 80 | 40 | 30 | 4 | 6 |
| … of those, HEAL † (needing a donor check) | 14 | 5 | 8 | 1 | 0 |
| … of those, also pointing to a YU choice | 5 | 1 (A43) | 3 (B7, B8, B9) | 0 | 1 (D4) |
| … of those, with interim stress | 4 | 0 | 4 (B1, B3, B4, B5) | 0 | 0 |
| HONOR | 4 | 4 | — | — | — |
| YU (rows pointing only to the six choices) | 20 | 14 | 3 | 1 | 2 |
| CLOSED | 2 | 2 | — | — | — |
| Passed to IX | 1 | — | — | 1 | — |

107 rows in all. Since the first draft: A9c, A9d and A13c are new rows; A12b went from CLOSED to
YU-6; A13b was split into a HEAL (A13b) and a YU-4 remainder (A13c); A38e went from YU-4 to
HEAL †; B16 and D5 went from HEAL to YU; D4 now also points
to YU-6. Some rows heal several words at once. Counted by words rather than rows, the HEAL rows
touch about 115 lines. The six YU choices settle the remaining doctrine questions, including the
-me respelling across all 180 -me lines.
`[canon: the disposition column of VII.A to VII.D, counted by script on 2026-11-10]`

---

## VIII. Would a two-line record dissolve most conflicts?

**The idea.** Each entry keeps two lines:
- `pronunciation:`, the donor-faithful IPA, with donor sounds, tone and length where they are
  known and sourced;
- `said_aloud:`, one bracketed line showing how a reader of the respelling actually says the word
  in YOUSPEAK, with the respelling beside it.

The current one-line format already reaches for this with "anglicized … acceptable". Nineteen
lines carry such an alternate. Twelve of the audit's findings are cases of the two readings fighting
for one slot.

### Three worked examples

**1. hayatqing: donor sounds and the suffix.**

Today:

    pronunciation: /ħaˈjaːt.t͡ɕɪŋ/ (hah-YAHT-ching; 3 syllables); anglicized /haˈjaːt.kɪŋ/

Two lines:

    pronunciation: /ħaˈjaːt.tɕʰiŋ/ (3 syllables; Arabic ḥayāt + Mandarin qíng, rising tone)
    said_aloud: [haˈjɑːt.tʃɪŋ] (hah-YAHT-ching)

Four conflicts stop being conflicts:
- ħ against h (A9);
- /t͡ɕɪŋ/ against /tɕʰiŋ/ against /tʃɪŋ/ against "-king" (A1, A4, A11);
- cardinal /a/ against English /ɑː/ (A14);
- the unrecorded tone (A30).

Each reading has a home. Sources: ح /ħ/ [verified: https://en.wikipedia.org/wiki/Arabic_phonology];
q [tɕʰ], [iŋ] and the rising-tone mark [verified: https://en.wikipedia.org/wiki/Pinyin].

**2. sabrme: the syllable count.**

Today:

    pronunciation: /ˈsɑb.r̩.meɪ/ (SABR-meh; 2 syllables)

Here the IPA counts 3 syllables and the line declares 2.

Two lines:

    pronunciation: /ˈsˤabr.me/ (2 syllables; Arabic ṣabr + Sumerian me)
    said_aloud: [ˈsɑ.bər.meɪ] (SAH-ber-may)

The donor word is one syllable ending in -br, which is why the donor line counts 2. English
speakers insert a vowel and say 3. Both counts are true, each of its own layer. Four things are
settled at once:
- B16;
- the split between faqrme's inserted schwa and sabrme's syllabic r, the same donor shape
  treated two ways (III);
- the -me vowel: donor /me/ beside said [meɪ];
- the emphatic ṣ, which is /sˤ/ [verified: https://en.wikipedia.org/wiki/Arabic_phonology].

In one-line form the same choice is B16's (a) or (b), which is why B16 sits under YU-6.

**3. daome: tone.**

Today:

    pronunciation: /daʊ.meɪ/ (DOW-meh; 2 syllables; scholarly alt /tâʊ.meɪ/ TAU-meh)

Two lines:

    pronunciation: /tâʊ.me/ (2 syllables; Mandarin dào, falling tone + Sumerian me)
    said_aloud: [ˈdaʊ.meɪ] (DOW-may)

The tone gets a home without asking any reader to produce it (A30, YU-5 option B). The
"scholarly alt" that today reverses the stated policy becomes the main record. Stress, which
Mandarin does not have, belongs to the said-aloud line, where the missing mark (A42) is healed.
Source: 道 *dào* [tâʊ] [verified: https://en.wikipedia.org/wiki/Tao].

### What it dissolves, and what it does not

Of the audit's 49 findings:
- **Dissolved, 12.** Both readings get a legitimate place: A1, A9, A11, A12, A14, A18, A23, A24,
  A25, A27, A30, A49.
- **Made easier but still needing a decision, 8.** The donor line still needs a tradition (YU-4)
  or the said-aloud line still needs one reading or one code (YU-1): A3, A5, A13, A15, A16, A37,
  A38, A46.
- **Not touched, 29.** Plain errors stay errors in either format:
  - notation: dots, tie bars, ASCII g;
  - wrong counts;
  - layers disagreeing about stress;
  - respellings that misspell their own IPA;
  - one morpheme read two ways (auto-, -phanes, qatsi).

  Two of these also carry a doctrine question that two lines do not settle: which element of a
  compound takes the primary (A43, YU-4c), and which tradition decides a vowel whose respelling
  is healed (A20, YU-4a).

So, by count, two lines do **not** dissolve most findings. Most findings are ordinary slips, and
the HEAL rows fix them in either format. By weight, two lines dissolve most of the **doctrine**:
- YU-2, YU-5 and YU-6 are answered by the format itself.
- YU-1 and YU-3 shrink from "which sound is right" to "which code the respelling uses".
- YU-4 shrinks to "which tradition goes in the donor line".

Four costs:
- **Every entry gets a second line.** For most entries the current IPA is already a said-aloud
  form and can move across unchanged. The donor lines need sourced research per donor, and for
  reconstructed languages (Sumerian, Akkadian, Hittite, Hurrian, Etruscan, Tocharian, Egyptian,
  Ugaritic) a "donor line" is a scholarly convention and must say so.
- **The readers of `pronunciation:` must learn the new field.** That means
  `pipeline/voice/build_lexicon.py` and `ipa2espeak.py`, the generators that read frontmatter,
  and the checker. The voice would then speak the said-aloud line.
- **Two lines can drift apart.** The checker can test that they share a syllable structure and
  that the said-aloud line has exactly one primary stress.
- **The respelling layer and the said-aloud line overlap.** A ruling would decide whether the
  respelling lives inside the said-aloud line, as in the examples, or stays separate.

---

## IX. Proposed pronunciations for the silent words

Twelve canon words have no `pronunciation:` line. A drafting pass of this session proposed one
for each on 2026-11-10, and the adversarial review corrected the draft; the lines below carry
those corrections. Each line is a proposal, like everything in VII. It follows VII.0's notation,
and its -me and -ance syllables take whatever YU-1 and YU-3 decide. Every line below, the anchor
particles included, passes the checker's own parsing and rules (X.8).

For each word: the proposed line, how it will be said aloud, the donor form with its source, and
the judgment calls a reader should see.

### IX.0 What was checked

- **Exactly 12 entries are silent**: `canon/core/{aseme,hanme,mitakuyame,teotlme}.md` and the
  eight `canon/worship-action/*ance.md`. The public lexicon `home/data/lexicon.min.json` has an
  empty pronunciation for the same twelve.
- **`forged.json` holds 26 forms**, not 26 forms never written back:
  - 12 are drafts for the silent words.
  - 12 equal canon. Six of those (doxomme, kimme, panimqing, sukhance, theobasis, veriseem) were
    `# IPA` placeholders that **were** written back in `10a4f7b` (2026-06-09, Session 086, the
    same commit that added `forged.json`, `phonology.md` and the audit): `git show
    10a4f7b^:canon/core/doxomme.md` reads `pronunciation: # IPA`, and `10a4f7b` reads
    /ˈdɒk.sɒm.meɪ/. `1a1d0e4` (2026-06-24) is a parentless root commit that re-adds the whole
    tree. The other six (daseinqing, kenshome, kundaliniqing, prapancame, vimarsame,
    wahdatwujudme) were copied from canon.
  - 2 conflict with canon: alayame (VII.C5) and kinhme (VII.B20).
- **The voice already speaks the forged forms.** `pipeline/voice/lexicon.tsv` has 144 rows, 20
  of them taken from `forged.json`. So for alayame and kinhme the voice and canon disagree today.
- **The voice's converter drops two donor sounds.** `pipeline/voice/ipa2espeak.py` has no
  mapping for ɬ or ʼ. Whatever line is adopted, teotlme will be spoken without its lateral and
  kinhme without its ejective until the converter learns them. No generator was run.
- `forged.json` notes are cut off at about 400 characters, so its reasoning can be audited only
  in part.

### IX.1 House conventions the lines follow

Counted over all 243 lines today `[canon: check_pronunciation.py, 2026-11-10]`:

| Convention | Count today | Used below |
|---|---|---|
| -me realized /meɪ/, unstressed | 178 of 180 | yes |
| -me respelled `may` / `meh` / `me` | 126 / 51 / 3 | `may`, as a placeholder for YU-1. phonology.md:28 says `meh` (V.1) |
| A stress mark replaces the dot (-me lines) | 160 of 180; 20 write both | replaces |
| Affricates without a tie bar | 47 of 60 tokens | no tie bar |
| Two-syllable -me words: stem stressed / suffix / unmarked | 22 / 1 (kinhme) / 2 (daome, kwothme) | stem |
| -ance as /əns/ / /æns/ (-mance) / /ans/ | 7 / 2 / 1 (kunance) | /əns/, pending YU-3 |
| -me alternates inside the parentheses / after them | 9 / 2 (chayimme, voghbme) | inside for -me |
| Hebrew-donor alternates after the parentheses | barakqing, zakarqing, natsarqing, chayimme, kunance | after, for -ance |
| Hebrew pretonic *a* | /a/ in barakqing, zakarqing, natsarqing, panimqing, halakhame, chayimme; ahavame's /ə/ is healed to /a/ (A45) | /a/ |
| Hebrew gemination (dagesh forte) | not kept in tikkunme /tɪˈkuːn/, bittulme /bɪˈtuːl/; kept in ereckappayime /ɑp.pɑː/ | not kept |
| Hebrew vocal shva | /ə/ in devekutqing, shevirame | /ə/ |
| q-spelled Semitic stems | /q/ in qorbme and damqme; /k/ in faqrme, shawqame and paqduqing. The house is split, and no spelling convention follows from it. VII heals the Arabic and Akkadian ones to /q/ (A12c, D4); Hebrew qof follows A12a | Hebrew qof /k/, with a /q/ alternate |

### IX.2 The four -me words

**aseme** (headword àṣẹme), `canon/core/aseme.md`

    pronunciation: /aˈʃɛ.meɪ/ (ah-SHEH-may; 3 syllables; Yoruba àṣẹ [à.ʃɛ̄] + Sumerian me; tone not marked; anglicized /ɑːˈʃeɪ.meɪ/ (ah-SHAY-may) acceptable)

- **Said aloud.** "ah-SHEH-may", or "ah-SHAY-may", which many English speakers use for *àṣẹ*
  itself [from memory: not re-checked]. The stressed /ɛ/ is sayable in English, since the
  following m can close the syllable (as in *lemma*).
- **Donor.** *àṣẹ* "power, authority; let it be so", /à.ʃɛ̄/, low tone then mid tone [verified:
  https://kaweah.freedombox.rocks/kiwix/wiktionary_en_all_maxi_2023-04/a%E1%B9%A3%E1%BA%B9, a
  2023-04 mirror of Wiktionary; the live page returned 404]. Grave marks low tone, acute high,
  mid is unmarked; ⟨ṣ⟩ is [ʃ]; the dot under a vowel marks an open vowel, so ẹ is [ɛ] [verified:
  https://en.wikipedia.org/wiki/Yoruba_language].
- **Judgment calls.**
  1. Tone is left out of the main line (YU-5) and recorded in the note.
  2. The stress is *interim* (VII.0): Yoruba has tone, not stress, and the line follows the
     entry's own `ah-SHEH` and the `forged.json` draft. The first draft justified it by the tone
     rising from low to mid; that is VI.3's option C, which is YU-5's choice, not a rule. House
     Yoruba practice stresses the first syllable in all three lines (ifeqing, emime, oriance);
     YU-4b (ii) would give `/ˈa.ʃɛ.meɪ/ (AH-sheh-may)`.
  3. Initial /a/ is short: Yoruba has no contrastive length.
  4. The entry body says the ẹ of *àṣẹ* is "also low tone". By the orthography it is mid. That is
     recorded here (and in VI.1), not edited.
  5. The ASCII slug hides the /ʃ/; without the respelling, readers will say "a-SEEM".

**hanme**, `canon/core/hanme.md`

    pronunciation: /ˈhɑːn.meɪ/ (HAHN-may; 2 syllables; Korean han 恨 [ha̠(ː)n] + Sumerian me)

- **Said aloud.** As written. Without the respelling, English readers may say "HAN-mee".
- **Donor.** 한 (恨) "deep-seated resentment", [ha̠(ː)n]; the long vowel is still prescribed in
  Standard Korean, but "most speakers in both Koreas no longer distinguish vowel length"
  [verified: https://en.wiktionary.org/wiki/한]. Korean has no word stress [from memory: not
  re-checked].
- **Judgment calls.**
  1. The stress leaves the suffix. The entry body writes `hahn-MAY` (three times), but also says
     the -me "follows established YOUSPEAK pattern", which is the unstressed suffix. With a
     one-syllable stem, both YU-4b options give HAHN.
  2. /ɑː/ is the house symbol for this syllable (kanme, ehanme). The donor vowel [a̠] is a little
     fronter.
  3. The /n.m/ seam stays unassimilated.
  4. The three body passages (lines 131, 135, 148) will contradict the line. Record, do not edit.

**mitakuyame**, `canon/core/mitakuyame.md` (also the fourth ankyrance anchor)

    pronunciation: /miˈtɑː.ku.ja.meɪ/ (mee-TAH-koo-yah-may; 5 syllables; Lakota mitákuye + Sumerian me; Lakota stress on the second syllable preserved)

- **Said aloud.** As written. The risk is moving the stress to YA by English or Spanish habit;
  the respelling guards against it.
- **Donor.** *Mitákuye Oyás'iŋ* [verified: https://en.wikipedia.org/wiki/Mitakuye_Oyasin].
  Lakota has five oral vowels; length is not contrastive; stress is marked with the acute
  [verified: https://en.wikipedia.org/wiki/Lakota_language]. So *mitákuye* is [miˈtakuje], by
  that page's rules. The split mi- "my" + takúye "relatives" was seen only in a search summary
  [not verified].
- **Judgment calls.**
  1. Only the stressed vowel carries ː, the house symbol for a stressed open a (I.5). It claims
     no Lakota length; the `forged.json` draft's length marks on unstressed vowels have no donor
     basis. The strictly donor-only line would be /miˈtɑ.ku.ja.meɪ/, as wakanme writes /ˈkɑn/.
  2. The stress stays on the donor's *tá*. On the surface that is fourth from the end, which 14
     existing lines share (sunyatame, mathemame, liturgiame and wiconime among them).
  3. The line follows the canon spelling *-ya-*, not the donor's *-ye*. Whether that change was
     deliberate the entry does not say.
  4. `mee` for unstressed /i/ is approximate.

**teotlme**, `canon/core/teotlme.md`

    pronunciation: /ˈtɛ.oːtɬ.meɪ/ (TEH-ohtl-may; 3 syllables; Classical Nahuatl teōtl [ˈte.oːt͡ɬ] + Sumerian me; Nahuatl /tɬ/ lateral affricate preserved); anglicized /ˈtɛ.oʊ.təl.meɪ/ (TEH-oh-tul-may) acceptable

- **Said aloud.** "TEH-oh-tul-may", four syllables, as English treats *Nahuatl* /ˈnɑːwɑːt(ə)l/
  [verified: https://en.wiktionary.org/wiki/Nahuatl].
- **Donor.** *teōtl* [ˈte.oːt͡ɬ] [verified: https://en.wiktionary.org/wiki/teotl]. Stress is
  "generally" on the second-to-last syllable; tl is one sound, /tɬ/; long vowels are separate
  phonemes [verified: https://en.wikipedia.org/wiki/Classical_Nahuatl].
- **Judgment calls.**
  1. The stem keeps its own donor stress, *TE-ōtl*, as the stated rule says. The first draft
     computed Nahuatl's second-to-last rule over the whole compound and stressed *ōtl*. That
     contradicts the stated rule and every other Nahuatl line: teyoliame is stressed on its
     stem's second-to-last syllable (B6), and nextlame (D2) and tlamatisme are stressed in the
     stem. The entry itself says "stress on the second syllable", and `forged.json` follows it;
     the line departs from both, and says so here.
  2. /tɬ/ without a tie bar, as tlamatisme writes it.
  3. ō is donor-long /oː/, as hotepme's /hoː/. The respelling `ohtl` is approximate.
  4. The /tɬ.m/ seam: English speakers will insert a vowel or drop the l. The entry keeps the
     absolutive *-tl*, which its frontmatter says is "dropped in many compounds" and its body
     (line 149) says is kept: an internal disagreement, recorded here.

### IX.3 The eight worship-action -ance words

**Stress when the suffix replaces the donor's stressed syllable.** Five donors are stressed on
the last syllable (*qorbán, qiná, palál, halél, t'shuvá*), and -ance replaces that syllable. Every
entry's own stated stress, and `forged.json`, then stress the nearest stem syllable before it.
This follows from the stated rule (the suffix is unstressed) and is recorded as a sub-rule, not
a new choice. kipporance and yadahance keep the donor's stressed vowel.

**Hebrew tradition.** The house's Modern-based practice (VII.0): Modern vowel qualities and
final stress, no length marks beyond the house symbol for a stressed open vowel, qof as /k/ with
a /q/ alternate (A12a), no gemination, vocal shva as /ə/. Tiberian values are shown where they
differ, so that YU-4a can see what is being chosen against. Tiberian forms are this session's
application of the tables in https://en.wikipedia.org/wiki/Tiberian_vocalization and
https://en.wikipedia.org/wiki/Tiberian_Hebrew (both opened today).

**epiclance**, `canon/worship-action/epiclance.md`

    pronunciation: /ˈɛp.ɪ.kləns/ (EP-i-clance; 3 syllables; Greek epíklēsis + Latin -ance; English epi- stress as in epitaph, epigram; primary stress on first syllable); Greek-stress alternative /ɛˈpiː.kləns/ (eh-PEE-clance) acceptable

- **Said aloud.** As written.
- **Donor.** ἐπίκλησις, /e.pí.klɛː.sis/ in Attic and /eˈpi.kli.sis/ in Koine, accented on πί
  [verified: https://en.wiktionary.org/wiki/ἐπίκλησις]. English *epiclesis* stresses "cle"
  [verified: https://en.wiktionary.org/wiki/epiclesis].
- **Judgment calls.**
  1. The entry stresses EP-; the donor rule would give eh-PEE. The line keeps the entry's stress
     on the model of English *epi-* words, with the Greek stress as the alternate. *epitaph* and
     *epigram* are stressed on the first syllable [from memory: not re-checked]; *epic* is not
     an example, since it comes from ἔπος, not the prefix ἐπί- [from memory: not re-checked].
     This is the same English-or-donor question as A37, so it sits in YU-4a.
  2. The entry's "stress on first and last" is not followed. -ance is never stressed in canon.
     Only tutorial 03 stresses it (panimaance /ˌpɑːnɪm.ˈɑːns/). The recorded suffix-stress
     exceptions are jeongqing, kinhme and muditaqing (IV).
  3. The stem ends in the cluster kl-, which becomes the onset of the suffix syllable.
  4. `canon/worship-action/README.md` and tutorial 07 gloss epiclance as prostration
     (*proskynēsis*); the entry's donor is *epiclesis*, "calling down". The line follows the
     entry; the gloss disagreement is recorded only.

**hallance**, `canon/worship-action/hallance.md`

    pronunciation: /ˈhal.əns/ (HAL-lance; 2 syllables; Hebrew hallel + Latin -ance)

- **Said aloud.** English speakers will say /ˈhæl.əns/, as in *Hal*; that can simply be accepted.
- **Donor.** הַלֵּל *halél* "Hallel" [verified: https://en.wiktionary.org/wiki/הלל]; הָלַל
  *hālal* "to shine; (piel) to praise" [verified:
  https://www.blueletterbible.org/lexicon/h1984/kjv/wlc/0-1/]. Tiberian-style [halˈleːl]; Modern
  [haˈlel].
- **Judgment calls.**
  1. /a/ in a closed stressed syllable, as barakqing's /rak/. The first draft contrasted this
     with palance's /ɑː/ as patah against qamatz; neither Modern Hebrew (both [a]) nor Tiberian
     (qamatz [ɔ]) makes that contrast, so the difference is only the house's symbol for a closed
     against an open syllable (I.5).
  2. No gemination; the h stays /h/, against Modern h-dropping.
  3. The donor's stressed *-lél* is absorbed by the suffix, so the stress falls on *hal-*.

**kipporance**, `canon/worship-action/kipporance.md`

    pronunciation: /kɪˈpoʊ.rəns/ (kip-POH-rance; 3 syllables; Hebrew kippur / kappōret + Latin -ance)

- **Said aloud.** As written; some will say "kip-PORE-ance", which is harmless.
- **Donor.** כָּפַר *kāp̄ar*, piel "cover over, atone" [verified:
  https://www.blueletterbible.org/lexicon/h3722/kjv/wlc/0-1/]; כִּפֵּר *kipér*, כִּפּוּר *kipúr*,
  final stress [verified: https://en.wiktionary.org/wiki/כפר and
  https://en.wiktionary.org/wiki/כפור]; Yom Kippur [ˈjom kiˈpuʁ] [verified:
  https://en.wikipedia.org/wiki/Yom_Kippur]; כַּפֹּרֶת *kapōreṯ* [verified:
  https://en.wikipedia.org/wiki/Mercy_seat]. Modern *kapóret* [kaˈpoʁet].
- **Judgment calls.**
  1. The vowel is *kappōret*'s holam; the YOUSPEAK spelling decides. It is written /oʊ/, not the
     first draft's /oː/: under the Modern default "vowel length is non-contrastive" [verified:
     https://en.wikipedia.org/wiki/Modern_Hebrew_phonology], A18 removes Hebrew length marks for
     that reason, and the respelling `POH` is /oʊ/ in the house code (ponome).
  2. No gemination, though kittume (Akkadian) keeps its geminate.
  3. The stress on *po* is the stressed syllable of both *kippúr* and *kapóret*.

**palance**, `canon/worship-action/palance.md`

    pronunciation: /ˈpɑː.ləns/ (PAH-lance; 2 syllables; Hebrew pālal + Latin -ance); anglicized /ˈpæl.əns/ (PAL-ance) acceptable

- **Said aloud.** /ˈpæl.əns/, as in *balance* and *palace*, which English readers will default to.
- **Donor.** פָּלַל *pālal*, "paw-lal'" [verified:
  https://www.blueletterbible.org/lexicon/h6419/kjv/wlc/0-1/]. Tiberian-style [pɔːˈlaːl]; Modern
  [paˈlal] by the Modern rules (no dictionary IPA was found).
- **Judgment calls.**
  1. /ɑː/ is the house symbol for a stressed open a (I.5), not a donor contrast with hallance.
  2. The donor's stressed *-lál* is absorbed, so the stress falls on *pa-*.

**qinance**, `canon/worship-action/qinance.md`

    pronunciation: /ˈkiː.nəns/ (KEE-nance; 2 syllables; Hebrew qinah + Latin -ance); Tiberian-style alt /ˈqiː.nəns/ acceptable

- **Said aloud.** As written.
- **Donor.** קִינָה *qînâ* "dirge, lament", "kee-naw'" [verified:
  https://www.blueletterbible.org/lexicon/h7015/kjv/wlc/0-1/]. Tiberian-style [qiːˈnɔː]; Modern
  [kiˈna], since Modern Hebrew merged /q/ into /k/ [verified:
  https://en.wikipedia.org/wiki/Modern_Hebrew_phonology].
- **Judgment calls.**
  1. Qof is /k/ under the Modern default, with the Tiberian /q/ as the alternate, as A12a
     decides for tikkunme and devekutqing. The first draft wrote /q/ on the claim that qorbme is
     the only q-spelled Semitic -me word; that is false (IX.1), and qorbme's donor is
     Proto-Semitic. If YU-4a chooses a Tiberian-style Hebrew, the line and its alternate swap.
  2. The entry's `KWI-nance` is not followed: q as /kw/ is the English *qu* habit, with no basis
     in the donor, and "KWI-nance" has two syllables, not the three the entry claims. It was the
     forging author's stated intent; if it is honoured, the line becomes /ˈkwɪn.əns/
     (KWIN-ance).
  3. The donor's stressed *-ná* is absorbed, so the stress falls on *qi-*.
  4. A reader who knows qing may read *qinance* as "CHIN-ance"; `forged.json`'s note records an
     orchestrator hint that took it for Mandarin *qīn*. The README and tutorial 07 gloss it as
     "communal celebration"; the entry says *qinah*, lament. The line follows the entry.

**qorvance**, `canon/worship-action/qorvance.md`

    pronunciation: /ˈkɔːr.vəns/ (KOR-vance; 2 syllables; Hebrew qorban / qarov + Latin -ance); alt with Tiberian qof /ˈqɔːr.vəns/ acceptable

- **Said aloud.** As written.
- **Donor.** קָרְבָּן *qārbān* "offering", "kor-bawn'" [verified:
  https://www.blueletterbible.org/lexicon/h7133/kjv/wlc/0-1/]; Modern *korbán*, final stress
  [verified: https://en.wiktionary.org/wiki/קרבן]; קָרוֹב *qārôḇ* "near", "kaw-robe'" [verified:
  https://www.blueletterbible.org/lexicon/h7138/kjv/wlc/0-1/]. The bet of *qorbān* is a stop
  [b]; the v of qorvance comes from *qarov*.
- **Judgment calls.**
  1. Qof as in qinance. qorbme, from the same root but labelled Proto-Semitic, keeps /q/.
  2. /ɔːr/ is the house reading of o before r (qorbme, morphame).
  3. The donor's stressed *-bán* is absorbed, so the stress falls on *qor-*.

**teshuvance**, `canon/worship-action/teshuvance.md`

    pronunciation: /təˈʃuː.vəns/ (te-SHOO-vance; 3 syllables; Hebrew teshuvah + Latin -ance)

- **Said aloud.** As written.
- **Donor.** תְּשׁוּבָה *tᵊšûḇâ*, "tesh-oo-baw'" [verified:
  https://www.blueletterbible.org/lexicon/h8666/kjv/wlc/0-1/]; Modern *t'shuvá* /tʃuˈva/
  [verified: https://en.wiktionary.org/wiki/תשובה]; Tiberian-style [tăʃuːˈvɔː].
- **Judgment calls.**
  1. The shva is /ə/, as in devekutqing and shevirame. Modern Hebrew drops it, which would give a
     two-syllable "CHOO-vance" that loses the spelled *te-*.
  2. Shureq is /uː/, as tikkunme's /kuːn/.
  3. The donor's stressed *-vá* is absorbed, so the stress falls on *shu-*.

**yadahance**, `canon/worship-action/yadahance.md`

    pronunciation: /jaˈdɑː.əns/ (ya-DAH-ance; 3 syllables; Hebrew yadah + Latin -ance; h silent, as the final he of the Hebrew); spelling-pronunciation /jaˈdɑː.həns/ (ya-DAH-hance) acceptable

- **Said aloud.** /jaˈdɑː.həns/: English readers will sound the spelled h, which also breaks the
  /ɑː.ə/ hiatus.
- **Donor.** יָדָה *yāḏâ*, "yaw-daw'"; the praise and confess senses are hiphil [verified:
  https://www.blueletterbible.org/lexicon/h3034/kjv/wlc/0-1/]. The hiphil surface form is *hôḏâ*
  [from memory: not re-checked], so the YOUSPEAK stem is the dictionary lemma, not the form that
  carries "praise". Tiberian-style [jɔːˈðɔː]; Modern [jaˈda].
- **Judgment calls.**
  1. Pretonic /ja/, not `forged.json`'s /jə/: the house pretonic a is /a/ (IX.1).
  2. d as /d/, not Tiberian [ð].
  3. The silent h leaves the hiatus /ɑː.ə/, which the house already allows (panimaance, oriance).
  4. The stress stays on DAH: the spelled h keeps the stem's last vowel out of the suffix.
  5. The entry's "Four syllables" does not match its own three-part respelling.
  6. The alternate is written IPA first, as the house writes alternates; the first draft had it
     the other way round.

### IX.4 Conflicts with existing lines

- **alayame** (VII.C5). The same line as C5, now with its donor note: `/ˈɑː.lʌ.jʌ.meɪ/
  (AH-luh-yuh-may; 4 syllables; Sanskrit ālaya + Sumerian me)`. Sanskrit *ālaya* is /ɑː.lɐ.jɐ/,
  with no /aɪ/ [verified: https://en.wiktionary.org/wiki/आलय]; canon's `LIE` is an English
  spelling-pronunciation, and the same form also sits in
  `archaeology/sanskrit/yogacara-alaya-vijnana.md:51` and
  `labs/logos/experiments/core/198-alayame.md:60`. Initial stress is [from memory: not
  re-checked] (the † in C5).
- **kinhme** (VII.B20). This section does not recommend its own line. B20 moves the stress only;
  the ejective and the long vowel wait for YU-6 (D8). For that ruling: Yucatec Maya has *kʼiin*
  with a long vowel [verified:
  https://kaweah.freedombox.rocks/kiwix/wiktionary_en_all_maxi_2023-04/Reconstruction%3AProto-Mayan/q%CA%BCiihng,
  a 2023-04 Wiktionary mirror]; in Proto-Mayan notation "nh" is the velar nasal [ŋ], which became
  [n] in Yukatekan [verified: https://en.wikipedia.org/wiki/Proto-Mayan_language], so the canon
  spelling *k'inh* looks like Proto-Mayan notation, not Yucatec. `forged.json` and the voice say
  /ˈkʼiːn/.
- **shannonme** (VII.B30). `SHAN-un-may` in both files, as B30.

### IX.5 The ankyrance anchor particles

`grammars/ankyrance/manifesto.md` §VII says the particles "are grammatical inventory, not canon
words", and `script/morphemes.json` lists them as pending. These lines belong in that registry
or the manifesto's §II table when that work happens, not in canon frontmatter.

    mi:          pronunciation: /miː/ (MEE; 1 syllable; Tok Pisin mi < English me; the colon is a pause, not a sound)
    yu:          pronunciation: /juː/ (YOO; 1 syllable; Tok Pisin yu < English you)
    yumi:        pronunciation: /ˈjuː.miː/ (YOO-mee; 2 syllables; Tok Pisin yumi; mi kept full, never reduced to /mɪ/ or /mə/)
    mitakuyame:  as IX.2

- **Donor.** Tok Pisin *mi* "I", *yu* "thou", *yumi* "(all of you,) and I", the inclusive we;
  Tok Pisin "has five pure vowels" [verified: https://en.wikipedia.org/wiki/Tok_Pisin]. The page
  says nothing about stress.
- **Judgment calls.**
  1. /iː, uː/ are the house symbols for stressed i and u; Tok Pisin's pure vowels differ only in
     length.
  2. The one-syllable lines carry no stress mark. No canon word is monosyllabic, so the checker
     had no rule for this; it now accepts an unmarked one-syllable line (X.8).
  3. *yumi* with initial stress is [from memory: not re-checked]; level stress /ˌjuːˈmiː/ is a
     defensible alternative.
  4. *mi:* /miː/ stays distinct from the -me suffix /meɪ/. Tutorial 01's -me /mɛ/ sits closer to
     it than canon does, one more reason to reconcile the tutorial.
  5. Tok Pisin *yumi* is the inclusive plural; "you and I" is *yumitupela* (per
     `archaeology/tok-pisin/pronouns-clusivity-and-number.md`, added on this branch, and the Tok
     Pisin page's table). That bears on the
     manifesto's reading of *yumi* as the dyad: a meaning question, not a sound one.
  6. The manifesto records *yu* coinciding with the founder's name. That holds for the spelling;
     whether it holds for the sound depends on how Yu says the name, which no record here
     states. Only Yu can settle it.

### IX.6 What these lines lean on, and what they leave standing

The lines depend on: YU-1 (the `may` placeholder), YU-3 (/əns/), YU-4a (the Modern Hebrew
default; epiclance's English stress), YU-4b (aseme's interim stress), and YU-5 (tone in notes
only). Adopting them leaves body text that disagrees, to be recorded, not silently edited:

| Entry | Body text |
|---|---|
| aseme | /à.ʃɛ.meɪ/ and "ẹ … also low tone" |
| hanme | `hahn-MAY`, three times |
| teotlme | /tɛ.ɒtl.meɪ/, `teh-OTL-may`, "stress on the second syllable" |
| mitakuyame | /mi.tɑ.ku.jɑ.meɪ/ |
| qinance | `KWI-nance`, "three syllables" |
| yadahance | "Four syllables" |
| epiclance | "stress on first and last" |

Other records will still disagree: tutorials 01 and 03 (-me /mɛ/, -ance /ɑːns/), PRIMER
(kimance /ˈkiːmɑːns/, panimaance /pɑːˈniːmɑːns/, sukhance /ˈsʌkhəns/), and `lexicon.tsv`, which
covers 144 of the 243 words with lines.

---

## X. What remains open

1. **A second status list for the 49 findings has not been compared with VII.** The session's
   auditor re-checked all 49 against today's canon on its own (48 still hold; #7 is healed; no
   line present at the audit commit has changed since), but that list was returned to the
   session and not written to a file. VII was built separately, from the audit and the
   checker. The two have not been compared row by row.
2. **Donor facts marked † or [from memory]** need a source before their lines are applied:
   - the stress of Pitjantjatjara, Māori, *darśan* and *śamatha* (the classical Sanskrit rule),
     Pali, Georgian, Ojibwe and Akkadian words, and Basque dialect variation;
   - Old Irish *ch* and Irish compound stress, Sanskrit ṛ and short a, Nuer *th*, Egyptian ḫ,
     the Hebrew dual *-áyim* and *zakhár*;
   - the Mayan apostrophe;
   - *ālaya*, *nommo*, *nyama*, *satori*, *mana* and the Avestan words *hūxta*, *xᵛaršta*.

   Hebrew stress also needs a word-level check for chayimme, halakhame, zakarqing, natsarqing and
   panimqing. These lines stress the last syllable of the stem, which agrees with the Modern
   Hebrew pattern [verified: https://en.wikipedia.org/wiki/Modern_Hebrew_phonology], but no
   word-level check was made. (ahavame was checked and is healed in A45.)
3. **Unchecked stress in a few lines not flagged by anyone:**
   - maname /maˈnaː/ (Polynesian *mana*);
   - katsintawime (Hopi);
   - ridame (Arabic *riḍā*). The doubt is about usage, not the rule: *riḍā* has two syllables
     and its final CVV is heavy but not superheavy, so the verified rule ("if the word has only
     two syllables, stress the first one" [verified:
     https://en.wikipedia.org/wiki/Arabic_phonology]) gives *RI-ḍā*, while the line stresses
     *ḍā*. Whether actual usage follows the rule for this word was not checked.
   - yvymarame: Guaraní y is a central vowel /ɨ/ [from memory: not re-checked], but the line
     writes /ɪ/, while ngünecheme keeps its /ɨ/.
4. **Two spelling questions that pronunciation cannot settle**, because they belong to the
   forge:
   - **zudhame** is spelled *zudh-*, but its stated donor is Arabic *zuhd*. Its IPA /ð/ follows
     the spelling, while its respelling `ZUH-duh` follows neither.
   - **The -me suffix's e is never silent**, against English habit, in 109 words (II.5). Only
     teaching can carry this, for example a syllable dot or a note in every learner-facing list.
5. **kwothme's th.** Nuer *th* may be a dental stop rather than /θ/ [from memory: not re-checked].
6. **Tool work if VIII is ratified.** A field name, the parsers listed in VIII, and a checker
   rule. None of it was started here.
7. **The 2026-06-09 documents.** If these rulings are ratified, `phonology.md` §§1–6 and the
   audit's closing line would gain a dated note pointing here. They would not be rewritten. The
   repo's own discipline is to record, not to silently fix.
8. **The adversarial review of 2026-11-10, and where this revision departs from it.** A review
   pass re-ran the checker, re-opened the sources and checked the first draft row by row. It
   found 30 required corrections (21 in this document, 9 in the silent-words draft that became
   IX, two of those being conflicts between the drafts), 5 checker bugs and 26 suggestions. All
   30 corrections are applied above. All 26 suggestions are taken up, three only as notes:
   A20's vowel and A34's stress are pointed to YU-4a, and jinsme and hailsme are marked as
   English habit in II.2 rather than given their own rows. Where the review offered a choice,
   or where this revision did not do exactly what it asked, the reason is here:
   - **The ḥ words (A9).** The review offered either more HEAL rows or moving A9 to YU-6. This
     revision adds the rows (A9c), because §3 names Arabic ḥā /ħ/ among the stated donor-marked
     segments. For the same reason it also heals the Arabic emphatics in ridame and tarabqing
     (A9d), which the review did not ask for: otherwise hadaratme and sabrme would get /dˤ/
     and /sˤ/ while two other lines kept the plain sound. If that reach is unwanted, A9d is
     withdrawn as one row.
   - **Hebrew qof.** The review offered /k/ with a /q/ alternate in the silent words, or moving
     Hebrew qof into YU-4 and withdrawing A12a's HONOR. This revision keeps the HONOR and writes
     /k/, because the corpus's Hebrew follows Modern Hebrew elsewhere and §3's "Semitic qoph
     /q/" comes from qorbme, whose donor is Proto-Semitic. The dependency on YU-4a is stated in
     A12a, so the choice stays open to Yu.
   - **barakqing (A12b).** Sent to YU-6, not YU-4: it is the spelling-against-donor split.
   - **No-stress donors (B1, B3, B4, B5, A38e).** The review offered either sending B1 to B5 to
     YU-4 or stating an interim rule and applying it to A38e. This revision applies the interim
     rule (VII.0) to B1 to B5, with YU-4b's options shown in each row, so each line is ready
     and the choice stays open. It does not apply it to A38e: Sanskrit has a stress tradition,
     so A38e is a † HEAL like A38d, not an interim line.
   - **shamathaqing's /ɑː/ (A13b).** The review asked to remove its long /ɑː/ while leaving
     stressed vowels to YU-4. In the current line that /ɑː/ is the stressed vowel. It goes only
     because A38e moves the stress to *śa*; if that † HEAL is not applied, the /ɑː/ stays with
     YU-4's stressed-vowel question.
   - **The h count (II.2).** The review asked for a note that II.1's t, p and k counts include
     th, ph and kh read as plain stops. The checker's cost model was fixed instead, so those
     counts no longer include them (t 64, p 31, k 43), and no note is needed.
   - **The checker's syllable fallback (review bug 5).** Not changed in the code: per word it
     already reports a "matches nuclei" hint and a dot-missing note. III now states how its
     totals treat the six undotted lumps and the three vowel-less pieces.

   **The checker changes on this branch** (`script/tools/check_pronunciation.py`), all found by
   the review:
   - SEED gains (th, t), (ph, p) and (kh, k). A digraph read as a plain stop now aligns as one
     unit, so h is 30 (24 /h/, 5 silent, 1 /ħ/), not 35 with 10 silent.
   - A later /…/ on a line counts as an alternate only when its clause introduces it
     ("anglicized", "alt", "alternative") or "acceptable" follows it. Others go to a new
     `gloss_ipa` field. 19 lines hold a real alternate, not 25. Every /…/ is still
     character-checked; messages now say "alternate" or "gloss or donor form".
   - In `--inventory`, a letter unit that straddles the stem and suffix boundary (kimme's mm)
     keeps its stem letters in the stem table. m is 56, mm 1.
   - Rule 2 accepts a one-syllable IPA with no primary mark (two or more marks are still an
     inconsistency), and such a line gets no respelling-stress note. No canon word is affected;
     the anchor particles in IX.5 are.

   The summary of canon findings is identical before and after these changes.

   **Every proposed line was run through the checker's own `check_line`**, with each word's
   declared suffix family: 116 whole lines in VII and IX, plus the option fragments shown in
   rows. All pass with no inconsistency, with two expected exceptions. jeongqing's line keeps
   its suffix stress, which A2 honours, so rule 4 flags it by design. melamance carries the
   note it already has (spelled -mance, declared -ance). The twelve silent-word lines and the
   three anchor particles pass with no finding at all. The counts quoted in I to V were
   re-derived from the fixed checker on 2026-11-10; the review's own reproductions (the stress
   table, the -me split, the core sets, the 109 endings, the 23 dot-plus-stress lines) still
   hold.

### Sources opened in this session (2026-11-10)

The first table lists pages opened by the session that wrote VII; pages re-opened during the
review integration are marked (r). IX's sources, opened by the silent-words drafting pass, are
in the second table.

| Source | Used for |
|---|---|
| https://en.wikipedia.org/wiki/Sumerian_language | Vowels /a e i u/ distinguished by the script; /o/ posited but not accepted; vowel length not reconstructable for most words; knowledge filtered through Akkadian |
| https://en.wikipedia.org/wiki/Me_(mythology) | "Me (𒈨; Sumerian: me; Akkadian: parṣu)" |
| https://en.wikipedia.org/wiki/Pinyin | q [tɕʰ], "similar to the ch in English punchy"; ying [iŋ]; second tone written with an acute |
| https://en.wikipedia.org/wiki/Checked_and_free_vowels | English checked vowels "commonly stand only in stressed closed syllables"; exceptions "mostly in interjections" |
| https://wals.info/chapter/2 (r) | Vowel inventories: small 93, average (5–6 qualities) 287, large 184, of 564 languages; 287 of 564 is 50.9% |
| https://en.wikipedia.org/wiki/Navajo_phonology | zh ≈ [ʒ] (*-zhah ~ -shah* [ʒàh ~ ʃàh]); two tones, high written with an acute |
| https://en.wikipedia.org/wiki/Classical_Nahuatl | x /ʃ/; tl /tɬ/ "treated as a single sound"; stress generally on the second-to-last syllable |
| https://en.wikipedia.org/wiki/Hopi_language (r) | ⟨q⟩ /k̠/, a "voiceless pre-uvular plosive", distinct from ⟨kya⟩ in native words and from loan ⟨ka⟩; ts /ts/; long vowels written double; Third Mesa tone |
| https://en.wikipedia.org/wiki/Irish_orthography | broad ch /x/ |
| https://en.wikipedia.org/wiki/Arabic_phonology (r) | ح /ħ/, ع /ʕ/, ص /sˤ/, ض /dˤ/, ط /tˤ/, ق /q/; stress rules after Halpern (2009), including "if the word has only two syllables, stress the first one" |
| https://en.wikipedia.org/wiki/Modern_Hebrew_phonology (r) | "The [k] allophone merged with /q/ into SIH /k/"; fricative kaf /χ/; final or second-to-last stress; vowel length non-contrastive; ח → /χ/ |
| https://en.wikipedia.org/wiki/English_phonology (r) | Consonant + /j/ onsets only "before /uː/ or its modified/reduced forms" |
| https://en.wikipedia.org/wiki/Basque_language (r) | Euskaltzaindia's recommended weak stress on the second syllable; marked, varying stress in central and eastern dialects |
| https://en.wikipedia.org/wiki/Avestan_alphabet (r) | x /x/, xᵛ /xʷ/ |
| https://en.wikipedia.org/wiki/Ragnar%C3%B6k (r) | Old Norse *Ragnarǫk* [ˈrɑɣnɑˌrɒk] |
| https://en.wiktionary.org/wiki/אהבה (r) | *ahavá*: Modern /ʔa.haˈva/, Tiberian /ʔa.hăˈvɔː/, final stress |
| https://en.wiktionary.org/wiki/ברך (r) | *berékh*, *berákh*, *barákh*: final kaf romanized kh |
| https://en.wiktionary.org/wiki/אמת | Modern /(ʔ)eˈmet/; Tiberian /ʔɛ̆ˈmɛθ/ |
| https://en.wiktionary.org/wiki/דבקות | *dvekút* |
| https://en.wiktionary.org/wiki/שבירה | *shvirá* |
| https://en.wiktionary.org/wiki/דממה | *dmamá* /dmaˈma/ |
| https://en.wikipedia.org/wiki/Yoruba_language (r) | Three level tones; acute high, grave low, mid unmarked; *ó bẹ* triplet; ṣ [ʃ]; "The oral /e, o/ are close-mid [e, o]"; the dot below marks the open ẹ [ɛ], ọ [ɔ] |
| https://en.wikipedia.org/wiki/Vedic_accent | udātta, anudātta, svarita |
| https://en.wikipedia.org/wiki/Sanskrit_phonology | ś /ɕ/, ṣ /ʂ/, c /tɕ/; the accent "disappeared completely" in the classical stage |
| https://en.wikipedia.org/wiki/Ancient_Greek_phonology (r) | η /ɛː/ in Attic; θ χ as /tʰ kʰ/, fricatives "in Attic Koine around the first century AD"; iotacism |
| https://en.wikipedia.org/wiki/Japanese_phonology | r [ɾ]; [ts] before /u/; pitch accent |
| https://en.wikipedia.org/wiki/Tao | 道 *dào* [tâʊ] |
| https://en.wikipedia.org/wiki/Ubuntu_philosophy | Zulu [ùɓúntʼù] |
| https://en.wiktionary.org/wiki/wičhóni | acute on ó; "life" |
| https://en.wikipedia.org/wiki/Lakota_language | stress generally on the second syllable, marked with an acute; č /tʃ/, čh [tʃʰ] |
| https://en.wikipedia.org/wiki/Mapuche_language (r) | ch /tʃ/; ng /ŋ/; a closed last syllable takes stress, otherwise the second-to-last; central vowel /ɘ/, "traditionally ... a close central vowel", near-close [ɨ̞] unstressed |
| https://en.wikipedia.org/wiki/Revised_Romanization_of_Korean | ㅈ written j, unaspirated; 벽 [pjʌk̚] |
| https://en.wiktionary.org/wiki/mandala | English /ˈmʌn.də.lə/; Sanskrit *máṇḍala* |
| https://en.wikipedia.org/wiki/Aymara_language | "Stress is usually on the second-to-last syllable" |
| https://en.wikipedia.org/wiki/Pitjantjatjara_dialect | tj is the palatal stop; no stress rule stated |
| https://en.wikipedia.org/wiki/Māori_language | no stress rule in the part read; vowel length phonemic |
| https://en.wiktionary.org/wiki/darshan | from Sanskrit *darśana*; no English IPA |

Opened and gave nothing usable for the purpose: https://en.wiktionary.org/wiki/K%27iche%27 (no
pronunciation); https://en.wikipedia.org/wiki/English_phonology on checked vowels (it was used
later for onsets, above).

**Sources for IX** (opened by the silent-words drafting pass, 2026-11-10):

| Source | Used for |
|---|---|
| https://kaweah.freedombox.rocks/kiwix/wiktionary_en_all_maxi_2023-04/a%E1%B9%A3%E1%BA%B9 | *àṣẹ* /à.ʃɛ̄/ (a 2023-04 Wiktionary mirror; the live page returned 404) |
| https://en.wiktionary.org/wiki/한 | 恨 [ha̠(ː)n]; vowel length no longer distinguished by most speakers |
| https://en.wikipedia.org/wiki/Mitakuye_Oyasin | *Mitákuye Oyás'iŋ* |
| https://en.wiktionary.org/wiki/teotl | *teōtl* [ˈte.oːt͡ɬ] |
| https://en.wiktionary.org/wiki/Nahuatl | English /ˈnɑːwɑːt(ə)l/ |
| https://en.wiktionary.org/wiki/ἐπίκλησις, https://en.wiktionary.org/wiki/epiclesis | Greek accent on πί; English stress on "cle" |
| https://en.wikipedia.org/wiki/Tiberian_vocalization, https://en.wikipedia.org/wiki/Tiberian_Hebrew | Tiberian vowel and consonant values |
| https://www.blueletterbible.org/lexicon/h7133/kjv/wlc/0-1/ and h7138, h7015, h6419, h3034, h1984, h3722, h8666 | *qorbān, qārôḇ, qînâ, pālal, yāḏâ, hālal, kāp̄ar, tᵊšûḇâ* |
| https://en.wiktionary.org/wiki/קרבן, תשובה, הלל, כפר, כפור | *korbán, t'shuvá, halél, kipér, kipúr* |
| https://en.wikipedia.org/wiki/Mercy_seat, https://en.wikipedia.org/wiki/Yom_Kippur | *kapōreṯ*; [ˈjom kiˈpuʁ] |
| https://en.wikipedia.org/wiki/Tok_Pisin | *mi, yu, yumi*; five pure vowels |
| https://kaweah.freedombox.rocks/kiwix/wiktionary_en_all_maxi_2023-04/Reconstruction%3AProto-Mayan/q%CA%BCiihng | Proto-Mayan *qʼiihng; Yucatec *kʼiin* |
| https://en.wikipedia.org/wiki/Proto-Mayan_language | "nh" = [ŋ], > [n] in Yukatekan |
| https://en.wiktionary.org/wiki/आलय | *ālaya* /ɑː.lɐ.jɐ/ |

---

_Written 2026-11-10 by an agent session for the reconciling work that `phonology-audit.md` left
open, and revised the same day after an adversarial review by another agent pass. A proposal:
nothing here is ratified, nothing in canon was changed, and no ruling takes effect until Yu
ratifies it._
