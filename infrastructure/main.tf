terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.GOOGLE_CLOUD_PROJECT_ID
  region = var.GOOGLE_CLOUD_REGION
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "google-cloud-bucket" {
  name          = var.GOOGLE_CLOUD_BUCKET_NAME  # Concatenating DL bucket & Project name for unique naming
  location      = var.GOOGLE_CLOUD_REGION

  # Optional, but recommended settings:
  storage_class = var.GOOGLE_CLOUD_BUCKET_STORAGE_CLASS
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 60  // days
    }
  }

  force_destroy = true
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET_ID
  project    = var.GOOGLE_CLOUD_PROJECT_ID
  location   = var.GOOGLE_CLOUD_REGION
}

