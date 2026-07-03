import requests
import os
from datetime import datetime


def main(context):
    GSHEET_REFRESH_TOKEN = os.environ.get("GSHEET_REFRESH_TOKEN")
    GSHEET_CLIENT_ID = os.environ.get("GSHEET_CLIENT_ID")
    GSHEET_CLIENT_SECRET = os.environ.get("GSHEET_CLIENT_SECRET")
    SHEET_ID = os.environ.get("SHEET_ID")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    final_output_text = ""
    
    req_body = context.req.body
    # {"hasan": "true", "amount": "1", "item": "e", "arash": "true", "mehdi": "true", "payer": "Arash"}
    amount = req_body.get("amount")
    item = req_body.get("item")
    payer = req_body.get("payer")
    arash = req_body.get("arash")
    hasan = req_body.get("hasan")
    mehdi = req_body.get("mehdi")

    hasan_chat_id = "606109067"
    arash_chat_id = "160720011"
    mehdi_chat_id = "493805697"


    all_chat_ids = [hasan_chat_id, arash_chat_id, mehdi_chat_id]
    br = "\n"


    the_date = datetime.now().strftime("%m/%d/%Y")

    try:
        token_res = requests.post("https://oauth2.googleapis.com/token", data={
            "client_id": GSHEET_CLIENT_ID,
            "client_secret": GSHEET_CLIENT_SECRET,
            "refresh_token": GSHEET_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }).json()
        access_token = token_res.get("access_token")

        append_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/Accounts!A:K:append?valueInputOption=USER_ENTERED"
        
        row_values = [
            the_date, 
            item, 
            payer, 
            amount,
            False, 
            False, 
            mehdi, 
            arash, 
            hasan
        ]
        
        gs_res = requests.post(
            append_url, 
            headers={"Authorization": f"Bearer {access_token}"},
            json={"values": [row_values]}
        ).json()

        if "updates" in gs_res:
            row_ref = gs_res["updates"]["updatedRange"].split("!")[-1].split(":")[-1].replace("A", "").replace("K", "")
            names_and_emojis = {"Farhood": " 🦁Farhood", "Mehdi" : " 🎬Mehdi", "Arash" : " 🦉Arash", "Hasan" : " 😴Hasan"}
            payer = names_and_emojis.get(answer.get('payer'))
            final_output_text = (
                f"❇️ Recorded!{br}Input: \"{text}\"{br}{br}"
                f"💸 Amount: {answer.get('amount')}{br}"
                f"ℹ️ Category: {answer.get('itemsCategory')}{br}"
                f"😎 Payer: {payer}{br}"
                f"🧮 Splitters:"
            )
            if mehdi: final_output_text += " 🎬Mehdi"
            if arash: final_output_text += " 🦉Arash"
            if hasan: final_output_text += " 😴Hasan"
            
            final_output_text += f"{br}➡️Row Number: {row_ref}{br}📅Date: {the_date}"
        else:
            final_output_text = f"Error: Sheet update failed.{br}Data: {json.dumps(answer)}"

    except Exception as e:
        final_output_text = f"System Error: {str(e)}"

    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for uid in all_chat_ids:
        # requests.post(tg_url, json={"chat_id": uid, "text": final_output_text})
        pass

    
    
    requests.post(tg_url, json={"chat_id": hasan_chat_id, "text": req_body})
    requests.post(tg_url, json={"chat_id": hasan_chat_id, "text": final_output_text})
    
    return context.res.json({"status": "ok"})
