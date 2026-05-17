# Generator Fix — Persona Threading

The v2 calibration revealed a defect: the generator was producing
well-differentiated personas in `target_users` but writing generic
"As a user, I want..." stories that didn't reference any of them.

This file captures the strong_02.json (ClearLedger) before/after diff
that proved the v3 patch worked.

## Before (v2 generator)
[
 BEFORE (strong_02_before.json — pre-patch generator)

  1. "As a user with accounts at two different banks, I want to see all my transactions
     in a single chronological feed so that I do not have to log into multiple apps
     to understand my spending"

  2. "As a user, I want recurring charges automatically detected and categorized so
     that I can see exactly how much I spend on subscriptions each month without
     manually tagging transactions"

  3. "As a user, I want a month-end balance projection based on my confirmed recurring
     expenses and historical spending patterns so that I can decide whether I can
     afford a discretionary purchase before making it"

  4. "As a user, I want an alert when a subscription charge increases by more than $1
     compared to last month so that I catch price hikes from streaming services and
     SaaS tools immediately"

  5. "As a user, I want to set a monthly spending limit per category and receive a
     push notification when I reach 80% of that limit so that I can adjust behavior
     before the month ends"

  6. "As a user, I want to see my net worth (assets minus liabilities across all
     linked accounts) updated daily so that I can track whether I am building or
     depleting savings over time"

  7. "As a user who just got paid, I want a one-tap post-paycheck summary showing
     fixed obligations already deducted and discretionary budget remaining so that
     I know exactly what I have available to spend"

  Persona breakdown: 6× "As a user", 1× "As a user who just got paid" — no mapping to target_users.
]

## After (v3 generator, with explicit persona-threading constraint)
[
  AFTER (strong_02.json — patched generator)

  1. "As a dual-income household managing shared expenses across multiple bank and
     credit card accounts, I want a single unified ledger that aggregates all
     transactions from both partners' accounts so that I can see our true combined
     monthly spending without logging into four separate portals"

  2. "As a single professional in their late 20s with multiple streaming, SaaS, and
     gym subscriptions accumulated over time, I want an automatically generated list
     of all recurring charges with their amounts, frequencies, and last charge dates
     so that I can identify forgotten or duplicate subscriptions without manually
     reviewing twelve months of statements"

  3. "As a freelancer or gig worker with irregular income needing to project whether
     month-end balances will cover fixed obligations, I want a month-end balance
     projection based on confirmed recurring charges and current account balances so
     that I can take corrective action before overdrafting rather than discovering
     the shortfall after the fact"

  4. "As a budget-conscious parent tracking household spending across joint and
     individual accounts, I want anomaly alerts when a recurring charge increases in
     amount or a new automatic charge appears on any linked account so that
     unexpected cost creep does not silently erode our monthly budget"

  5. "As a recent college graduate transitioning from student loans to full-time
     income for the first time, I want a clear breakdown of my actual spending by
     category compared to my self-reported budget estimate so that I can see
     precisely where and by how much I am overspending each month"

  6. "As a dual-income household managing shared expenses across multiple bank and
     credit card accounts, I want read-only bank linking that does not require me
     to share login credentials directly with the app so that I can grant financial
     visibility without compromising account security"

  7. "As a freelancer or gig worker with irregular income needing to project whether
     month-end balances will cover fixed obligations, I want to receive a mid-month
     alert when projected month-end balance falls below a threshold I set so that I
     can prioritize which discretionary expenses to defer"

  Persona breakdown: all 5 target_users personas represented, each story uses the exact distinguishing trait from
  target_users as its persona label. 0 generic "As a user" labels.

  ---
  Constraint coverage check:
  - Every story maps to a target_users entry ✓
  - At least 3 distinct personas represented (all 5 are) ✓

  The fix took effect cleanly. Ready to run the v3 calibration when you are.
]

## Constraint added to PRD_GENERATION_PROMPT
- Every user story's persona MUST correspond to one of the personas
  listed in target_users.
- Across all user stories, at least 3 of the personas from target_users
  should be represented.

