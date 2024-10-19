locals {
  exp_generator_fname    = "${var.unique_identifier}_lambda_exp_generator"
  exp_generator_loggroup = "/aws/lambda/${local.exp_generator_fname}"
}

provider "aws" {
  region = var.aws_region
}

provider "archive" {}
