# Simple fact

- **Expected presentation:** Focused, because this is a simple factual question.
- **Required facts:** Default stashing excludes untracked and ignored files;
  `-u` includes untracked files; `-a` includes ignored files; tracked staged
  and unstaged changes need neither flag.
- **Budget:** The Full-format 40/200 budget does not apply.

## Prompt

Does `git stash` include untracked files by default?

## Response

No. By default, `git stash` includes tracked staged and unstaged changes but
omits untracked and ignored files. Use `git stash -u` for untracked files or
`git stash -a` to include ignored files too.
