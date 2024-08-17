import streamlit as st

def about_us():
    # List of images and their descriptions
    content = [
        {
            "image": "E:\\Nikhil\\Cognizant\\main2\\images\\img2.png",
            "title": "Ayush Jain",
            "title1": "PIXEL Lead",
            "description": "Worked on the backend using MongoDB. Connecting Web App to the database for User data storage."
        },
        {
            "image": "E:\\Nikhil\\Cognizant\\main2\\images\\img3.jpg",
            "title": "Dhruv Yaranalkar",
            "title1": "PIXEL 1",
            "description": "Worked on the backend using MongoDB. Connecting Web App to the database for User data storage."
        },
        {
            "image": "E:\\Nikhil\\Cognizant\\main2\\images\\img4.jpg",
            "title": "Nikhil Ingale",
            "title1": "PIXEL 2",
            "description": "Worked with the LLM technology using LangChain. Model building, Model integration."
        },
        {
            "image": "E:\\Nikhil\\Cognizant\\main2\\images\\img5.jpg",
            "title": "Atharva Pimple",
            "title1": "PIXEL 3",
            "description": "Worked with the security for applpying security measures to the app data."
        },
        {
            "image": "E:\\Nikhil\\Cognizant\\main2\\images\\img6.jpg",
            "title": "Sakshi Gaikwad",
            "title1": "PIXEL 4",
            "description": "Worked with the Frontend. Built UI using Streamlit, HTML and CSS."
        },
        {
            "image": "E:\\Nikhil\\Cognizant\\main2\\images\\img7.jpg",
            "title": "Srushti Rajput",
            "title1": "PIXEL 5",
            "description": "Worked with the Frontend. Built UI using Streamlit, HTML and CSS."
        }
    ]

    for i, item in enumerate(content):
        col1, col2 = st.columns(2)
        
        if i % 2 == 0:  # Even index, image on the left
            with col1:
                st.image(item["image"],width=200)
            with col2:
                Subheader_VolumesKPI = f"<p style='font-family: Sans serif; color: cyan; font-size: 30px;'>{item["title"]}</p>"
                st.header(item["title1"])
                st.markdown(Subheader_VolumesKPI, unsafe_allow_html=True)
                st.markdown(item["description"])
        else:  # Odd index, image on the right
            with col1:
                Subheader_VolumesKPI = f"<p style='font-family: Sans serif; color: cyan; font-size: 30px;'>{item["title"]}</p>"
                st.header(item["title1"])
                st.markdown(Subheader_VolumesKPI, unsafe_allow_html=True)

                st.markdown(item["description"])
            with col2:
                st.image(item["image"],width=200)
        
        st.write("---")  # Add a separator between sections

if __name__ == "__main__":
    about_us()