import streamlit as st
import folium
from streamlit_folium import st_folium
import math
import random
import request
from datetime import date

st.set_page_config(page_title="Odyssey Asteroid-Simulator", layout="wide", page_icon="")
st.title("Odyssey Asteroid-Simulator")
st.write("Simulate and visualize asteroid impacts on Earth using adjustable parameters.")



st.subheader("Select Impact Location")
m = folium.Map(location=[20,0],zoom_start=2)
st_data = st_folium(m, width=450, height=350)

location=None
if st_data and st_data['last_clicked']:  
    location = st_data['last_clicked']
    st.write("**Selected Location:**",location)

# sliders
st.header("⚙️ Asteroid Parameters")
asteroid_type = st.selectbox("Asteroid Type",["D-type (Carbon-rich)", "V-type (Vestoids)", "S-type (Stony)", "M-type (Metallic)",  "C-type (Carbon)", "Custom"])
densities = {
             "D-type (Carbon-rich)":1300,
             "V-type (Vestoids)":3500,
             "S-type (Stony)":2700,
             "M-type (Metallic)":7800,
             "C-type (Carbon)":1700
}
asteroid_images = {
    "D-type (Carbon-rich)": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Asteroid_Bennu_OSIRIS-REx_Image_%28cropped%29.jpg",
    "V-type (Vestoids)": "https://upload.wikimedia.org/wikipedia/commons/2/25/VestaFullView.jpg",
    "S-type (Stony)": "https://upload.wikimedia.org/wikipedia/commons/e/e3/243_Ida.jpg",
    "M-type (Metallic)": "https://upload.wikimedia.org/wikipedia/commons/d/de/16_Psyche_-_Artist%27s_Concept.jpg",
    "C-type (Carbon)": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Asteroid_Bennu_OSIRIS-REx_Image_%28cropped%29.jpg",
}

if asteroid_type != "Custom":
    st.image(asteroid_images[asteroid_type],
caption=f"{asteroid_type}", use_container_width=True)


if asteroid_type == "Custom":
    density = st.number_input("Enter Custom Density (kg/m³)", min_value=1000, max_value=15000, value=7500)
else:
    density = densities[asteroid_type]
     
diameter = st.slider("Asteroid Diameter (meters)", 10, 20000, 5000)
velocity = st.slider("Speed (km/s)", 1, 72, 25)
impact_angle = st.slider("Impact Angle (Degree)", 0, 90, 45)
     #defense
st.subheader("Defend Earth")
defend=st.radio("Do you want to defend earth",["Yes","No"])
if defend=="Yes":    
    strategy=st.selectbox("Choose your mitigation strategy",["Kinetic Impactor","Gravity Tractor"])
       
calculate = st.button("🚀 Calculate Impact")

#nasa api part
st.subheader("Near earth asteroid data")
   


if calculate:
    st.subheader("IMPACT RESULT")
    if diameter<=25:
        st.success("The asteroid burned up in the Earth's atmosphere.No impact occured")
    radius = diameter/2
    volume = (4/3) * math.pi * (radius ** 3)
    mass = density * volume
    velocity_mps = velocity * 1000
    defense_success=None
    if defend == "Yes" and strategy:      
        defense_success=random.random()<0.65
        if defense_success:
            st.success(f"Defense succesful({strategy}) -The asteroid is deflected")
            st.stop()
           
        else:
            st.error("Defense failed{strategy}-The asteroid hit the Earth")
            if strategy=="Kinetic Impactor":
                velocity_mps *=0.9
            elif strategy=="Gravity Tractor":
                velocity_mps *=0.95
       
    KE=0.5*mass*(velocity**2)
    crater_diameter=(KE/1e12)**0.3
    TNT=KE/4.184e+9
    if KE > 2e50:
        fatalities="Billions"
    elif KE > 1e18:
        fatalities = "Million"
    elif KE > 1e16:
        fatalities = "Thousands"
    else:
        fatalities = "few hundreds"
    if impact_angle < 45 and KE > 1e15:            
        tsunami = f"{round (KE/1e15,2)} meters high(Approximately)"
    else:
        tsunami = "no significance of tsunami"

    #front end result impavt result

    #
    st.write(f"Asteroid Type:{asteroid_type}")
    st.write(f"Density:{density}kg/m3")
    st.metric("Kinetic Energy", f"{KE:.2e} J")
    st.metric("Asteroid Mass", f"{mass:.2e}kg")
    st.metric("Crater Diameter", f"{crater_diameter:.2f}km")
    st.metric("TNT Equivalent", f"{TNT:.2e}tons")
    st.metric("Estimated Casualties",fatalities)
    st.metric("Tsunami Height", tsunami)
    #evacuation
    st.subheader("EVACUATION AND SAFETY PLAN")
    if fatalities=="Billions":
        st.warning('Evacuate all areas within 1000 km ')
        st.write("Asteroid has caused  global impact")
        st.write("It is global lockdown")
    elif fatalities=="Millions":
        st.warning('Evacuate all coastal and populated areas within 500km of impact')
        st.write("Move inland or to higher ground")
        st.write("There is going to be after shock waves and atmospheric effects")
    elif fatalities=="Thousands":
        st.warning("Evacuate nearest cities within 200km raadius")
        st.write("Move to higher ground")
    elif fatalities =="few hundreds":
        st.success("No major evacuation needed.Minor local impact")
       

    st.success("✅ Simulation complete! You can adjust parameters to explore more impacts.")

    # Restart button
    if st.button("🔁 Simulate Again"):
        st.experimental_rerun()

