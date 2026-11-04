---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Review this change before I merge it:

```python
@app.get('/reports/<int:report_id>')
@login_required
def get_report(report_id):
    cached = cache.get(f'report:{report_id}')
    if cached:
        return cached
    report = Report.query.get_or_404(report_id)
    body = render_report(report, viewer=current_user)  # hides salary columns for non-admins
    cache.set(f'report:{report_id}', body, timeout=600)
    return body
```
