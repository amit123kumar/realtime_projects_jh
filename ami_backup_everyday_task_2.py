from __future__ import print_function
from datetime import datetime as DateTime, timedelta as TimeDelta
from dateutil.parser import parse

import datetime
import boto3
import time
import string
import random

#my variable
InstanceId='i-0f3ea37f463e74c8e'
#Region='us-west-2'+





timestamp = time.asctime( time.localtime(time.time()) )
#print('present time is ' + str(timestamp))
print(str(timestamp))
time=str(timestamp)
time = time.replace(' ', '_', 20)
time = time.replace(':', '_', 20)
imagename="AMI_Jenkins_ON_"+str(time)+"_"+str(random.randint(1,10134))
print("my image name is " + imagename)
client = boto3.client('ec2')
#print('Loading method')
print(timestamp)
def lambda_handler(event, context):
    #creating AMI
    print('creating image started....')
    img_response=client.create_image(InstanceId=InstanceId,Name=imagename,NoReboot=False)
    print('successfully image created....')
    print("response on ami create " + str(img_response))
    print("ami image id :" + str(img_response['ImageId']))
    my_image_id = str(img_response['ImageId'])
    
    now = datetime.datetime.now()
    print (str(now.strftime("%d/%m/%y")))
    created_date = str(now.strftime("%d/%m/%y"))
    
    date_1 = DateTime.today() 
    end_date = date_1 + TimeDelta(days=3)
    end_date = str(end_date.strftime("%d/%m/%y"))
    response1 = client.create_tags(Resources=[my_image_id], Tags=[{'Key': 'Server_Name', 'Value': 'jenkins'},{'Key': 'Created_Date', 'Value': created_date},{'Key': 'Deletion_Date', 'Value': end_date}]) 
    #print('tags creation status :' + str(response1))
    date1 = parse(created_date)
    #date2 = parse(end_date)
    #count = str(date2 - date1)
    #diff_days= int(count[0])
    #print ('no of days :' + str(diff_days))
    
    
    #print date2 > date2
    
    response = client.describe_images(Filters=[{'Name': 'tag:Server_Name','Values': ['jenkins']}])['Images']
    #print ('describe : :' + str(response))
    for k in response:
        #print ('describeing tags: :' + str(k['Tags']))
        #print ('describeing dates : :' + str(k['Tags']))
         for t in k['Tags']:
               #print ('describeing dates : :' + str(t))
               #print('keyz....' + t['Key'])
               if(t['Key'] == 'Deletion_Date'):
                   ami_date= t['Value']
                   preasentdate = parse(created_date)
                   print('ami date deletion: ' + ami_date )
                   ami_date = parse(ami_date)
                   count = str(preasentdate- ami_date )
                   print("couning here :" + count )
                   if(count[0].isdigit()):
                       diff_days= int(count[0])
                   else:
                       diff_days= int(count[0]+count[1])
                  
                   print ('no of days befor deleting :' + str(diff_days))
                   #print('details here......' + str(k))
                   if(diff_days > 2):
                       print('details here......' + k['ImageId'])
                       image_Id_to_be_deleted = k['ImageId']
                       response = client.deregister_image(ImageId=image_Id_to_be_deleted)
                       print('AMI IMage with ......' + k['ImageId'] + "unregisterd successfully")
    
