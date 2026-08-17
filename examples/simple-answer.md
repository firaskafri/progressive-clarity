# Simple answer

- **Expected view:** At a glance, selected automatically.
- **Required facts:** Default stashing excludes untracked files; `-u` includes them; ignored files require `-a`.
- **Budget:** At a glance is at most 40 counted words.

## Prompt

Does `git stash` include untracked files by default?

## Response

<!-- words:simple-glance:start -->
No. `git stash` saves tracked changes by default; use `git stash -u` to include untracked files. Ignored files still remain unless you use `-a`.
<!-- words:simple-glance:end -->
