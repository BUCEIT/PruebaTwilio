import os
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError

app = FastAPI()

# LA CLAVE NO ESTÁ AQUÍ
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "Eres un asistente de WhatsApp para una agencia de marketing digital. "
    "Respondes claro, cercano y profesional. "
    "Máximo 3-4 frases."
)

@app.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
):
    try:
        response = client.responses.create(
            model="gpt-5.1",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": Body},
            ]
        )

        reply_text = response.output_text.strip()

    except RateLimitError:
        reply_text = "Ahora mismo no puedo responder. Inténtalo más tarde."

    except AuthenticationError:
        reply_text = "Problema interno con la IA."

    except OpenAIError:
        reply_text = "Error al procesar tu mensaje."

    return PlainTextResponse(
        content=f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>""",
        media_type="application/xml",
    )
