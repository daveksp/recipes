resource "aws_kms_key" "rds_key" {
  description = "kms key for database credentials"
}

resource "aws_db_instance" "recipe-database" {
    #count                    = length(var.availability_zones)
    allocated_storage        = 8
    storage_type             = "gp2"
    engine                   = "mysql"
    engine_version           = "8.0"
    #engine_version           = "5.7"
    instance_class           = "db.t3.micro"
    identifier               = "recipe-db"
    username                 = "apiUser"
    password                 = "dbpassword"
    parameter_group_name     = "default.mysql8.0" 
    #parameter_group_name     = "default.mysql5.7" 
    db_name                  = "recipesApiDb"  

    vpc_security_group_ids   = [aws_security_group.rds.id]
    
    db_subnet_group_name     = aws_db_subnet_group.recipe_db_subnet_group.name

    skip_final_snapshot      = true
    publicly_accessible      = true  
}



