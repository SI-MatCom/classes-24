
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
import numpy as np


### Parámetros para Random Forest Classifier

# Especifica el número de árboles que se utilizarán en el bosque. Cuantos más árboles, más robusto será el modelo, pero también aumentará el tiempo de entrenamiento
n_estimators = 100

# Controla la aleatoriedad en el algoritmo. Si se establece un valor específico en esta variable, se obtiene resultados reproducibles cada vez que ejecutes el modelo. Esto es útil para fines de depuración y comparación de modelos.
random_state = 42


def classifier(change_function, dataset, labels):
    """
    Returns the precision, recall and F1 metrics of the Random Forest model to predict its label
    
    Args:
        - change_function (function) : Function to obtain the representation of each data. It returns a list of integers or a list of list of integers. 
        - dataset (list) : Dataset.
        - labels (list): List of labels for each element of the dataset. Its size matches the dataset.

    Return:
        - str
    
    """

    global random_state
    global n_estimators
    
    # Aplicar la función de cambio a cada elemento del conjunto de datos y aplanar los resultados
    features = []
    for d1, d2, _ in dataset:
        new_representation = change_function(d1, d2)
        features.append(np.concatenate([x.flatten() for x in new_representation]))
    
    # Dividir el conjunto de datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Inicializar el clasificador Random Forest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Entrenar el modelo
    clf.fit(X_train, y_train)
    
    # Predecir las etiquetas en el conjunto de prueba
    y_pred = clf.predict(X_test)

    metrics = \
        "\tAccuracy: {:.2f}".format(accuracy_score(y_test, y_pred)) + \
        "\n\tRecall: {:.2f}".format(recall_score(y_test, y_pred, average='weighted')) + \
        "\n\tF1 Score: {:.2f}".format(f1_score(y_test, y_pred, average='weighted'))
    
    return metrics