# Exercise 2 – Git mini exo (slide 26)

## Part 1: Setup & config

1. Install Git (Debian/Ubuntu: `sudo apt install git`, macOS: `brew install git`).
2. Check the version:
   ```bash
   git --version
   ```
3. Configure identity:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   git config --global init.defaultBranch main
   ```

## Part 2: Create your first repository

```bash
mkdir my-first-repo       # create the folder
cd my-first-repo          # navigate into it
git init                  # initialise a Git repository
touch readme.txt          # create the file
```

## Part 3: Your first commit

1. State of the repository: `git status`
2. Stage the file: `git add readme.txt`
3. Commit: `git commit -m "Add readme file"`
4. History: `git log`

## Part 4: Make changes

1. `echo "A second line" >> readme.txt`
2. `git status` now reports `readme.txt` as **modified** but **not staged for commit**:
   Git sees that the working copy differs from the last commit.
3. ```bash
   git add readme.txt
   git commit -m "Add a second line to readme"
   ```
4. **2 commits** (`git log --oneline | wc -l`).

## Part 5: Exploration

- `git diff` – shows line-by-line differences between the working directory and
  the staging area (unstaged changes). `git diff --staged` compares staging area vs last commit.
- `git log --oneline` – compact history: one line per commit (short hash + message).

## Part 6: Working with branches

1. List branches: `git branch`
2. Create `feature-script`: `git branch feature-script`
3. Switch to it: `git switch feature-script` (or `git checkout feature-script`)
4. Create and switch to `dev` in one command: `git switch -c dev` (or `git checkout -b dev`)
5. Back to `feature-script`: `git switch feature-script`
6. Verify: `git branch` (current branch has `*`) or `git branch --show-current`

## Part 7: Create a bash script on a branch

```bash
git switch feature-script           # 1. be on the right branch
touch install.sh                    # 2. create the file
```

3. Content of `install.sh`:
   ```bash
   #!/usr/bin/env bash
   echo "Starting installation..."
   sudo apt-get update
   sudo apt-get install -y git
   echo "Installation complete!"
   ```
4. Make it executable: `chmod +x install.sh`
5. Commit:
   ```bash
   git add install.sh
   git commit -m "Add install script"
   ```
6. History on this branch: `git log --oneline`

## Part 8: Merge branches

1. `git switch main`
2. `ls` – `install.sh` is **not** present: it only exists in commits of `feature-script`,
   and `main` has not received them yet.
3. Merge: `git merge feature-script`
4. `ls` – `install.sh` has appeared.
5. `git log --oneline` – the commit "Add install script" is now on `main`. Since `main` had no
   new commits, Git did a **fast-forward** merge (no merge commit, linear history).
6. Delete the merged branch: `git branch -d feature-script`

## Part 9: Push to GitHub

1. Create the repository `my-first-repo` on github.com.
2. Do **not** tick "Add a README" (otherwise the histories diverge and the first push is rejected).
3. Link local and remote:
   ```bash
   git remote add origin https://github.com/<username>/my-first-repo.git
   ```
4. Push:
   ```bash
   git branch -M main
   git push -u origin main
   ```
5. After refreshing, GitHub shows `readme.txt` and `install.sh` and the commit history.

## Part 10: Delete and clone

```bash
cd ..                                                       # 1. leave the project folder
rm -rf my-first-repo                                        # 2. delete the local folder
git clone https://github.com/<username>/my-first-repo.git   # 3. clone from GitHub
cd my-first-repo && ls                                      # 4. verify the files are there
```

## Part 11: Full workflow practice

```bash
# 1-2. delete local folder, then delete the GitHub repo (Settings > Danger Zone > Delete)
rm -rf my-first-repo

# 3-4. new project + git init
mkdir bash-installer && cd bash-installer
git init -b main

# 5-6. README on main
cat > README.md <<'EOT'
# bash-installer
Small bash script that sets up a development environment.
EOT
git add README.md
git commit -m "Add README"

# 7. feature branch
git switch -c feature-install

# 8-9. add the previous script and commit it
cp ../01-bash/install.sh .
git add install.sh
git commit -m "Add install script"

# 10-12. back on main, merge, clean up
git switch main
git merge feature-install
git branch -d feature-install

# 13-14. new GitHub repository (empty, no README) then push
git remote add origin https://github.com/<username>/bash-installer.git
git push -u origin main
```

## Reflection questions

1. **Why is version control useful?** It records the full history, lets you undo mistakes,
   makes collaboration possible, and acts as a backup.
2. **Staging vs committing?** Staging (`git add`) selects which changes go into the next
   snapshot; committing (`git commit`) permanently records that snapshot in history.
3. **When to commit?** Small, coherent, working steps – each commit does one logical thing.
4. **`git init` vs `git clone`?** `init` creates a new empty repository locally;
   `clone` copies an existing remote repository including its full history.
5. **Why good commit messages?** They explain *what* and *why*, so people (including future you)
   can understand, search and revert changes (`git bisect`, `git blame`).
6. **Purpose of branches?** Isolated lines of development: work without breaking `main`.
7. **When create a branch?** For any new feature, bug fix or experiment, and when several
   people work at the same time.
