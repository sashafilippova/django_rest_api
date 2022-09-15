DROP TABLE if EXISTS eviction_records;

CREATE TABLE eviction_records (
    case_id varchar(16) NOT NULL,
    court varchar(30), 
    case_caption varchar(120),
    judge varchar(30),
    filed_date date NOT NULL,
    case_type varchar(16),
    amount int,
    disposition varchar(30),
    disposition_date date,
    plaintiff_name varchar(60),
    plaintiff_address text,
    plaintiff_attorney varchar(60),
    defendant_name varchar(60),
    defendant_address text, 
    defendant_attorney varchar(60),
    last_updated date,
    PRIMARY KEY (case_id)
);