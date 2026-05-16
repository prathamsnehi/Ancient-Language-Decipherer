Start local server:

```bash
source .venv/bin/activate
uvicorn app:app --port 8000
```

Tunnel to public internet using ngrok:

```bash
ngrok http 8000
```

Done
