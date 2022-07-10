"""Main streamlit app"""
import os
from pathlib import Path
from typing import Tuple, Any
import streamlit as st
from camp_inscription.person import Person, AllPersons
from camp_inscription.utils import read_local_css
from camp_inscription.messages import RAW_PERSON_TEXT


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
    """Get the main logo image path"""
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

    # Retrieve the image paths for the person's team
    team_paths = get_team_paths(team=person.team)

    read_local_css("style.css")
    team_css = person.team.replace("_", "")

    st.image(image=get_image_path())
    st.image(image=team_paths["badge"])
    st.markdown("# Retiro de Jóvenes 2022 - TBUCF")
    st.markdown(
        RAW_PERSON_TEXT.format(
            name=person.name,
            team=person.team_info["Equipo"],
            district=person.team_info["Distrito_HR"],
            leader_man=person.team_info["ConfidenteH"],
            leader_woman=person.team_info["ConfidenteM"],
            team_css=team_css,
        ),
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(" ")

    with col2:
        st.image(image=team_paths["logo"])

    with col3:
        st.write(" ")
