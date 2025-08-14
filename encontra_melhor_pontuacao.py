import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.inspection import permutation_importance
import warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0" 
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
from scikeras.wrappers import KerasClassifier
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # 0 = todos, 1 = info, 2 = warnings, 3 = apenas erros
warnings.filterwarnings("ignore")


# ---------------------------
# Seeds
# ---------------------------
def set_all_seeds(seed=42):
    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

set_all_seeds(42)

# ---------------------------
# Dados
# ---------------------------
df = pd.read_csv("backtest_acoes.csv")
df = df.drop(columns=['Ativo', 'proximo Balanco'], errors='ignore')





y = (df['Total'] > 0).astype(int)   # alvo binário
X = df.drop(columns=['Total'])

# (opcional) se você quiser manter os valores originais, comente a linha abaixo
# X[X > 0] = 1

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ---------------------------
# Modelo
# ---------------------------
def build_model(meta, units1=32, units2=16, dropout=0.0, lr=1e-3):
    input_dim = meta["n_features_in_"]
    model = Sequential([
        Dense(units1, activation='relu', input_shape=(input_dim,)),
        Dropout(dropout),
        Dense(units2, activation='relu'),
        Dropout(dropout),
        Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=15,
    restore_best_weights=True,
    verbose=0
)

clf = KerasClassifier(
    model=build_model,
    epochs=200,
    batch_size=32,
    verbose=0,
    validation_split=0.2,
    fit__callbacks=[early_stop]
)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", clf)
])

# ---------------------------
# Grade de hiperparâmetros (mantenha pequena para começar)
# ---------------------------
param_grid = {
    "clf__model__units1": [32, 64],      # 2 
    "clf__model__units2": [16, 32, 64],  # 3
    "clf__model__dropout": [0.0, 0.3],   # 2
    "clf__model__lr": [1e-3],            # 1
    "clf__batch_size": [16, 32],         # 2
    "clf__epochs": [150],                # 1
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

grid = GridSearchCV(
    pipe,
    param_grid=param_grid,
    scoring="accuracy",      # mude para "roc_auc" ou "f1" se preferir
    cv=cv,
    n_jobs=1,                # deixe 1 para evitar problemas de determinismo
    verbose=1
)

grid.fit(X_train, y_train)

print("\n=== Melhor combinação (val_accuracy média no CV) ===")
print(grid.best_params_)
print(f"Best CV accuracy: {grid.best_score_:.4f}")

# ---------------------------
# Avaliação no hold-out
# ---------------------------
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)
test_acc = accuracy_score(y_test, y_pred)
print(f"Hold-out test accuracy: {test_acc:.4f}")
corte = test_acc * 100
# ---------------------------
# (Opcional) Importância por permutação com o melhor pipeline
# ---------------------------
result = permutation_importance(best_model, X_test, y_test, n_repeats=10, random_state=42)
importances_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": result.importances_mean
}).sort_values(by="Importance", ascending=False)


positivos = importances_df["Importance"] > 0
negativos = importances_df["Importance"] < 0

# Soma total dos valores absolutos positivos e negativos
soma_pos = importances_df.loc[positivos, "Importance"].sum()
soma_neg = abs(importances_df.loc[negativos, "Importance"]).sum()

# Aplica a transformação em uma única coluna
importances_df["Importance (%)"] = importances_df["Importance"].apply(
    lambda x: round((x / soma_pos * 100), 2) if x > 0 else
              round(-(abs(x) / soma_pos * 100), 2) if x < 0 else 0
)



print("\n=== Importância das features (Permutation Importance) ===")
print(importances_df)

# 🔹 Ordenar pelas mais importantes
importances_df = importances_df.sort_values(by='Importance (%)', ascending=True)

Lista_ordenada = pd.read_csv("analise_acoes.csv")
Lista_ordenada = Lista_ordenada.drop(columns=['Total', 'Liquidez minima','Preço atual'], errors='ignore')  # evita erro se alguma coluna não existir

# Converte df_importance em dicionário
importance_dict = dict(zip(importances_df["Feature"], importances_df["Importance (%)"]))

# Atualiza os valores nas colunas correspondentes
for col, val in importance_dict.items():
    if col in Lista_ordenada.columns:
        Lista_ordenada.loc[Lista_ordenada[col] >= 1, col] = val

Lista_ordenada['Total'] = Lista_ordenada.select_dtypes(include='number').sum(axis=1)
Lista_ordenada = Lista_ordenada.sort_values(by='Total', ascending=False)
#Lista_ordenada_filtrada = Lista_ordenada[Lista_ordenada['Total'] > corte]
Lista_ordenada_filtrada = Lista_ordenada[Lista_ordenada['Total'] > 10]
Lista_ordenada_filtrada.to_csv("analise_acoes_porcentagem.csv", index=False, encoding='utf-8-sig')

# Seleciona apenas as colunas desejadas
colunas = ["Ativo Meta", "Empresa", "Total", "próxima entrada", "proximo Balanco"]

# Se quiser salvar só essas colunas:
Lista_ordenada_filtrada[colunas].to_csv(r"robo\Robo Fundamental\selecao_salva.csv", index=False, encoding='utf-8-sig')
# ...existing code...
print(Lista_ordenada_filtrada)