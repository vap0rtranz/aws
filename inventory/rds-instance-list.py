# this is an AWS inventory for RDS
# you must supply an AWS IAM keypair with Read to RDS across specified regions
# output is to STDOUT in white space delimited (except Tags are comma
# seperated)
# feel free to change the fields to any variable of the DBInstance boto class
# but please sanitize changes to these fields

import argparse
from pprint import pprint
import boto.rds
import unicodedata

access_key = ''
secret_key = ''

def get_rds_instances(region,fields):
    rds_conn = boto.rds.connect_to_region(region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    dbinstances = rds_conn.get_all_dbinstances()
    for instance in dbinstances:
      #pprint(i.__dict__)
# trying to use variable of class DBInstance as string to sanitize in loop fails 
      #for field in fields: 
        #instance."field" = str(instance."field")
      #  print(instance.field)
# stuck sanitizing each field
      instance.id = str(instance.id)
      instance.instance_class = str(instance.instance_class) 
      instance.engine = str(instance.engine)
      instance.multi_az = str(instance.multi_az)
      instance.availability_zone = str(instance.availability_zone)
      instance.allocated_storage = str(instance.allocated_storage)
      print instance.id, instance.instance_class, instance.engine, instance.multi_az, instance.availability_zone, instance.allocated_storage

def main():
# which regions to pull from
# note AZs for each region are included
    regions = [ 'us-east-1','us-west-1','us-west-2','eu-west-1','sa-east-1',
                'ap-southeast-1','ap-southeast-2','ap-northeast-1', 'eu-central-1', 'ap-northeast-2' ]
# which fields to print from DBInstance class attributes
    fields = [ 'id', 'instance_class', 'engine', 'multi_az', 'availability_zone', 'allocated_storage' ]
    parser = argparse.ArgumentParser()
    parser.add_argument('access_key', help='Access Key');
    parser.add_argument('secret_key', help='Secret Key');
    args = parser.parse_args()
    global access_key
    global secret_key
    access_key = args.access_key
    secret_key = args.secret_key
    
    print("DB ID, Instance class, Engine, MultiAZ, AZ, Storage")
    for region in regions: get_rds_instances(region,fields)

if  __name__ =='__main__':main()
