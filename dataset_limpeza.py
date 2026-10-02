from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent

hatebr = pd.read_csv(BASE / "data" / "raw" / "HateBR.csv")
print(hatebr["label_final"].value_counts(dropna=False))

dataset_padrao = pd.DataFrame({
    "id": "hatebr_" + hatebr["id"].astype(str),
    "texto": hatebr["comentario"],
    "label": hatebr["label_final"].map({1: "ofensivo", 0: "nao_ofensivo"}),
    "fonte": "hatebr",
})

n_antes = len(dataset_padrao)

#limpeza
dataset_padrao = dataset_padrao.dropna(subset=["texto", "label"])
dataset_padrao["texto"] = dataset_padrao["texto"].str.strip()
dataset_padrao = dataset_padrao[dataset_padrao["texto"].str.len() > 2]
dataset_padrao = dataset_padrao.drop_duplicates(subset=["texto"])

saida = BASE / "data" / "processed"
saida.mkdir(parents=True, exist_ok=True)
dataset_padrao.to_csv(saida / "dataset_limpeza.csv", index=False)

print(n_antes, "->", len(dataset_padrao), "linhas após a limpeza")
print(dataset_padrao["label"].value_counts())
