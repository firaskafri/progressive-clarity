# Material warning

- **Expected mode and views:** Default Verbose mode renders all views; the prohibition and data-loss warning appear first in At a glance.
- **Required facts:** Early deletion can make data unreadable; the old key remains restricted through migration; recovery is verified before destruction.
- **Budget:** At a glance is at most 40 counted words unless safety requires more; At a glance plus In context is at most 200.

## Prompt

Can I delete the old encryption key immediately after rotating to a new key?

## Response

### At a glance

<!-- words:warning-glance:start -->
No. Deleting the old key before re-encryption can make existing data permanently unreadable. Keep it available until migration and recovery verification finish.
<!-- words:warning-glance:end -->

### In context

<!-- words:warning-context:start -->
Restrict the old key to decryption only and block new encryption with it. Inventory every record, delayed job, and backup that references its identifier; assign an owner to track completion.
<!-- words:warning-context:end -->

### At depth

<!-- words:warning-depth:start -->
Process records in auditable batches, compare plaintext checksums after migration, and restore a representative backup with the replacement key. Confirm that access logs show no remaining dependency, then use the approved destruction workflow and retain its evidence.
<!-- words:warning-depth:end -->
