Start local server:

```bash
source .venv/bin/activate
cd translation-back
uvicorn main_api:app --port 8000
```

Tunnel to public internet using ngrok:

```bash
ngrok http 8000
```

Done
