---
title: YOUSPEAK Codepoint Assignment Table
opened: 2026-04-24
updated: 2026-04-30
data_source: morphemes.json
encoding_range: Unicode Private Use Area (PUA) U+E100–U+E1FF
---

# YOUSPEAK Codepoint Assignments

_Unicode PUA encoding for the YOUSPEAK writing system. 256 slots reserved (U+E100–U+E1FF). Structured assignment by morpheme class. Extensible to U+E200+ when the inventory exceeds 256._

---

## Design principles

1. **PUA encoding** (not full Unicode proposal) — immediate usability; future migration path to official Unicode codepoints if the script achieves institutional adoption.
2. **Range-structured** — content morphemes, grammatical morphemes, structural marks each have their own subrange. Class is inferable from codepoint.
3. **Stable** — once assigned, a morpheme's codepoint does not change. Additions go to the next available slot; nothing is rearranged.
4. **Sparse** — ample empty slots left for extension.

## Subrange structure (U+E100–U+E1FF, 256 slots)

| Subrange | Count | Class | Allocated | Reserved |
|---|---|---|---|---|
| U+E100 – U+E13F | 64 | content morphemes | 38 | 26 |
| U+E140 – U+E15F | 32 | grammatical morphemes (prefixes/suffixes) | 13 | 19 |
| U+E160 – U+E17F | 32 | structural marks (compound-separator, annotations) | 8 | 24 |
| U+E180 – U+E1FF | 128 | reserved for future use (cadences/tones, ligatures, compound-atomic forms) | 0 | 128 |

## Content morphemes (U+E100 – U+E13F)

| Codepoint | Latin | Tongue | Native | Meaning |
|---|---|---|---|---|
| U+E100 | doxa | Greek | δόξα | glory, manifested-weight |
| U+E101 | kallos | Greek | κάλλος | beauty (substantive) |
| U+E102 | ortho | Greek | ὀρθός | right, straight, true |
| U+E103 | phanes | Greek | φαν- | appearing, shining-forth |
| U+E104 | algia | Greek | ἄλγος | structural ache |
| U+E105 | anagno | Greek | ἀναγνώρισις | recognition-moment |
| U+E106 | stasis | Greek | στάσις | standing-still |
| U+E107 | meta | Greek | μετά | after, beyond, complete-change |
| U+E108 | strophe | Greek | στροφή | turning |
| U+E109 | thauma | Greek | θαῦμα | wonder, marvel |
| U+E10A | syn | Greek | σύν | together-with |
| U+E10B | phora | Greek | φορά | carrying |
| U+E10C | cand | Latin | candor | luminous-warm-clear-white |
| U+E10D | dokim | Greek | δοκιμ- | testing, assaying |
| U+E10E | arti | Lat/Gr | ars/arete/artios | fitted, skilled-making |
| U+E10F | veri | Latin | verum | truth |
| U+E110 | compler | Latin | com+plere | filling-together |
| U+E111 | diplos | Greek | διπλόος | twofold |
| U+E112 | sema | Greek | σῆμα | sign, meaning |
| U+E113 | anastro | Greek | ἀναστρο- | inversion |
| U+E114 | kalypt | Greek | καλύπτω | enclose, enfold |
| U+E115 | haphe | Greek | ἁφή | touching |
| U+E116 | allos | Greek | ἄλλος | other, different |
| U+E117 | parallax | Greek | παράλλαξις | parallel-shift |
| U+E118 | hypo | Greek | ὑπό | under |
| U+E119 | stix | Greek | στίξις | punctuation, stopping |
| U+E11A | kairos | Greek | καιρός | right-time, time-layer |
| U+E11B | morphe | Greek | μορφή | form, shape |
| U+E11C | klimax | Greek | κλῖμαξ | ladder, scale |
| U+E11D | lanthes | Greek | λανθάν- | escape-notice |
| U+E11E | sleight | English | sleight | deceptive-skill |
| U+E11F | seem | English | seem | appear-as |
| U+E120 | andros | Greek | ἀνδρός | of-a-person |
| U+E121 | gloria | Latin | gloria | glory (creature-scale) |
| U+E122 | vide | Latin | videre | seeing |
| U+E123 | cede | Latin | cedere | yielding |
| U+E124 | choro | Greek | χορός | chorus |
| U+E125 – U+E129 | (reserved) | | | 5 slots open |
| U+E12A | **-me** | **Sumerian** | **𒈨 *me*** | **received-divine-ordinance · cosmic-gift-quality** *(exceptional: content-range codepoint for a suffix; justified because -me carries full theological content-load from Sumerian me — see note below)* |
| U+E12B – U+E13F | (reserved) | | | 21 slots open |

> **Note on U+E12A range exception**: -me is the most productive YOUSPEAK suffix (25+ members) and the source of the core theological claim of the language (Sumerian *me* = divine ordinances as gifts constituting civilization). It operates grammatically as a suffix (mclass = suffix in glyph_specs_v1.py) but carries the content-weight of a theological root morpheme. Its codepoint is therefore placed in the content range (U+E12A) rather than the grammatical range, reflecting its semantic weight. Glyph spec: `archaeology/script-mechanics/` Chapter 3 + 7 (S075); design: descent-into-reception — downward triangle in upward-opening arc.

## Grammatical morphemes (U+E140 – U+E15F)

| Codepoint | Latin | Tongue | Native | Meaning |
|---|---|---|---|---|
| U+E140 | a- | Greek | ἀ- | privative |
| U+E141 | -sis | Greek | -σις | state-noun suffix |
| U+E142 | -ance | Latin | -antia | quality/state suffix |
| U+E143 | -mance | Gr/En | -mantia | quality-mode suffix |
| U+E144 | -ence | Latin | -entia | quality/state suffix |
| U+E145 | -ma | Greek | -μα | result-of-action suffix |
| U+E146 | -iance | Latin | -iantia | luminous-quality suffix |
| U+E147 | -escence | Latin | -escentia | becoming suffix |
| U+E148 | -mia | Greek | -μία | state-noun suffix |
| U+E149 | ana- | Greek | ἀνά- | up, back, again |
| U+E14A | en- | Greek | ἐν- | in, within |
| U+E14B | com- | Latin | con- | together |
| U+E14C | -y | Gr/En | -y | noun-abstract suffix |
| U+E14D – U+E15F | (reserved) | | | 19 slots open |

## Structural marks (U+E160 – U+E17F)

| Codepoint | Role | Display |
|---|---|---|
| U+E160 | compound-separator (thin space between morpheme-glyphs within one word) | rendered as a half-width space or a small vertical bar |
| U+E161 | reading-annotation open (introduces Latin gloss) | rendered as an upper-corner bracket ⌜ |
| U+E162 | reading-annotation close | lower-corner bracket ⌟ |
| U+E163 | diplosemic-pair indicator (marks an Anastrophance-sibling relation) | small double-headed arrow ↔ rendered above the word |
| U+E164 | canon-mark (formal liturgical register) | diamond ◆ rendered at the word's start |
| U+E165 | phrase-end mark (minor rhythmic pause; daṇḍa-style) | short vertical bar \| at mid-height; equivalent to comma in liturgical prose |
| U+E166 | sentence-end mark (major rhythmic pause; double-daṇḍa-style) | double short vertical bar \|\| ; equivalent to period |
| U+E167 | breath-pause mark (breath-pause in liturgy; Greek *ano teleia*-style) | small centered dot · ; marks a breath or meditative pause within a phrase |
| U+E168 – U+E17F | (reserved) | 24 slots open |

> **Note on punctuation marks (U+E165–U+E167)**: Proposed in `archaeology/script-mechanics/05-reading-flow.md` (S075), informed by Sanskrit daṇḍa tradition (| and ||) and Greek *ano teleia* (·). These three marks cover the liturgical-prose rhythm needs of YOUSPEAK text. Not yet implemented in the font; codepoints reserved for production-phase implementation.

## Example compound encodings

Each word is the codepoint-sequence of its morphemes, in compound order:

| Word | Morpheme breakdown | Codepoint sequence |
|---|---|---|
| doxakallos | doxa + kallos | U+E100 U+E101 |
| kallodoxa | kallos + doxa | U+E101 U+E100 |
| orthophanes | ortho + phanes | U+E102 U+E103 |
| doxalgia | doxa + algia | U+E100 U+E104 |
| anagnoristasis | ana + gno(risis) + stasis | U+E149 U+E105 U+E106 |
| metastrophesis | meta + strophe + -sis | U+E107 U+E108 U+E141 |
| athaumasma | a- + thauma + -ma | U+E140 U+E109 U+E145 |
| synophora | syn + phora | U+E10A U+E10B |
| kallophanes | kallos + phanes | U+E101 U+E103 |
| dokimance | dokim + -ance | U+E10D U+E142 |
| artiance | arti + -iance | U+E10E U+E146 |
| verisleight | veri + sleight | U+E10F U+E11E |
| candence | cand + -ence | U+E10C U+E144 |
| complerescence | com- + compler + -escence | (U+E14B + U+E110 + U+E147) or just U+E110 + U+E147 |
| diplosemy | diplos + sema + -y | U+E111 U+E112 U+E14C |
| veriseem | veri + seem | U+E10F U+E11F |
| **doxame** | **doxa + -me** | **U+E100 U+E12A** |
| **kallome** | **kallos + -me** | **U+E101 U+E12A** |
| **mitakuyame** | **mitakuya + -me** | **[mitakuya codepoint TBD] U+E12A** |

## Reserved-for-growth

- **U+E125–U+E129** — 5 content morpheme slots (next: ki, qing, kin, tacit, mushin when codepoints added)
- **U+E12B–U+E13F** — 21 content morpheme slots
- **U+E14D–U+E15F** — 19 grammatical morpheme slots
- **U+E168–U+E17F** — 24 structural mark slots (tone-marks, cadence-indicators, register-shifts)
- **U+E180–U+E1FF** — a full 128-slot pane reserved for future needs: ligatures for very-common compounds (optional precomposed forms), cadence/tone marks (for Cadences/ chapter, future), substrate-variants (for Substrata/ chapter, future), or expansion when the canon-morpheme count exceeds the current range

## Migration note — future Unicode proposal

If YOUSPEAK script achieves adoption (institutional use, public-script-community formation, documentation sufficient for Unicode Technical Committee review), a formal Unicode proposal can be made. At that point, codepoints would migrate from the PUA to officially-assigned Unicode positions. All YOUSPEAK-aware tools (the transliterator, the font, the IME) would handle the remapping. Documents encoded in PUA can be migrated by a one-pass search-and-replace.

Until then, PUA is sufficient for all private, institutional, and research use.

---

_Codepoint table opened 2026-04-24. Updated 2026-04-30 (S075): U+E12A formally assigned to -me; U+E165–U+E167 reserved for liturgical punctuation (daṇḍa-style marks). Reflects morpheme inventory as of Canon size ~59 words / 90 morphemes in spec._
