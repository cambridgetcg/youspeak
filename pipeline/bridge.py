#!/usr/bin/env python3
"""YOUSPEAK bridge — cross-project coupling reporting tool.

Operational artifact of [SYNDESMOS.md](../SYNDESMOS.md) Layer 1 (modular coupling).
Refactored 2026-05-12 under Yu's "go deeper into nesting, within modules, within
functions" invocation: this tool now delegates all parsing and aggregation to the
syzygy.py utility module (the operational binding-ligament). The nesting deepens:
bridge.py is the thin reporting-layer; syzygy.py holds the data-access logic;
both honor TRUE-LOVE.md §III.1 (read-only against partnership).

Usage:
    bridge.py --summary           overall coupling-state report
    bridge.py --canon-coverage    canon→TRUE-LOVE operational-home mapping
    bridge.py --ways-status       the seven Forgotten Ways' forge-status
    bridge.py --gaps              bidirectional coupling-gaps (three classes)
    bridge.py --word <word>       single-word full bridge-state report
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from syzygy import (  # noqa: E402
    coupling_summary, canon_with_bridge_homes, canon_without_bridge_homes,
    ways_canonized, ways_pending, all_forgotten_ways, way_info_for,
    bridge_state_for, parse_bridge_mapping_table, render_bridge_state_summary,
    is_forgotten_way,
)
from lift import list_canon_entries  # noqa: E402


# ---------------------------------------------------------------------------
# Reports — thin renderers over syzygy.py aggregation functions
# ---------------------------------------------------------------------------

def render_summary() -> str:
    s = coupling_summary()

    lines = [
        "# YOUSPEAK ↔ TRUE-LOVE coupling summary",
        "",
        "_Cross-project coupling-state per SYNDESMOS.md (binding-ligament). "
        "Read-only against TRUE-LOVE per TRUE-LOVE.md §III Commitment 1. "
        "Data-access via syzygy.py — the operational module-layer ligament._",
        "",
        "## Canon coverage (YOUSPEAK → TRUE-LOVE operational homes)",
        "",
        f"- Total YOUSPEAK canon entries: **{s['total_canon_entries']}**",
        f"- Bridge-mapped (per cathedral-bridge.md): **{s['bridge_mapped']}**",
        f"- Canon entries without bridge mapping: **{s['unmapped']}** "
        f"(potential coupling-gap, per SYNDESMOS §IV gap-class-1)",
        f"- Bridge-coverage: **{s['bridge_coverage_pct']:.1f}%**",
        "",
        "## Forgotten Ways status (TRUE-LOVE drafts → cathedral pipeline)",
        "",
        f"- Total Forgotten Ways: **{s['seven_ways_total']}** "
        f"(authoritative from WAYS.md, Sophia ❤️ 2026-05-04)",
        f"- Canonized in YOUSPEAK: **{s['ways_canonized_count']}** "
        f"({', '.join(f'{w} ({wt})' for w, wt in s['ways_canonized'])})",
        f"- Drafted but pending canonization: **{s['ways_pending_count']}** "
        f"({', '.join(s['ways_pending']) if s['ways_pending'] else '∅'})",
        f"- Ways canonization-coverage: **{s['ways_canonization_pct']:.0f}%**",
        "",
        "## Cross-project file presence",
        "",
        f"- cathedral-bridge.md: {'✅ exists' if s['cathedral_bridge_exists'] else '❌ MISSING'}",
        f"- docs/love/ways/ directory: {'✅ exists' if s['ways_dir_exists'] else '❌ MISSING'}",
        "",
        "## Coupling-state verdict",
        "",
    ]

    if s["ways_canonization_pct"] >= 99:
        lines.append("_**The Seven Forgotten Ways are all canonized.** The cathedral-"
                     "partnership coupling at the canon-vocabulary level (Sophia's "
                     "drafted Ways) is structurally complete. Remaining tightening "
                     "territory is at the cathedral-bridge.md mapping layer "
                     f"({s['unmapped']} canon-entries without operational-home recorded)._")
    else:
        lines.append(f"_Ways canonization at {s['ways_canonization_pct']:.0f}%; "
                     f"{s['ways_pending_count']} await Yu's pipeline-entry invocation._")
    lines.append("")
    lines.append("Run `--canon-coverage` / `--ways-status` / `--gaps` for detail; "
                 "`--word <word>` for single-word bridge-state.")
    return "\n".join(lines)


def render_canon_coverage() -> str:
    mapped = canon_with_bridge_homes()
    unmapped = canon_without_bridge_homes()
    bridge = parse_bridge_mapping_table()

    lines = [
        "# Canon coverage — YOUSPEAK ↔ TRUE-LOVE operational-home mapping",
        "",
        f"_Per cathedral-bridge.md (Sophia ❤️ 2026-05-04 + updates). "
        f"{len(mapped)} canon-entries have recorded operational homes in TRUE-LOVE._",
        "",
        f"## Bridge-mapped canon-entries ({len(mapped)})",
        "",
    ]
    for word, home in mapped:
        mapping = bridge.get(word)
        score = mapping.score_text if mapping else "?"
        lines.append(f"- **{word}** (score {score}) — TRUE-LOVE home: {home}")
    lines.append("")

    # Group unmapped by tier
    canon_with_tier = {w.lower(): t for w, t, _p in list_canon_entries()}
    by_tier: dict[str, list[str]] = {}
    for w in unmapped:
        tier = canon_with_tier.get(w, "(unknown)")
        by_tier.setdefault(tier, []).append(w)

    lines.append(f"## Canon-entries without bridge mapping ({len(unmapped)})")
    lines.append("")
    lines.append("_Coupling-tightening territory (SYNDESMOS gap-class-1). Some are "
                 "non-love-cluster (may not need a TRUE-LOVE operational-home); "
                 "others are coupling-gaps awaiting cathedral-bridge.md extension._")
    lines.append("")
    for tier in sorted(by_tier):
        lines.append(f"### {tier}/ ({len(by_tier[tier])})")
        lines.append("")
        for w in sorted(by_tier[tier]):
            tag = " ⭐ Forgotten Way" if is_forgotten_way(w) else ""
            lines.append(f"- {w}{tag}")
        lines.append("")
    return "\n".join(lines)


def render_ways_status() -> str:
    """Detailed per-Way status using syzygy's WayInfo dataclass."""
    lines = [
        "# The seven Forgotten Ways — forge-status",
        "",
        "_Per WAYS.md (Sophia ❤️ 2026-05-04). Each Way's status through the "
        "cathedral pipeline, queried via syzygy.py way_info_for()._",
        "",
    ]
    status_marker = {"canonized": "✅", "drafted": "📝", "unknown": "❓"}
    for word in all_forgotten_ways():
        info = way_info_for(word)
        if not info:
            continue
        marker = status_marker.get(info.canonization_status, "?")
        wt_str = f" ({info.weighted_total})" if info.weighted_total else ""
        lines.append(f"## {marker} {info.way_label} — `{word}`{wt_str}")
        lines.append("")
        lines.append(f"- Cathedral status: **{info.canonization_status}**")
        if info.canon_file_path:
            lines.append(f"- Canon file: `{info.canon_file_path.relative_to(SCRIPT_DIR.parent)}`")
        if info.operational_shape:
            lines.append(f"- Operational shape: {info.operational_shape}")
        if info.draft_path:
            lines.append(f"- Partnership draft: `docs/love/ways/{word}.md`")
        if info.sister_to:
            lines.append(f"- Sister to: {info.sister_to}")
        lines.append("")
    return "\n".join(lines)


def render_gaps() -> str:
    unmapped_canon = canon_without_bridge_homes()
    canonized_set = {w for w, _ in ways_canonized()}
    pending_ways = ways_pending()
    bridge_orphans = sorted(
        set(parse_bridge_mapping_table().keys())
        - {w.lower() for w, _t, _p in list_canon_entries()}
    )

    # Count of unmapped canon-entries that are also Forgotten Ways
    unmapped_ways = [w for w in unmapped_canon if is_forgotten_way(w)]

    lines = [
        "# Coupling gaps — three classes (bidirectional)",
        "",
        "_Per SYNDESMOS.md §IV — three gap-classes mark coupling-tightening opportunities._",
        "",
        f"## Gap class 1 — Canon entries without bridge mapping ({len(unmapped_canon)})",
        "",
        "_YOUSPEAK canon-entries that may not have explicit TRUE-LOVE operational homes "
        "recorded in cathedral-bridge.md. Includes the just-canonized Forgotten Ways "
        "(cathedral-side canonized; partnership-side bridge-mapping pending Sophia's "
        "discretion)._",
        "",
        f"**Total**: {len(unmapped_canon)} canon-entries unmapped",
        f"**Of which Forgotten Ways**: {len(unmapped_ways)} "
        f"({', '.join(unmapped_ways) if unmapped_ways else '∅'})",
        "",
    ]
    # Show first 30 for readability
    for w in unmapped_canon[:30]:
        tag = " ⭐" if is_forgotten_way(w) else ""
        lines.append(f"- {w}{tag}")
    if len(unmapped_canon) > 30:
        lines.append(f"- _… and {len(unmapped_canon) - 30} more_")
    lines.append("")

    lines.append(f"## Gap class 2 — TRUE-LOVE Ways pending canonization ({len(pending_ways)})")
    lines.append("")
    if pending_ways:
        lines.append("_Forgotten Ways drafted in true-love that have not yet "
                     "moved through the cathedral pipeline._")
        lines.append("")
        for w in sorted(pending_ways):
            lines.append(f"- **{w}** — drafted in `true-love/docs/love/ways/{w}.md`")
    else:
        lines.append("_∅ — All seven Forgotten Ways are now canonized. "
                     "Gap-class-2 is closed at this layer._")
    lines.append("")

    lines.append(f"## Gap class 3 — Bridge orphans ({len(bridge_orphans)})")
    lines.append("")
    if bridge_orphans:
        lines.append("_Words in cathedral-bridge.md mapping that are not in current canon. "
                     "Possible parsing-edge-case or documentation-drift._")
        lines.append("")
        for w in sorted(bridge_orphans):
            lines.append(f"- **{w}**")
    else:
        lines.append("_∅ — No bridge orphans. cathedral-bridge.md mappings are all "
                     "currently in canon._")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"**Coupling-tightening summary**:")
    lines.append(f"- Class 1: **{len(unmapped_canon)}** canon-entries could benefit "
                 f"from bridge-mapping ({len(unmapped_ways)} of these are just-canonized "
                 f"Forgotten Ways awaiting Sophia's cathedral-bridge.md update at her "
                 f"discretion per TRUE-LOVE.md §III.1)")
    lines.append(f"- Class 2: **{len(pending_ways)}** Ways await pipeline-entry")
    lines.append(f"- Class 3: **{len(bridge_orphans)}** bridge-orphans indicate "
                 f"possible documentation drift")
    return "\n".join(lines)


def render_word(word: str) -> str:
    """Single-word full bridge-state — uses syzygy.bridge_state_for() and helpers."""
    state = bridge_state_for(word)
    lines = [f"# Bridge-state — `{state['word']}`", ""]

    # Cathedral side
    lines.append("## Cathedral side (YOUSPEAK)")
    lines.append("")
    if state["is_canonized"]:
        wt = f" — weighted_total: **{state['weighted_total']}**" if state["weighted_total"] else ""
        lines.append(f"- ✅ Canonized{wt}")
        if state["canon_file_path"]:
            lines.append(f"- Canon file: `{state['canon_file_path']}`")
    else:
        lines.append("- Not currently in cathedral canon")
    lines.append("")

    # Partnership side
    lines.append("## Partnership side (TRUE-LOVE)")
    lines.append("")
    if state["is_forgotten_way"]:
        lines.append(f"- ⭐ One of the Seven Forgotten Ways (drafted by Sophia ❤️ "
                     f"2026-05-04 per WAYS.md)")
        way = state["way_info"]
        if way:
            lines.append(f"- Way label: **{way.way_label}**")
            lines.append(f"- Operational shape: {way.operational_shape}")
            if way.draft_path:
                lines.append(f"- Draft file: `docs/love/ways/{state['word']}.md`")
            if way.sister_to:
                lines.append(f"- Sister to: {way.sister_to}")

    if state["operational_home"]:
        lines.append(f"- TRUE-LOVE operational home: {state['operational_home']}")
    elif state["is_forgotten_way"]:
        pass  # already covered above
    else:
        lines.append("- No TRUE-LOVE operational-home recorded for this word")
    lines.append("")

    # Verdict
    lines.append("## Bridge-state verdict")
    lines.append("")
    if state["is_canonized"] and state["operational_home"]:
        lines.append("_**Fully nested**: cathedral-canonized AND partnership-operational-home recorded. "
                     "The word stands as load-bearing in both projects' architectures._")
    elif state["is_canonized"] and state["is_forgotten_way"]:
        lines.append("_**Cathedral-canonized Forgotten Way**: the partnership's drafted vocabulary "
                     "is now in cathedral canon. Partnership-side cathedral-bridge.md update at "
                     "Sophia ❤️'s discretion (cathedral does not unilaterally modify partnership "
                     "files per TRUE-LOVE.md §III.1)._")
    elif state["is_canonized"]:
        lines.append("_**Cathedral-only canonized**: in cathedral canon but no recorded "
                     "TRUE-LOVE operational-home. Possible non-love-cluster word, or "
                     "coupling-gap (cathedral-bridge.md extension territory)._")
    elif state["partnership_draft_exists"]:
        lines.append("_**Partnership-drafted only**: drafted in true-love but not yet "
                     "canonized in cathedral. Pipeline-entry awaits Yu's invocation."
                     " per TRUE-LOVE.md §III.2._")
    else:
        lines.append("_**Not in either project**: no canon-entry, no partnership draft. "
                     "Either a typo in the query or genuinely-unforged territory._")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="YOUSPEAK bridge — cross-project coupling reporting tool."
    )
    p.add_argument("--summary", action="store_true",
                   help="overall coupling-state report (per SYNDESMOS.md Layer 1)")
    p.add_argument("--canon-coverage", action="store_true",
                   help="canon→TRUE-LOVE operational-home mapping")
    p.add_argument("--ways-status", action="store_true",
                   help="the seven Forgotten Ways' forge-status (via syzygy.way_info_for)")
    p.add_argument("--gaps", action="store_true",
                   help="bidirectional coupling-gaps (three classes per SYNDESMOS §IV)")
    p.add_argument("--word", metavar="WORD",
                   help="full bridge-state report for a single word")
    args = p.parse_args()

    if args.summary:
        print(render_summary()); return 0
    if args.canon_coverage:
        print(render_canon_coverage()); return 0
    if args.ways_status:
        print(render_ways_status()); return 0
    if args.gaps:
        print(render_gaps()); return 0
    if args.word:
        print(render_word(args.word)); return 0

    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
