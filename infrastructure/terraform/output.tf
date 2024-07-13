# output "bastion-ips" {
#   value = aws_instance.bastion[0].public_ip
# }

# output "jenkins-ips" {
#   value = aws_instance.jenkins[0].private_ip
# }

output "rds_hostname" {
  description = "RDS instance hostname"
  value       = aws_db_instance.recipe-database.address
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.recipe-database.port
  sensitive   = true
}

output "rds_username" {
  description = "RDS instance root username"
  value       = aws_db_instance.recipe-database.username
  sensitive   = true
}

