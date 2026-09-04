import json
import os
from pathlib import Path
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

# Set Up File System Persistence Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MEDIA_DIR = DATA_DIR / "uploads"

DATA_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)

MEMBERS_FILE = DATA_DIR / "members.json"
AWARDS_FILE = DATA_DIR / "awards.json"
MEDIA_META_FILE = DATA_DIR / "media.json"


# JSON Helper Functions
def load_data(file_path, default_data):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_data


def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Find Logo File
def find_logo():
    extensions = ["logo.png", "logo.jpg", "logo.jpeg", "logo.PNG", "logo.JPG"]
    for ext in extensions:
        file_path = BASE_DIR / ext
        if file_path.exists():
            return file_path
    return None


logo_file = find_logo()

# Header Section
col_logo, col_header = st.columns([1, 4])

with col_logo:
    if logo_file:
        st.image(str(logo_file), width=160)
    else:
        st.warning("⚠️ Upload logo.png to GitHub")

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

# Default Initial Data
default_members = [
    {"Name": "Dhiraj Patil", "Role": "President", "Contact": "9876543210"},
    {"Name": "Rahul Sharma", "Role": "Vice President", "Contact": "9876543211"},
    {"Name": "Amit Deshmukh", "Role": "Secretary", "Contact": "9876543212"},
]

default_awards = [
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

# Load Persistent Data
if "members" not in st.session_state:
    st.session_state.members = load_data(MEMBERS_FILE, default_members)

if "awards" not in st.session_state:
    st.session_state.awards = load_data(AWARDS_FILE, default_awards)

if "media" not in st.session_state:
    st.session_state.media = load_data(MEDIA_META_FILE, [])

# Sidebar Navigation
if logo_file:
    st.sidebar.image(str(logo_file), width=130)

st.sidebar.title("🚩 Jay Hind Group")
st.sidebar.write("📍 **Address:** N-12 Hudco Tv centre Ch.sambhajingar")
st.sidebar.divider()

page = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Gallery (Photos & Videos)",
        "👥 Mandal Committee Members",
        "🏆 Awards & Achievements",
        "⚙️ Admin Dashboard (Add/Delete Data)",
    ],
)

st.sidebar.divider()
st.sidebar.caption("💻 Developed by **Dhiraj Patil**")

# --- PAGE 1: MEDIA GALLERY ---
if page == "🏠 Gallery (Photos & Videos)":
    st.header("🎬 Shree Ganpati Bappa Media Gallery")
    st.write(
        "Welcome to the Jay Hind Group official Mandal portal! View our Ganesha celebrations, darshan photos, and event videos."
    )

    if st.session_state.media:
        cols = st.columns(2)
        for idx, item in enumerate(st.session_state.media):
            with cols[idx % 2]:
                if item["type"] == "photo":
                    media_path = MEDIA_DIR / item["filename"]
                    if media_path.exists():
                        st.image(
                            str(media_path),
                            caption=item["caption"],
                            use_container_width=True,
                        )
                elif item["type"] == "video_file":
                    media_path = MEDIA_DIR / item["filename"]
                    if media_path.exists():
                        st.video(str(media_path))
                        st.caption(item["caption"])
                elif item["type"] == "video_url":
                    st.video(item["url"])
                    st.caption(item["caption"])
    else:
        st.info(
            "No media uploaded yet. Go to the **Admin Dashboard** tab in the sidebar to upload photos and videos!"
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

# --- PAGE 4: ADMIN DASHBOARD ---
elif page == "⚙️ Admin Dashboard (Add/Delete Data)":
    st.header("⚙️ Manage Mandal Data")

    tab1, tab2, tab3 = st.tabs(
        ["👥 Manage Members", "🏆 Manage Awards", "🎬 Upload Media (Photos/Videos)"]
    )

    # 1. Manage Members
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
                    save_data(MEMBERS_FILE, st.session_state.members)
                    st.success(f"Member '{m_name}' saved permanently!")
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
                    save_data(MEMBERS_FILE, st.session_state.members)
                    st.success(
                        f"Member '{selected_member}' deleted successfully!"
                    )
                    st.rerun()
            else:
                st.info("No members available to delete.")

    # 2. Manage Awards
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
                    save_data(AWARDS_FILE, st.session_state.awards)
                    st.success(f"Award '{a_title}' saved permanently!")
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
                    save_data(AWARDS_FILE, st.session_state.awards)
                    st.success(
                        f"Award '{selected_award}' deleted successfully!"
                    )
                    st.rerun()
            else:
                st.info("No awards available to delete.")

    # 3. Upload Photo / Video
    with tab3:
        st.subheader("📸 Upload Photo or 🎥 Video")
        media_type = st.radio(
            "Select Media Option:",
            ["Photo File", "Video File Upload", "YouTube / Video Link"],
            horizontal=True,
        )

        if media_type == "Photo File":
            uploaded_file = st.file_uploader(
                "Choose an image file", type=["jpg", "jpeg", "png"]
            )
            caption = st.text_input("Photo Caption", value="Ganpati Bappa Morya!")

            if st.button("Upload Photo"):
                if uploaded_file is not None:
                    file_name = uploaded_file.name
                    save_path = MEDIA_DIR / file_name

                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.session_state.media.append(
                        {
                            "type": "photo",
                            "filename": file_name,
                            "caption": caption,
                        }
                    )
                    save_data(MEDIA_META_FILE, st.session_state.media)
                    st.success("Photo uploaded successfully!")
                    st.rerun()
                else:
                    st.error("Please select an image file first.")

        elif media_type == "Video File Upload":
            uploaded_file = st.file_uploader(
                "Choose a video file (MP4/MOV)", type=["mp4", "mov", "avi", "mkv"]
            )
            caption = st.text_input("Video Caption", value="Aarti / Celebration Video")

            if st.button("Upload Video File"):
                if uploaded_file is not None:
                    file_name = uploaded_file.name
                    save_path = MEDIA_DIR / file_name

                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.session_state.media.append(
                        {
                            "type": "video_file",
                            "filename": file_name,
                            "caption": caption,
                        }
                    )
                    save_data(MEDIA_META_FILE, st.session_state.media)
                    st.success("Video uploaded successfully!")
                    st.rerun()
                else:
                    st.error("Please select a video file first.")

        elif media_type == "YouTube / Video Link":
            v_url = st.text_input(
                "Paste Video URL (YouTube Link / Direct MP4 URL)",
                placeholder="https://www.youtube.com/watch?v=...",
            )
            caption = st.text_input("Video Caption", value="Mandal Event Video")

            if st.button("Add Video Link"):
                if v_url:
                    st.session_state.media.append(
                        {"type": "video_url", "url": v_url, "caption": caption}
                    )
                    save_data(MEDIA_META_FILE, st.session_state.media)
                    st.success("Video link added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a video URL.")

# Developer Branding Footer
st.markdown(
    '<div class="developer-footer">Developed by <span>Dhiraj Patil</span></div>',
    unsafe_allow_html=True,
)
