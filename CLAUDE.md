# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SKD** is the corrections and research repository for the Cologne digitization of Shabdakalpadruma (*Śabdakalpadruma*), the encyclopedic Sanskrit dictionary compiled by Raja Radhakanta Deva (1766–1826). The canonical source lives in `csl-orig/v02/skd/skd.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `issues/` | Per-issue correction workflows (`issueNNN/` pattern) |
| `corrections/` | Additional correction batches outside the issue pattern |
| `verbs01/` | Root identification: maps SKD verb entries to MW root spellings, identifies prefixed verbs |
| `2014/` | Archived work files from 2014 (historical reference) |

### Issue correction pattern (`issues/issueNNN/`)

Standard workflow:
1. Copy current `skd.txt` to a local `temp_skd_0.txt` (not tracked by git)
2. Apply corrections incrementally as `temp_skd_1.txt`, etc.
3. Rebuild XML with `generate_dict.sh` and validate with `xmlchk_xampp.sh`
4. Commit to `csl-orig`, sync to Cologne
5. Commit documentation back here

### Verb root pipeline (`verbs01/`)

Identifies SKD verb entries and maps them to MW equivalents, with preverb (upasarga) resolution. Cross-referenced with VCP verb analysis ([SKD issue #9](https://github.com/sanskrit-lexicon/SKD/issues/9)).

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/SKD/issues).

## Common Commands

### Apply line-level corrections
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh skd ../../SKDScan/2020
sh xmlchk_xampp.sh skd
```

## Dependencies

- **Python 3**
- **skd.txt** — in `$BASE/cologne/csl-orig/v02/skd/skd.txt`
