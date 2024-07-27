
import mysql.connector
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

import mysql.connector

class Profile:
    def __init__(self) -> None:
        #self.conn= sqlite3.connect("test.db")
        self.conn= mysql.connector.connect(user='root', password='Dna10@avan',
                              host='127.0.0.1',
                              database='dbms_proj')
        self.cursor= self.conn.cursor()
        st.markdown(
        """
        <div style="text-align: center;">
            <h1><i>Get-A-Job</i></h1>
        </div>
        """,
        unsafe_allow_html=True)

        # selects page to be displayed
        self.selected_option = st.sidebar.selectbox("Select an option", ["Manager", "Broker Website", "Student"])
        # Create an SQLite database engine
        #self.engine = create_engine('sqlite:///test.db', echo=False)
        self.engine = create_engine(f"mysql+mysqlconnector://root:Dna10@avan@127.0.0.1/dbms_proj")

    def manager(self):
        # manager screen displays 2 buttons
        # function triggers a query that displays rows from broker website and slots
        self.cursor.execute("select * from slots;")
        result= self.cursor.fetchall()
    
        cols= [c[0] for c in self.cursor.description]  #get cols
        df_slots= pd.DataFrame(result, columns=cols)
        choose_view= st.radio(label="View Job-Slots/Broker Website",options=['Job-Slots','Broker Website']) # radio button
        if choose_view=="Job-Slots":
            temp_modified_df= st.data_editor(df_slots,num_rows="dynamic")

            if st.button("Update Slots"):
                st.dataframe(temp_modified_df)
                
                temp_modified_df.to_sql('slots', self.conn, index=False, if_exists='replace')
        
        if choose_view=="Broker Website":
            df_broker_website = pd.read_sql_query("select * from broker_website", self.conn)
            temp_modified_jobs_df= st.data_editor(df_broker_website, num_rows="dynamic")

            if st.button("Update Job listing"):
                st.dataframe(temp_modified_jobs_df)
                temp_modified_jobs_df.to_sql('broker_website', self.conn, index=False, if_exists='replace')
            # allow manager to update the table if pos_expired

        self.close_connection()
    
    """   
        def student(self):
            st.write("Helping Students manage job schedules since a minute! :sunglasses: ")
            student_df = pd.read_sql_query("select * from students", self.conn)

            def display_checkboxes(dataframe):
                checkbox_column = []

                for index, row in dataframe.iterrows():
                    # Create a checkbox for each row
                    checkbox_value = st.checkbox("", key=f"checkbox_{index}")
                    checkbox_column.append(checkbox_value)
                dataframe['Show'] = checkbox_column
            display_checkboxes(student_df)
            st.write("Updated DataFrame:")
            st.table(student_df)
"""        
    def close_connection(self): 
        # Close the cursor and connection
        self.cursor.close()
        self.conn.close()

    def select_page(self):
        if self.selected_option=="Manager":
            self.manager()
        #if self.selected_option=="Student":
        #    self.student()



profile_instance = Profile()
profile_instance.select_page()
        

    

    