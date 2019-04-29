create table patient(p_id serial, f_name varchar(30), l_name varchar(30), age int, dob DATE, address varchar(30), phone_number varchar(15), sex char(1), height numeric, weight numeric, primary key (p_id));

create table staff(s_id serial, f_name varchar(30), l_name varchar(30), address varchar(30), phone_number varchar(15), s_type varchar(10), d_id int REFERENCES hospital_department, username VARCHAR(32), password VARCHAR(32), primary key(s_id));

create table hospital_department(d_id serial, dept_name varchar(50), office_info varchar(50), visit_cost numeric, primary key(d_id));

create table insurance_company(ip_id serial, name varchar(50), policy_id int, phone_number varchar(15), primary key(ip_id));

create table insured_by(p_id int REFERENCES patient, ip_id int REFERENCES insurance_company);

create table procedures(pr_id serial, name varchar(30), cost numeric, facility varchar(30), per_hour char(1), primary key(pr_id));

create table patient_history(ph_id serial, p_id int REFERENCES patient, s_id int REFERENCES staff, pr_id int REFERENCES procedures, start_time timestamp, end_time timestamp, description varchar(500), primary key(ph_id));

create table procedure_history(ph_id int REFERENCES patient_history, s_id int REFERENCES staff);

create table ward(p_id int REFERENCES patient, d_id int REFERENCES hospital_department, arrival timestamp, departure timestamp, cost_per_day numeric);

create table medications(m_id serial, name varchar(30), purpose varchar(100), cost numeric, primary key(m_id));

create table prescribed(ph_id int REFERENCES patient_history, m_id int REFERENCES medications, dosage varchar(15));

create table bills(b_id serial, p_id int REFERENCES patient, start_date timestamp, end_date timestamp, total_cost numeric, total_paid numeric, primary key (b_id));

GRANT ALL PRIVILEGES ON ALL TABLES IN Schema public TO public;
