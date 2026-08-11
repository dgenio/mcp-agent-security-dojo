# Blind-user adoption gate

Do not broadly promote the Security Dojo until strangers can obtain value from it without maintainer narration.

This is a lightweight decision protocol, not a universal OSS benchmark.

## Test setup

Recruit people who have not worked on the repository. Give each person only the repository URL and ask them to evaluate the project as they normally would. Do not walk them through commands or explain the intended result during the test.

For the default flagship journey, record:

- whether they reached a meaningful result without maintainer help;
- time to first meaningful result;
- what they think the demonstrated control changed;
- what they think the control does **not** guarantee;
- whether they voluntarily inspected or tried an underlying library;
- where they stopped, guessed, or asked for help.

Do not collect sensitive analytics or personal data. A small manual worksheet is sufficient.

## Initial decision guardrails

Use these as falsifiable launch criteria:

- **Completion:** at least 8/10 blind users complete the flagship without maintainer help.
- **Time-to-value:** median first meaningful result is under 10 minutes.
- **Comprehension:** at least 8/10 can correctly explain what the primary control did and one important limitation.
- **Downstream interest:** at least 20% voluntarily inspect or try at least one underlying library.

If a result misses a threshold, inspect the failure mode before changing scope. A failed onboarding test is normally a reason to simplify instructions, dependencies, output, or product-to-problem mapping—not to add scenarios or content.

## Portfolio decisions

### GO

Invest further when outsiders reproduce the central result and at least one downstream signal appears: library trial/use, an independent issue/PR, a bypass contribution, citation, reuse, or adaptation.

### ITERATE

People run the lab but do not inspect/use the underlying libraries. Treat this as an interesting educational asset with a weak product bridge. Improve the CTA, standalone library UX, or correspondence between the demonstrated control and the library. Do not add more scenarios yet.

### FREEZE

After two serious distribution experiments, people consume the lab but essentially no downstream behavior appears. Stop feature expansion and keep it as a stable educational asset.

### MERGE

If blind users cannot explain why this lab and another dgenio lab need to exist independently, move the useful material into the clearer home rather than preserving repository boundaries for their own sake.

### ARCHIVE

Archive when the lab produces none of the following: an audience, product proof, external evidence/contributions, or an important reference/education function.

## Promotion rule

Only after the gate is credible should the lab become a distribution asset. Start with one strong technical experiment. Do not create a content factory around unvalidated onboarding.
