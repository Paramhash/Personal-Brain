# Syncthing Setup — Mac to PC Hub Sync

## Topology

```
Macbook (Client)                PC Hub (Windows)              Threadripper (Compute)
────────────────                ────────────────              ──────────────────────
raw/  ──[Send Only]──────────→  raw/                          
                                wiki/  ──[Send+Receive]──────  wiki/
                                raw/   ──[Send+Receive]──────  raw/
```

- **Mac → PC**: Mac is Send Only for `raw/`. It pushes new drop files; it never receives
  PC's moves, deletions, or processed-file changes. No sync conflicts possible.
- **PC ↔ Threadripper**: Full vault sync in both directions. `analyze.py` runs on the
  Threadripper, reads `wiki/`, and writes `wiki/research/` back to PC automatically.

---

## 1. Install Syncthing

**Mac**
```bash
brew install syncthing
brew services start syncthing
```

**PC (Windows)**
```powershell
winget install Syncthing.Syncthing
```
Then add Syncthing to Windows startup: Task Scheduler or the Syncthing tray app.

**Threadripper (headless Linux)**
```bash
# Debian/Ubuntu
sudo apt install syncthing

# Enable as a user service
systemctl --user enable syncthing
systemctl --user start syncthing
```

---

## 2. Open the Web UI

On each machine, navigate to `http://127.0.0.1:8384` in a browser.

For the Threadripper (headless), forward the port over SSH first:
```bash
ssh -L 8384:localhost:8384 user@threadripper-ip
```
Then open `http://127.0.0.1:8384` locally.

---

## 3. Exchange Device IDs

On each machine: **Actions → Show ID** — copy the device ID (a long alphanumeric string).

On the PC web UI:
- **Add Remote Device** → paste Mac's device ID → name it `Macbook`
- **Add Remote Device** → paste Threadripper's device ID → name it `Threadripper`

The remote machines will show a prompt to accept the connection — approve it.

---

## 4. Configure the Mac → PC Raw Folder

### On the Mac
1. **Add Folder** in the Syncthing web UI
2. **Folder Path**: point to the `raw/` directory inside your vault clone on the Mac
   - Example: `/Users/yourname/personal-brain/raw`
3. **Folder Type**: `Send Only`
4. **Share with**: `PC Hub` (the device you added in step 3)
5. Save

### On the PC
When the Mac's share request arrives, accept it and:
1. **Folder Path**: `C:\Code\Active\personal-brain\raw`
2. **Folder Type**: `Receive Only`
3. Save

> **Why Receive Only on PC?** The PC's `ingest.py` moves files within `raw/` (to
> `raw/assets/processed/`). Making PC receive-only for this share prevents those local
> moves from being interpreted as deletions and synced back to the Mac.

### Add a `.stignore` on the Mac
Inside the Mac's `raw/` folder, create `.stignore` to prevent the Mac from ever
pushing PC-generated metadata back even if the folder type changes later:

```
assets/
```

---

## 5. Configure the PC ↔ Threadripper Full Vault Sync

This lets `analyze.py` on the Threadripper read the full wiki and write research notes
back to the PC.

### On the PC
1. **Add Folder**
2. **Folder Path**: `C:\Code\Active\personal-brain` (vault root)
3. **Folder Type**: `Send & Receive`
4. **Share with**: `Threadripper`
5. Add `.stignore` at vault root on PC to exclude git internals from sync:
   ```
   .git/
   __pycache__/
   *.pyc
   ```

### On the Threadripper
Accept the share and set:
1. **Folder Path**: `/home/yourname/personal-brain` (or wherever you want the vault)
2. **Folder Type**: `Send & Receive`

---

## 6. Verify

**Mac → PC path:**
1. Drop any `.txt` file into the Mac's `raw/` folder
2. Within a few seconds it should appear in `C:\Code\Active\personal-brain\raw\` on PC
3. If `ingest.py` is running on PC, the file will be processed and archived to
   `raw/assets/processed/`

**PC → Threadripper path:**
1. Confirm `wiki/` contents appear on the Threadripper after Level 0 processes something
2. Run `analyze.py` on Threadripper — its output in `wiki/research/` should sync back to PC

---

## 7. Environment Variables

Both machines running `ingest.py` or `analyze.py` need their API keys set:

**PC (PowerShell profile or System env)**
```powershell
$env:GEMINI_API_KEY  = "..."
$env:ANTHROPIC_API_KEY = "..."
```

**Threadripper (bash profile or systemd service env)**
```bash
export ANTHROPIC_API_KEY="..."
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Files appear on PC but ingest doesn't fire | Check `ingest.py` is running; check Windows Defender isn't blocking watchdog |
| Syncthing shows "Out of Sync" on PC | PC is Receive Only — this is expected when local moves happen; click "Revert Local Changes" only if you want to undo PC-side changes |
| Threadripper vault is stale | Check Syncthing service is running: `systemctl --user status syncthing` |
| Port 8384 unreachable on Threadripper | Use SSH tunnel: `ssh -L 8384:localhost:8384 user@host` |
