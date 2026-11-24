# Evaluation protocol

The case bank contains authored synthetic fixtures, not study evidence or recorded model results. Development and evaluation labels separate intended use, but the cases are public and are not contamination-proof, blinded or genuinely unseen by the skill author. No independent model outcome is claimed by this repository.

Export baseline prompts and skill-conditioned prompts. Use the same model, host, sampling settings and source files across conditions. For a previous-version comparison, point --skill-root at that checkout. The exporter reads one guidance language per case, not both. Run jobs in fresh contexts through an authorized host. Save exact responses and run metadata. Do not send private manuscripts through an unapproved API.

```bash
python3 evals/evaluate.py export --condition baseline --out baseline-jobs.jsonl
python3 evals/evaluate.py export --condition skill --out skill-jobs.jsonl
python3 evals/evaluate.py check --jobs skill-jobs.jsonl --responses responses.jsonl
```

Each response record must contain case_id, model, host, run_id, executed_at, prompt_sha256, and response. These are user-supplied execution records, not cryptographic proof that a model ran. The checker rejects missing cases, duplicates, unknown cases, prompt-hash mismatches and empty responses. It does not rate prose or approve research claims.

Have a reviewer inspect claim preservation against source notes before rating clarity, specificity, author voice, editing necessity, visual honesty and researcher effort. Randomize presentation and hide condition labels from the reviewer where feasible. Keep meaning errors separate from readability preferences. A model judging itself is not independent evaluation. Record disagreements and critical errors, not a made-up human-likeness percentage. Test acceptable unchanged outputs and repeated editing too.

A release may pass software tests while model evaluation remains not executed. Do not replace missing observations with hand-written ideal answers. acceptable_example in the case bank is an illustrative answer, not an exact-match target and not included in exported prompts. Human authorship, publication acceptance and stars are never evaluation outcomes.

## v2.3.4 safeguard scenarios

`research-safeguards-cases.jsonl` contains authored synthetic pressure cases. They have not been run against an independent model. Static tests check their coverage and metadata, not compliance or scientific truth. Use the actual authorized host and retain responses, model/version, input hashes and reviewer judgments for a later behavioral evaluation. Do not count these cases as measured improvements.
