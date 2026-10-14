# Logic errors a clean merge can still contain

A merge with no conflicts can still be wrong. These are the shapes to look for in each
hotspot and in the files around it. Each comes with the question that exposes it.

| Pattern | What it looks like | Ask |
|---|---|---|
| **Half-generalised branch** | One side widened a condition (`if mode in SUPPORTED`), the other side kept a hard-coded inner path for the old value | Does every new value reach code that handles it, or only the outer check? |
| **New option without its defaults** | A new mode, type or flag is accepted, but its default config, template, seed data or resource was added on the other side only, or not at all | Start the system with only defaults and the new option: does it start? |
| **Entry accepts, initialisation misses** | The parser or router accepts a new type, but the initialisation chain (registry, factory, migration, DI wiring) never constructs it | Trace the new type from entry to first real use. Is every link present after the merge? |
| **Action merged, configuration not** | The code that deploys or calls something landed; the config, secret, route, flag or permission it needs did not | List what the new code reads at runtime. Is each item present in every environment's config after the merge? |
| **Companion change missing** | The change needs a matching change in another repository (client, schema, infrastructure, pinned dependency) that isn't merged or published | Which other repository must change with this one, and is that change on the exact ref this one will resolve? |
| **Safety net weakened** | A test, assertion, validation or guard was relaxed or deleted on one side to get green, and the merge kept the weaker version | Compare the tests and guards on the hotspot files against both parents. Did anything get looser? |
| **One side wins wholesale** | A conflict resolved by taking one side's whole file, dropping the other side's unrelated edits in that file | For each conflicted file, list the other side's changes and confirm each survived or was deliberately dropped |
| **Reordered or renamed under the other side** | One side renamed or reordered something (config keys, enum values, migration order), the other side added uses of the old name or order | Search the merged result for the old names and old ordering assumptions |

## How to use this list

1. Run `scripts/merge_evidence.py` to get the hotspots and any "dropped?" files.
2. For each hotspot, read both sides' changes since the merge base and walk the table.
3. Write one line per hotspot in the report: which patterns you checked, and the result.
4. When the merge changes behaviour behind a flag or a config value, test both values.
