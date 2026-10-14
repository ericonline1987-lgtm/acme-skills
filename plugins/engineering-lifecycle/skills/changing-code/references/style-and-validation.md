# Style, names, validation and comments

Read this when the change involves formatting, naming, input handling, config files,
comments, or deleting a test or guard.

## Style

- Follow the project's formatter, linter, type checker and layout. A new warning your
  change introduces is a regression.
- Format only the files you changed. Before committing, look for lines that changed
  only in whitespace or wrapping and revert them; a reformat belongs in its own commit.

## Names

- Names carry business meaning: `unpaid_invoice_count`, not `n` or `tmp2`, outside tiny
  local scopes.
- Public fields, config keys and API names stay consistent with existing contracts. A
  rename of a public name is a contract change (see `boundaries.md`).

## Input validation fails closed

- Reject malformed, unsupported or ambiguous input and config with a clear error that
  names the field. Don't coerce silently unless an existing compatibility rule says so.
- Config files are code. In YAML, an unquoted value containing `: `, starting with `#`,
  or starting with `|`, `>`, `&`, `*`, `!`, `%`, `@` or a backtick can parse as something
  else entirely (a nested map, a comment, a block). Quote such values, and confirm the
  file parses to what you meant by loading it.

## Comments

- Comment the why: invariants, edge cases, trade-offs, links to the decision.
- Don't narrate what the next line does. If a comment explains intent that a better name
  or structure could carry, change the code instead.

## Deleting tests and guards

Two kinds look alike:

| Kind | Example | Delete with the feature? |
|---|---|---|
| Tombstone | "The legacy export endpoint stays removed" | Yes, it guarded the removal |
| Safety or build guard | "No secrets in the bundle", "schema matches" | No, it protects something still live |

When unsure, keep it and ask.

## Retiring things in sets

When one resource is retired, look for its siblings (its config keys, routes, jobs,
dashboards, docs) and retire them in the same change, using a literal-string search for
each name. Half-removed resources fail later and far away.

## Final read

Remove debug leftovers, dead code you created, misleading names and stale comments.
