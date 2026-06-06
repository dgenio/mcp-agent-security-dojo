# Ethical external-distribution checklist

This repository reproduces real agent attack patterns for teaching. Before
sharing it externally — a talk, a workshop, a blog post, a client engagement, or
simply pointing people at the repo — run through this checklist so the material
stays educational and is not mistaken for a production security product or a
ready-to-use attack toolkit.

Use it as a literal pre-flight: copy the boxes into a PR or engagement note and
tick them off.

## 1. Framing and honesty

- [ ] The audience is told this is an **educational lab / reference
      architecture**, not a production security control.
- [ ] The deliberately weak detectors (regex / substring) and simulated tools are
      called out, with a pointer to
      [`security-model.md#limitations`](security-model.md#limitations).
- [ ] No claim is made that the dojo "secures" or "audits" a real agent
      deployment. It demonstrates *patterns*.
- [ ] The Weaver Stack integration status is presented honestly per the
      [library map](library-map.md): the adapters are local reference
      implementations, the real packages are not yet wired in.

## 2. Safety of the material itself

- [ ] All data shown is the repo's **fake fixtures** (`examples/`). No real
      customer data, secrets, or credentials are introduced.
- [ ] The unsafe scenarios remain **local-only**: no live network calls, no real
      APIs, no destructive operations are added for a demo.
- [ ] Any modified or added scenario still writes only within the working tree
      (traces under `traces/`).
- [ ] Examples named like `internal_secrets.txt` are clearly flagged as invented.

## 3. Responsible use of attack content

- [ ] The injection strings, poisoned tool cards, and auth-weakening diffs are
      presented as **what to detect and prevent**, not as a copy-paste attack
      recipe against third parties.
- [ ] The audience is reminded that running these techniques against systems they
      do not own or have permission to test is out of scope and likely unlawful.
- [ ] If recording or publishing, no real internal hostnames, tokens, or
      employer-confidential details are visible on screen.

## 4. Attribution and licensing

- [ ] The project is attributed and the [MIT license](../LICENSE) is respected;
      cite via [`CITATION.cff`](../CITATION.cff) where appropriate.
- [ ] Derivative material (slides, forks, screenshots) keeps the
      "not production-ready" framing intact.
- [ ] Links point at the canonical repository rather than an unmaintained fork.

## 5. Repository hygiene before sharing widely

- [ ] `make lint` and `make test` pass on the shared revision.
- [ ] [`README.md`](../README.md), [`SECURITY.md`](../SECURITY.md), and
      [`CHANGELOG.md`](../CHANGELOG.md) reflect the current state.
- [ ] GitHub repository **topics**, **description**, and **social-preview image**
      are set (these are repository-settings actions, not part of the codebase —
      see the [recommended topics](../README.md#topics) and
      [`assets/banner.svg`](assets/banner.svg)).
- [ ] Any new scenario added for the talk is documented and wired into the README
      table and threat model, per [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## 6. After the engagement

- [ ] Feedback or new realistic failure modes are filed as issues rather than
      kept private, so the lab keeps improving.
- [ ] Any fixes made live are upstreamed via a PR with a changelog entry.
