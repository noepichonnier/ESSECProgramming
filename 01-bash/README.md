# Exercise 1 – Configure a development environment (slide 18)

`install.sh` sets up a Python dev environment from scratch on Debian/Ubuntu:

1. updates package lists
2. installs git, curl, wget, vim, build tools, Python 3, pip and venv
3. creates a virtual environment in `~/.venvs/aidams`
4. installs pytest, fastapi and uvicorn inside it
5. verifies each tool is available

```bash
chmod +x install.sh
./install.sh
source ~/.venvs/aidams/bin/activate
```

Design choices: `set -euo pipefail` (fail fast), a `PACKAGES` array (easy to
extend), `sudo` only when not root, and the script can be re-run safely.
