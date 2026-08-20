# Sequential procedure

- **Expected structure:** Non-fit procedure with an optional orientation followed by the complete natural step sequence.
- **Required facts:** Verifiers receive the new public key before signers switch; both keys overlap; old signatures expire before revocation; rollback remains possible.
- **Budget:** Full-format budgets are not applicable to this non-fit procedure.

## Prompt

Show me how to rotate an application signing key without interrupting verification.

## Response

### Orientation

Use an overlap period: publish the new verifier before signing with the new key, then retire the old key only after old signatures expire. Keep rollback access throughout.

### Procedure

1. Generate the new key in the approved key store, record its identifier, and leave the current signer unchanged.
2. Publish the new public key to every verifier while retaining the old public key.
3. Confirm that each verifier accepts test signatures from both keys and that monitoring distinguishes their identifiers.
4. Switch a small signer cohort to the new private key. Keep the old signer available for rollback.
5. Expand signing only after verification errors remain within the accepted threshold.
6. Wait longer than the maximum lifetime of signatures produced by the old key, including clock-skew allowance and delayed jobs.
7. Confirm that no valid old signatures remain in flight, then disable old-key signing.
8. Revoke and destroy the old key through the approved key-management process only after recovery evidence and audit records are complete.
