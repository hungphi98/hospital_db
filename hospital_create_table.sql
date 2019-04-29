create table patient(p_id int, f_name varchar(30), l_name varchar(30), age int, dob DATE, address varchar(30), phone_number varchar(15), sex char(1), height numeric, weight numeric, primary key (p_id));

create table staff(s_id int, f_name varchar(30), l_name varchar(30), address varchar(30), phone_number varchar(15), s_type varchar(10), d_id int, primary key(s_id));

create table hospital_department(d_id int, dept_name varchar(50), office_info varchar(50), visit_cost numeric, primary key(d_id));

create table insurance_company(ip_id serial, name varchar(50), policy_id int, phone_number varchar(15), primary key(ip_id));

create table insured_by(p_id int, ip_id int, primary key(ip_id));

create table procedures(pr_id int, name varchar(30), cost numeric, facility varchar(30), pr_type varchar(10), primary key(pr_id));

create table patient_history(ph_id int, p_id int, s_id int, pr_id int, start_time timestamp, end_time timestamp, description varchar(500), primary key(ph_id));

create table procedure_history(ph_id int, s_id int, primary key ());

create table ward(p_id int, d_id int, arrival timestamp, departure timestamp, cost_per_day numeric);

create table medications(m_id serial, name varchar(30), purpose varchar(100), cost numeric, primary key(m_id));

create table prescribed(ph_id int, m_id int, dosage varchar(15), primary key());

create table bills(p_id int, b_id serial, start_date timestamp, end_date timestamp, total_cost numeric, total_paid numeric, primary key (b_id));

create table users(username VARCHAR(32), password VARCHAR(32), s_id serial, PRIMARY KEY(username));
