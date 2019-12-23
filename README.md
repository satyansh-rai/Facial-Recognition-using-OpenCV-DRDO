# Web Application for DRDO

## Setup Instructions

 - Install mysql on your local machine
### Database setup 
 - Create a database 
    ``` sql
    CREATE DATABASE database_name;
    ```
 - Switch to the created database 
    ``` sql
    USE database_name;
    ```
 - Create users table with its columns 
 ``` sql
 CREATE TABLE users (id INT(11) AUTO_INCREMENT PRIMARY_KEY,
                    name VARCHAR(100),
                    email VARCHAR(100),
                    username VARCHAR(30),
                    password VARCHAR(100),
                    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

 ```

### Setup Python Environment
 - In a python3 environment install the requirements
    ``` shell
    pip3 install -r requirements.py
    ```


### Setup app.py
 - Point `app.config['MYSQL_PASSWORD']` to  the right root mysql password set during setup.
 - Point `app.config['MYSQL_DB']` to the `database_name`
  
### Start Application
 - Start application
    ``` shell
    python3 app.py
    ```