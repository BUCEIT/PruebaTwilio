from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
):
    """
    Webhook que llama Twilio cuando llega un WhatsApp.
    From = número del usuario
    Body = texto que ha escrito el usuario
    """
    print(f"Mensaje de {From}: {Body}")

    # Aquí de momento solo vamos a hacer un "eco"
    reply_text = f"Has dicho: {Body}"

    # Twilio espera una respuesta en formato XML (TwiML)
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>"""

    return PlainTextResponse(content=twiml_response, media_type="application/xml")
