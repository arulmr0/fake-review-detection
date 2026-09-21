# D2 — Preparation and Feasibility Video

Recorded 20 November 2026, submitted 24 November. Check the required
length and format on Canvas before recording; the timings below are
proportions of whatever that length is, not fixed minutes.

Recorded with OBS Studio: screen capture plus voice-over from this
script. The first take had audio clipping — input levels were too high —
and was re-recorded rather than patched.

## What the video has to prove

Agreed with the supervisor on 29 October. Three things, in this order:

1. The data is in hand and its provenance is known.
2. The pipeline runs end to end, on screen, not in principle.
3. The Semester 2 plan is achievable with the compute and time actually
   available.

Anything that does not serve one of those three was cut. The first
storyboard spent a third of its length on background and was reordered
after the 19 November feedback, so the live run now comes early.

## Structure

**1. The problem (~10%)**
Two things are called a fake review: text a paid human wrote, and text a
model generated. Detectors are usually built and tested on one. Does one
transfer to the other? On screen: one example of each, side by side.

**2. Data and provenance (~15%)**
The two corpora, where they came from, their licences, and why neither
is committed to the repository. On screen: `data/README.md` and
`python -m frd.download --verify` printing checksums.

**3. The pipeline running (~30%) — the core of the video**
A live run, not slides. On screen, in order:

```
make demo
```

showing the stand-in data being generated, every model running in every
condition, results appended to `results/results.csv` with the commit
hash, and the figures written. Then:

```
python -m frd.cli predict "Absolutely the best hotel ever, five stars is not enough!!"
```

Say plainly while it runs: this is the generated stand-in data so the
demonstration needs no download, and the real numbers come from the real
corpora.

**4. Feasibility results (~25%)**
The condition-comparison figure. The within-dataset bars are in line
with the literature; the cross-dataset bars are far lower for every
model. State what this supports and what it does not — two corpora,
two production methods, no significance test yet.

**5. Semester 2 and its risks (~20%)**
Demonstrator first, because it carries the ethics amendment (R6) and a
user evaluation. Then a second generator, so the generalisation claim is
tested across generators and not only across corpora. Then robustness,
explainability, and the dissertation. Close on R5 and R6 and how each is
being managed.

## Recording notes

- Test audio levels before the full take. The first attempt clipped.
- Full screen at a readable font size; terminal text at 16pt or larger.
- Close every unrelated window and notification.
- Let commands actually finish on camera. A cut mid-run undermines the
  one thing the video exists to prove.
- Watch the whole thing back before submitting — audio, legibility, and
  whether the argument survives without the speaker's presence.

## Note

Writing this script changed D1. Saying the feasibility argument out loud
exposed two places where the reasoning was vague, and both paragraphs
were rewritten in the report after the first take.
