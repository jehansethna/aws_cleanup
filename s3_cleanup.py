import boto3
from datetime import datetime
import pytz
import configparser

# Get the current time with UTC adjusted.
def get_current_date():
  present = datetime.now()
  utc = pytz.UTC
  present = utc.localize(present)
  return present

# Calculate the difference between two dates in days format.
def days_between(d1,d2):
  return abs((d2 - d1).days)

# Delete buckets created within the last 10 days.
def display_existing_buckets(presentdate, s3_delete_bucket_name):
  # Let's use Amazon S3
  s3 = boto3.resource('s3')

  bucket_count = 0
  
  print "Existing buckets are :"
  # Making s3 call to get list of buckets
  for bucket in s3.buckets.all():
    if s3_delete_bucket_name in bucket.name:
      bucket_count = bucket_count + 1
      print "Bucket Name - ", bucket.name, " -> ", days_between(presentdate,bucket.creation_date)
  print "The number of buckets with username", s3_delete_bucket_name, "is", bucket_count

def delete_buckets(presentdate, s3_delete_bucket_name):
  print "Deleting buckets created with 5 days"
  
  s3 = boto3.resource('s3')

  for bucket in s3.buckets.all():
    if s3_delete_bucket_name in bucket.name:
      if days_between(presentdate, bucket.creation_date) < 5:
        print "Deleting bucket - ", bucket.name
        bucket.delete()

def create_bucket(s3_delete_bucket_name):
  print "Creating 1 new bucket"
  s3 = boto3.resource('s3')
  bucket = s3.Bucket(s3_delete_bucket_name)
  response = bucket.create(ACL='public-read', CreateBucketConfiguration={'LocationConstraint':'us-west-2'})  

def main():
  # print "In Main of s3_cleanp.py"
  presentdate = get_current_date()
  #print "The current date is ", presentdate.strftime("%Y-%m-%d")
 
  config = configparser.ConfigParser()
  config.read('configuration.ini')
  s3_delete_bucket_name = config['S3']['Username']
  print "Name whose buckets need to be deleted - ", s3_delete_bucket_name 
  
  display_existing_buckets(presentdate, s3_delete_bucket_name)
  create_bucket(s3_delete_bucket_name)
  display_existing_buckets(presentdate, s3_delete_bucket_name)
  delete_buckets(presentdate, s3_delete_bucket_name)
  display_existing_buckets(presentdate, s3_delete_bucket_name)

if __name__ == '__main__':
  main()
