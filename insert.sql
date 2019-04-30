INSERT INTO patient(f_name, l_name, age, dob, address, phone_number, sex, height, weight) VALUES('John', 'Doe', 27, '1990-01-01', '801 National R W', '765-277-0909', 'M', 1.88, 70.3);
INSERT INTO patient(f_name, l_name, age, dob, address, phone_number, sex, height, weight) VALUES('Elizabeth', 'Smith', 15, '2004-07-27', '517 N 5th St', '765-277-1514', 'F', 1.3, 90.3);
INSERT INTO patient(f_name, l_name, age, dob, address, phone_number, sex, height, weight) VALUES('Zach', 'Taylor', 69, '1950-01-01', '20 S Blvd', '765-962-7564', 'M', 1.9, 100);
INSERT INTO patient(f_name, l_name, age, dob, address, phone_number, sex, height, weight) VALUES('Susan', 'Anthony', 3, '2016-01-01', '9 N 9th', '765-914-2775', 'F', 0.5, 20);
INSERT INTO patient(f_name, l_name, age, dob, address, phone_number, sex, height, weight) VALUES('Bill', 'Radford', 80, '1939-01-01', '1755 West Main St', '765-855-2309', 'M', 2.1, 150);


INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('cardiology', 'CST217', 50.0);
INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('Acute Rehab', '4th Floor', 100.0);
INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('Emergency Room', '1st Floor', 1500.0);
INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('Psych Ward', '6th Floor', 500.0);
INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('Mother Baby', '3rd Floor', 250.0);
INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('ICU', '2nd Floor', 1000.0);
INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('Nuerology', '7th Floor', 2000.0);
INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('Outpatient', '1st Floor', 0.0);
INSERT INTO hospital_department (dept_name, office_info, visit_cost) VALUES ('Orthopedics', '1st Floor', 100.0);



INSERT INTO staff (f_name, l_name, address, phone_number, s_type, d_id, username, password) VALUES ('Alice', 'White', '120 Broadway', '911', 'admin',1, 'admin', 'admin');
INSERT INTO staff (f_name, l_name, address, phone_number, s_type, d_id, username, password) VALUES ('Christian', 'Wilkins', '15 South 20th', '765-962-5419', 'admin',2, 'admin', 'admin');

INSERT into insurance_company (name, policy_id, phone_number) VALUES ('Medicaid', '12345', '812-567-2859');
INSERT into insurance_company (name, policy_id, phone_number) VALUES ('Medicare', '72752', '587-999-2859');
INSERT into insurance_company (name, policy_id, phone_number) VALUES ('Health For All', '10116', '342-901-9959');
INSERT into insurance_company (name, policy_id, phone_number) VALUES ('Wellness Mutual', '67548', '765-987-1423');

INSERT into procedures (name, cost, facility, per_hour) VALUES ('MRI', 500.0, 'Outpatient', 'N');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('Cat Scan', 1000.0, 'Outpatient', 'N');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('X-Ray', 500.0, 'Outpatient', 'N');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('Appendectomy', 250.0, 'Emergency Room', 'Y');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('Coronary Bypass', 1000.0, 'Cardiology', 'Y');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('Brain Surgery', 1500.0, 'Neurology', 'Y');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('Triple Bypass', 1500.0, 'Cardiology', 'N');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('ACL Reconstruction', 500.0, 'Orthodpedics', 'N');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('UCL Reconstruction', 500.0, 'Orthopedics', 'N');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('C-Section', 1000.0, 'Mother Baby', 'Y');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('Natural Birth', 500.0, 'Mother Baby', 'Y');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('Liver Transplant', 2500.0, 'Outpatient', 'Y');
INSERT into procedures (name, cost, facility, per_hour) VALUES ('Kidney Transplant', 3000.0, 'Outpatient', 'Y');

INSERT into medications (name, purpose, cost) VALUES ('Depakote', 'Anti-Epileptic drug to prevent seizures', 100.0);
INSERT into medications (name, purpose, cost) VALUES ('Keppra', 'Anti-Epileptic drug to prevent seizures', 200.0);
INSERT into medications (name, purpose, cost) VALUES ('Hydrocodone', 'Pain killing drug prescribed after procedures', 500.0);
INSERT into medications (name, purpose, cost) VALUES ('Tylenol-3', 'Pain killing drug', 100.0);
INSERT into medications (name, purpose, cost) VALUES ('Carvedilol', 'Used for congestive heart failure', 500.0);
INSERT into medications (name, purpose, cost) VALUES ('Metoprolol', 'Used for congestive heart failure', 100.0);
INSERT into medications (name, purpose, cost) VALUES ('Depakote', 'Anti-Epileptic Drug to prevent seizures', 100.0);
INSERT into medications (name, purpose, cost) VALUES ('Lipitor', 'Useed to lower cholesterol, common for patients w/ kidney failure', 500.0);
INSERT into medications (name, purpose, cost) VALUES ('Acetylcysteine', 'Used for patients with liver failure', 100.0);
INSERT into medications (name, purpose, cost) VALUES ('Aspirin', 'Helpful for headaches, or for someone who had a heart attack', 100.0);
INSERT into medications (name, purpose, cost) VALUES ('Ibuprofen', 'Pain manager', 25.0);
INSERT into medications (name, purpose, cost) VALUES ('Oxycodone', 'Strong prescription pain killer', 100.0);
INSERT into medications (name, purpose, cost) VALUES ('Avapro', 'Treats high-blood pressure', 100.0);
