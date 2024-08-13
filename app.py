import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from utils.chatbot import ChatBot
from model.Message import Message
from model.Conversation import Conversation
from model.User import User
from datetime import timedelta
from urllib.parse import urlparse

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
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

chatbot = ChatBot(app.config['PATH_INTENTS'], app.config['PATH_DATA'])
message = Message(app.config['DATABASE_HOST'], app.config['DATABASE_USER'], app.config['DATABASE_PASS'], app.config['DATABASE_NAME'])
conversation = Conversation(app.config['DATABASE_HOST'], app.config['DATABASE_USER'], app.config['DATABASE_PASS'], app.config['DATABASE_NAME'])
user = User(app.config['DATABASE_HOST'], app.config['DATABASE_USER'], app.config['DATABASE_PASS'], app.config['DATABASE_NAME'])

# Home Page
@app.route("/")
@app.route("/index")
def index():
    data = {
        'page' : 'Home',
        'current_page' : 'home',
    }
    return render_template("pages/index.html", data=data)

# Login Page
@app.route("/login", methods=['GET'])
def login():
    data = {
        'page' : 'Login',
        'current_page' : 'login',
    }
    return render_template("pages/login.html", data=data)

# Login Process
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

# Regsiter Page
@app.route("/register", methods=['GET'])
def register():
    data = {
        'page' : 'Register',
        'current_page' : 'register',
    }
    
    return render_template("pages/register.html", data=data)

# Regist Process
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


# Chat Page
@app.route("/chat", methods=['GET'])
@app.route("/chat/<int:conv>", methods=['GET'])
def chat(conv=None):
    data = {
        'page' : 'Chat',
        'current_page' : 'chat',
        'user' : False,
        'now_conversation' : False,
        'active_conversations' : False,
        'archived_conversations' : False
    }
    user_id = session.get("user_id")
    if user_id != None:
        data['user'] = user.get_user_by_id(user_id)
        data['active_conversations'] = conversation.get_all_conversation('active', user_id)
        data['archived_conversations'] = conversation.get_all_conversation('archived', user_id)
        print(f"\n data['active_conversations'] : {data['active_conversations']}")
        
    print(f'\n conv : {conv}')
    print(f'\n user_id : {user_id} \n\n')
    # if not session.get("user_id"):
    
    if conv != None:
        if user_id == None:
            return redirect("/login")
        
        data['now_conversation'] = conversation.get_conversation(conv, user_id)
        data['messages'] = message.get_all_messages(conv)
  
    return render_template("pages/chat.html", data=data)

# Get Response
@app.route("/get")
def get_bot_response():
    user_message = request.args.get('msg')
    response = chatbot.get_response(user_message)
    conversation_id = int(request.args.get('conv', None))
    
    print(f'\n conversation_id: {conversation_id} \n\n')
    if conversation_id > 0:
        message.insert_message(conversation_id, 'user', user_message)
        message.insert_message(conversation_id, 'bot', response)

    return response

# New Conversation
@app.route("/new")
def add_conv():
    user_id = session.get("user_id")
    print(f'\n user_id : {user_id}')
    print(f'\n type(user_id) : {type(user_id)}')
    
    if user_id == None:
        return redirect("/login")
    
    status = conversation.create_conversation(user_id)
    if status == True:
        new_conv = conversation.get_latest_conversation(user_id)[0]
        return redirect(f"/chat/{new_conv}")
    else:
        return redirect('/')

# Rename Conversation
@app.route("/chat/<int:conv>/edit", methods=['POST'])
def edit_conv(conv):
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
        
    title = request.form.get('title', None)
    if title != None:
        conversation.edit_conversation(conv, user_id, title)
        print(f'\nSuccess edit title\n\n')
        
    return redirect(f'/chat/{conv}')

# Archive Conversation
@app.route("/chat/<int:conv>/archive", methods=['GET'])
def archive_conv(conv):
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    
    conversation.end_conversation(conv, user_id)
    print(f'\nSuccess archive conversation id={conv}\n\n')
    conv = conversation.get_latest_conversation(user_id, 'active')[0]
    
    previous_path = urlparse(request.referrer).path
    path_segments = previous_path.split('/')
    path_first_segments = path_segments[1] if len(path_segments) > 1 else None
    conv_id_before = path_segments[2] if len(path_segments) > 2 else None
    
    print(f' \n A___ \n')
    if path_first_segments == 'chat' and conv_id_before != None:
        print(f' \n B___ \n')
        conv_before = conversation.get_conversation(conv_id_before, user_id)
        if conv_before[4] == None:
            print(f' \n C___ \n')
            return redirect(f'/{path_first_segments}/{conv_id_before}')
        else:
            print(f' \n D___ \n')
            return redirect(f'/chat/{conv}')
    elif path_first_segments == 'setting':
        print(f' \n E___ \n')
        return redirect(f'/{path_first_segments}')
    else:
        print(f' \n F___ \n')
        return redirect(previous_path)
    
# Unarchive Conversation
@app.route("/chat/<int:conv>/unarchive", methods=['GET'])
def unarchive_conv(conv):
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    
    conversation.start_conversation(conv, user_id)
    print(f'\nSuccess Unarchive conversation id={conv}\n\n')
    conv = conversation.get_latest_conversation(user_id, 'active')[0]
    
    previous_path = urlparse(request.referrer).path
    path_segments = previous_path.split('/')
    path_first_segments = path_segments[1] if len(path_segments) > 1 else None
    conv_id_before = path_segments[2] if len(path_segments) > 2 else None
    
    print(f' \n A___ \n')
    if path_first_segments == 'chat' and conv_id_before != None:
        print(f' \n B___ \n')
        conv_before = conversation.get_conversation(conv_id_before, user_id)
        if conv_before[4] == None:
            print(f' \n C___ \n')
            return redirect(f'/{path_first_segments}/{conv_id_before}')
        else:
            print(f' \n D___ \n')
            return redirect(f'/chat/{conv}')
    elif path_first_segments == 'setting':
        print(f' \n E___ \n')
        return redirect(f'/{path_first_segments}')
    else:
        print(f' \n F___ \n')
        return redirect(previous_path)

# Delete Conversation
@app.route("/chat/<int:conv>/delete", methods=['POST'])
def delete_conv(conv):
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    
    delete = request.form.get('delete', None)
    if delete != None:
        conversation.delete_conversation(conv, user_id)
        print(f'\nSuccess delete conversation id={conv}\n\n')
        conv = conversation.get_latest_conversation(user_id)[0]
        
        previous_path = urlparse(request.referrer).path
        path_segments = previous_path.split('/')
        path_first_segments = path_segments[1] if len(path_segments) > 1 else None
        conv_id_before = path_segments[2] if len(path_segments) > 2 else None
        
        print(f' \n A___ \n')
        if path_first_segments == 'chat' and conv_id_before != None:
            print(f' \n B___ \n')
            conv_before = conversation.get_conversation(conv_id_before, user_id)
            if conv_before[4] == None:
                print(f' \n C___ \n')
                return redirect(f'/{path_first_segments}/{conv_id_before}')
            else:
                print(f' \n D___ \n')
                return redirect(f'/chat/{conv}')
        elif path_first_segments == 'setting':
            print(f' \n E___ \n')
            return redirect(f'/{path_first_segments}')
        else:
            print(f' \n F___ \n')
            return redirect(previous_path)
        
    return redirect(f'/chat/{conv}')


# Setting Page
@app.route("/setting")
def setting():
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    
    data = {
        'page' : 'Setting',
        'current_page' : 'setting',
        'active_conversations' : conversation.get_all_conversation('active', user_id),
        'archived_conversations' : conversation.get_all_conversation('archived', user_id),
        'all_conversations' : conversation.get_all_conversation('all', user_id),
        'user' : user.get_user_by_id(user_id),
        'now_conversation' : False,
        'archived_chats' : conversation.get_archived_conversations(user_id)
    }
    
    print(f"\n data['active_conversations'] : {data['active_conversations']} \n\n")
    print(f"\n data['now_conversation'] : {data['now_conversation']} \n\n")
    
    return render_template("pages/setting.html", data=data)

# Profile Edit Process
@app.route("/profile/edit", methods=['POST'])
def profile_edit():
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    
    full_name = request.form.get('full_name', None)
    username = request.form.get('username', None)
    email = request.form.get('email', None)
    
    if full_name != None and username != None and email != None:
        status = user.update_user_details(user_id, username, full_name, email)
        if status == True:
            flash("Profile updated successfully.", ['success', 'bottom'])
            return redirect('/setting')
        else:
            flash("Profile update failed.", ['danger', 'bottom'])
            return redirect('/setting')
    else:
        flash("Please fill out the field.", ['warning', 'bottom'])
        return redirect('/setting')

# Passowrd Update Process
@app.route("/profile/update-pass", methods=['POST'])
def update_pass():
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    
    old_password = request.form.get('old_password', None)
    new_password = request.form.get('new_password', None)
    confirm_password = request.form.get('confirm_password', None)
    
    if old_password != None and new_password != None and confirm_password != None:
        result = user.update_user_password(user_id, old_password, new_password, confirm_password)
        if result == True:
            flash("Password updated successfully.", ['success', 'bottom'])
            return redirect('/setting')
        else:
            flash(result, ['danger', 'bottom'])
            return redirect('/setting')
    else:
        flash("Please fill out the field.", ['warning', 'bottom'])
        return redirect('/setting')

            
        


# Archive All Conversation
@app.route("/chat/archive-all", methods=['POST'])
def archive_all_conv():
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    
    conversation.end_all_conversation(user_id)
    print(f'\nSuccess archive all conversations \n\n')
    return redirect(f'/setting')

# Delete All Conversation
@app.route("/chat/delete-all", methods=['POST'])
def delete_all_conv():
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    
    delete = request.form.get('delete', None)
    if delete != None:
        conversation.delete_all_conversation(user_id)
        print(f'\nSuccess delete all conversations \n\n')
        
    return redirect(f'/setting')
    

        

# @app.route("/conv/<int:value>")
# def conversation(value):
#     return f'The value is {value}'


if __name__ == '__main__':
    app.run(debug=True, port=5050)