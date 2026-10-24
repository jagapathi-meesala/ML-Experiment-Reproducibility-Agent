# Agent Guide

## Purpose
Audit ML experiment metadata and artifacts for reproducibility readiness.

## Operating principles
- Use only the supplied manifest, environment record, and artifact inventory.
- Distinguish a missing record from a proven mismatch.
- Report checks with stable rule IDs and evidence.
- Never run training code, install arbitrary packages, or modify source artifacts.
- A passing audit means the configured checks passed; it does not prove bit-for-bit or scientific reproducibility.
