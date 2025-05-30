CREATE DATABASE neondb;
\c neondb;

CREATE TABLE application(
	name  varchar(30) PRIMARY KEY
);

CREATE TABLE transaction(
	transaction_id varchar(30) PRIMARY KEY,
	user_id varchar(30) not null,
	module varchar(20) not null,
	ip_address varchar(20) not null,
);


CREATE TABLE applicationtransaction(
	transaction_id varchar(30) ,
	application_name varchar(30),
	state varchar(20),
	timestamp timestamp not null,
	validate_result varchar(20),
	failed_reason varchar(30),
	account_type varchar(20),
	log_level  varchar(20),
	operation varchar(20),
	direction varchar(20),
	status_code integer,
	amount real,
	transaction_type varchar(20),
	realized_verifications varchar(30),
	latency integer,
	PRIMARY KEY (transaction_id, application_name),
	
	FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id),
	FOREIGN_KEY (application_name) REFERENCES application(name)
);
