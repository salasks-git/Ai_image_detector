# Step 4: Launching & Troubleshooting

Use this document to start your local engine and fix minor bugs if they present themselves during live testing.

---

## Pre-Launch Checklist

1. Ensure `tools.py` and `app.py` reside in the **same folder**.
2. Activate your virtual environment:

```bash
source .venv/bin/activate
```

3. Export your Gemini API key (replace with your actual key):

```bash
export GEMINI_API_KEY="your-api-key-here"
```

> To make this permanent, add the export line to your `~/.zshrc` or `~/.bashrc`.

---

## Launch

From the project directory, run:

```bash
streamlit run app.py
```

### Expected Output

On success, your terminal will print:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Your default browser should open automatically. If it doesn't, navigate to `http://localhost:8501` manually.

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'nest_asyncio'` | Dependencies not installed | `pip install nest_asyncio` |
| `ModuleNotFoundError: No module named 'google.genai'` | Gemini SDK missing | `pip install google-genai` |
| `ModuleNotFoundError: No module named 'streamlit'` | Streamlit not installed | `pip install streamlit` |
| `google.api_core.exceptions.InvalidArgument` | API key is empty or invalid | Re-run `export GEMINI_API_KEY="..."` with a valid key |
| `RuntimeError: This event loop is already running` | `nest_asyncio` not installed | `pip install nest_asyncio` — it must be imported before asyncio (already handled in `app.py`) |
| `PermissionError` writing `ela_heatmap.png` | CWD is read-only | Make sure you run `streamlit` from the project folder where you have write access |
| App loads but analysis hangs | Network issue reaching Gemini API | Check your internet connection; verify your API key has quota remaining |

### Quick Fix: Reinstall All Dependencies

If multiple modules are missing, reinstall everything from `01-setup.md`:

```bash
pip install google-genai streamlit pillow nest_asyncio
```

---

## Stopping the Server

Press `Ctrl + C` in the terminal to stop Streamlit.