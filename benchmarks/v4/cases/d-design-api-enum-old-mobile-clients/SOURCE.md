# Sources

- Google API Improvement Proposals, AIP-180 Backwards compatibility — https://google.aip.dev/180
- Stripe blog, APIs as infrastructure: future-proofing Stripe with versioning — https://stripe.com/blog/api-versioning
- Martin Fowler, ParallelChange — https://martinfowler.com/bliki/ParallelChange.html

## Grader basis

- enum-breaks-old-decoders: AIP-180 (user code may not handle new enum values gracefully; caution for enums in responses). Behaviour of Swift Codable and Moshi default enum decoding is platform knowledge (not separately cited).
- gate-by-client-version: Stripe versioning (transform responses per client version; old versions keep working); AIP-180 caution on response enums.
- keep-total: AIP-180 (must not remove fields or change types; renaming = add new, keep old); Stripe ("fields that were present before should stay present"); Fowler ParallelChange.
- non-usd-on-old-clients: AIP-180 (must not change a field's semantics in ways likely to break reasonable code) applied to currency meaning.
- future-proof-new-clients: AIP-180 (enums used in responses should document that they may grow) — client-side tolerance is the corresponding practice.

## Why a capable general model might miss it

Adding an enum value is widely described as "additive and safe", so models often miss that strict mobile decoders fail on it, and they treat the money change as a pure schema problem without seeing the currency-semantics issue for clients that will never update.

The API and client details are synthetic.
