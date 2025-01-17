
import spacy
nlp = spacy.load("en_core_web_sm")

"""
La biblioteca spaCy permite filtrar los tokens de un documento luego de tokenizarlo, para obtener aquellos que realmente interesan.
Esta es la lista que brinda la biblioteca, con su significado respectivo:
- ADJ: adjetivo
- ADP: aposición
- ADV: adverbio
- AUX: auxiliar
- CCONJ: conjunción coordinante
- DET: determinante
- INTJ: interjección
- NOUN: sustantivo
- NUM: número
- PARTE: partícula
- PRON: pronombre
- PROPN: nombre propio
- SCONJ: conjunción subordinante
- SYMBOL: símbolo
- VERB: verbo
- X: otro
"""

# Lista de etiquetas a utilizar para filtrar los tokens de los documentos procesados
tag_list = ['ADJ', 'NOUN', 'VERB', 'PROPN']

def tokenize(text, special_tokens=['and', 'or', 'not', '(', ')', '&', '~', '|']):
    """
    Tokenize and select text tokens

    Args:
    - text : str
        Document.
    - special_tokens : [str]
        Special tokens that will never be deleted. By default: ['and', 'or', 'not', '(', ')', '&', '~', '|'].

    Return:
    - list<str>

    """
    global tag_list

    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.text.isalpha() or token.lemma_ in special_tokens: # or token.pos_ in tag_list 
            tokens.append(token.lemma_)

    return tokens

    
