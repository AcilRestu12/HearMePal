import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from utils.chatbot import ChatBot
from model.Message import Message
from model.Conversation import Conversation
from model.User import User

# Memuat file .env
load_dotenv()

app = Flask(__name__)

# Menggunakan variabel dari file .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PATH_INTENTS'] = os.getenv('PATH_INTENTS')
app.config['PATH_DATA'] = os.getenv('PATH_DATA')
app.config['DATABASE_HOST'] = os.getenv('DATABASE_HOST')
app.config['DATABASE_USER'] = os.getenv('DATABASE_USER')
app.config['DATABASE_PASS'] = os.getenv('DATABASE_PASS')
app.config['DATABASE_NAME'] = os.getenv('DATABASE_NAME')

chatbot = ChatBot(app.config['PATH_INTENTS'], app.config['PATH_DATA'])
message = Message(app.config['DATABASE_HOST'], app.config['DATABASE_USER'], app.config['DATABASE_PASS'], app.config['DATABASE_NAME'])
conversation = Conversation(app.config['DATABASE_HOST'], app.config['DATABASE_USER'], app.config['DATABASE_PASS'], app.config['DATABASE_NAME'])
user = User(app.config['DATABASE_HOST'], app.config['DATABASE_USER'], app.config['DATABASE_PASS'], app.config['DATABASE_NAME'])

@app.route("/")
@app.route("/index")
def index():
    data = {
        'page' : 'Home',
        'current_page' : 'home',
    }
    return render_template("pages/index.html", data=data)

@app.route("/chat", methods=['GET'])
@app.route("/chat/<int:conv>", methods=['GET'])
def chat(conv=None):
    if not session.get("user_id"):
        return redirect("/login")
    
    print(session.get("user_id"))
    
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
        'all_conversations' : conversation.get_all_conversation('active'),
        'now_conversation' : False
    }
    return render_template("pages/setting.html", data=data)

@app.route("/login", methods=['GET'])
def login():
    data = {
        'page' : 'Login',
        'current_page' : 'login',
    }
    return render_template("pages/login.html", data=data)

@app.route("/login", methods=['POST'])
def login_user():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    
    result = user.login(email, password)
    print(f"\n {type(result)}\n\n")
    if isinstance(result, tuple):
        session["user_id"] = result[0]
        print(f"\n {session['user_id']}\n\n")
        flash('Login successfully.', ['success', 'bottom'])
        return redirect('/chat')
    else:
        print(f'\n {result}\n\n')
        flash(result, ['warning', 'bottom'])
        return redirect('/register')

@app.route("/register", methods=['GET'])
def register():
    data = {
        'page' : 'Register',
        'current_page' : 'register',
    }
    
    return render_template("pages/register.html", data=data)

@app.route("/register", methods=['POST'])
def regist():
    full_name = request.form.get('full_name', None)
    username = request.form.get('username', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    confirm_password = request.form.get('confirm_password', None)
    
    result = user.register_user(username, email, full_name, password, confirm_password)
    if result == True:
        print(f'\n User {username} berhasil dibuat\n\n')
        flash('Account created successfully.', ['success', 'top'])
        return redirect('/login')
    else:
        print(f'\n User {username} gagal dibuat\n\n')
        flash(result, ['warning', 'top'])
        return redirect('/register')
    
@app.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('user_id', None)
    return redirect(url_for('login'))



    

        

# @app.route("/conv/<int:value>")
# def conversation(value):
#     return f'The value is {value}'


if __name__ == '__main__':
    app.run(debug=True, port=5050)