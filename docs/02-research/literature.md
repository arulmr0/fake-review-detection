# Literature

One row per paper. The critique column is the point of this file: a list
of summaries is not a literature review, and the D1 draft was sent back
in Week 5 for exactly that reason.

## Synthesis table

| # | Study | Venue, year | Fake reviews are | Features / model | Reported | Generalisation tested? |
|---|---|---|---|---|---|---|
| 1 | Ott et al. | ACL 2011 | human, crowdsourced | n-grams + POS, SVM | ~90% acc | No |
| 2 | Jindal & Liu | WSDM 2008 | duplicates, heuristic labels | surface + metadata, LR | AUC ~0.78 | No |
| 3 | Mukherjee et al. | ICWSM 2013 | platform-filtered (Yelp) | text + behavioural, SVM | ~68% acc | Partly — compares corpora |
| 4 | Rayana & Akoglu | KDD 2015 | platform-filtered | text + metadata + graph (SpEagle) | AUC ~0.87 | Across Yelp cities |
| 5 | Salminen et al. | JRCS 2022 | machine-generated (GPT-2) | fastText / RoBERTa | ~0.97 F1 | No — same generator throughout |
| 6 | Transformer + LSTM study | IJCCE 2024 | mixed | RoBERTa embeddings + LSTM | ~0.97 F1 | No |

## Notes and critique

**1. Ott, M., Choi, Y., Cardie, C. and Hancock, J.T. (2011) 'Finding
deceptive opinion spam by any stretch of the imagination', ACL 2011.**
_ACL Anthology, free._
The corpus everything else is measured against: 800 truthful and 800
crowdsourced deceptive hotel reviews. Classifiers beat human judges
comfortably. The weakness is built into the design — a worker paid to
invent a hotel stay writes differently from someone running a paid
review operation, so the corpus may measure imagination rather than
deception. Primary Semester 1 dataset, chosen because it is clean,
balanced and small enough to iterate on.

**2. Jindal, N. and Liu, B. (2008) 'Opinion spam and analysis', WSDM
2008.** _HW Discovery (ACM DL)._
Framed the problem. Labels spam by finding near-duplicate reviews, which
is a proxy that catches lazy spam and misses everything else. Cited in
D1 for the framing, with the labelling weakness stated rather than
glossed.

**3. Mukherjee, A., Venkataraman, V., Liu, B. and Glance, N. (2013)
'What Yelp fake review filter might be doing?', ICWSM 2013.** _AAAI open
proceedings, free._
The most useful paper I have read. Reviews a real platform filtered are
much harder to classify than crowdsourced fakes, and behavioural signals
carry more than wording does. This is what convinced me a single
headline score on the Ott corpus proves very little, and it is the
origin of the cross-dataset design.

**4. Rayana, S. and Akoglu, L. (2015) 'Collective opinion spam detection:
bridging review networks and metadata', KDD 2015.** _HW Discovery (ACM
DL)._
Combines review text, reviewer behaviour and the review graph. Source of
the YelpChi / YelpNYC / YelpZip datasets. Out of Semester 1 scope
because the chosen corpora carry no reviewer metadata — recorded as
requirement W2, not as an oversight.

**5. Salminen, J., Kandpal, C., Kamel, A.M., Jung, S. and Jansen, B.J.
(2022) 'Creating and detecting fake reviews of online products', Journal
of Retailing and Consumer Services, 64.** _ScienceDirect via HW
Discovery; dataset on OSF._
Generates fake reviews with a language model, then detects them, and
reports very high accuracy. The catch is that the detector is trained
and tested on output from the same generator, so the result says more
about that generator's fingerprint than about detecting machine-written
text in general. This is the gap D1 states, and the second Semester 1
dataset.

**6. 'Fake review detection using transformer-based enhanced LSTM and
RoBERTa' (2024), International Journal of Cognitive Computing in
Engineering.** _Open access, ScienceDirect._
Current state of the art on within-dataset numbers. Same limitation as
5: no test on data from a different source. Useful as evidence that the
generalisation gap is not something the field has closed.

## Methods references

**Dietterich, T.G. (1998) 'Approximate statistical tests for comparing
supervised classification learning algorithms', Neural Computation
10(7).** _HW Discovery._
McNemar's test is the right comparison for two classifiers on one test
set; the repeated cross-validation t-test I had assumed is not. Planned
for Semester 2, described in the D1 methodology.

**Lundberg, S.M. and Lee, S.-I. (2017) 'A unified approach to
interpreting model predictions', NeurIPS 2017.** _NeurIPS proceedings,
free._
SHAP. Semester 2, to test whether the models learn deception or corpus
artefacts — a question the Week 9 results made pressing.

## AI tool use

Recorded per the handbook. ChatGPT (Oct 2026) was used to widen search
vocabulary — it suggested "opinion spam", "shill review" and "review
spam" as synonyms, which found papers 2 and 4. Claude (Oct 2026)
explained a scikit-learn shape error that turned out to be a vectoriser
refit inside the CV loop; the fix was written by hand (commit `4f2a1c7`).
No generated text appears in any deliverable, and every claim in this
file was checked against the original paper.
