# Configure the AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "ca-central-1" # Replace with your desired region
}

# Launch an EC2 instance
resource "aws_instance" "example" {
  ami                    = "ami-055943271915205db" # Replace with your desired AMI ID
  instance_type          = "t2.micro"
  key_name               = "Django" # Replace with your key pair name

  tags = {
    Name = "Test EC2 Instance"
  }
}