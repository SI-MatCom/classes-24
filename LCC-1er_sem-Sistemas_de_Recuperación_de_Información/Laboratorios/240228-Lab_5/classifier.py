

# from classifier import classifier

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import precision_score, f1_score, recall_score

# Parámetros para KNN
n_neighbors = 5

# Parámetros para SVM
C = 1.0
gamma = 0.001

def classifier(model, change_function, dataset, labels):
    """
    Returns the precision, recall and F1 metrics of a model to predict its label
    
    Args:
        - model (str) : Model to use. Supported: 
            'knn' -> K-Nearest Neighbors
            'svm' -> Support Vector Machine
        - change_function (function) : Function to obtain the representation of each data. It returns a list of integers or a list of list of integers.
        - dataset (list) : Dataset.
        - labels (list): List of labels for each element of the dataset. Its size matches the dataset.

    Return:
        - str
    
    """

    # Aplicar la función de cambio a cada elemento del conjunto de datos y aplanar los resultados
    features = [change_function(data).flatten() for data in dataset]

    # Dividir el conjunto de datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.25)

    # Entrenar el modelo seleccionado (KNN o SVM) y evaluar el rendimiento
    if model == 'knn':
        global n_neighbors
        
        # Entrenamiento del modelo KNN 
        clss = KNeighborsClassifier(n_neighbors=n_neighbors)
        clss.fit(X_train, y_train)

    else: 
        global C, gamma

        # Entrenamiento del modelo SVM 
        clss = SVC(C=C, gamma=gamma)
        clss.fit(X_train, y_train)
        
    # Calcular las métricas de rendimiento del clasificador
    metrics = f"""
    Precision: {
        round(precision_score(y_test, clss.predict(X_test), average='weighted'), 4)
    }
    Recall: {
        round(recall_score(y_test, clss.predict(X_test), average='weighted'), 4)
    }
    F1 Score: {
        round(f1_score(y_test, clss.predict(X_test), average='weighted'), 4)
    }
    """
    return metrics 
    