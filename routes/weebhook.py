from flask import Blueprint, request, jsonify, Response
from dotenv import load_dotenv
import os

load_dotenv()

weebhook_router = Blueprint('weebhook', __name__)

@weebhook_router.route('/weebhook', methods=['GET'])
def validateToken():
  # cuando el endpoint este registrado como webhook, debe mandar de vuelta
  # el valor de 'hub.challenge' que recibe en los argumentos de la llamada
  if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
      return "Verification token mismatch", 403
    return request.args["hub.challenge"], 200

  return "Nothing to do", 200


@weebhook_router.route('/weebhook', methods=['POST'])
def tafic():
  # endpoint para procesar los mensajes que llegan

  data = request.get_json()
  log(data)  # logging, no necesario en produccion

  inteligente = False

  if data["object"] == "page":

    for entry in data["entry"]:
      for messaging_event in entry["messaging"]:

        if messaging_event.get("message"):  # alguien envia un mensaje
          # el facebook ID de la persona enviando el mensaje
          sender_id = messaging_event["sender"]["id"]
          print("sender: ",recipient_id)
          # el facebook ID de la pagina que recibe (tu pagina)
          recipient_id = messaging_event["recipient"]["id"]
          print("page: ",recipient_id)
          # el texto del mensaje
          message_text = messaging_event["message"]["text"]
          print("text: ",recipient_id)

          send_message(sender_id, "Hola")

    return "ok", 200


def send_message(recipient_id, message_text):

  log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

  params = {
    "access_token": os.environ["PAGE_ACCESS_TOKEN"]
  }
  headers = {
    "Content-Type": "application/json"
  }
  data = json.dumps({
    "recipient": {
      "id": recipient_id
    },
    "message": {
      "text": message_text
    }
  })
  r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
  if r.status_code != 200:
    log(r.status_code)
    log(r.text)


def log(message):  # funcion de logging para heroku
  print(str(message))
  sys.stdout.flush()