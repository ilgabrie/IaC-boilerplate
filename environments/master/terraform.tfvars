# Variable values go here
#
# WARNING: Since these values often contain sensitive information, don't commit
# this file to version control.

#Enter your project ID
project = "paas-bigdata-1000047987-288310"

#Staging bucket, used used to stage files, such as Hadoop jars, between client machines and the cluster.
staging_bucket = "terraform"

#Enter your region
region = "europe-west3"

# replace with n1-standard-1 if you only want to test
machine_types = {
  "master" = "n1-standard-2"
  "worker" = "n1-standard-2"
}

cidrs = [ "10.0.0.0/16", "10.1.0.0/16" ]

# replace with a service account you want to be used in the VMs to be created
# leave in blank if you want to use a new service account
service_account = "terraform@paas-bigdata-1000047987-288310.iam.gserviceaccount.com"

