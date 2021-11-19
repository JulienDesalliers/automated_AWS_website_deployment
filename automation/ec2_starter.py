import boto3

def create_ec2_instance(instance_type, name):
    user_data = '''#!/bin/bash
cd /home/ubuntu
mkdir flask-server
cd flask-server

sudo apt-get update
python3 --version
sudo apt install python3-pip -y
sudo apt install python3.8-venv
python3 -m venv venv
. venv/bin/activate
sudo pip install flask


echo "from flask import Flask" >> app.py
echo "app = Flask(__name__)" >> app.py

echo "@app.route(\'/\')" >> app.py
echo "def health_check():" >> app.py
echo "    return \'<p>health check</p>\'" >> app.py

echo "@app.route(\'/cluster1\')" >> app.py
echo "def cluster1():" >> app.py
echo "    return \'<p>Hello from $(ec2metadata --instance-id)</p>\'" >> app.py

echo "@app.route(\'/cluster2\')" >> app.py
echo "def cluster2():" >> app.py
echo "    return \'<p>Hello from $(ec2metadata --instance-id)</p>\'" >> app.py

echo "app.run(host=\'0.0.0.0\', port=80)" >> app.py

sudo python3 app.py
    '''
    try:
        ressource_ec2 = boto3.client("ec2")
        instance = ressource_ec2.run_instances(
            ImageId="ami-09e67e426f25ce0d7",
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName="dev",
            SecurityGroups = ['launch-wizard-1'],
            UserData = user_data,
        )
        ec2 = boto3.resource('ec2')
        ec2.create_tags(Resources=[instance['Instances'][0]['InstanceId']], Tags=[
            {
                'Key': 'Name',
                'Value': name,
            },
        ])
        instance['Instances'][0]['InstanceId']
        return instance
    except Exception as e:
        print(e)


ec2_1 = create_ec2_instance("m4.large", "ec2_1")