from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__mumu__)
openai.api_key = os.environ.get("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")

@app.route("/mumu", methods=['POST'])
def mumu():
    gelen_mesaj = request.form.get('Body')
    numara = request.form.get('From')

    # Mumu'nun kişiliği
    sistem_mesaji = "Sen Mumu'sun. Samimi, kısa cevap veren, yardımcı bir WhatsApp asistanısın. Kullanıcı Samsung A34 kullanıyor ve Güzelbahçe'de yaşıyor. Türkçe cevap ver. Emojiyi abartma."

    cevap = openai.ChatCompletion.create(
        model="gpt-4o-mini", # Ucuz ve hızlı
        messages=[
            {"role": "system", "content": sistem_mesaji},
            {"role": "user", "content": gelen_mesaj}
        ]
    )

    yanıt = cevap.choices[0].message.content

    twiml = MessagingResponse()
    twiml.message(yanıt)
    return str(twiml)

if __name__ == "__main__":
    app.run(port=5000)
