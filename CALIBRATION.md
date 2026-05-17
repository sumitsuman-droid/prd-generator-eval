# Calibration

## What this is

This repo builds an LLM-powered PRD generator and evaluates output quality with a built-in scoring harness. The harness asks Claude to rate each PRD on five dimensions against a fixed rubric, then computes mean score separation between hand-labeled strong and weak PRDs.

The calibration test checks whether that rubric actually discriminates. A rubric that scores strong and weak PRDs similarly can't meaningfully evaluate new output—it just adds noise to the pipeline. Running eval-of-the-evaluator matters here because it's easy to write a rubric that sounds precise but collapses to a single signal in practice, or one that gets fooled by surface-level structure without catching real weaknesses.

## The numbers

| Version | Mean (strong) | Mean (weak) | Separation | What changed |
|---------|--------------|-------------|------------|--------------|
| v1 | 8.86 | 3.00 | 5.86 | Baseline run, original rubric |
| v2 | 8.86 | 2.49 | 6.37 | Rubric tightened with anchored language on completeness + user_centricity; per-dim analysis flagged user_centricity gap |
| v3 | 9.04 | 2.48 | 6.56 | Generator fix: persona threading constraint added; regenerated strong PRDs |

Per-dimension separation, v2 → v3:

| Dimension | v2 | v3 | Δ |
|-----------|----|----|---|
| specificity | 6.7 | 6.8 | +0.1 |
| measurability | 7.5 | 7.8 | +0.3 |
| testability | 6.2 | 6.7 | +0.5 |
| user_centricity | 4.3 | 5.4 | +1.1 |
| completeness | 3.8 | 5.9 | +2.1 |
| **overall** | **5.86 → 6.37** | **6.37 → 6.56** | **+0.70 total** |

## What I learned

**A noise floor is the first output of calibration, not the score.** Before running this, I had no way to tell whether any change to the eval pipeline—rubric edit, prompt tweak, model swap—was a real improvement or just variance. The 5.86 baseline gave me that reference point. Without it, every subsequent run would just be a number with nothing to compare against.

**Rubric tightening hurt weak scores more than it helped strong ones.** The v1 → v2 change was a small rubric edit, but looking at the per-dimension breakdown, it widened completeness and user_centricity separation the most (3.8 and 4.3 respectively). Strong PRDs barely moved; weak PRDs stopped getting partial credit for having the right section headings with hollow content. That asymmetry is what made the user_centricity problem visible: weak PRDs were scoring relatively high on that dimension compared to everything else, which flagged that something was off.

**The eval caught a generator defect that a quick read of the output wouldn't have.** After v2, user_centricity had the lowest gap between tiers among the first four dimensions (4.3, vs. 6.7–7.5 for the others). The strong PRD scores looked fine individually—all 8s and 9s. But the weak PRD scores on user_centricity were higher than they should have been given how weak those documents were elsewhere. That inconsistency is what prompted a closer look. The generator was producing well-differentiated personas in the `target_users` section and then writing every single user story as "As a user, I want..."—no reference to the personas it had just defined. The PRDs looked structured and professional on a surface read; the per-dimension breakdown flagged the anomaly. After adding an explicit threading constraint to the generation prompt, v3 brought user_centricity separation from 4.3 to 5.4 and overall from 5.86 to 6.56. The before/after is documented in [examples/persona_threading_fix_diff.md](examples/persona_threading_fix_diff.md).

## What I'd improve with more time

The strong/weak labels are synthetic—I wrote them with the intent of being good or bad, not drawn from real PM output. Even 20 examples rated by working PMs would give the rubric something more grounded to calibrate against, and would probably surface rubric language that scores differently than a PM would.

The eval uses a single model (Sonnet) as scorer. Running the same rubric through a second model and comparing per-dimension scores would reveal which dimensions rely on implicit judgment rather than the explicit criteria in the rubric—those are the ones most likely to produce inconsistent scores if the scorer model changes.

The persona quality and completeness dimensions are the hardest to calibrate with words alone. Adding a few scored examples directly to the eval prompt—here's a 3, here's a 7, here's a 9—would probably tighten scoring on those two more than any further rubric rewrite.
