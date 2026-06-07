# TDWI Agentic Sales Pipeline — Workshop Setup

This repository is the starter project for the hands-on workshop. **Workshop lab content lives in the Jupyter notebooks:**

- Part 1 (Cloud Agent environment setup): [`LAB3-Part-1-Cloud-Agent-Environment-Setup.ipynb`](LAB3-Part-1-Cloud-Agent-Environment-Setup.ipynb)
- Part 2 (fix pipeline with Cloud Agent): [`LAB3-Part-2-Running-Cursor-Cloud-Agents.ipynb`](LAB3-Part-2-Running-Cursor-Cloud-Agents.ipynb)
- Part 3 (PR review automations, Revenue Explorer): [`LAB3-Part-3-Automations.ipynb`](LAB3-Part-3-Automations.ipynb)

### Lab map

| Part | You do | You learn |
|------|--------|-----------|
| **Setup** ([README](README.md)) | Fork, clone, `.venv`, test push | Your own GitHub repo for Cloud Agents |
| **1** | Dockerfile + `environment.json`, secrets | Reproducible Cloud Agent environment |
| **2** | Run failing tests → `AGENTS.md` → Cloud Agent → review & merge PR | Agent context, draft PRs, human verification |
| **3** | PR review Automation → Cloud Agent adds Streamlit app → mark PR ready | Event-driven agents; Automations vs Bugbot vs CI |

Follow the steps below to fork, clone, and verify you can push to your own copy on GitHub. There are two benefits of forking:
1. You will be able to run Cursor Cloud Agents in your own environment, which is the point of this lab.
2. You can push your changes to your own copy of the repository.

---

## 1. Create a GitHub account if you don't have one (if you already have an account, skip this step)

   1. Go to [GitHub](https://github.com) and create an account.

## 2. Authenticate your local Git to your GitHub account

1. You only need to complete this step if you created a new account **or** if your local Git is not authenticated to your GitHub account. If you are unsure, you can skip this step now and come back to it if you are prompted for a password in step 6
2. Create a **classic** Personal Access Token with the **`repo`** scope:
   1. Sign in to [GitHub](https://github.com)
   2. Open your profile menu (top right) → **Settings**
   3. In the left sidebar, scroll to **Developer settings** → **Personal access tokens** → **Tokens (classic)**
   4. Click **Generate new token** → **Generate new token (classic)**
   5. Add a note (e.g. `TDWI workshop`), set an expiration if you like, and check the **`repo`** scope
   6. Click **Generate token**, then **copy the token immediately** (you will not see it again). Store it somewhere safe—you will use it as your password when Git prompts you over HTTPS

## 3. Fork the workshop repository

1. Go to the main workshop repo on GitHub:  
   **https://github.com/willjhenry/tdwi-agentic-sales-pipeline-starter**
2. Click **Fork** → **Create a new fork**
3. Click **Create fork** in the lower right

## 4. Clone your fork in Cursor

1. Copy the HTTPS URL from **your** forked repo (**Code** → **HTTPS**, then copy the link)
2. In Cursor, open the Command Palette (**Cmd/Ctrl + Shift + P**) → type: **Git: Clone**
3. Paste the HTTPS URL and clone the repo
4. Select **Open** when asked if you would like to open the cloned repository
5. Select **Open Workspace** when the popup appears in the lower right

## 5. Set up the Python environment (`.venv`)

You need Python 3 installed locally. In Cursor, open a terminal (**Terminal** → **New Terminal**) with the project folder as the working directory, then run the commands for your OS.

**Mac**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows** (PowerShell or Command Prompt in the integrated terminal)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If Windows reports that `python` is not found, try `py -m venv .venv` instead of `python -m venv .venv`.

**Both platforms — select the interpreter in Cursor**

1. Open the Command Palette (**Cmd/Ctrl + Shift + P**) → **Python: Select Interpreter**
2. Choose the interpreter labeled **`.venv`** (path should include `.venv` in this project)

When the venv is active, your terminal prompt usually shows `(.venv)`. You can confirm with `which python` (Mac) or `where python` (Windows)—the path should point inside `.venv`.

## 6. Make your first push

1. Create a test file, `test.txt`. In the file write:
   `this is just a test file to test committing and pushing`
2. Commit the change in Cursor:
   1. Open the **Source Control** tab in the Primary Side Bar
   2. Press the **+** (plus) to the right of `test.txt` to stage the file
   3. Write a simple commit message in the **Message** input, e.g. `a test commit`
   4. Press the **Commit** button
   5. Press the **Synchronize Changes** button in the lower left corner
   6. If Git prompts for credentials: enter your **GitHub username** and, for the password, paste your **Personal Access Token** (created in step 2)—not your GitHub account password

---

After setup, open [`LAB3-Part-1-Cloud-Agent-Environment-Setup.ipynb`](LAB3-Part-1-Cloud-Agent-Environment-Setup.ipynb), then [`LAB3-Part-2-Running-Cursor-Cloud-Agents.ipynb`](LAB3-Part-2-Running-Cursor-Cloud-Agents.ipynb). After Part 2, continue with [`LAB3-Part-3-Automations.ipynb`](LAB3-Part-3-Automations.ipynb).
