import argparse
from pprint import pprint
import boto.ec2

access_key = ''
secret_key = ''

def get_ec2_instances(region,prod_env_tags,nonprod_env_tags):
    ec2_conn = boto.ec2.connect_to_region(region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    reservations = ec2_conn.get_all_reservations()
    instances = [instance for r in reservations for instance in r.instances]
    for instance in instances:
      #pprint(i.__dict__)
      if instance.platform is None:
        platform = 'linux'
      else:
        platform = 'windows'
      if any(env in prod_env_tags for env in instance.tags):
        environment = 'PROD/UAT'
      elif any(env in nonprod_env_tags for env in instance.tags):
        environment = 'DEV'
      else:
        environment = 'Unknown'
      instance.id = str(instance.id)
      instance.instance_type = str(instance.instance_type)
      instance.tags = str(instance.tags)
      print instance.id, instance.instance_type, instance.placement, environment, platform, instance.tags
      #print(i.id, i.instance_type, i.region)

def main():
    regions = [ 'us-east-1','us-west-1','us-west-2','eu-west-1','sa-east-1',
                'ap-southeast-1','ap-southeast-2','ap-northeast-1', 'eu-central-1', 'ap-northeast-2' ]
    prod_env_tags = [ 'PROD', 'UAT', 'STAG', 'Stag', 'prod', 'uat' ]
    nonprod_env_tags = [ 'QA', 'DEV', 'dev' ]
    parser = argparse.ArgumentParser()
    parser.add_argument('access_key', help='Access Key');
    parser.add_argument('secret_key', help='Secret Key');
    args = parser.parse_args()
    global access_key
    global secret_key
    access_key = args.access_key
    secret_key = args.secret_key
    
    print("EC2 ID, Instance type, AZ, Env, Platform, Tags")
    for region in regions: get_ec2_instances(region,prod_env_tags,nonprod_env_tags)

if  __name__ =='__main__':main()
