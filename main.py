from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError

app = FastAPI()

# ❗ Pega aquí tu API key real SIN ESPACIOS NI ASTERISCOS
client = OpenAI(api_key="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")

SYSTEM_PROMPT = (
    "Eres un asistente de WhatsApp para una agencia de marketing digital. "
    "Respondes siempre con un tono cercano, claro y profesional, en mensajes "
    "cortos (3-4 frases máximo). Si la pregunta es ambigua, pides aclaración."
)

@app.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
):

    try:
        # 👉 API NUEVA (OpenAI Responses API)
        response = client.responses.create(
            model="gpt-5.1",
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": Body
                }
            ]
        )

        reply_text = response.output_text.strip()

    except RateLimitError:
        reply_text = (
            "Ahora mismo he superado el límite de uso del modelo de IA. "
            "Inténtalo de nuevo en unos minutos."
        )

    except AuthenticationError:
        reply_text = (
            "Hay un problema con la clave de acceso a la IA. "
            "Por favor, contacta con soporte técnico."
        )

    except OpenAIError:
        reply_text = (
            "He tenido un problema al procesar tu mensaje. "
            "¿Puedes volver a intentarlo?"
        )

    # 👉 Twilio requiere respuestas en formato TwiML
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>"""

    return PlainTextResponse(content=twiml_response, media_type="application/xml")
