import pandas as pd
import streamlit as st
import mysql.connector
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


class AccessProfile:
    def __init__(self) -> None:
        self.conn = mysql.connector.connect(user='root', password='Dna10@avan',
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
        # Create a mysql database engine
        quoted_password = quote_plus("Dna10@avan")
        self.engine = create_engine(f"mysql+mysqlconnector://root:{quoted_password}@127.0.0.1:3306/dbms_proj", echo=True)

        self.selected_names_non_fws=st.session_state.get("selected_names_non_fws", [])
        self.selected_names_fws=st.session_state.get("selected_names_fws", [])

        self.selected_ids_non_fws= st.session_state.get("selected_ids_non_fws",[])
        self.selected_ids_fws= st.session_state.get("selected_ids_fws",[])

        #self.filtered_df_fws= st.session_state.get("self.filtered_df_fws",pd.DataFrame())


    def manager(self):
        # view slots
        self.cursor.execute("select * from slots;")
        result= self.cursor.fetchall()
    
        cols= [c[0] for c in self.cursor.description]  #get cols
        df_slots= pd.DataFrame(result, columns=cols)
        choose_view= st.radio(label="View Job-Slots/Broker Website/Swap Requests",options=['Job-Slots','Broker Website','View Swap Requests']) # radio button

        #st.write(f"FWS Shift change req: {self.selected_names_fws}")
        #st.write(f"NON-FWS Shift change req: {self.selected_names_non_fws}")


        if choose_view=="Job-Slots":
            
            temp_modified_df= st.data_editor(df_slots,num_rows="dynamic")

            if st.button("Update Slots"):
                st.dataframe(temp_modified_df)
                #diff_df= pd.concat([df_slots,temp_modified_df], sort=False).drop_duplicates(keep=False, inplace=False)
                diff_df= temp_modified_df[df_slots.ne(temp_modified_df).any(axis=1)] # get the changes applied to the rows
                
                update_rows=[]
                # update the slots table 
                if not diff_df.empty:
                    #build list to rows to update
                    for i,row in diff_df.iterrows():
                        update_rows.append((row['slots_available_hrs'],row['slot_id']))
                    print(update_rows)
                    self.cursor.executemany("Update slots set slots_available_hrs= %s where slot_id= %s",update_rows)
                    self.conn.commit()
                    print(self.cursor.rowcount, "Records of a slots table updated successfully")
                #temp_modified_df.to_sql('slots', self.engine, index=False, if_exists='replace')
        
        if choose_view=="Broker Website":
           
            df_broker_website = pd.read_sql_query("select * from broker_website", self.conn)
            modified_broker_website_df= st.data_editor(df_broker_website, num_rows="dynamic")

            if st.button("Update Job listing"):
                st.dataframe(modified_broker_website_df)
                diff_broker_website_df= modified_broker_website_df[df_broker_website.ne(modified_broker_website_df).any(axis=1)] # get the changes applied to the rows
                updated_broker_website_rows=[]
                
                if not diff_broker_website_df.empty:
                    for _,row in diff_broker_website_df.iterrows():
                        updated_broker_website_rows.append((row['pos_expired'],row['id']))
                    print(updated_broker_website_rows)
                    self.cursor.executemany("Update broker_website set pos_expired= %s where id= %s",updated_broker_website_rows)
                    self.conn.commit()
                    print(self.cursor.rowcount, "Records of a broker_website table updated successfully!")

        if choose_view=="View Swap Requests" and (self.selected_names_non_fws or self.selected_names_fws ):
            student_ids_to_swap= self.selected_ids_non_fws + self.selected_ids_fws
            student_names_to_swap= self.selected_names_non_fws + self.selected_names_fws
            swap_df= pd.DataFrame({"Student_ID":student_ids_to_swap,"Student_Name":student_names_to_swap})
            #st.dataframe(swap_df)
            gd = GridOptionsBuilder.from_dataframe(swap_df)
            gd.configure_selection(selection_mode='multiple', use_checkbox=True)
            gridoptions = gd.build()

            grid_table = AgGrid(swap_df, height=150, gridOptions=gridoptions,
                            update_mode=GridUpdateMode.SELECTION_CHANGED)
            st.write('Selected Students to replace slots: ')
            selected_row = grid_table["selected_rows"]
            print(type(selected_row))
            if selected_row:
                swap_selected_students_df= pd.DataFrame(selected_row).iloc[:, 1:]
                st.dataframe(pd.DataFrame(selected_row).iloc[:, 1:])
                
                if st.button("Substitute"):
                    try:
                        
                        student_id= swap_selected_students_df['Student_ID'].iloc[0]
                        for i, row in swap_selected_students_df.iterrows():
                            st.write(row['Student_ID'])
                            s_id = row['Student_ID']
                            self.cursor.callproc('p_student_substitute_shift', args=(s_id,))
                        
                            #self.cursor.callproc('p_student_substitute_shift', args=(s_id,))
                        
                        self.conn.commit()
                                                                    
                        st.write("A procedure will be initiated here!")
                    except mysql.connector.Error as err:
                        # Check if the exception is specific to "No rows found"
                        if err.errno == 1644:
                            print("No rows found for the given conditions.")
                        else:
                            # Handle other types of errors if needed
                            print(f"Error: {err}")
                    

    
    def student(self):
        # choose display for FWS or NON-FWS student
        st.markdown("View FWS/NON-FWS Student")
        choose_view= st.radio(label="",options=['FWS','NON-FWS']) # radio button
        choose_student_info= st.radio("Student Info", options=["View Profile", "View Jobs"])
        if choose_view=="FWS":
            
            if choose_student_info == "View Profile":
                student_profile_df_fws = pd.read_sql_query("select * from v_student_profile", self.conn) # refers a view v_student_profile
                st.dataframe(student_profile_df_fws)
                self.selected_names_fws = st.multiselect("Select students to drop shifts:", student_profile_df_fws['student_name'])
                if self.selected_names_fws:
                    st.session_state.selected_names_fws = self.selected_names_fws
                    st.session_state.selected_ids_fws= student_profile_df_fws[student_profile_df_fws['student_name'].isin(
                                                            self.selected_names_fws)]['student_id'].to_list()
                    st.write(f"Students successfully added your shift for substitution: {','.join(self.selected_names_fws)}")

            if choose_student_info == "View Jobs":
                student_jobs_df_fws= pd.read_sql_query("select * from v_student_jobs_fws", self.conn)
                st.dataframe(student_jobs_df_fws)

            
        if choose_view=="NON-FWS":
            
             if choose_student_info == "View Profile":
                student_profile_df_nonfws = pd.read_sql_query("select * from v_student_profile_non_fws", self.conn) # refers a view v_student_profile_non_fws
                st.dataframe(student_profile_df_nonfws)
                self.selected_names_non_fws = st.multiselect("Select names:", student_profile_df_nonfws['student_name'])
                if self.selected_names_non_fws:
                    st.session_state.selected_names_non_fws = self.selected_names_non_fws
                    st.session_state.selected_ids_non_fws= student_profile_df_nonfws[student_profile_df_nonfws['student_name'].isin(
                                                            self.selected_names_non_fws)]['student_id'].to_list()
                    
                    st.write(f"Students successfully added your shift for substitution: {','.join(self.selected_names_non_fws)}")
                    

             if choose_student_info == "View Jobs":
                student_jobs_df_nonfws= pd.read_sql_query("select * from v_student_jobs_nonfws", self.conn)
                st.dataframe(student_jobs_df_nonfws)
                

        self.close_connection()

    def close_connection(self): 
        # Close the cursor and connection
        self.cursor.close()
        self.conn.close()

    def select_page(self):
        if self.selected_option=="Manager":
            self.manager()
        if self.selected_option=="Student":
            self.student()


profile_instance = AccessProfile()
profile_instance.select_page()