import streamlit as st
import pandas as pd
import math
import functions 
import reports
st.title ("ImmersaVLM")
# grab what species of animal they want to filter from the database
    # this can be done by either A: going through and outputing allt he unique species in the table or B have a running dictionary of them and pull from that
user_selected_s = st.multiselect("species to filter by :",[ "Dolphin","Whale","Fish","Otter"])
user_selected_c = st.slider ("what is minumum confidance level:", min_value=00, max_value=100 , value=0 , step=10, format="%d%%")

# button to test data 


if st.button("test report"): reports.generate_report(1)



# create talbe header
st.subheader("table")

# create varible for all results, this varible can change later to when filter is added and allows for differnt changes
if user_selected_s or user_selected_c > 0:  
     results= functions.results_by_filter(user_selected_s, user_selected_c)
else:
     results = functions.get_all_results()

     
tf = pd.DataFrame(
    results,
    columns=["ID","Species","Filename","Confidence"]
)
# set up for generate reports function later on. #TODO ADD FUNCTIONALTY TO HAVE IT CREATE A PDF WITH ALL THE EXPECTED QUALITES
tf["Generate report"] = "Generate Report"

# limits the page to 15 entries per page
ROWS_PER_PAGE = 15
total_pages = max(1, (len(tf) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE) #

# 2. Render the interactive pagination buttons FIRST (on top)
current_page = st.pagination(num_pages=total_pages)

# 3. Slice the DataFrame based on the active button page
start_idx = (current_page - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE
sliced_tf = tf.iloc[start_idx:end_idx]

st.dataframe(sliced_tf, width='stretch', hide_index=True, height=565)



##if user_selected_s or user_selected_c > 0:  
 #    results= functions.results_by_filter(user_selected_s, user_selected_c)
#else:
 #    results = functions.get_all_results()


