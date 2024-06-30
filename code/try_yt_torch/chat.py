import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize


PATH_INTENTS = '../../data/intents.json'
# PATH_MODEL = 'model_torch.h5'
# PATH_METADATA = 'metadata_torch.json'
PATH_DATA = 'data_torch.pth'

# Checking cuda
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Open file json
with open(PATH_INTENTS, 'r') as f:
    intents = json.load(f)

# Load file data of result training
data = torch.load(PATH_DATA)

# Taking the parameter from data
input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']
# print(model_state)

# Create model
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Load model
model.load_state_dict(model_state)
model.eval()

# Create chat bot
bot_name = 'Torch'
print("Let's chat! Type 'quit' to exit")

# Loop the chat bot
while True:
    # Get setence of input user
    setence = input('You: ')
    
    # Break loop if quit
    if setence == 'quit':
        break
    
    # Tokenizing the setence
    setence = tokenize(setence)
    
    # Getting bag of words from setence
    x = bag_of_words(setence, all_words)
    
    # Reshape the bag of words
    x = x.reshape(1, x.shape[0])    # 1 -> row; x.shape[0] -> column
    
    # Create data for predict
    x = torch.from_numpy(x)
    
    # Predict data
    output = model(x)
    
    # Getting the result of predict
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    
    # Calculate the probablity of predict
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    # Checking the probability to threshold
    threshold = 0.25
    print(f'prob : {prob.item()}')
    if prob.item() > threshold:    
        # Getting response from tag
        for intent in intents['intents']:
            if tag == intent['tag']:
                # Pick random response from intent
                response = random.choice(intent['responses'])
                
                # Print the response
                print(f"{bot_name} : {response}\n")
    # If not >= threshold
    else:
        print(f"{bot_name} : I do not understand....\n")
