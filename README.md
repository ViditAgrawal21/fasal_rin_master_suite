# Fasal Rin Automation Suite — Master Launcher

Small launcher EXE (~10-20 MB) that lets users download and open all 4 Fasal Rin automation tools.

## Tools included
| Tool | Description |
|------|-------------|
| Fasal Rin Loan Automation | Automates loan applications on the Fasal Rin portal |
| Loan Discrepancy Management | Handles discrepancy resolution |
| IS Claim Discrepancy | Automates IS claim discrepancy submissions |
| IS Claim Automation | Automates IS claim filing |

## How it works
1. User downloads `FasalRinSuite.exe` (this launcher)
2. Launcher shows all 4 tool cards with current admin-set prices
3. User clicks **Download** — tool EXE fetched from GitHub Releases
4. User clicks **Open** — tool EXE launched as subprocess
5. Each tool handles its own subscription/license

## Build
```
pip install -r requirements.txt
python build.py
```
Output: `dist/FasalRinSuite.exe`

## Distribution
Upload `dist/FasalRinSuite.exe` to GitHub Releases on this repo.
Share the release link with users — they download once and get all future updates via the built-in updater.
