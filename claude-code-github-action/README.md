# Claude Code GitHub Action: hands-on lab

Files from the Zero Cost AI video **"Claude Code GitHub Action: Fix Bugs with @claude (Hands-On Lab)"**.

In this lab you put a small Python project on GitHub, connect the [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action), and fix a real bug by writing one comment: `@claude please fix this bug`. Claude finds the cause, pushes a fix to a new branch, and the project's Tests workflow proves it works.

**Time:** about 15 minutes. **Cost:** a few cents of Claude usage (or your Pro/Max subscription) and a couple of free GitHub Actions minutes.

## What you need

- A GitHub account (you must be an admin of the repo you test on; your own repo is fine)
- [Git](https://git-scm.com), the [GitHub CLI](https://cli.github.com) (`gh auth login` once), and Python 3.10+ with `pip install pytest`
- One way to log in to Claude:
  - a Claude **Pro, Max, Team or Enterprise** plan and [Claude Code](https://code.claude.com) installed (for `claude setup-token`), **or**
  - an **API key** from the [Claude Console](https://platform.claude.com)

## The lab project

[`example-files/claude-action-lab`](example-files/claude-action-lab):

| File | What it does |
|---|---|
| [`shipping.py`](example-files/claude-action-lab/shipping.py) | Orders of $50 or more should ship free. **The bug:** it uses `>` instead of `>=` |
| [`tests/test_shipping.py`](example-files/claude-action-lab/tests/test_shipping.py) | 3 tests; `test_exactly_50_ships_free` fails because of the bug |
| [`CLAUDE.md`](example-files/claude-action-lab/CLAUDE.md) | Project rules Claude reads on every run (small fixes, never edit a test to make it pass) |
| [`.github/workflows/claude.yml`](example-files/claude-action-lab/.github/workflows/claude.yml) | **The Claude Code Action workflow**: runs when a comment mentions `@claude` |
| [`.github/workflows/tests.yml`](example-files/claude-action-lab/.github/workflows/tests.yml) | Runs `pytest` on every push and pull request, so you can see the fix work |

## Step 0: get the files and see the bug

```bash
git clone --depth 1 https://github.com/NEDBS12/youtube-tuto.git
cp -r youtube-tuto/claude-code-github-action/example-files/claude-action-lab ./claude-action-lab
cd claude-action-lab
python -m pytest -q          # 1 failed, 2 passed
```

On Windows PowerShell, use `Copy-Item -Recurse youtube-tuto\claude-code-github-action\example-files\claude-action-lab .\claude-action-lab` instead of `cp -r`.

## Step 1: create the repo

```bash
git init && git add . && git commit -m "Starter"
gh repo create claude-action-lab --public --source=. --push
```

(`--private` works too.) The **Tests** workflow runs right away and fails: that's the bug.

> The lab folder already contains `claude.yml`, so it's pushed in this step. In the video it's typed in step 4 to explain each line; the result is the same. It does nothing until steps 2 and 3 are done.

## Step 2: install the Claude GitHub App

1. Open **https://github.com/apps/claude** and click **Install**.
2. Choose **Only select repositories** → `claude-action-lab` → **Install**.

The action uses the app's **Contents**, **Issues** and **Pull requests** read and write permissions.

**Shortcut:** inside Claude Code, `/install-github-app` installs the app, saves the secret and opens a pull request with the workflow for you. This lab does it by hand so you see each piece.

## Step 3: add the secret

**With a Claude subscription** (the lab's `claude.yml` uses this):

```bash
claude setup-token                          # signs you in and prints a long-lived token
gh secret set CLAUDE_CODE_OAUTH_TOKEN       # paste the token when asked
```

**With an API key instead:**

```bash
gh secret set ANTHROPIC_API_KEY             # paste your sk-ant-... key
```

Then, in `.github/workflows/claude.yml`, replace the `claude_code_oauth_token: ...` line with
`anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`, commit and push.

Never paste a token or key into a file you commit. Secrets are encrypted, and nobody can read them back.

## Step 4: understand the workflow

```yaml
on:
  issue_comment:                 # runs on every new issue / PR comment...
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')   # ...but only if it mentions @claude
    permissions:                 # push branches, comment, log in as the Claude app, read CI
      contents: write
      pull-requests: write
      issues: write
      id-token: write
      actions: read
    steps:
      - uses: actions/checkout@v6               # your code on the runner
      - uses: anthropics/claude-code-action@v1  # the Claude Code Action
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          claude_args: "--max-turns 10"         # cap the work (and cost) of one run
```

There's no `prompt:` input, so the action runs in **interactive mode**: it waits for `@claude`.

## Step 5: test it with @claude

1. On GitHub, open **Issues → New issue**:
   - **Title:** `Orders of exactly $50 still pay shipping`
   - **Body:** `A customer with a $50.00 order was charged $4.99 shipping. Free shipping should start at $50.`
2. Create the issue, then **add a comment**: `@claude please fix this bug.`
   (This workflow listens to comments, so put `@claude` in a comment, not in the issue body.)
3. Claude replies with a progress comment. Watch the run in the **Actions** tab (about 1 to 3 minutes).
4. When it's done, the comment explains the cause and links to a new branch (`claude/issue-1-...`). Use its link to **create the pull request**.
5. In the pull request: the change in `shipping.py` is `>` → `>=`, and the **Tests** check is green.
6. Merge it, then check locally:

```bash
git pull
python -m pytest -q          # 3 passed
```

**Bonus:** in the pull request, comment `@claude add a test for an order of 49.99` or `@claude review this change`.

Claude's exact wording, branch name and number of commits vary from run to run. What you're checking: the bug is fixed in `shipping.py`, the tests weren't edited, and CI is green.

## Troubleshooting

- **Nothing happens after `@claude`:** check the app is installed on this repo, Actions are enabled (**Settings → Actions**), the secret name matches the workflow, and `@claude` is a whole word (not `@claude-bot`).
- **The run fails with an auth error:** recreate the token (`claude setup-token`) or key and set the secret again.
- **The commenter isn't allowed:** only users with write access to the repo can trigger Claude.
- **Tests don't run on Claude's commits:** don't pass `github_token: ${{ secrets.GITHUB_TOKEN }}` to the action; let it use the Claude app.

## Clean up

Delete the repo (`gh repo delete claude-action-lab`), or remove the secret and the workflow. Uninstall the Claude app in **GitHub → Settings → Applications** if you don't use it elsewhere. Deleting a secret doesn't revoke it: revoke an API key in the Claude Console.

## Files in this folder

- `claude-code-github-action.mp4`: the video
- `claude-code-github-action.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/claude-action-lab/`: the lab project (no secrets in it)

## Learn more

- [Claude Code GitHub Actions docs](https://code.claude.com/docs/en/github-actions)
- [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) and its [examples folder](https://github.com/anthropics/claude-code-action/tree/main/examples)
