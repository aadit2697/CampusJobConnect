
use dbms_proj;


-- drop foreign keys
SET foreign_key_checks = 0;
-- drop tables if exist
drop table if exists broker_website;
drop table if exists slots;
drop table if exists JOBS;
drop table if exists managers;
drop table if exists departments;
drop table if exists students;
SET foreign_key_checks = 1;

-- CREATING TABLES



-- Create departments table

CREATE TABLE departments (

    department_id INTEGER PRIMARY KEY AUTO_INCREMENT,

    department_name VARCHAR(20) UNIQUE

);

 
-- Create managers table with foreign key

CREATE TABLE managers (

    m_id VARCHAR(10) PRIMARY KEY,
    manager_name VARCHAR(20),
    job_id INTEGER,
    department_id INTEGER,

    CONSTRAINT fk_managers_department_id FOREIGN KEY (department_id) REFERENCES departments(department_id)

);

-- Create JOBS table with foreign key

CREATE TABLE JOBS (

    job_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    job_name VARCHAR(20) UNIQUE,
    department_id INTEGER,
    
    CONSTRAINT fk_jobs_department_id FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Create slots table with foreign keys

CREATE TABLE slots (

    slot_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    manager_id VARCHAR(10),
    department_id INTEGER,
    student_id INTEGER,
    job_id INTEGER,
    job_name VARCHAR(30),
    slots_taken_hrs INTEGER,
    slots_available_hrs INTEGER,
    CONSTRAINT fk_slots_manager_id FOREIGN KEY (manager_id) REFERENCES managers(m_id),
    CONSTRAINT fk_slots_dept_id FOREIGN KEY (department_id) REFERENCES departments(department_id)

);

CREATE TABLE broker_website (
    id INTEGER PRIMARY key AUTO_INCREMENT,
    job_id INTEGER NOT NULL,
    job_name varchar(20),
    fws Boolean DEFAULT FALSE,
    department_id INTEGER,
    pos_expired Boolean DEFAULT FALSE,

    CONSTRAINT fk_website_dept_id FOREIGN KEY (department_id) REFERENCES departments(department_id),
    CONSTRAINT fk_website_job_id FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

create table students (
    student_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(20),
    fws Boolean DEFAULT FALSE,
    in_job Boolean,
    job_id INTEGER,
    slot_id INTEGER,
    supervisor_id INTEGER,

    CONSTRAINT fk_students_job_id FOREIGN KEY (job_id) REFERENCES JOBS(job_id),
    CONSTRAINT fk_students_slot_id FOREIGN KEY (slot_id) REFERENCES slots(slot_id)
    -- CONSTRAINT fk_students_supervisor_id FOREIGN KEY (supervisor_id) REFERENCES supervisors(m_id)
);


/*
3 - 4 managers in a dept, manager job_id: 3
dept are just different dining halls (5 in no.s)
job_id and job_name will appear for students with

*/


-- INSERTING ROWS INTO TABLES
-- departments
INSERT INTO departments( department_name) VALUES( "Earnie Davis");
INSERT INTO departments( department_name) VALUES( "Saddler");
INSERT INTO departments( department_name) VALUES( "Graham");

-- managers
INSERT INTO managers(m_id, manager_name, job_id, department_id) VALUES("M1", "Wilbur", 3, 1);
INSERT INTO managers(m_id, manager_name, job_id, department_id) VALUES("M2", "Johnny", 3, 2);
INSERT INTO managers(m_id, manager_name, job_id, department_id) VALUES("M3", "Torreto", 3, 3);
INSERT INTO managers(m_id, manager_name, job_id, department_id) VALUES("M4", "Dominic", 3, 3);
INSERT INTO managers(m_id, manager_name, job_id, department_id) VALUES("M5", "Jessie", 3, 2);


-- jobs
INSERT INTO JOBS( job_name, department_id) VALUES( "Subway Wrapper", 1);
INSERT INTO JOBS( job_name, department_id) VALUES( "Cleaning",1);
INSERT INTO JOBS( job_name, department_id) VALUES( "Dishwashin",2);
INSERT INTO JOBS( job_name, department_id) VALUES( "ID-check",2);
INSERT INTO JOBS( job_name, department_id) VALUES( "Eggs",3);
INSERT INTO JOBS( job_name, department_id) VALUES( "Fried",3);
INSERT INTO JOBS( job_name, department_id) VALUES( "Bakery",3);
INSERT INTO JOBS( job_name, department_id) VALUES( "Cafe",3);
INSERT INTO JOBS( job_name, department_id) VALUES( "Disinfecting",2);
INSERT INTO JOBS( job_name, department_id) VALUES( "Sous-chef",1);


-- slots

INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M1", 1, 1,1, "Subway Wrapper", 2,3);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M1", 1, 3,2, "Cleaning", 5,1);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M1", 2, 5,3, "Dishwashing", 3,6);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M2", 2, 1,4, "ID-check", 2,4);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M3", 3, 1,5, "Eggs", 2,5);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M4", 3, 2,6, "Fries", 1,6);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M1", 3, 2,7, "Bakery", 5,3);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M2", 3, 2,8, "Cafe", 5,0);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M4", 2, 4,9, "Disinfecting", 2,3);
INSERT INTO slots( manager_id, department_id, student_id, job_id, job_name, slots_taken_hrs,slots_available_hrs) VALUES("M4", 1, 4,10, "Sous-chef", 2,3);



-- broker_website
INSERT INTO broker_website( job_id,job_name, fws, department_id,pos_expired) VALUES(7,"Bakery", FALSE,1,FALSE);
INSERT INTO broker_website( job_id,job_name, fws, department_id,pos_expired) VALUES(1,"Subway Wrapper", FALSE,3,TRUE);
INSERT INTO broker_website( job_id,job_name, fws, department_id,pos_expired) VALUES(3,"Dishwashing", FALSE,3,FALSE);
INSERT INTO broker_website( job_id,job_name, fws, department_id,pos_expired) VALUES(2,"Cleaning", FALSE,2,FALSE);
INSERT INTO broker_website( job_id,job_name, fws, department_id,pos_expired) VALUES(7,"Bakery", FALSE,3,FALSE);


-- student
INSERT INTO students(student_name,fws, in_job, job_id,slot_id, supervisor_id ) VALUES( "Avan",FALSE, FALSE,NULL, NULL, null);
INSERT INTO students(student_name,fws, in_job, job_id,slot_id, supervisor_id ) VALUES( "Allen",FALSE, TRUE,NULL, NULL, null);
INSERT INTO students(student_name,fws, in_job, job_id,slot_id, supervisor_id ) VALUES( "Jonathan",TRUE, TRUE,7,7, null); -- add supervisor id after creating supervio
INSERT INTO students(student_name,fws, in_job, job_id,slot_id, supervisor_id ) VALUES( "Jonathan-II",TRUE, FALSE,7,7, null);
-- will insert into other tables in future


-- CREATING Triggers
-- drop trigger if exists create_job;
DELIMITER $$
create TRIGGER create_job AFTER UPDATE ON slots
FOR EACH ROW
	IF NEW.slots_available_hrs > 5 THEN
	INSERT INTO broker_website(id, job_id,job_name, fws, department_id,pos_expired) values(null,1,NEW.job_name,FALSE,2,null);
    END IF;
-- END;
-- DELIMITER;

-- CREATING VIEW TO DISPLAY STUDENT PROFILE

DROP VIEW IF EXISTS v_student_profile;
CREATE  VIEW v_student_profile AS
SELECT s.student_id,s.student_name, j.job_name 
FROM STUDENTS s
JOIN JOBS j
on s.job_id= j.job_id;


-- Commit;