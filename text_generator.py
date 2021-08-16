import tensorflow as tf
import pickle
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')
import logging
tf.get_logger().setLevel('INFO')
tf.get_logger().setLevel('WARNING')
tf.get_logger().setLevel('ERROR')

def load_model_tokenizer():
	model = load_model('textgen_model.h5')
	with open('textgen_tokenizer.pickle', 'rb') as handle:
		tokenizer = pickle.load(handle)
	return model, tokenizer

def predict(x,model):
	return model.predict_classes(x)

def generate_text_sequence(seed_text, n_words):
	model,tokenizer=load_model_tokenizer()
	text_seq_length=5
	text=[]
	for _ in range(n_words):
		encoded=tokenizer.texts_to_sequences([seed_text])[0]
		encoded=pad_sequences([encoded],maxlen=text_seq_length, truncating='pre')
		y_predic=predict(encoded,model)
		# y_predic=np.argmax(model.predict(encoded), axis=-1)
		predicted_word=''
		for word,index in tokenizer.word_index.items():
			if index==y_predic:
				predicted_word=word
				break
		seed_text=seed_text+" "+predicted_word
		text.append(predicted_word)
	return ' '.join(text)


def get_output_sequence(seed_text):
	output=generate_text_sequence(seed_text,10)
	output_text=('{"text":"'+seed_text+" "+output+'"}')
	return output_text