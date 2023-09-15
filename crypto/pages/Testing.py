from st_vizzu import *
import streamlit as st
df=st.session_state['DataFrame']
obj=create_vizzu_obj(df)
bar_obj=bar_chart(df,
            x = "Date", 
            y = "Close",
            title= "Close Values Bar chart"
            )
anim_obj = beta_vizzu_animate( bar_obj,
    x = "Date",
    y =  ["Close", "Volume"],
    title = "Close and Volume",
    label= "Volume-Adjusted Close prices",
    color="Genres",
    legend="color",
    sort="byValue",
    reverse=True,
    align="center",
    split=False,
)
_dict = {"size": {"set": "Close"}, 
    "geometry": "circle",
    "coordSystem": "polar",
    "title": "Animation for the OHLCV",
    }
anim_obj2 = vizzu_animate(anim_obj,_dict)
vizzu_plot(anim_obj2)

        
    
