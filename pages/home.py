import streamlit as st

def show():
    # Custom CSS for dark theme, cyan accents, footer styles, and Bootstrap
    st.markdown("""
    <style>
    .cyan-text {
        color: #00FFFF;
    }
    .service-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .footer {
        background-color: #262730;
        color: #ffffff;
        padding: 20px;
    }
    .footer a {
        color: #00FFFF;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    .social-icons a {
        color: #ffffff;
        margin-right: 15px;
        font-size: 24px;
    }
    .social-icons a:hover {
        color: #00FFFF;
    }
    .footer a {
        color: #00FFFF !important;
        text-decoration: none !important;
    }
    .footer a:hover {
        text-decoration: underline !important;
    }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<h1 style='text-align: center;'><span class='cyan-text'>TEAM PIXELS</span></h1>", unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2,1])
    
    with col1:
        st.markdown("<h2>WE ARE <span class='cyan-text'>CREATIVE</span> DESIGNERS</h2>", unsafe_allow_html=True)
        st.write("At Team Pixels, we redefine creativity with every project we undertake. Our design journey spans decades, transcending traditional boundaries and setting new standards in the design industry.")
    
    with col2:
        st.image("E:\\Nikhil\\Cognizant\\main3\\images\\logo.png", width=200)
    
    # Services section
    st.markdown("<h2>WHAT WE <span class='cyan-text'>DO?</span></h2>", unsafe_allow_html=True)
    st.write("We’re a dynamic team skilled in crafting digital experiences that resonate with users. Our range of services includes:")
    
    col1, col2, col3= st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='service-box'>
        <h3>Website Design</h3>
        <p>We craft visually stunning and user-friendly websites tailored to your brand identity.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='service-box'>
        <h3>Web App</h3>
        <p>Our expertise extends to developing robust Web applications using Streamlit.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='service-box'>
        <h3>UI & UX Design</h3>
        <p>Our UI/UX designs are centered around the user experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    
    # About Us section
    st.markdown("<h2>WHO ARE <span class='cyan-text'>WE?</span></h2>", unsafe_allow_html=True)
    st.write("Team Pixels is a collective of forward-thinking individuals passionate about design and technology. We bring together our diverse backgrounds and experiences to deliver solutions that not only meet but exceed expectations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='service-box'>
        <h3>Clean Code</h3>
        <p>We adhere to the highest standards of coding practices, ensuring that our projects are not just aesthetically pleasing but also efficient and scalable.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='service-box'>
        <h3>Modern Design</h3>
        <p>Our designs are modern, sleek, and tailored to the latest trends. We believe in pushing the envelope and delivering designs that stand the test of time.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("PROJECT", "1")
    col2.metric("PLEASURE", "8.9")
    col3.metric("TEAM MEMBERS", "6")

    # Footer
def footer():
    st.markdown("""
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-3 col-md-6">
                    <h3>Get in Touch</h3>
                    <p>Stay updated with our latest templates and design innovations. We’re just a click away!</p>
                    <form action="#" method="post" novalidate="true">
                        <input type="text" name="EMAIL" class="form-control" placeholder="Email">
                        <button class="btn btn-primary" type="submit">Subscribe</button>
                    </form>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h3>Connect To Team</h3>
                    <ul>
                        <li><a href="https://www.linkedin.com/in/sakshi-gaikwad-18b587229/">Sakshi Gaikwad</a></li>
                        <li><a href="https://www.linkedin.com/in/srushti-rajput-215473230/">Srushti Rajput</a></li>
                        <li><a href="https://www.linkedin.com/in/ayush-jain-8b6985231/">Ayush Jain</a></li>
                        <li><a href="https://www.linkedin.com/in/dhruv-yaranalkar-41a58b229/">Dhruv Yaranalkar</a></li>
                        <li><a href="https://www.linkedin.com/in/nikhil-ingale-23055622b">Nikhil Ingale</a></li>
                        <li><a href="https://www.linkedin.com/in/atharva-pimple-7062a5287/">Atharva Pimple</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h3>Help</h3>
                    <ul>
                        <li><a href="#">FAQ</a></li>
                        <li><a href="#">Terms & Conditions</a></li>
                        <li><a href="#">Support Policy</a></li>
                        <li><a href="#">Privacy</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h3>Socials</h3>
                    <div class="social-icons">
                        <a href="https://www.facebook.com/" class="fab fa-facebook"></a>
                        <a href="https://twitter.com/" class="fab fa-twitter"></a>
                        <a href="https://www.linkedin.com/" class="fab fa-linkedin"></a>
                        <a href="https://in.pinterest.com/" class="fab fa-pinterest"></a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <div class="row align-items-center">
                    <div class="col-lg-6 col-sm-7">
                        <p class="mb-0">© FinGenAi Inc. 2024 All rights reserved.</p>
                    </div>
                    <div class="col-lg-6 col-sm-5 text-right">
                        <p>Made with &hearts; by <a href="/home" target="_blank">TEAM PIXELS</a></p>
                    </div>
                </div>
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)
