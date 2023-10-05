from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import math
import mlflow

class Regression(object):
    kfold = KFold(n_splits=3)
            
    def __init__(self, regularization, name, lr, method, theta_type, momentum, num_epochs=500, batch_size=50, cv=kfold):
        self.lr         = lr
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.method     = method
        self.theta_type = theta_type
        self.momentum = momentum
        self.cv         = cv
        self.regularization = regularization
        self.name = name

    def mse(self, ytrue, ypred):
        return mean_squared_error(ytrue, ypred)
    
    def r2(self, ytrue, ypred):
        return r2_score(ytrue, ypred)
    
    # Get Xavier theta values
    def getXavierTheta(self, num):
        lower, upper = -(1.0 / math.sqrt(num)), (1.0 / math.sqrt(num))

        numbers = np.random.rand(num)

        scaled = lower + numbers * (upper - lower)

        return scaled
    
    def fit(self, X_train, y_train):
        # Create a list of kfold scores
        self.kfold_scores = list()
        
        # Reset val loss
        self.val_loss_old = np.infty

        for fold, (train_idx, val_idx) in enumerate(self.cv.split(X_train)):           
            X_cross_train = X_train[train_idx]
            y_cross_train = y_train[train_idx]
            X_cross_val   = X_train[val_idx]
            y_cross_val   = y_train[val_idx]

            # Assigning theta values based on provided theta_type
            self.theta = self.getXavierTheta(X_cross_train.shape[1]) if self.theta_type == 'xavier' else np.zeros(X_cross_train.shape[1])
            
            with mlflow.start_run(run_name=f"Fold-{fold}", nested=True):
                # Log parameters for each fold in mlflow
                params = {
                    "Regularization": type(self).__name__,
                    "Method": self.method,
                    "Theta": self.theta,
                    "Learning Rate": self.lr,
                    "Momentum": self.momentum
                }

                mlflow.log_params(params=params)
                
                for epoch in range(self.num_epochs):
                    perm = np.random.permutation(X_cross_train.shape[0])
                            
                    X_cross_train = X_cross_train[perm]
                    y_cross_train = y_cross_train[perm]
                    
                    # Seprate the 
                    if self.method == 'stochastic':
                        for batch_idx in range(X_cross_train.shape[0]):
                            X_method_train = X_cross_train[batch_idx].reshape(1, -1)
                            y_method_train = y_cross_train[batch_idx].reshape(1, )
                            train_loss = self._train(X_method_train, y_method_train)
                    elif self.method == 'mini-batch':
                        for batch_idx in range(0, X_cross_train.shape[0], self.batch_size):
                            X_method_train = X_cross_train[batch_idx:batch_idx+self.batch_size, :]
                            y_method_train = y_cross_train[batch_idx:batch_idx+self.batch_size]
                            train_loss = self._train(X_method_train, y_method_train)
                    else:
                        X_method_train = X_cross_train
                        y_method_train = y_cross_train
                        train_loss = self._train(X_method_train, y_method_train)

                    mlflow.log_metric(key="train_loss", value=train_loss, step=epoch)

                    yhat_val = Regression.predict(self, X_cross_val)
                    val_loss_new = self.mse(y_cross_val, yhat_val)
                    mlflow.log_metric(key="val_loss", value=val_loss_new, step=epoch)
                    
                    # Record dataset in mlflow
                    mlflow_train_data = mlflow.data.from_numpy(features=X_method_train, targets=y_method_train)
                    mlflow.log_input(mlflow_train_data, context="training")
                    
                    mlflow_val_data = mlflow.data.from_numpy(features=X_cross_val, targets=y_cross_val)
                    mlflow.log_input(mlflow_val_data, context="validation")
                    
                    #early stopping
                    if np.allclose(val_loss_new, self.val_loss_old):
                        break
                    self.val_loss_old = val_loss_new
            
                self.kfold_scores.append(val_loss_new)
                print(f"Fold {fold}: {val_loss_new}")
  
            
                    
    def _train(self, X, y):
        yhat = Regression.predict(self, X)
        m    = X.shape[0]        
        grad = (1/m) * X.T @(yhat - y) + self.regularization.derivation(self.theta)

        if not hasattr(self, 'prev_step'):
            self.prev_step = np.zeros_like(self.theta)

        self.prev_step = self.momentum * self.prev_step + self.lr * grad
        self.theta = self.theta - self.prev_step
        
        return self.mse(y, yhat)
    
    def predict(self, X):
        return X @ self.theta
    
    def _coef(self):
        return self.theta[1:]  

    def _bias(self):
        return self.theta[0]
    

class LassoPenalty:
    def __init__(self, l):
        self.l = l
        
    def __call__(self, theta): 
        return self.l * np.sum(np.abs(theta))
        
    def derivation(self, theta):
        return self.l * np.sign(theta)
    
class Lasso(Regression):
    
    def __init__(self, reg, method, lr, theta, momentum, l):
        self.regularization = LassoPenalty(l)
        super().__init__(self.regularization,  reg, lr, method, theta, momentum)