# Terraform configuration goes here
provider "google" {
#  credentials = file("/home/admin/ilgabrie/paas-bigdata-terraform-key.json")
  project = var.project
  region  = var.region
  zone    = var.zone
}

// Terraform plugin for creating random ids
resource "random_id" "instance_id" {
   byte_length = 8
}

#// Enable googleapis
#resource "google_project_service" "compute_api" {
#  project = var.project
#  service = "compute.googleapis.com"
#  disable_on_destroy = false
#}
#resource "google_project_service" "oslogin_api" {
#  project = var.project
#  service = "oslogin.googleapis.com"
#  disable_on_destroy = false
#}
#resource "google_project_service" "iam_api" {
#  project = var.project
#  service = "iam.googleapis.com"
#  disable_on_destroy = false
#}

####################################################################################
# Networking
####################################################################################
# Could be implemented an own network and sub network

data "google_compute_network" "dataproc_network" {
  name = "ilgabrie-vpc"
}
###################################################################################
# Dataproc
###################################################################################

resource "google_dataproc_workflow_template" "dev_template" {
  name = "dev-template"
  location = "europe-west3"
  placement {
    managed_cluster {
      cluster_name = "dev-cluster"
      config {
        gce_cluster_config {
          zone = "europe-west3-b"
        }
        master_config {
          num_instances = 1
          machine_type = "n1-standard-8"
          disk_config {
            boot_disk_type = "pd-standard"
            boot_disk_size_gb = 50
          }
        }
        software_config {
          image_version = "2.0.11-debian10"
        }
      }
    }
  }
  jobs {
    step_id = "dev-job"
    pyspark_job {
      main_python_file_uri = "gs://tsi-ucf-data/scripts/test_bigquery.py"
      jar_file_uris = ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"]
    }
  }
}
