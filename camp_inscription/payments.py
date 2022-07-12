import numpy as np
import pandas as pd
from camp_inscription.person import AllPersons, BASE_URL
from camp_inscription.settings import APP_KEY


PAYMENT_TABLE = "registro-pagos"
SUPPORTS_TABLE = "apoyos"


def get_data(table: str) -> pd.DataFrame:
    """Retrieve data into a dataframe"""
    ap = AllPersons()
    records = ap._get_data(BASE_URL.format(app_key=APP_KEY, table=table))
    records = [rec["fields"] for rec in records]
    dataset = pd.DataFrame(records)
    return dataset


def person_summary(dataset: pd.DataFrame) -> pd.DataFrame:
    """Retrieve a summary per person"""
    payments = dataset.groupby("Número de documento")["Total abono"].sum().reset_index()
    cols = ["Número de documento", "Nombres", "Apellidos","Celular", "Ministerio/Obra", "Detalle obra"]
    persons = dataset[cols].drop_duplicates(subset=["Número de documento"])
    return persons.merge(payments)


def main() -> None:
    """Execute person summary and save the results in a csv"""
    payments = get_data(table=PAYMENT_TABLE)
    supports = get_data(table=SUPPORTS_TABLE)
    person_data = person_summary(payments)
    person_data = person_data.merge(supports[["Número de documento", "Origen"]], how="left")
    person_data["Valor del apoyo"] = np.where(
        person_data.Origen.isna(), 0, 430_000 - person_data["Total abono"]
    )
    person_data["Saldo total"] = person_data["Total abono"] + person_data["Valor del apoyo"]
    person_data.to_csv("person_summary.csv", index=False)


if __name__ == "__main__":
    main()
