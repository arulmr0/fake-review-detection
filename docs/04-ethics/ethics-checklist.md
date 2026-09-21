# Ethics

**Submitted 28 October 2026**, two days before the Week 7 deadline of
30 October. Classification: low risk, secondary data only. The submitted
form and the approval confirmation are filed in this folder.

## Summary of the submission

**Human participants?** No, not in Semester 1. No recruitment, no
interviews, no user testing.

**Personal data?** No. Both corpora are published research datasets of
review text. Neither carries names, contact details, or account
identifiers. Reviews are used as text, not linked to individuals, and no
attempt is made to re-identify any author.

**Data source and licence.** Ott et al. (2011), distributed via Kaggle
for research use; Salminen et al. (2022), published on OSF alongside the
paper. Both are cited in D1. Neither is redistributed: the repository
records sources and checksums and downloads them on demand.

**Data storage.** Datasets stay on the student's machine and are
excluded from version control. No dataset file is committed, uploaded to
a third-party service, or shared. Trained models are likewise not
committed.

**Scraping?** No. Live collection from a review platform was considered
at the first supervision meeting and rejected on terms-of-service and
ethics grounds before any code was written. Recorded as requirement W1.

**Risk of harm.** Low. The subject is the detection of deceptive text,
not the production of it. The project does not publish a tool for
generating fake reviews, and the machine-generated corpus used is an
existing published dataset rather than newly generated text.

**Dual-use consideration.** A detector can in principle be probed to
learn what evades it. The mitigation is proportionate to a student
project: no adversarial-evasion experiments, and the model is released
as a research artefact with a model card stating its limitations, not as
a service.

## Semester 2 amendment (drafted, not yet submitted)

The demonstrator evaluation will involve 8–10 participants, which the
current approval does not cover. Drafted over the winter break for
submission in Week 1 of Semester 2:

- Participant information sheet — purpose, what the session involves,
  right to withdraw, what is recorded.
- Consent form — explicit, written, obtained before any session.
- Data handling — responses stored pseudonymously, no special-category
  data collected, retained only to the end of the assessment period.
- Recruitment — fellow students and staff, no incentive, no coercion.

Registered as risk R6. The evaluation is designed so that a pilot with
classmates can proceed if approval is delayed, which keeps it off the
critical path.
