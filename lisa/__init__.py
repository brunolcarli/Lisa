import os
import nltk
import spacy

# TODO mover esse download para outro local posteriormente

# Baixa pacotes do nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# baixa pacotes do spacy
os.system('python -m spacy download pt')

# printa um ascii art bonitão xD
lisa_api = r'''
====================
╦  ╦╔═╗╔═╗  ╔═╗╔═╗╦
║  ║╚═╗╠═╣  ╠═╣╠═╝║
╩═╝╩╚═╝╩ ╩  ╩ ╩╩  ╩
====================
'''
print(lisa_api)
