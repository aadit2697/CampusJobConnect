# Project Overview
<img width="881" alt="image" src="https://github.com/user-attachments/assets/eb2a3d82-4cf3-4504-ac2f-39ba5d29f2c6">

This project aims to build a system that maintains student records with  on-campus job data. Our project focuses on the efficient allocation of student hours and thus avoids occurrences like the double shifts. 

---

# :dart: Objectives:

1. Allow commercial managers to open/close job openings
   Assume total hours required per day 
   Dish room (6 hours)
   Food servers(10 hours)
   Sweep/mop (3 hours)
   Sub wrappers(7 hours)….

2. Display job openings as per availability.
   If students are eligible for the job openings
   if students have a part-time status and can still fulfill hours allocated.

3. Job allocation control
   Making sure new jobs aren’t allocated to students who already have a job.  Eg.  As per norms a student cannot work part time  at two dining halls due to time restrictions.

4. Student opt out control 
   Students could request and opt out of a shift with a button. Reduced waiting  time as compared to a mail.


# :bar_chart: Dataset Description

1. Students: Consists of students eligible for part-time positions. Eligibility is defined if they currently have a part time and how many hours/20 can they work.

2. Managers:  Managers control the number of slots open for a specific part-time position.

3. Department: Tags a position based on the where the job is based. For instance, a dining job, fitness trainer, or athletic tutor.

4. Broker Website: Serves as the interface to display the list of jobs available under each department there is. Multiple jobs from various departments will be listed here.

6. Supervisor: Supervisors have to report to more than one manager in a department. Each supervisor will be associated to one and only one department, but will report to multiple managers.

7. Slots: Slots are associated per department. The department managers control the number of slots to add/drop for positions available in respective departments.

# :triangular_ruler: ER Diagram

<img width="1349" alt="image" src="https://github.com/user-attachments/assets/f4ef710f-6eb6-4618-8fe4-73be94d1d356">


