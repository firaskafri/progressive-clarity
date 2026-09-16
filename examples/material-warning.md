# Material warning

- **Expected views:** Full is useful here for the decision, migration constraints,
  and verification detail. The warning itself does not force Full.
- **Required facts:** Early deletion can make data unreadable; the old key remains restricted through migration; recovery is verified before destruction.
- **Budget:** Provisional Advisory targets are 40 words at a glance and 200
  cumulatively through context; indispensable warnings take precedence.

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
