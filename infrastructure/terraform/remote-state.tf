terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "bptech"

    workspaces {
      name = "aws-recipe-account"
    }
  }
}