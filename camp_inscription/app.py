from typing import Tuple, Any
import streamlit as st
from camp_inscription.person import Person, AllPersons
from camp_inscription.utils import read_local_css
import os
from pathlib import Path


@st.cache
def get_all_ids():
    """Retrieve all ids"""
    all_people = AllPersons()
    return all_people.get_ids()


def get_image_path() -> str:
    img_path = os.path.join(Path(__file__).parent, "logo")
    img_path = [os.path.join(img_path, file_path) for file_path in os.listdir(img_path)]
    return img_path[0]


ALL_IDS = get_all_ids()
badge_path = os.path.join(Path(__file__).parent, "imgs/badges/asmara.jpg")
team_logo_path = os.path.join(Path(__file__).parent, "imgs/inv_logos/asmara.jpg")


def check_id_number() -> Tuple[bool, Any]:

    """Returns `True` if the id number is correct, and False if it is incorrect"""

    def id_entered():
        if st.session_state["id_number"] in ALL_IDS:
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
    read_local_css("style.css")
    st.image(image=get_image_path())
    st.image(image=badge_path)
    st.markdown("# Retiro de Jóvenes 2022 - TBUCF")
    person = Person(st.session_state["id_number"])
    payment = person.get_payment_data()
    name = (
        payment["fields.Nombres"].str.title() + " " + payment["fields.Apellidos"].str.title()
    ).values[0]
    team = person.get_team_data()
    st.markdown(f"""
    ¡Hola {name}! Estamos muy felices de contar contigo en este retiro.
    A continuación, te presentamos una información que debes tener muy presente:

    * **Equipo:** {team["fields.Equipo"].values[0]}
    * **Confidente:** {team["fields.Confidente"].values[0]}
    """)
    t = "<div> Este es <span class='highlight asmara'>el color</span> de tu equipo.</div>"
    st.markdown(t, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("")

    with col2:
        st.image(image=team_logo_path, width=250)

    with col3:
        st.write("")
