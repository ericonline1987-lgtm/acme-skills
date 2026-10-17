---
name: handling-artifacts
description: Use this skill whenever work produces or ships files — screenshots, recordings, traces, exports, debug scripts, reports — or a repository or deliverable is about to be shared outside the team or has grown too large. It decides where each file belongs, what to clean up, what to redact for the widest reader, and how to package a deliverable so it works elsewhere.
---

# Handling artifacts

Files outlive the task that made them. Put each one where its next reader will look,
remove what nobody needs, and never let a file carry more than its widest reader may see.

## 1. Classify every file you create

| Class | Examples | Lives in |
|---|---|---|
| Requested deliverable | The report, deck, export or tool the person asked for | Where its peers already live, or where the person says; ask if there is no clear home |
| Project asset | Source, tests, fixtures, maintained config, durable docs | The project's maintained paths |
| Workflow output | Build output, test reports the pipeline reads | The project's existing ignored output folder |
| Handed-over evidence | A test upload, probe file or screenshot someone will check | Where the checker can reach it, until they confirm |
| Disposable | Debug scripts, traces, temporary screenshots, downloads, dumps | The scratch location the platform or session provides; otherwise a fresh `mktemp -d` |

When unsure, ask whether a future run, a teammate or a fresh machine would need it. If
yes, it's a project asset; if only this run, it's disposable. If still unclear, ask; when
no one can be asked, treat it as disposable rather than writing it into the project.

## 2. Placement rules

- A deliverable is never left only in a scratch folder, and never deleted at the end.
  Once it is in its home, edit that one copy; a second copy drifts.
- Disposable files never go in tracked paths or under a fixed name in a shared temp folder,
  where another run can overwrite or read them.
- Don't create or widen `.gitignore` rules or folder conventions just to hold disposable
  files, and don't invent a project convention unless asked.
- Don't make `.bak` or timestamped copies of files under version control; history already
  has the old version. (Without version control, a backup before editing is reasonable.)
- Follow the platform's and session's own instructions about where files go; they win
  over this skill's defaults.

## 3. Clean up

Before finishing, delete disposable files you created in the project, unless the person
asked to keep them. Handed-over evidence waits until its consumer confirms; deleting it
early turns your proof into their false alarm.

## 4. Redact for the widest reader

- Set the bar by the widest audience the destination will ever have. A repository that
  might be opened up, mirrored or handed to a vendor is already external.
- Before real material (screenshots, exports, recordings, documents) reaches anyone not
  entitled to it, mask customer and account names, people's names, contact details,
  amounts, and internal hosts. Credentials and tokens stay out of every destination.
- When both a redacted and an original version exist, name the redacted files to share;
  never say "copy the folder" if originals are in it.
- A scanner that reads only text is blind to images, video and PDFs. Check rendered
  frames too, or say plainly that binaries were not checked.
- Passwords are one-shot input: exchange them for the token or session needed, store only
  that, and confirm the password left no file, log or history behind (see
  `guarding-agent-actions` for secrets in output).

## 5. Package a deliverable to work elsewhere

- One self-contained folder holds the deliverable and everything it loads; drafts and
  source material go in a separate folder the export leaves out.
- Copy any file the person supplied from an app's temporary or cache folder into the
  deliverable's own folder before referencing it.
- Prove it: copy the export to a clean location (network off if it should work offline)
  and open it there.

## 6. A repository grown heavy with binaries

Classify media by role: keep maintained, reviewable assets under the project's policy
(for example Git LFS); keep generated, sensitive or oversized files out of history.
Deleting a file today doesn't shrink history. To reclaim space, in this order:

1. Diagnose: `python3 scripts/repo_weight.py --repo <path>` lists the largest objects in
   all history and whether each is still in the current tree. Old deleted binaries are
   usually the real weight.
2. Back up outside the repo: `git bundle create <path> --all` and `git bundle verify <path>`.
3. Show the person exactly which paths will be removed; wait for an explicit yes.
4. Rewrite with `git filter-repo`, naming only the diagnosed paths.
5. Re-run step 1 and confirm the weight is gone and nothing else was.
6. Agree the force-push with everyone who uses the repository; every clone must re-clone,
   and an old clone pushed back restores what was removed.

## Report

One line per file created, moved or removed: `<path> | <class> | kept, deleted, or
handed over awaiting confirmation | redaction: not needed, applied (what), or not
covered (which binaries)`, then `left behind: <paths and why, or none>`.
