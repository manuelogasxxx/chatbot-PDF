/*
This file contains the DB from PostgreSQL used in this project

There are some tables

A diagram is shown with the relations
*/

CREATE DATABASE chatbot_pdf;

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(16) UNIQUE NOT NULL CHECK (char_length(username)>=4),
    register_date TIMESTAMP NOT NULL, 
    UNIQUE(username)
);

CREATE TABLE chats(
    chat_id SERIAL PRIMARY KEY,
    fk_user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL CHECK (char_length(title)>=1),
    creation_date TIMESTAMP,
    FOREIGN KEY (fk_user_id) REFERENCES users(user_id)
);

CREATE TABLE documents(
    document_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_route VARCHAR(255) NOT NULL,
    fk_user_id INT NOT NULL,
    load_date TIMESTAMP,
    FOREIGN KEY (fk_user_id) REFERENCES users(user_id)
);

CREATE TABLE chats_documents(
    fk_chat_id INT NOT NULL,
    fk_document_id INT NOT NULL,
    PRIMARY KEY (fk_chat_id,fk_document_id), 
    FOREIGN KEY (fk_chat_id) REFERENCES chats(chat_id)
);

CREATE TABLE types(
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(10)
);

CREATE TABLE messages(
    message_id  SERIAL PRIMARY KEY,
    fk_chat_id INT NOT NULL,
    content TEXT,
    sent_date TIMESTAMP

);
--Auxiliar table




