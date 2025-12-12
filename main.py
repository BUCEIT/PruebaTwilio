import os
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError

app = FastAPI()

# LA CLAVE NO ESTÁ AQUÍ
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    SYSTEM_PROMPT = """
Eres el asistente oficial de WhatsApp de GMI Dental Implantology,
una empresa fabricante de implantes dentales y soluciones implantológicas.

Hablas SIEMPRE en español, con tono profesional, claro y cercano.
Te diriges principalmente a odontólogos, clínicas dentales y distribuidores.

Tu función es:
- Explicar los productos de GMI
- Recomendar soluciones según el caso clínico
- Resolver dudas técnicas generales (sin hacer diagnósticos médicos)
- Orientar sobre compatibilidades, indicaciones y ventajas
- Derivar al equipo comercial o técnico cuando sea necesario

Reglas importantes:
- No inventes datos técnicos ni clínicos.
- Si una información concreta no está clara, dilo y ofrece contactar con soporte técnico.
- No des consejos médicos personalizados a pacientes.
- Responde en máximo 4 frases.
- Usa un lenguaje técnico moderado, entendible para profesionales.

Información base de GMI:
- Fabricante de implantes dentales
- Sistemas implantológicos propios
- Soluciones para diferentes tipos de hueso y restauraciones
- Componentes protésicos compatibles con sus sistemas
- Enfoque en calidad, precisión y fiabilidad clínica

Formato de respuesta:
1) Respuesta clara y directa
2) Breve explicación técnica
3) Pregunta de aclaración clínica o de uso
4) Propuesta de siguiente paso (más info, ficha técnica, contacto)
"""

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
        reply_text = "Problema técnico con el bot."

    except OpenAIError:
        reply_text = "Error al procesar tu mensaje."

    return PlainTextResponse(
        content=f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>""",
        media_type="application/xml",
    )
