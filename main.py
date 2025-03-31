import streamlit as st
import importlib

st.set_page_config(page_title="My Portfolio", layout="wide")

def show_menu():
    """
    Displays the sidebar menu with the list of projects and returns the user's choice
    along with a dictionary where the key is the project name and the value is the path
    to the project's module.
    """
    st.sidebar.title("Menu")
    projects = {
        "Home": "projects.main.app",
        "Analysis Dashboard": "projects.dashboard.app",
    }
    return st.sidebar.selectbox("Choose a project", list(projects.keys())), projects

def load_project(project_name, projects):
    """Dynamically loads the selected project module."""
    if project_name in projects:
        project_module = importlib.import_module(projects[project_name])
        project_module.show()
    else:
        st.error("Project not found.")

def main():
    """Main function that manages navigation between the main window and the projects."""
    choice, projects = show_menu()
    
    if choice:
        load_project(choice, projects)

if __name__ == "__main__":
    main()
