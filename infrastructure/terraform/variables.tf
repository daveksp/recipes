##### conditionals #####
variable "release_general" {
  description                = "Should release shared infrastructure"
  type                       = number
  default                    = 0
}

variable "release_website" {
  description                = "Should release website infrastructure"
  type                       = number
  default                    = 1
}

##### network #####
variable "availability_zones" {
  description                = "List of available AZs"
  type                       = list(string)
  default                    = ["us-east-1a", "us-east-1b"]
  # default                    = ["us-east-2a", "us-east-2b", "us-east-2c"]
}

variable "primary_dns" {
  description                = "primary dns"
  type                       = string
  default                    = "dkspinheiro.com"
}

variable "regions" {
  description                = "regions"
  type                       = map
  default                    = {
    "primary" = "us-east-2"
  }
}

##### key pairs #####
variable "instance_key_pair_name" {
  description                = "key-pair access for ec2 instance"
  type                       = string
  default                    = "terraform"
}

variable "public_key" {
  type                       = string
  default                    = "terraform"
}

##### AMIs #####
variable "jenkins_ami" {
  description                = "ami for jenkins instance"
  type                       = string
  default                    = "ami-0752c09840d594e66"
}

variable "bastion_ami" {
  description                = "ami for bastions"
  type                       = string
  default                    = "ami-051dfed8f67f095f5"
}

variable "enable_s3_website" {
  description                = "should deploy s3 website"
  type                       = bool
  default                    = false                 
}