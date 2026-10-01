# Threat Model and Safety Controls

## Intended use
Controlled analysis of harmless text strings for learning about representation changes and deterministic static matching.

## Out of scope
Executable payload creation, shellcode, malware development, exploit delivery, real security-product testing, stealth, persistence, command execution and operational evasion.

## Controls
- Localhost-only default server binding.
- Request-body and sample-length limits.
- Strict allowlist for pipeline step types and names.
- No shell commands, subprocess calls or dynamic code evaluation.
- Parameterized SQLite queries.
- Raw samples are not persisted by default.
- Structured rotating application logs.
- Reports contain metadata and hashes, not the original sample.
