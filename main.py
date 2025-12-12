import os
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError

app = FastAPI()

# Leer la API key desde la variable de entorno
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Falta OPENAI_API_KEY en Railway → Service → Variables (production)"
    )

client = OpenAI(api_key=api_key)

# Prompt del sistema: descripción del rol del bot
SYSTEM_PROMPT = (
    "Eres el asistente oficial de WhatsApp de GMI Dental Implantology, "
    "fabricante de implantes dentales y soluciones implantológicas. "
    "Hablas siempre en español, con tono profesional, claro y cercano, "
    "dirigido a odontólogos, clínicas dentales y distribuidores. "
    "Tu función es explicar los productos de GMI, sus indicaciones generales, "
    "ventajas y compatibilidades, sin dar diagnósticos médicos. "
    "Si falta información o es un caso clínico concreto, propones contactar "
    "con el equipo técnico o comercial. Respondes en un máximo de 4 frases."
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
            ],
            max_output_tokens=220,
        )

        reply_text = response.output_text.strip()

    except RateLimitError:
        reply_text = (
            "Ahora mismo he alcanzado el límite de uso de la IA. "
            "Inténtalo de nuevo en unos minutos."
        )

    except AuthenticationError:
        reply_text = (
            "Hay un problema interno con la configuración de la IA. "
            "Por favor, contacta con el administrador."
        )

    except OpenAIError:
        reply_text = (
            "He tenido un error al procesar tu mensaje. "
            "¿Puedes intentarlo otra vez?"
        )

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>"""

    return PlainTextResponse(content=twiml, media_type="application/xml")
