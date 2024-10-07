
variable "GOOGLE_CLOUD_PROJECT_ID" {
  description = "ID of your google cloud project"
  type = string
}

variable "GOOGLE_CLOUD_REGION" {
  description = "Region that your google cloud project is hosted in"
  type = string
}

variable "GOOGLE_CLOUD_BUCKET_NAME" {
  description = "Bucket name you want to add csv file to"
  type = string
}

variable "GOOGLE_CLOUD_BUCKET_STORAGE_CLASS" {
  description = "Class of your GCS bucket"
  type = string
  default = "STANDARD"
}

variable "BQ_DATASET_ID" {
  description = "ID of your bigquery dataset"
  type = string
}

