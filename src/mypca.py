"""
Custom PCA Class with biplot
authors:
    - Emmanuel Larralde
    - Jaime Pando
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MyPca:
    """
    Custom PCA class using unbiased covariance estimator.
    """
    def __init__(self, data_matrix: np.array) -> None:
        self.centered_data_matrix = data_matrix - data_matrix.mean(axis=0)
        my_cov = np.matmul(
            self.centered_data_matrix.T,
            self.centered_data_matrix
        )/(len(self.centered_data_matrix) - 1)

        values, vectors = np.linalg.eig(my_cov)
        idx = np.argsort(-values)
        self.explained_variance = values/values.sum()
        self.dirs = vectors[:, idx]

    def fit_transform(self, data_matrix: np.array, k: int) -> np.array:
        """
        Projects data_matrix to top k principal components
        """
        return np.matmul(data_matrix, self.dirs[:, 0:k])

    def scatter(self, labels: list = None) -> None:
        """
        Scatter plots training data on the space 
        spanned by top 2 principal components
        """
        y = self.fit_transform(self.centered_data_matrix, 2)
        plt.scatter(y[:, 0], y[:, 1])
        for sample, pt in zip(self.df.index, y):
            plt.annotate(sample, pt)

    def biplot(self, scale: float, labels: list = None) -> None:
        """
        Plots directions of every single feature on the space spanned by
        top 2 principal components.
        """
        _, num_features = self.centered_data_matrix.shape
        if labels is None:
            labels = [f"l{i}" for i in range(num_features)]
        for i, label in enumerate(labels):
            e = np.zeros(num_features)
            e[i] = 1
            x1, x2 = self.fit_transform(e, 2)
            plt.plot([0, scale*x1], [0, scale*x2])
            plt.annotate(label, (scale*x1, scale*x2))


class DfPca(MyPca):
    """
    Computes PCA directly from a dataframe
    """
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        super().__init__(df.values)

    def biplot(self, scale: float, labels: list = None) -> None:
        """
        Plots all samples and biplot from dataframe.
        """
        y = self.fit_transform(self.centered_data_matrix, 2)
        plt.scatter(y[:, 0], y[:, 1])
        for sample, pt in zip(self.df.index, y):
            plt.annotate(sample, pt)
        if labels is None:
            labels = self.df.columns
        super().biplot(scale, labels)
        plt.grid()

    def functional_plot(self, k: int) -> None:
        """
        Plots the  weighting of top k principal components.
        """
        vectors = self.dirs.T

        i = range(1, len(vectors[0]) + 1)
        plt.figure(figsize=(7, 3))
        for comp, vector in enumerate(vectors[:k]):
            plt.plot(i, vector, label=f"Componente {comp + 1}")
        plt.grid()
        plt.title("Datos funcionales")
        plt.xlabel("i")
        plt.ylabel("Ponderaciones")
        plt.legend()
