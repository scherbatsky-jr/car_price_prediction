import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

class LogisticRegression:
    
    def __init__(self, regularization, method, alpha, k, n, max_iter=5000):
        self.regularization = regularization
        self.k = k
        self.n = n
        self.method = method
        self.alpha = alpha
        self.max_iter = max_iter
    
    def fit(self, X, Y):
        self.W = np.random.rand(self.n, self.k)
        self.losses = []
        
        if self.method == "batch":
            start_time = time.time()
            for i in range(self.max_iter):
                loss, grad =  self.gradient(X, Y)
                self.losses.append(loss)
                self.W = self.W - self.alpha * grad
                if i % 500 == 0:
                    print(f"Loss at iteration {i}", loss)
            print(f"time taken: {time.time() - start_time}")
            
        elif self.method == "minibatch":
            start_time = time.time()
            batch_size = int(0.3 * X.shape[0])
            for i in range(self.max_iter):
                ix = np.random.randint(0, X.shape[0]) #<----with replacement
                batch_X = X[ix:ix+batch_size]
                batch_Y = Y[ix:ix+batch_size]
                loss, grad = self.gradient(batch_X, batch_Y)
                self.losses.append(loss)
                self.W = self.W - self.alpha * grad
                if i % 500 == 0:
                    print(f"Loss at iteration {i}", loss)
            print(f"time taken: {time.time() - start_time}")
            
        elif self.method == "stochastic":
            start_time = time.time()
            list_of_used_ix = []
            for i in range(self.max_iter):
                idx = np.random.randint(X.shape[0])
                while i in list_of_used_ix:
                    idx = np.random.randint(X.shape[0])
                X_train = X[idx, :].reshape(1, -1)
                Y_train = Y[idx]
                loss, grad = self.gradient(X_train, Y_train)
                self.losses.append(loss)
                self.W = self.W - self.alpha * grad
                
                list_of_used_ix.append(i)
                if len(list_of_used_ix) == X.shape[0]:
                    list_of_used_ix = []
                if i % 500 == 0:
                    print(f"Loss at iteration {i}", loss)
            print(f"time taken: {time.time() - start_time}")
            
        else:
            raise ValueError('Method must be one of the followings: "batch", "minibatch" or "sto".')
        
        
    def gradient(self, X, Y):
        m = X.shape[0]
        h = self.h_theta(X, self.W)
        loss = - np.sum(Y*np.log(h)) / m + self.regularization(self.W)
        error = h - Y
        grad = self.softmax_grad(X, error) + self.regularization.derivation(self.W)
        return loss, grad

    def softmax(self, theta_t_x):
        return np.exp(theta_t_x) / np.sum(np.exp(theta_t_x), axis=1, keepdims=True)

    def softmax_grad(self, X, error):
        return  X.T @ error

    def h_theta(self, X, W):
        return self.softmax(X @ W)
    
    def predict(self, X_test):
        return np.argmax(self.h_theta(X_test, self.W), axis=1)
    
    def plot(self):
        plt.plot(np.arange(len(self.losses)) , self.losses, label = "Train Losses")
        plt.title("Losses")
        plt.xlabel("epoch")
        plt.ylabel("losses")
        plt.legend()

    def accuracy(self, y, y_pred):
        correct_predictions = np.sum(y == y_pred)
        total_predictions = y.shape[0]
        return correct_predictions / total_predictions

    def precision(self, y, y_pred, c=0):
        true_positives = np.sum((y == c) & (y_pred == c))
        false_positives = np.sum((y != c) & (y_pred == c))
        if true_positives + false_positives == 0:
            return 0
        else:
            return true_positives / (true_positives + false_positives)

    def recall(self, y, y_pred, c=0):
        true_positives = np.sum((y == c) & (y_pred == c))
        false_negatives = np.sum((y == c) & (y_pred != c))
        if true_positives + false_negatives == 0:
            return 0
        else:
            return true_positives / (true_positives + false_negatives)

    def f1_score(self, y, y_pred, c=0):
        precision = self.precision(y, y_pred, c)
        recall = self.recall(y, y_pred, c)
        if precision + recall == 0:
            return 0
        else:
            return 2 * precision * recall / (precision + recall)

    def macro_precision(self, y, y_pred):
        precisions = [self.precision(y, y_pred, c) for c in range(self.k)]
        return np.sum(precisions) / self.k

    def macro_recall(self, y, y_pred):
        recalls = [self.recall(y, y_pred, c) for c in range(self.k)]
        return np.sum(recalls) / self.k

    def macro_f1(self, y, y_pred):
        f1s = [self.f1_score(y, y_pred, c) for c in range(self.k)]
        return np.sum(f1s) / self.k

    def weighted_precision(self, y, y_pred):
        class_counts = [np.count_nonzero(y == c) for c in range(self.k)]
        precisions = [class_counts[c] / len(y) * self.precision(y, y_pred, c) for c in range(self.k)]
        return np.sum(precisions)

    def weighted_recall(self, y, y_pred):
        class_counts = [np.count_nonzero(y == c) for c in range(self.k)]
        recalls = [class_counts[c] / len(y) * self.recall(y, y_pred, c) for c in range(self.k)]
        return np.sum(recalls)

    def weighted_f1(self, y, y_pred):
        class_counts = [np.count_nonzero(y == c) for c in range(self.k)]
        f1s = [class_counts[c] / len(y) * self.f1_score(y, y_pred, c) for c in range(self.k)]
        return np.sum(f1s)

    def classification_report(self, y, y_pred):
        cols = ["precision", "recall", "f1-score"]
        idx = list(range(self.k)) + ["accuracy", "macro", "weighted"]

        report = [[self.precision(y, y_pred, c),
                   self.recall(y, y_pred, c),
                   self.f1_score(y, y_pred, c)] for c in range(self.k)]

        report.append(["", "", self.accuracy(y, y_pred)])

        report.append([self.macro_precision(y, y_pred),
                       self.macro_recall(y, y_pred),
                       self.macro_f1(y, y_pred)])

        report.append([self.weighted_precision(y, y_pred),
                       self.weighted_recall(y, y_pred),
                       self.weighted_f1(y, y_pred)])

        return pd.DataFrame(report, index=idx, columns=cols)
    
class RidgePenalty:
    def __init__(self, l):
        self.l = l
        
    def __call__(self, theta): 
        return self.l * np.sum(np.square(theta))
        
    def derivation(self, theta):
        return self.l * 2 * theta
    
class NoPenalty():
    def __init__(self, l):
        self.l = l
        
    def __call__(self, theta): 
        return 0.0
        
    def derivation(self, theta):
        return 0.0
    
class Ridge(LogisticRegression):
    def __init__(self, reg, method, alpha, k, n, l):
        self.regularization = RidgePenalty(l)
        super().__init__(self.regularization, method, alpha, k, n)

class Normal(LogisticRegression):
    def __init__(self, reg, method, alpha, k, n, l):
        self.regularization = NoPenalty(l)
        super().__init__(self.regularization, method, alpha, k, n)

    
