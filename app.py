from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from utils.chatbot import ChatBot

PATH_INTENTS = 'data/intents_3.json'
PATH_DATA = 'model/meta/data_nn.pth'

app = Flask(__name__)
chatbot = ChatBot(PATH_INTENTS, PATH_DATA)


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
    
    print(f'\n Checking the request\n')
    if request.form:  
        print(f'\n There is request\n')
        setence = request.form['send-chat']          
        response = chatbot.get_response(setence)
        data['setence'] = setence
        print(f'\n setence : {setence}\n')
        data['response'] = response
        print(f'\n response : {response}\n')
    return render_template("pages/chat.html", data=data)

if __name__ == '__main__':
	app.run(debug=True)