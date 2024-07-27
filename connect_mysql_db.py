import mysql.connector
import pandas as pd
conn = mysql.connector.connect(user='root', password='Dna10@avan',
                              host='127.0.0.1',
                              database='dbms_proj')
cursor= conn.cursor()

cursor.execute("Select * from slots;")
result= cursor.fetchall()
print(cursor.description)
cols= [c[0] for c in cursor.description] 
result_df= pd.DataFrame(result, columns=cols)
 
print(result_df)

# update df
result_df.loc[result_df['slot_id']==2,'slots_available_hrs'] = 4

print(result_df)



cursor.close()
conn.close()