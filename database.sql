create database form;
use form;
CREATE TABLE users (
    id int PRIMARY KEY auto_increment,
    name varchar(50) NOT NULL,
    email varchar(50),
    message varchar(50),
    gender varchar(50),
    subscribe boolean
    );
    
select * from users;