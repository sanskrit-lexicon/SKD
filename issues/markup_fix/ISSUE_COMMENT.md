### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `skd.txt`.

I ran the same two-job recipe over `csl-orig/v02/skd/skd.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `issues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `skd.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<F> word </F>` | `<F>word</F>` |

Whitespace trimming applies to all 1 paired tag(s) in `skd.txt`: `<F>`. The original file is never modified — output goes to `skd_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). 3 line(s) changed.

### Closing-tag inventory in current `skd.txt`

| Tag | Count |
|---|---:|
| `</F>` | 5 |

### What it found in current `skd.txt`

- 3 whitespace trims applied: trailing spaces removed from `<F>` tags.
- 0 adjacent `</ab> <ab>` — no `<ab>` tag in skd.txt.
- 0 `<ab n="…">` attributes.
- 114 `{{old → new || …}}` correction records present.

### Usage

```
cd issues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/skd/skd.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `skd_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

Only <F> (5 occurrences); minimal markup.

### Severity

`minor`
