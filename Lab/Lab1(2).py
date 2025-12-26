from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedKFold
import pandas as pd

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Display dataset size before cross-validation
print(f"Total samples: {X.shape[0]}")
print(f"Number of features: {X.shape[1]}")
print(f"Number of classes: {len(set(y))}")
print(f"Dataset dimensions: {X.shape}\n")
print("=" * 70 + "\n")

# Create Stratified K-Fold with 10 splits
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Perform stratified k-fold cross-validation
fold_results = []
for fold, (train_index, test_index) in enumerate(skf.split(X, y), 1):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    train_size = X_train.shape[0]
    test_size = X_test.shape[0]
    
    fold_results.append({
        'Fold': fold,
        'Training Set Size': train_size,
        'Test Set Size': test_size,
        'Total': train_size + test_size
    })

# Create a pandas DataFrame
df = pd.DataFrame(fold_results)
print(df.to_string(index=False))