import streamlit as st
import requests

# --- Configuration & Styling ---

API_URL = "http://localhost:8000"  # Ensure this matches your FastAPI port

st.set_page_config(
    page_title="Skin Genius: AI Routine Builder",
    page_icon="🧠",
    layout="centered",
)

# Custom CSS for a modern, 'skincare' aesthetic
st.markdown(
    """
    <style>
    /* Main container styling */
    .stApp { background-color: #f4f7f6; color: #333333; }
    h1 { color: #388E3C; text-align: center; margin-bottom: 20px; font-family: 'Georgia', serif; }
    .stForm { padding: 30px; border-radius: 15px; background: white; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
    /* Button styling (primary color) */
    div.stButton > button:first-child { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 8px; border: none; transition: background-color 0.3s; }
    div.stButton > button:first-child:hover { background-color: #45a049; }
    /* Routine card styling */
    .routine-step { background-color: #ffffff; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); border-left: 5px solid #4CAF50; }
    .routine-step h4 { color: #388E3C; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Humanized Interface ---

st.markdown('<h1 style="color: #388E3C; text-align: center;">🧠 Skin Genius: Your Personalized Routine Builder</h1>', unsafe_allow_html=True)
st.markdown(
    """
    👋 **Welcome!** Let's get to know your skin so we can create a routine that actually works for *you*. 
    Tell us a little about your skin's needs below.
    """
)

# --- User Input Form (Using Columns for better layout) ---
with st.form(key='routine_form'):
    st.subheader("🧐 About Your Skin...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        skin_type = st.selectbox(
            "What is your primary skin type?",
            options=["Dry", "Normal", "Oily", "Combination", "Sensitive", "All"],
            index=0,
        )
    
    with col2:
        concern = st.selectbox(
            "What's the one thing you want to address?",
            options=["Hydration", "Acne", "Dullness", "Anti-aging", "Pores", "Redness", "Texture", "Oil Control", "Sun Protection"],
            index=0,
        )
    
    st.markdown("---")
    submit_button = st.form_submit_button(label="Build My Routine!")

# --- API Call and Response Handling ---
if submit_button:
    if not skin_type or not concern:
        st.error("❗Oops! Please make sure you've selected both options.")
    else:
        payload = {"skin_type": skin_type, "concern": concern}
        
        with st.spinner("Analyzing data and selecting perfect products... ⏳"):
            try:
                response = requests.post(f"{API_URL}/routine", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("Success"):
                        st.balloons()
                        st.success("🎉 Success! Your personalized routine is ready. Consistency is key!")
                        
                        # Function to display product cards
                        def display_routine(title, products, steps, skin_type):
                            st.header(title)
                            for i, product in enumerate(products):
                                st.markdown(f'<div class="routine-step">', unsafe_allow_html=True)
                                st.markdown(f"#### Step {i+1}: {steps[i]}")
                                st.markdown(f"**🧴 Product:** **{product['name']}**")
                                st.markdown(f"**🎯 Why it works:** This {product['type'].lower()} addresses **{', '.join(product['concerns'])}** and is suitable for your **{skin_type.lower()}** skin.")
                                st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Morning Routine
                        morning_steps = ["Cleanse", "Treat (Serum)", "Moisturize", "Protect (Sunscreen)"]
                        display_routine("🌞 Morning Routine: Protection & Hydration", data['routine']['morning'], morning_steps, skin_type)

                        # Night Routine
                        night_steps = ["Cleanse", "Tone (Optional)", "Treat (Active)", "Moisturize"]
                        display_routine("🌙 Night Routine: Repair & Renewal", data['routine']['night'], night_steps, skin_type)

                    else:
                        st.error(f"⚠️ {data.get('message', 'An unknown error occurred.')}")
                
                elif response.status_code == 404:
                    st.warning("⚠️ No perfect products found. Please ensure you have sufficient data in your Supabase table for this combination.")
                else:
                    st.error(f"❌ API Error: {response.status_code}. Something went wrong on the server.")
                    
            except requests.exceptions.ConnectionError:
                st.error("🛑 **API Connection Failed.** Please ensure the FastAPI server is running in a separate terminal.")
            except Exception as e:
                st.error(f"An unexpected application error occurred: {e}")