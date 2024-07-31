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

@app.route("/chat", methods=['GET', 'POST'])
def chat():
	data = {
		'page' : 'Chat',
		'current_page' : 'chat'
	}
	
	data['messages'] = message.get_all_messages()
	print(f"\n messages : {data['messages']}\n")
	
	print(f'\n Checking the request\n')
	# if request.form:  
	# 	print(f'\n There is request\n')
	# 	user_message = request.form['send-chat']   
	# 	conversation_id = 1  # Contoh ID percakapan
		
	# 	# Insert user message
	# 	message.insert_message(conversation_id, 'user', user_message)
		
	# 	# Process user message
	# 	response = chatbot.get_response(user_message)

	# 	# Insert bot response
	# 	message.insert_message(conversation_id, 'bot', response)
		
		
	# 	data['user_message'] = user_message
	# 	print(f'\n user_message : {user_message}\n')
	# 	data['response'] = response
	# 	print(f'\n response : {response}\n')
  
	
	return render_template("pages/chat.html", data=data)

@app.route("/get")
def get_bot_response():
    user_message = request.args.get('msg')
    return chatbot.get_response(user_message)

if __name__ == '__main__':
	app.run(debug=True, port=5050)