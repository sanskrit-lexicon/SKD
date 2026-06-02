# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SKD** is the development and correction repository for **Rājā Rādhākānta Deva's *Śabda-kalpadruma***, an indigenous Sanskrit→Sanskrit encyclopedic lexicon, within the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL).

- **Canonical source text**: [`csl-orig/v02/skd/skd.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/skd/skd.txt) (40,817 entries) — corrections are applied to that file, not stored here.
- This repository holds **development artifacts**: corrections, markup, comparison, and per-issue working files.
- An indigenous encyclopedic lexicon that cites classical authorities through quotations (`“…”`), abbreviated source sigla and `iti`, rather than Western `<ls>` markup.

## Architecture

| Path | Purpose |
|---|---|
| `2014/` | 2014 digitization working files |
| `corrections/` | Correction working files |
| `issues/` | Per-issue working files |
| `verbs01/` | Verb identification: maps verb entries to MW roots, with Devanāgarī renderings |

## Key commands

Corrections follow the CDSL `updateByLine.py` pattern, applied against the csl-orig source:

```sh
python updateByLine.py <input> <changefile> <output>
```

Change-file format (paired lines; `;`-prefixed comments):

```
1234 old <original line>
1234 new <replacement line>
```
Supports `new` (replace), `ins` (insert after), `del` (delete). All files UTF-8 (**no BOM**).

## Data format

SKD entries use standard CDSL Sanskrit-lexicography markup. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for the full tag reference.

| Tag | Role |
|---|---|
| `<L>NNNN<pc>PPP` | Entry begin, with print page-column ref |
| `<k1>`, `<k2>` | Primary / secondary headword (SLP1) |
| `<LEND>` | Entry end |
| `{#…#}` | Sanskrit text (SLP1) |
| `{%…%}` | Sanskrit gloss / italic display text |
| `¦` | Headword / definition separator |
| `<lex>…</lex>` | Lexical category |
| `<ls>…</ls>` | Literary source citation |

Annotated example — the first entry of `skd.txt`:

```
<L>1<pc>1-001-a<k1>a<k2>a
a¦, akAraH . AdyasvaravarRaH . asyoccAraRasTAnaM
kaRWaH . sa tu hrasvo dIrGaH plutaSca Bavati . iti
vyAkaraRaM .. asya leKanaprakAro yaTA, --
“dakzataH kuRqalI BUtvA kuYcitA vAmato gatA .
tatordDvasaNgatA reKA dakzordDvA tAsuSaNkaraH ..
viDirnArAyaRaScEva santizWet kramataH sadA .
ardDamAtrA SaktirUpA DyAnamasya ca kaTyate ..”
iti varRodDAratantraM .. asya tattvaM yaTA, --
“SwaRu tattvamakArasya atigopyaM varAnane .
SaraccandrapratIkASaM paYcakoRamayaM sadA ..
paYcadevamayaM varRaM SaktitrayasamanvitaM .
nirguRaM triguRopetaM svayaM kEvalyamUrttimAn ..
vindutattvamayaM varRaM svayaM prakftirUpiRI” .
iti kAmaDenutantraM .. asya paryyAyaH .
“aH SrIkaRWo mAtfkAdyo'nanto vizRuranuttaraH” .
iti vIjavarRABiDAnaM .. anyacca .
“aH SrIkaRWaH sureSaSca lalAwaYcEkamAtrikaH .
pUrRodarI sfzwimeDO sArasvataH priyambadaH ..
mahAbrAhmI vAsudevo DaneSaH keSavo'mftaM .
kIrttirnivfttirvvAgISo narakArirharo marut ..
brahmA vAmAdyajo hrasvaH karasuH praRavAdyakaH” .
praRavAdyAvayava ityarTaH .
“brahmARI kAmarUpaSca kAmeSI vAsinI biyat ..
viSveSaH SrIvizRukaRWO pratipattiTiraMSinI .
arkamaRqalavarRAdyO brAhmaRaH kAmakarziRI” ..
iti varRABiDAnatantraM ..
<LEND>
```

## Dependencies

- Python 3 (correction and comparison scripts).
- No build step in this repo; XML and web display are generated centrally from `csl-orig` via `csl-pywork`.

## GitHub Issue Conventions

This repository uses the Cologne dictionary-repo issue taxonomy. Every issue has exactly one **type**, one **severity**, and one **milestone**:

- **Type** (9): link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **Severity** (3): minor, medium, hard
- **Milestone** (4): Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md) for label definitions and the type→milestone mapping.