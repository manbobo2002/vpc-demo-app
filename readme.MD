# Instructions to use the application
## Data source
https://population.un.org/wpp/

1. Install python package 
pip3 install -r requirements.txt

1. load the databse in your database using loaddatabase/database_populate.py. Update below info.

#db_name = 'population'

rds_host = os.environ['DATABASE_HOST']
db_user = os.environ['DATABASE_USER']
password = os.environ['DATABASE_PASSWORD']
db_name = os.environ['DATABASE_DB_NAME']

1. Update the db.py with the database information. 

rds_host = os.environ['DATABASE_HOST']
db_user = os.environ['DATABASE_USER']
password = os.environ['DATABASE_PASSWORD']
db_name = os.environ['DATABASE_DB_NAME']

1. Run application 
python application.py

#!/bin/bash 
yum update -y
yum install -y httpd 
systemctl start httpd
systemctl enable httpd
yum install -y python3
mkdir /var/www/html/appcode
chown ec2-user /var/www/html/appcode
chmod -R o+r /var/www/html/appcode
cd /var/www/html/appcode
aws s3 cp s3://testbucketforsrikola/vpcapp.zip .
unzip vpcapp.zip
cd /var/www/html/appcode/vpcapp
python3 get-pip.py --user
pip install -r requirements.txt
vi ~/.bash_profile
export DATABASE_HOST=studentrdscluster.cluster-c3cm7swdxlpa.us-west-2.rds.amazonaws.com
export DATABASE_USER=admin
export DATABASE_PASSWORD=test12345
export DATABASE_DB_NAME=Population
source ~/.bash_profile
python3 db.py
python3 application.py