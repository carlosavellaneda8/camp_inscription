from typing import Tuple, Any
import streamlit as st
from camp_inscription.person import Person, AllPersons
from camp_inscription.utils import read_local_css
import os
from pathlib import Path


@st.cache
def get_all_records():
    """Retrieve all records"""
    all_people = AllPersons()
    all_people.get_teams_data()
    all_people.get_meta_data()
    return all_people


@st.cache
def get_all_ids(records: list) -> set:
    """Retrieve all ids"""
    ids = [record["fields"]["Número de documento"] for record in records]
    return set(ids)


def get_image_path() -> str:
    img_path = os.path.join(Path(__file__).parent, "logo")
    img_path = [os.path.join(img_path, file_path) for file_path in os.listdir(img_path)]
    return img_path[0]


def get_team_paths(team: str) -> dict:
    """Retrieve the team's path images"""
    output = {}
    parent_path = Path(__file__).parent
    output["badge"] = os.path.join(parent_path, f"imgs/badges/{team}.jpg")
    output["logo"] = os.path.join(parent_path, f"imgs/inv_logos/{team}.jpg")
    return output


all_records = get_all_records()
all_ids = get_all_ids(all_records.records)
badge_path = os.path.join(Path(__file__).parent, "imgs/badges/asmara.jpg")
team_logo_path = os.path.join(Path(__file__).parent, "imgs/inv_logos/asmara.jpg")


def check_id_number() -> Tuple[bool, Any]:

    """Returns `True` if the id number is correct, and False if it is incorrect"""

    def id_entered():
        if st.session_state["id_number"] in all_ids:
            st.session_state["id_correct"] = True
        else:
            st.session_state["id_correct"] = False

    if "id_correct" not in st.session_state:
        st.image(image=get_image_path())
        st.markdown("""
        # Retiro de Jóvenes 2022 - TBUCF
        """)
        st.number_input(
            "Ingresa tu número de documento:", on_change=id_entered,
            format="%d", value=0, key="id_number"
        )
        return False
    elif not st.session_state["id_correct"]:
        st.image(image=get_image_path())
        st.markdown("""
        # Retiro de Jóvenes 2022 - TBUCF
        """)
        st.number_input(
            "Ingresa tu número de documento:", on_change=id_entered,
            format="%d", value=0, key="id_number"
        )
        st.error("Documento incorrecto. Intenta nuevamente")
        return False
    else:
        return True


if check_id_number() & ("id_number" in st.session_state):
    # Retrieve person's info if the id number is correct
    person = Person(st.session_state["id_number"])
    person.get_person_info(all_records.records)
    person.get_team_info(all_records.meta)

    # TODO: Fix team leaders and team images!

    read_local_css("style.css")
    st.image(image=get_image_path())
    st.image(image=badge_path)
    st.markdown("# Retiro de Jóvenes 2022 - TBUCF")
    st.markdown(f"""
    ¡Hola {person.name}! Estamos muy felices de contar contigo en este retiro.
    A continuación, te presentamos una información que debes tener muy presente:

    * **Equipo:** {person.team_info["Distrito_HR"]}
    * **Confidente:** {person.team_info["Distrito_HR"]}
    """)
    team_css = person.team.replace("_", "")
    t = f"<div> Este es <span class='highlight {team_css}'>el color</span> de tu equipo.</div>"
    st.markdown(t, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("")

    with col2:
        st.image(image=team_logo_path, width=250)

    with col3:
        st.write("")
