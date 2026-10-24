---
name: environment-drift-check
description: Compare recorded software and accelerator environment fields.
---
# Environment Drift Check

1. Compare only configured fields that appear in both records.
2. Report unequal values with both observed values.
3. Report missing comparison fields as skipped/informational, not as proven drift.
4. Do not install packages or modify the environment.
