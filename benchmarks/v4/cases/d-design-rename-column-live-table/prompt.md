---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Postgres 15, `accounts` table is ~420M rows, ~6k writes/sec at peak. Rails 7.1 app, deploys are rolling (old and new pods serve traffic side by side for ~10 min).

We need to:
- rename `email` → `login_email`
- make it NOT NULL (about 2k legacy rows have NULL email; we fill them from `contact_email`)
- add a case-insensitive unique index on it

Plan is one migration Tuesday night, low traffic window:

```ruby
class RenameEmailOnAccounts < ActiveRecord::Migration[7.1]
  def change
    execute "UPDATE accounts SET email = contact_email WHERE email IS NULL"
    rename_column :accounts, :email, :login_email
    change_column_null :accounts, :login_email, false
    add_index :accounts, "lower(login_email)", unique: true, name: "idx_accounts_login_email_lower"
  end
end
```

Sanity check before I open the PR?
