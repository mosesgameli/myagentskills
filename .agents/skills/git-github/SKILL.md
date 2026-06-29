---
name: git-github
description: 'Run a standard Git + GitHub feature delivery workflow from commit to merged PR and synced main. Use when initializing repositories, creating feature branches, pushing changes, opening pull requests with gh, merging safely, and cleaning up branches using conventional commits.'
argument-hint: 'Feature name, conventional commit title, and PR body summary'
user-invocable: true
disable-model-invocation: false
---

# Git + GitHub Delivery Workflow

Execute a reliable end-to-end workflow for shipping code changes with Git and GitHub CLI.

This skill standardizes:
- repository initialization and first push
- feature branch creation and publication
- pull request creation with conventional commit naming
- merge and branch cleanup
- local branch resynchronization

## When To Use

Use this skill when you need to:
- create or continue work in a Git repository that targets `main`
- open PRs with `gh pr create`
- merge PRs with `gh pr merge --merge --delete-branch`
- keep local `main` in sync after merge

## Preconditions

Before running the workflow, ensure:
- Git is installed and configured (`user.name`, `user.email`)
- GitHub CLI is installed and authenticated (`gh auth status`)
- you have push permission to the target repository
- required checks (tests/lint/build) are known for the project

## Inputs

Required:
- changed files to commit
- conventional commit message (for commit and PR title)
- feature branch name in `feat/<feature-name>` format
- concise PR body describing what changed and why

Optional:
- PR number for explicit merge targeting
- list of required validation commands (tests/lint/typecheck)

## Primary Workflow

Follow this sequence unless a decision rule below says otherwise.

1. Initialize repository if needed.
	- `git init`
2. Stage changes.
	- `git add <files>`
3. Commit changes using conventional commit format.
	- `git commit -m "<type>(<scope>): <summary>"`
4. Push `main`.
	- `git push origin main`
5. Create feature branch.
	- `git checkout -b feat/<feature-name>`
6. Publish feature branch.
	- `git push origin feat/<feature-name>`
7. Open pull request.
	- `gh pr create --title "<conventional commit>" --body "<description of changes>" --base main --head feat/<feature-name>`
8. Merge pull request and delete branch.
	- `gh pr merge <pr-number> --merge --delete-branch`
9. Return to main.
	- `git checkout main`
10. Update local main.
	- `git pull origin main`

## Decision Rules

### Repository State

- If this is not yet a Git repository, run `git init`.
- If a repository already exists, skip `git init`.
- If `origin` does not exist, add it before any push.
  - `git remote add origin <repo-url>`

### Branch Strategy

- If `main` does not exist locally, create/rename to `main`.
  - `git branch -M main`
- If feature branch already exists, checkout instead of creating.
  - `git checkout feat/<feature-name>`
- If branch exists remotely but not locally, track it.
  - `git checkout -b feat/<feature-name> --track origin/feat/<feature-name>`

### Push Behavior

- If first push fails due to missing upstream, push with tracking.
  - `git push -u origin main`
  - `git push -u origin feat/<feature-name>`
- If push is rejected (non-fast-forward), pull/rebase according to team policy, then retry.

### PR Handling

- If PR number is unknown, capture it from `gh pr create` output or run `gh pr view --json number --jq .number`.
- If required checks are pending/failing, do not merge until checks pass.
- Use `--merge` only when merge commits are the agreed policy; otherwise align with repository merge policy.

## Quality Gates

Run these checks before PR creation and before merge.

1. Working tree state:
	- `git status --short` should only show intended changes before commit.
	- `git status --short` should be clean immediately after commit and push.
2. Commit quality:
	- Commit message matches conventional commit pattern.
	- Commit scope/summary reflects actual change set.
3. Validation:
	- Required tests/lint/type checks pass.
4. PR quality:
	- Title uses conventional commit format.
	- Body explains context, change summary, and impact.
5. Merge quality:
	- PR is approved (if required).
	- Required checks are green.

## Completion Criteria

Workflow is complete only when all conditions are true:
- changes are committed with conventional commit message
- feature branch is pushed to `origin`
- PR exists and is merged into `main`
- remote feature branch is deleted
- local branch context is `main`
- local `main` is up to date with `origin/main`

## Failure Recovery

- Wrong files staged: use `git restore --staged <files>` and restage correctly.
- Wrong commit message before push: use `git commit --amend -m "<new-message>"`.
- Wrong commit message after push: create corrective commit or coordinate safe history rewrite.
- Merged wrong PR: revert merge commit in a new PR.
- Local drift after merge: run `git fetch origin && git reset --keep origin/main` only if team policy allows.

## Suggested Conventional Commit Types

- `feat`: new user-facing functionality
- `fix`: bug fix
- `refactor`: internal code restructuring with no behavior change
- `docs`: documentation updates
- `test`: test-only changes
- `chore`: maintenance/build/tooling updates

## Example Invocation Inputs

- Feature name: `feat/login-rate-limit`
- Conventional commit: `feat(auth): add login rate limiting`
- PR body summary:
  - adds sliding-window rate limiter for login endpoint
  - introduces config for per-IP thresholds
  - includes unit tests and docs updates

