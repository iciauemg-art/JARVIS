import pandas as pd

#HateBR

hatebr = pd.read_csv("data/raw/hatebr_original.csv")
hatebr_padrao = pd.DataFrame({
    "id": ["hatebr_" + str(i) for i in range(len(hatebr))],
    "texto": hatebr["comment"],
    "label": hatebr["offensive_language"].map({1: "odio", 0: "nao_odio"}),
    "categoria_original": hatebr.get("hate_speech_group", None), #granulidade original
    "fonte": "hatebr",
})

#MINA-BR versao rotulada
minabr = pd.read_csv("data/raw/minabr_rotulada.csv")
minabr_padrao = pd.DataFrame({
    "id": ["minabr_" + str(i) for i in range(len(minabr))],
    "texto": minabr["comentario"],
    "label": minabr["odio"].map({1: "odio", 0: "nao_odio"}),
    "categoria_original": "misoginia",
    "fonte": "minabr",
})

#adicionar dataframes do Reddit depois

#unificar
dataset_combinado = pd.concat([hatebr_padrao, minabr_padrao], ignore_index=True)

#limpeza

dataset_combinado = dataset_combinado.dropna(subset=["texto", "label"])
dataset_combinado = dataset_combinado.drop_duplicates(subset=["texto"])
dataset_combinado = dataset_combinado[dataset_combinado["texto"].str.strip().str.len() > 2]

dataset_combinado.to_csv("data/processed/dataset_combinado.csv", index=False)
print(dataset_combinado["label"].value_counts())
print(dataset_combinado["fonte"].value_counts())
