import streamlit as st

def reset_form():
    """
    Resets the form inputs to their default values.

    This function clears the user's name, age, and favorite colors
    from the session state, resetting them to an empty string, zero,
    and an empty list, respectively.
    """
    st.session_state.name = ""
    st.session_state.age = 0
    st.session_state.colors = []

def show():
    """
    Displays a form with validation, submission, and reset functionality.

    The form contains a text input for name, a number input for age, and a multiselect
    for favorite colors. The form is validated to ensure the name is not empty. If the
    form is submitted, the values are stored in session_state and a success message is
    displayed. If the "Clear" button is clicked, the session_state is reset and the app
    is re-run.
    """
    st.title("📝 Form with Validation")

    with st.form("user_form"):
        st.text_input("Name", placeholder="your name",key="name")
        st.number_input("Age", min_value=0, max_value=120, placeholder="your age", key="age")
        
        colors = ["Red", "Green", "Blue", "Yellow", "Black", "White"]
        st.multiselect(
            "Favorite Colors", 
            options=colors,
            default=st.session_state.colors,
            key="colors"
        )
        
        button = st.columns([1,5,1])
        button_submit = button[0].form_submit_button("Submit")
        button[2].form_submit_button("reset",type="primary",on_click=reset_form)
    
    if button_submit:
        st.success(f"Hello, {st.session_state.name}, you are {st.session_state.age} years old and like {', '.join(st.session_state.colors)}!")

