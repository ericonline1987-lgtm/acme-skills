# acme-skills

Agent skills for Claude, packaged as two plugins in one marketplace.

| Plugin | Skills |
|--------|--------|
| `engineering-lifecycle` | writing-requirements, designing-systems, reviewing-code, writing-tests |
| `professional-craft` | writing-documents, building-presentations, writing-emails |

## Install (Claude Code)

```
/plugin marketplace add <your-github-org>/acme-skills
/plugin install engineering-lifecycle@acme-skills
/plugin install professional-craft@acme-skills
```

Install either plugin on its own if you only need one.

## Layout

```
.claude-plugin/marketplace.json   # lists the plugins
plugins/<plugin>/.claude-plugin/plugin.json
plugins/<plugin>/skills/<skill>/SKILL.md
plugins/<plugin>/shared/          # files shared by that plugin's skills
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
