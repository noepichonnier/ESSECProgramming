#!/usr/bin/env bash
# Replays parts 2-8 and 10 of the Git mini exo locally in a temporary folder
# (no GitHub account needed). Usage: ./workflow_demo.sh
set -euo pipefail

WORKDIR="$(mktemp -d)"
trap 'rm -rf "${WORKDIR}"' EXIT
cd "${WORKDIR}"

export GIT_AUTHOR_NAME="Demo" GIT_AUTHOR_EMAIL="demo@example.com"
export GIT_COMMITTER_NAME="Demo" GIT_COMMITTER_EMAIL="demo@example.com"

mkdir my-first-repo && cd my-first-repo
git init -q -b main
touch readme.txt
git add readme.txt && git commit -q -m "Add readme file"

echo "A second line" >> readme.txt
git status --short
git add readme.txt && git commit -q -m "Add a second line to readme"

git switch -q -c feature-script
printf '#!/usr/bin/env bash\necho "Starting installation..."\necho "Installation complete!"\n' > install.sh
chmod +x install.sh
git add install.sh && git commit -q -m "Add install script"

git switch -q main
echo "On main before merge: $(ls | tr '\n' ' ')"
git merge -q feature-script
echo "On main after merge:  $(ls | tr '\n' ' ')"
git branch -d feature-script
git log --oneline
