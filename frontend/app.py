import streamlit as st
import requests

# --- App Configuration ---
API_URL = "http://localhost:8000"  # Your FastAPI backend URL

# --- Page Setup ---
st.set_page_config(
    page_title="Skincare Routine Builder",
    page_icon="✨",
    layout="centered",
)

st.title("✨ Personalized Skincare Routine Builder")
st.markdown("Enter your skin type and main concern to get a customized routine.")

# --- User Input Form ---
with st.form(key='routine_form'):
    skin_type = st.selectbox(
        "Select your skin type:",
        options=["Dry", "Normal", "Oily", "Combination", "All"]
    )
    concern = st.selectbox(
        "Select your main concern:",
        options=["Hydration", "Acne", "Dullness", "Anti-aging", "Pores", "Sensitivity"]
    )
    
    submit_button = st.form_submit_button(label="Generate Routine")

# --- API Call and Response Handling ---
if submit_button:
    # Validate input
    if not skin_type or not concern:
        st.error("Please select both your skin type and a concern.")
    else:
        # Prepare the data payload
        payload = {
            "skin_type": skin_type,
            "concern": concern,
        }
        
        # Call the FastAPI backend endpoint
        with st.spinner("Generating your routine..."):
            try:
                response = requests.post(f"{API_URL}/routine", json=payload)
                
                # Check for a successful response (status code 200)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("Success"):
                        # Display the generated routines
                        st.success("Your personalized routine is ready!")
                        
                        st.header("🌅 Morning Routine")
                        for product in data['routine']['morning']:
                            st.subheader(product['name'])
                            st.write(f"**Type:** {product['type']}")
                            st.write(f"**Skin Types:** {', '.join(product['skin_types'])}")
                            st.write(f"**Concerns:** {', '.join(product['concerns'])}")
                            st.markdown("---")
                        
                        st.header("🌙 Night Routine")
                        for product in data['routine']['night']:
                            st.subheader(product['name'])
                            st.write(f"**Type:** {product['type']}")
                            st.write(f"**Skin Types:** {', '.join(product['skin_types'])}")
                            st.write(f"**Concerns:** {', '.join(product['concerns'])}")
                            st.markdown("---")
                            
                    else:
                        st.error(data.get("message", "An unknown error occurred."))
                
                # Handle API errors
                elif response.status_code == 404:
                    st.warning("No products found for this combination. Please try a different selection.")
                else:
                    st.error(f"Error from API: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the API. Please ensure the FastAPI server is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")