import os
import librosa
from numpy import dot
from numpy.random import randn

def load_data(training_dir = 'audio/drum_samples/train'):
    """
    Loads file paths for a dataset from a directory.

    Args:
        training_dir (str, optional): The directory path containing the training data.
            Defaults to 'audio/drum_samples/train'.

    Returns:
        list: A list of file paths for the training data.
    """

    training_files = [os.path.join(training_dir, f) for f in os.listdir(training_dir)]
    return training_files


def bool2int(x):
    """
    Converts a list of booleans to a single integer.

    Args:
        x (list): A list of booleans to be converted.

    Returns:
        int: An integer representing the combination of True positions in the input list.
    """

    y = 0
    for i, j in enumerate(x):
        if j: y += 1<<i
    return y


def hash_func(vecs, projections):
    """
    Hashes a list of vectors using random projections and a thresholding function.

    Args:
        vecs (list): A list of vectors to be hashed.
        projections (list): A random projection matrix used for hashing.

    Returns:
        list: A list of integer hash values for each vector in the input list.
    """

    bools = dot(vecs, projections.T) > 0
    return [bool2int(bool_vec) for bool_vec in bools]



class Table:
    """
    Represents a single hash table used in the Locality-Sensitive Hashing (LSH) scheme.

    Attributes:
        table (dict): The hash table itself, where keys are hash values and values are lists of entries.
        hash_size (int): The size of the hash table (number of hash functions).
        projections (np.ndarray): A random matrix used for projecting vectors during hashing.
    """

    def __init__(self, hash_size, dim):
        """
        Initializes the Table object with the specified hash size and dimensionality.

        Args:
            hash_size (int): The size of the hash table (number of hash functions).
            dim (int): The dimensionality of the vectors to be hashed.
        """

        self.table = dict()
        self.hash_size = hash_size
        self.projections = randn(self.hash_size, dim)
        
        
    def add(self, vecs: list, label: str):
        """
        Adds a list of vectors and their corresponding label to the hash table.

        For each vector, its hash value is computed using the random projections,
        and the vector's information (including label) is added to the corresponding bucket
        in the hash table.

        Args:
            vecs (list): A list of vectors to be added.
            label (str): The label associated with the vectors.
        """

        entry = {'label': label}
        hashes = hash_func(vecs, self.projections)
        for h in hashes:
            if h in self.table:
                self.table[h].append(entry)
            else:
                self.table[h] = [entry]

    def query(self, vecs: list) -> list:
        """
        Performs a nearest neighbor search for a list of query vectors.

        This function computes the hash values for the query vectors using the random projections
        and retrieves all entries from the corresponding buckets in the hash table.
        These entries are considered potential candidates for nearest neighbors.

        Args:
            vecs (list): A list of query vectors to search for.

        Returns:
            list: A list of candidate entries (including labels) retrieved from the hash table.
        """

        hashes = hash_func(vecs, self.projections)
        results = list()
        for h in hashes:
            if h in self.table:
                results.extend(self.table[h])
        return results
    

class LSH:
    """
    Implements Locality-Sensitive Hashing (LSH) for approximate nearest neighbor search.

    Attributes:
        num_tables (int): The number of hash tables used for LSH.
        hash_size (int): The size of each hash table (number of hash functions).
        tables (list[Table]): A list containing the individual hash tables.
    """

    def __init__(self, dim: int):
        """
        Initializes the LSH object with the specified dimensionality.

        Args:
            dim (int): The dimensionality of the vectors to be hashed.
        """

        self.num_tables = 4
        self.hash_size = 8
        self.tables = list()
        for i in range(self.num_tables):
            self.tables.append(Table(self.hash_size, dim))
            
    def add(self, vecs: list, label: str):
        """
        Adds a list of vectors and their corresponding label to all hash tables.

        Args:
            vecs (list): A list of vectors to be added.
            label (str): The label associated with the vectors.
        """

        for table in self.tables:
            table.add(vecs, label)

    def query(self, vecs: list) -> list:
        """
        Performs a nearest neighbor search for a list of query vectors.

        Args:
            vecs (list): A list of query vectors to search for.

        Returns:
            list: A list of candidate vectors (may include duplicates)
                   identified from all hash tables.
        """

        results = list()
        for table in self.tables:
            results.extend(table.query(vecs))
        return results

    def describe(self):
        """
        Prints the content of each hash table for debugging or inspection.
        """

        for table in self.tables:
            print(table.table)
            

