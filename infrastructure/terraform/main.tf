provider "aws" {
  version                    = "~> 5.44.0"
  region                     = "us-east-1"
#  shared_config_files        = ["/Users/davidpinheiro/.aws/config"]
#  shared_credentials_files   = ["/Users/davidpinheiro/.aws/credentials"]
#  profile                    = "bptec"
}


# we create a new key-pair locally, then we import the terraform-aws key that we have created through
# the command line: ssh-keygen -f terraform-aws -t rsa
# import public key on AWS console
# mv terraform-aws ~/.ssh
# ssh -i ~/.ssh/terraform-aws ec2-user@something.something

########### INSTANCES ###########



# ########### LOAD BALANCERS ###########

resource "aws_elb" "api_elb" {
  name = "api-elb"
  security_groups = ["${aws_security_group.demosg1.id}"]
  subnets = [
    aws_subnet.public_subnets[0].id, 
    aws_subnet.public_subnets[1].id
  ]
  cross_zone_load_balancing   = true
  
  health_check {
    healthy_threshold = 2
    unhealthy_threshold = 2
    timeout = 3
    interval = 30
    target = "HTTP:8089/health_check"
  }
  listener {
    lb_port = 80
    lb_protocol = "http"
    instance_port = "8089"
    instance_protocol = "http"
  }
}

resource "aws_launch_configuration" "api-config" {
  name_prefix = "recipe-api"
  #image_id = "ami-08a0d1e16fc3f61ea" 
  image_id = "ami-05a83999674d8b76a"
  instance_type = "t3.medium"
  key_name = var.instance_key_pair_name
  security_groups = [ "${aws_security_group.demosg1.id}" ]
  associate_public_ip_address = true
  user_data = "${file("resources/data.sh")}"
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "web" {
  name = "${aws_launch_configuration.api-config.name}-asg"
  min_size             = 1
  desired_capacity     = 1
  max_size             = 2
  
  health_check_type    = "ELB"
  load_balancers = [
    "${aws_elb.api_elb.id}"
  ]
  launch_configuration = "${aws_launch_configuration.api-config.name}"
  enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupTotalInstances"
  ]
  metrics_granularity = "1Minute"
  vpc_zone_identifier  = [
    aws_subnet.public_subnets[0].id, 
    aws_subnet.public_subnets[1].id
  ]
  
  # Required to redeploy without an outage.
  lifecycle {
    create_before_destroy = true
  }
  tag {
    key                 = "Name"
    value               = "web"
    propagate_at_launch = true
  }
}