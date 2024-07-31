from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from utils.chatbot import ChatBot
from model.Message import Message

PATH_INTENTS = 'data/intents_3.json'
PATH_DATA = 'data/meta/data_nn.pth'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'db_hearmepal'

app = Flask(__name__)
chatbot = ChatBot(PATH_INTENTS, PATH_DATA)
message = Message(DB_HOST, DB_USER, DB_PASS, DB_NAME)

@app.route("/")
@app.route("/index")
def index():
    return render_template("pages/index.html")

@app.route("/chat")
@app.route("/chat/<int:conv>")
def chat(conv=None):
    data = {
        'page' : 'Chat',
        'current_page' : 'chat',
    }

    print(f'conv: {conv}\n\n')
    
    if conv != None:
        data['conversation_id'] = conv
        print(f"data['conversation_id']: {data['conversation_id']}\n\n")
        data['messages'] = message.get_all_messages(conversation_id=conv)
  
    return render_template("pages/chat.html", data=data)

@app.route("/get")
def get_bot_response():
    user_message = request.args.get('msg')
    conversation_id = int(request.args.get('conv'))
 
    print(f'conversation_id: {conversation_id}')
    # Insert user message
    message.insert_message(conversation_id, 'user', user_message)

    # Process user message
    response = chatbot.get_response(user_message)

    # Insert bot response
    message.insert_message(conversation_id, 'bot', response)

    return response


@app.route("/conv/<int:value>")
def conversation(value):
    return f'The value is {value}'


if __name__ == '__main__':
    app.run(debug=True, port=5050)