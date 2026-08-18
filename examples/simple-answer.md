# Simple answer

- **Expected views:** At a glance, In context, and At depth render in order.
- **Required facts:** Default stashing excludes untracked and ignored files; `-u` includes untracked files; `-a` includes ignored files; tracked staged and unstaged changes need neither flag.
- **Budget:** At a glance is at most 40 counted words; At a glance plus In context is at most 200.

## Prompt

Does `git stash` include untracked files by default?

## Response

### At a glance

<!-- words:simple-glance:start -->
No. By default, `git stash` omits untracked and ignored files, so verify repository status before assuming the working tree is fully preserved.
<!-- words:simple-glance:end -->

### In context

<!-- words:simple-context:start -->
Use `git stash -u` to add untracked files or `git stash -a` to add ignored files too. Tracked staged and unstaged changes need neither flag.
<!-- words:simple-context:end -->

### At depth

<!-- words:simple-depth:start -->
Inspect the entry with `git stash show --stat` before cleanup. `git stash apply` keeps the stash entry after restoration; `git stash pop` removes it only after a successful apply. A pathspec can restrict which tracked paths enter the stash.
<!-- words:simple-depth:end -->
