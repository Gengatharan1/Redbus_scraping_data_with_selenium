# Home page navigation
if menu_option == "Home":
    st.sidebar.subheader("Content")
    options = ["About the Developer", "Skills Take Away From This Project", "Objective", "Prerequisites", "Required Python Libraries", "Approach"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "About the Developer":
        about_the_developer()
    elif choice == "Skills Take Away From This Project":
        skills_takeaway()
    elif choice == "Objective":
        objective()
    elif choice == "Prerequisites":
        prerequisites()
    elif choice == "Required Python Libraries":
        required_python_libraries()
    elif choice == "Approach":
        approach()