# URL Shortener API Documentation

## Overview

This project implements a basic URL shortener API using FastAPI and PostgreSQL. The API provides two main endpoints:

## Endpoints

POST /shorten: Accepts a long URL and returns a shortened URL.
GET /{short_code}: Redirects to the original URL associated with the given short code.


## Project Structure

main.py: Contains the FastAPI application with the defined endpoints.
requirements.txt: Lists the dependencies for the project.


## Prerequisites

Python 3.7 or later
PostgreSQL


## Installation
1. Open command line and install requirements.
2. Open psql command line and set up the database and user

### Install requirements

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Set Up PostgreSQL

```
psql -U postgres
CREATE DATABASE url_shortener;
CREATE USER shortener_user WITH ENCRYPTED PASSWORD 'shortener_password';
GRANT ALL PRIVILEGES ON DATABASE url_shortener TO shortener_user;
\c url_shortener
CREATE TABLE urls (
                short_code TEXT PRIMARY KEY,
                original_url TEXT NOT NULL
                );
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE urls TO shortener_user;
```
### Run the Application

```
python main.py
```