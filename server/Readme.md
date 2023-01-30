Install MySQL by running the following command in the terminal: 
sudo apt install mysql-server

After the installation is complete, start the MySQL service by running: 
sudo systemctl start mysql

To secure the MySQL installation, run the following command: 
sudo mysql_secure_installation

You will be prompted to set a root password, answer Y to all the questions.

Log in to MySQL as the root user: 
mysql -u root -p

Create a new user for your project by running this command: 
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';

Create a new database for your project by running this command: 
CREATE DATABASE your_dbname;

Grant the user all privileges on the new database by running this command: GRANT ALL PRIVILEGES ON your_dbname.* TO 'your_username'@'localhost';

You can check the user and database are created by running command 
SHOW DATABASES; and SELECT user,host FROM mysql.user;

Now, in the code, you need to replace the following line with your mysql credentials

engine = create_engine("dialect+driver://user:password@host:port/dbname")
Make sure the python-mysqldb package is installed by running 
sudo apt install python-mysqldb

You can check if the mysql is working by running 
sudo service mysql status

Now, you can run your project and test the api's