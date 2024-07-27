import random
import json
import torch
from utils.model import NeuralNet
from utils.nltk_utils import bag_of_words, tokenize

class ChatBot():
    def __init__(self, path_intents, path_data):
        # Checking cuda
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.load_intents(path_intents)
        self.load_data(path_data)
        self.create_model()
        
    
    def load_intents(self, path_intents):
        # Open file json
        with open(path_intents, 'r') as f:
            self.intents = json.load(f)
    
    def load_data(self, path_data):
        # Load file data of result training
        data = torch.load(path_data)

        # Taking the parameter from data
        self.input_size = data['input_size']
        self.hidden_size = data['hidden_size']
        self.output_size = data['output_size']
        self.all_words = data['all_words']
        self.tags = data['tags']
        self.model_state = data['model_state']
    
    def create_model(self):
        # Create model
        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)

        # Load model
        self.model.load_state_dict(self.model_state)
        self.model.eval()
    
    def get_response(self, setence):
        # Tokenizing the setence
        setence = tokenize(setence)
        
        # Getting bag of words from setence
        x = bag_of_words(setence, self.all_words)
        
        # Reshape the bag of words
        x = x.reshape(1, x.shape[0])    # 1 -> row; x.shape[0] -> column
        
        # Create data for predict
        x = torch.from_numpy(x)
        
        # Predict data
        output = self.model(x)
        
        # Getting the result of predict
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]
        
        # Calculate the probablity of predict
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        
        # Checking the probability to threshold
        threshold = 0.5
        print(f'tag : {tag}')
        print(f'prob : {prob.item()}')
        if prob.item() > threshold:    
            # Getting response from tag
            for intent in self.intents['intents']:
                if tag == intent['tag']:
                    # Pick random response from intent
                    response = random.choice(intent['responses'])
                    return response
        # If not >= threshold
        else:
            return "I do not understand...."
        

