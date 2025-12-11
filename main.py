import os
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("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"))

SYSTEM_PROMPT = (
    "Eres un asistente de WhatsApp para una agencia de marketing digital. "
    "Respondes siempre de forma cercana, clara y corta (máximo 3-4 frases). "
    "Tu objetivo es ayudar, orientar y mantener un tono humano y natural."
)

@app.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
):
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": Body},
        ]
    )

    reply_text = completion.choices[0].message.content.strip()

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>"""

    return PlainTextResponse(content=twiml_response, media_type="application/xml")
