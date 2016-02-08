import argparse
from pprint import pprint
import boto.ec2

access_key = ''
secret_key = ''

def get_ec2_instances(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    reservations = ec2_conn.get_all_reservations()
    #for reservation in reservations:    
    #    print region+':',reservation.instances,
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
      #pprint(i.__dict__)
      if i.platform is None:
        platform = 'linux'
      else:
        platform = 'windows'
      p_env_label = [ 'PROD', 'UAT', 'STAG', 'Stag', 'prod', 'uat' ]
      np_env_label = [ 'QA', 'DEV', 'dev' ]
      if any(env in p_env_label for env in i.tags):
        environment = 'PROD/UAT'
      elif any(env in np_env_label for env in i.tags):
        environment = 'DEV'
      else:
        environment = 'Unknown'
      #mytags = str(i.tags)
      #list_of_words = mytags.split()
      #iname = list_of_words[list_of_words.index("Name") + 1]
      print(i.id, i.instance_type, i.region, environment, platform, i.tags)

    #for vol in ec2_conn.get_all_volumes():
    #    print region+':',vol.id

def main():
    regions = [ 'us-east-1','us-west-1','us-west-2','eu-west-1','sa-east-1',
                'ap-southeast-1','ap-southeast-2','ap-northeast-1', 'eu-central-1', 'ap-northeast-2' ]
    parser = argparse.ArgumentParser()
    parser.add_argument('access_key', help='Access Key');
    parser.add_argument('secret_key', help='Secret Key');
    args = parser.parse_args()
    global access_key
    global secret_key
    access_key = args.access_key
    secret_key = args.secret_key
    
    for region in regions: get_ec2_instances(region)

if  __name__ =='__main__':main()
