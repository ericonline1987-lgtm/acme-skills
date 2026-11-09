---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Our new signup page. QA signed off with "looks fine on my laptop". Can you review it for accessibility and layout problems before we ship? Prioritise what actually matters.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1200, user-scalable=no">
<title>Sign up – Tallyhub</title>
<style>
  body { font-family: "Inter", sans-serif; margin: 0; background: #fff; color: #222; }
  .wrap { width: 1200px; margin: 0 auto; display: flex; }
  .hero { width: 640px; }
  .hero img { width: 640px; }
  .panel { width: 480px; padding: 40px; }
  h2 { font-size: 28px; margin: 0 0 24px; }
  .hint { color: #999; font-size: 13px; margin: 6px 0 18px; }
  input { width: 100%; border: 1px solid #ddd; padding: 12px; font-size: 15px; }
  input:focus { outline: none; }
  input.invalid { border-color: #e53935; }
  .btn { background: #4caf50; color: #fff; padding: 14px; text-align: center;
         border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: 600; }
  .terms a { color: #4caf50; text-decoration: none; }
</style>
</head>
<body>
<div class="wrap">
  <div class="hero"><img src="/img/team-dashboard.png"></div>
  <div class="panel">
    <h2>Create your account</h2>
    <input type="email" id="email" placeholder="Work email">
    <p class="hint">We'll never share your email.</p>
    <input type="password" id="pw" placeholder="Password">
    <p class="hint">At least 12 characters, including a number.</p>
    <div class="btn" onclick="submitForm()">Create account</div>
    <p class="terms hint">By signing up you agree to our <a href="/terms">Terms</a>.</p>
  </div>
</div>
<script>
  function submitForm() {
    const email = document.getElementById('email');
    if (!email.value.includes('@')) { email.classList.add('invalid'); return; }
    // ... POST /api/signup
  }
</script>
</body>
</html>
```
