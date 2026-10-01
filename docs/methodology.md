# Experimental Methodology

1. Submit a harmless text sample and choose an ordered list of representation steps.
2. The baseline detector evaluates the original text against fixed synthetic lab markers.
3. The pipeline applies each selected text transformation in order.
4. The same detector evaluates the resulting text.
5. The system records SHA-256 hashes, lengths, step timings and match states.
6. The analyst compares the baseline and transformed outcomes.

A changed result means only that a deterministic synthetic substring rule did or did not match the transformed text. It is not evidence of bypassing antivirus, EDR, IPS, firewalls or any production security control.

## Reproducibility
Each run has a UUID, UTC timestamp, explicit pipeline definition, content hashes and per-step timing metrics. Raw sample content is returned to the analyst in the immediate API response but is not stored in SQLite.
