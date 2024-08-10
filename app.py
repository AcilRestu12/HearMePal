from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from utils.chatbot import ChatBot
from model.Message import Message
from model.Conversation import Conversation

PATH_INTENTS = 'data/intents_3.json'
PATH_DATA = 'data/meta/data_nn.pth'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'db_hearmepal'

app = Flask(__name__)
chatbot = ChatBot(PATH_INTENTS, PATH_DATA)
message = Message(DB_HOST, DB_USER, DB_PASS, DB_NAME)
conversation = Conversation(DB_HOST, DB_USER, DB_PASS, DB_NAME)

@app.route("/")
@app.route("/index")
def index():
    return render_template("pages/index.html")

@app.route("/chat", methods=['GET'])
@app.route("/chat/<int:conv>", methods=['GET'])
def chat(conv=None):
    data = {
        'page' : 'Chat',
        'current_page' : 'chat',
        'all_conversations' : conversation.get_all_conversation('active'),
        'now_conversation' : False
    }

    print(f'conv: {conv}\n\n')
    
    if conv != None:
        data['now_conversation'] = conversation.get_conversation(conv)
        data['messages'] = message.get_all_messages(conv)
  
    return render_template("pages/chat.html", data=data)
    # return data

# Rename Conversation
@app.route("/chat/<int:conv>/edit", methods=['POST'])
def edit_conv(conv):
    user_id = 1
    title = request.form.get('title', None)

    if title != None:
        conversation.edit_conversation(conv, user_id, title)
        print(f'\nSuccess edit title\n\n')
        
    return redirect(f'/chat/{conv}')

# Archive Conversation
@app.route("/chat/<int:conv>/archive", methods=['GET'])
def archive_conv(conv):
    user_id = 1
    conversation.end_conversation(conv, user_id)
    print(f'\nSuccess archive conversation id={conv}\n\n')
    conv = conversation.get_latest_conversation()[0]
    
    return redirect(f'/chat/{conv}')

# Delete Conversation
@app.route("/chat/<int:conv>/delete", methods=['POST'])
def delete_conv(conv):
    user_id = 1
    delete = request.form.get('delete', None)

    if delete != None:
        conversation.delete_conversation(conv, user_id)
        print(f'\nSuccess delete conversation id={conv}\n\n')
        conv = conversation.get_latest_conversation()[0]
        
    return redirect(f'/chat/{conv}')

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


@app.route("/new")
def add_conv():
    user_id = 1
    title = None
    status = conversation.create_conversation(user_id, title)
    if status == True:
        new_conv = conversation.get_latest_conversation()[0]
        return redirect(f"/chat/{new_conv}")
    else:
        return redirect('/')

@app.route("/setting")
def setting():
    data = {
        'page' : 'Setting',
        'current_page' : 'setting',
    }
    return render_template("pages/setting.html", data=data)

        

# @app.route("/conv/<int:value>")
# def conversation(value):
#     return f'The value is {value}'


if __name__ == '__main__':
    app.run(debug=True, port=5050)