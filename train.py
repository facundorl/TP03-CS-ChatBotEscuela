import json
import numpy as np
import pickle
import unicodedata
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def normalize_text(text):
    """Normaliza texto: pasa a minúsculas y quita acentos/tildes para tolerar faltas de ortografía (RF-01)."""
    text = text.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


with open(r'C:\Users\facundor632\Desktop\test\TP03-CS-ChatBotEscuela\intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

words = []
classes = []
documents = []
ignore_letters = ['?', '¿', '!', '¡', '.', ',', ':', ';', '(', ')', '"', '-']


for intent in intents['intents']:
    for pattern in intent['patterns']:
        clean_pattern = normalize_text(pattern)
        word_list = [w.strip('?!¡.,:;()"-') for w in clean_pattern.split()]
        word_list = [w for w in word_list if len(w) > 0 and w not in ignore_letters]
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(list(set(words)))
classes = sorted(list(set(classes)))


pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

print(f"Vocabulario ({len(words)} palabras normalizadas):", words[:12], "...")
print(f"Clases ({len(classes)} intenciones):", classes)


training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    word_patterns = doc[0]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

np.random.shuffle(training)
training = np.array(training, dtype=object)

train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))


model = Sequential([
    Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(classes), activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)


model.save('chatbot_model.h5')
print("¡Modelo re-entrenado y guardado con éxito como chatbot_model.h5!")
