import base64
import io
import os
import pandas as pd
from PIL import Image
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Jay Hind Group - Shree Ganesha Utsav Mandal",
    page_icon="🌺",
    layout="wide",
)

# Custom Festival Theme Styling
st.markdown(
    """
    <style>
    .group-title {
        color: #FF6F00;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .main-title {
        color: #D32F2F;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #E65100;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .address-text {
        color: #888;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #E65100;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    .developer-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #111;
        color: #ddd;
        text-align: center;
        padding: 8px 0;
        font-size: 14px;
        border-top: 1px solid #333;
        z-index: 9999;
    }
    .developer-footer span {
        color: #FF9800;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Helper function to find logo
def get_logo_file():
    possible_names = [
        "logo.png",
        "logo.jpg",
        "logo.jpeg",
        "Image (2).jpg",
        "Image (2).png",
    ]
    for name in possible_names:
        if os.path.exists(name):
            return name
    return None


logo_path = get_logo_file()

# TOP HEADER LAYOUT WITH LOGO ON TOP-LEFT
col_logo, col_header = st.columns([1, 4])

with col_logo:
    if logo_path:
        st.image(logo_path, width=160)
    else:
        st.image("https://img.icons8.com/color/96/ganesha.png", width=100)

with col_header:
    st.markdown(
        '<div class="group-title">🚩 JAY HIND GROUP 🚩</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="main-title">🌺 ॐ श्री गणेशाय नमः 🌺</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-title">Shree Ganesha Utsav Mandal Portal</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="address-text">📍 N-12 Hudco Tv centre Ch.sambhajingar</div>',
        unsafe_allow_html=True,
    )

st.divider()

# Initialize Session State Data Storage
if "members" not in st.session_state:
    st.session_state.members = [
        {"Name": "Dhiraj Patil", "Role": "President", "Contact": "9876543210"},
        {
            "Name": "Rahul Sharma",
            "Role": "Vice President",
            "Contact": "9876543211",
        },
        {"Name": "Amit Deshmukh", "Role": "Secretary", "Contact": "9876543212"},
    ]

if "awards" not in st.session_state:
    st.session_state.awards = [
        {
            "Year": "2024",
            "Award Name": "Best Eco-Friendly Ganpati",
            "Category": "City Level 1st Prize",
        },
        {
            "Year": "2023",
            "Award Name": "Best Social Service Mandal",
            "Category": "Blood Donation & Relief Campaign",
        },
    ]

if "photos" not in st.session_state:
    st.session_state.photos = []

# Sidebar Navigation
if logo_path:
    st.sidebar.image(logo_path, width=120)

st.sidebar.title("🚩 Jay Hind Group")
st.sidebar.write("📍 **Address:** N-12 Hudco Tv centre Ch.sambhajingar")
st.sidebar.divider()

page = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Home & Bappa Photos",
        "👥 Mandal Committee Members",
        "🏆 Awards & Achievements",
        "⚙️ Admin Dashboard (Add/Delete Data)",
    ],
)

st.sidebar.divider()
st.sidebar.caption("💻 Developed by **Dhiraj Patil**")

# --- PAGE 1: PHOTOS & GALLERY ---
if page == "🏠 Home & Bappa Photos":
    st.header("📸 Shree Ganpati Bappa Photo Gallery")
    st.write(
        "Welcome to the Jay Hind Group official Mandal portal! View our Ganesha celebrations and darshan photos."
    )

    if st.session_state.photos:
        cols = st.columns(3)
        for idx, photo in enumerate(st.session_state.photos):
            with cols[idx % 3]:
                st.image(
                    photo["image"],
                    caption=photo["caption"],
                    use_column_width=True,
                )
    else:
        st.info(
            "No photos uploaded yet. Go to the **Admin Dashboard** tab in the sidebar to upload Bappa photos!"
        )

# --- PAGE 2: COMMITTEE MEMBERS ---
elif page == "👥 Mandal Committee Members":
    st.header("👥 Jay Hind Group Members & Committee")
    st.write("Meet the dedicated team working for our Ganesha Utsav Mandal.")

    if st.session_state.members:
        df_members = pd.DataFrame(st.session_state.members)
        st.dataframe(df_members, use_container_width=True)
    else:
        st.info("No members added yet.")

# --- PAGE 3: AWARDS ---
elif page == "🏆 Awards & Achievements":
    st.header("🏆 Jay Hind Group Awards & Recognition")
    st.write("Honors and awards achieved by our Mandal over the years.")

    if st.session_state.awards:
        df_awards = pd.DataFrame(st.session_state.awards)
        st.dataframe(df_awards, use_container_width=True)
    else:
        st.info("No awards recorded yet.")

# --- PAGE 4: ADMIN DASHBOARD (ADD & DELETE) ---
elif page == "⚙️ Admin Dashboard (Add/Delete Data)":
    st.header("⚙️ Manage Mandal Data")

    tab1, tab2, tab3 = st.tabs(
        ["👥 Manage Members", "🏆 Manage Awards", "📸 Upload Bappa Photo"]
    )

    # 1. Manage Members (Add + Delete)
    with tab1:
        col_add, col_del = st.columns(2)

        with col_add:
            st.subheader("➕ Add Member")
            m_name = st.text_input("Member Full Name")
            m_role = st.selectbox(
                "Role / Designation",
                [
                    "President",
                    "Vice President",
                    "Secretary",
                    "Treasurer",
                    "Committee Member",
                    "Volunteer",
                ],
            )
            m_contact = st.text_input("Contact Number (Optional)")

            if st.button("Save Member"):
                if m_name:
                    st.session_state.members.append(
                        {"Name": m_name, "Role": m_role, "Contact": m_contact}
                    )
                    st.success(f"Member '{m_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter the member's name.")

        with col_del:
            st.subheader("🗑️ Delete Member")
            if st.session_state.members:
                member_names = [m["Name"] for m in st.session_state.members]
                selected_member = st.selectbox(
                    "Select Member to Delete", member_names
                )

                if st.button("Delete Selected Member"):
                    st.session_state.members = [
                        m
                        for m in st.session_state.members
                        if m["Name"] != selected_member
                    ]
                    st.success(
                        f"Member '{selected_member}' deleted successfully!"
                    )
                    st.rerun()
            else:
                st.info("No members available to delete.")

    # 2. Add/Delete Award
    with tab2:
        col_a_add, col_a_del = st.columns(2)

        with col_a_add:
            st.subheader("➕ Add Award")
            a_year = st.text_input("Year", value="2025")
            a_title = st.text_input("Award Title / Name")
            a_category = st.text_input("Category / Details")

            if st.button("Save Award"):
                if a_title:
                    st.session_state.awards.append(
                        {
                            "Year": a_year,
                            "Award Name": a_title,
                            "Category": a_category,
                        }
                    )
                    st.success(f"Award '{a_title}' recorded successfully!")
                    st.rerun()
                else:
                    st.error("Please enter the award title.")

        with col_a_del:
            st.subheader("🗑️ Delete Award")
            if st.session_state.awards:
                award_titles = [a["Award Name"] for a in st.session_state.awards]
                selected_award = st.selectbox(
                    "Select Award to Delete", award_titles
                )

                if st.button("Delete Selected Award"):
                    st.session_state.awards = [
                        a
                        for a in st.session_state.awards
                        if a["Award Name"] != selected_award
                    ]
                    st.success(
                        f"Award '{selected_award}' deleted successfully!"
                    )
                    st.rerun()
            else:
                st.info("No awards available to delete.")

    # 3. Upload Photo
    with tab3:
        st.subheader("📸 Upload Ganpati Bappa Photo")
        uploaded_img = st.file_uploader(
            "Choose an image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"]
        )
        p_caption = st.text_input(
            "Photo Caption / Year", value="Ganpati Bappa Morya!"
        )

        if st.button("Upload Photo"):
            if uploaded_img is not None:
                img = Image.open(uploaded_img)
                st.session_state.photos.append(
                    {"image": img, "caption": p_caption}
                )
                st.success(
                    "Photo uploaded successfully! Check the 'Home & Bappa Photos' tab."
                )
            else:
                st.error("Please select an image file first.")

# Developer Branding Footer
st.markdown(
    '<div class="developer-footer">Developed by <span>Dhiraj Patil</span></div>',
    unsafe_allow_html=True,
)
