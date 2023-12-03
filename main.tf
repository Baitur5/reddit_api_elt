terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-1"
}

resource "aws_redshiftserverless_namespace" "namespaces" {
  namespace_name = var.namespace_name
}

resource "aws_redshiftserverless_workgroup" "subreddit" {
  namespace_name = aws_redshiftserverless_namespace.namespaces.id
  workgroup_name = var.workgroup_name
  publicly_accessible = "true"
}


# Create S3 bucket
resource "aws_s3_bucket" "reddit_bucket" {
  bucket = var.s3_bucket
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

resource "aws_s3_bucket_ownership_controls" "own_control" {
  bucket = aws_s3_bucket.reddit_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "acl" {
  depends_on = [aws_s3_bucket_ownership_controls.own_control]

  bucket = aws_s3_bucket.reddit_bucket.id
  acl    = "private"
}