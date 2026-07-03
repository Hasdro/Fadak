import requests
import os


def main(context):
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    
    req_body = context.req.body
    hasan_chat_id = "606109067";
    requests.post(tg_url, json={"chat_id": hasan_chat_id, "text": req_body})
    
    return context.res.json({"status": "ok"})
