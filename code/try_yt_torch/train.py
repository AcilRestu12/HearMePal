import json
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltk_utils import tokenize, stem, bag_of_words
from model import NeuralNet

# Open file json
with open('torch/intents.json', 'r') as f:
    intents = json.load(f)
    
# Define list
all_words = []  # Setence
tags = []       # Tags of setence
xy = []         # X and Y of setence

# Getting setence, tags, xy
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))
    
# Stemming
ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]       

# Remove duplicate word
all_words = sorted(set(all_words))      
tags = sorted(set(tags)) 
               
# print(tags)

# Define train data
x_train = []
y_train = []
for (pattern_setence, tag) in xy:
    # Getting the feature
    bag = bag_of_words(pattern_setence, all_words)
    x_train.append(bag)
    
    # Getting label from index of tag
    label = tags.index(tag)
    y_train.append(label)   # CrossEntropyLoss
    
# Convert to array
x_train = np.array(x_train)
y_train = np.array(y_train)


# Create custom class dataset
class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples
    
# Define Hyperparameter
batch_size = 8
hidden_size = 8
input_size = len(x_train[0])
output_size = len(tags)
learning_rate = 0.001
num_epochs = 1000
# print(input_size, len(all_words))
# print(output_size, tags)

# Create dataset
dataset = ChatDataset()
# train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=2)
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)
# train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers = 2, persistent_workers=True)

# Checking cuda
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Create model
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss & optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
# Training model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device, dtype=torch.int64)
        
        # Forward
        outputs = model(words)
        loss = criterion(outputs, labels)
        
        # Backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    # Print loss per 100 epoch
    if (epoch + 1) % 100 == 0:
        print(f'epoch : {epoch+1}/{num_epochs}, loss={loss.item():.4f}')

# Print final loss when training done
print(f'final loss, loss={loss.item():.4f}')

# Save data
data = {
    'model_state' : model.state_dict(),
    'input_size' : input_size,
    'output_size' : output_size,
    'hidden_size' : hidden_size,
    'all_words' : all_words,
    'tags' : tags,
}

# Save file of data
FILE = 'torch/data.pth'
torch.save(data, FILE)
print(f'Training complete. file saved to {FILE}')

