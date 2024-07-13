# ########### VPC ###########
resource "aws_vpc" "recipe_vpc" {
  cidr_block                 = "10.0.0.0/16"
  instance_tenancy           = "default"
  enable_dns_support         = true    # gives an internal domain name
  enable_dns_hostnames       = true   # gives an internal host name

  tags = {
    Name                     = "general"
    Project                  = "general"
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id                     = aws_vpc.recipe_vpc.id
  tags = {
    Name                     = "general-igw"
    Project                  = "general"
  }
}


# ########### SUBNETS ###########
resource "aws_subnet" "public_subnets" {
  count                      = length(var.availability_zones)
  vpc_id                     = aws_vpc.recipe_vpc.id
  cidr_block                 = "10.0.${count.index + 1}.0/24"
  availability_zone          = var.availability_zones[count.index]
  map_public_ip_on_launch    = true

  tags = {
    Name                     = "public-${var.availability_zones[count.index]}"
    Project                  = "general"
  }
}

resource "aws_subnet" "private_subnets" {
  count                      = length(var.availability_zones)
  vpc_id                     = aws_vpc.recipe_vpc.id
  cidr_block                 = "10.0.${count.index + 4}.0/24"
  availability_zone          = var.availability_zones[count.index]
  map_public_ip_on_launch    = false

  tags = {
    Name                     = "private-${var.availability_zones[count.index]}"
    Project                  = "Recipe API"
  }
}


resource "aws_db_subnet_group" "recipe_db_subnet_group" {
  name                       = "recipe-db-subnet-group"
  subnet_ids                 = [aws_subnet.public_subnets[0].id, aws_subnet.public_subnets[1].id]

  tags = {
    Name                     = "Recipe Database Subnet Group"
    Project                  = "Recipe API"
  } 
}


resource "aws_subnet" "restrict_subnets" {
  count                      = length(var.availability_zones)
  vpc_id                     = aws_vpc.recipe_vpc.id
  cidr_block                 = "10.0.${count.index + 7}.0/24"
  availability_zone          = var.availability_zones[count.index]
  map_public_ip_on_launch    = false

  tags = {
    Name                     = "restrict-${var.availability_zones[count.index]}"
    Project                  = "general"
  }
}


# ########### NAT GATEWAY ###########
resource "aws_eip" "nat_gateway_eip" {
  vpc                        = true
}



resource "aws_nat_gateway" "nat_gateway" {
  #count                      = length(var.availability_zones)
  subnet_id                  = aws_subnet.public_subnets[0].id
  allocation_id              = aws_eip.nat_gateway_eip.id  

  tags = {
    #Name                     = "Nat Gateway-${var.availability_zones[count.index]}"
    Name                     = "Nat Gateway-Recipe"
    Project                  = "Recipe"
    Environment              = "production"
  }
}



# ########### ROUTE TABLE ###########
resource "aws_route_table" "public_route_table" {
  vpc_id                     = aws_vpc.recipe_vpc.id

  route {
    cidr_block               = "0.0.0.0/0"
    gateway_id               = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name                     = "recipe_public_route_table"
    Project                  = "Recipe API"
  }
}

resource "aws_route_table" "private_route_table" {
  vpc_id                     = aws_vpc.recipe_vpc.id

  route {
    cidr_block               = "0.0.0.0/0"
    gateway_id               = aws_nat_gateway.nat_gateway.id
  }

  tags = {
    Name                     = "recipe_private_route_table"
    Project                  = "Recipe API"
  }
}


resource "aws_route_table" "restrict_route_table" {
  vpc_id                     = aws_vpc.recipe_vpc.id

  route {
    cidr_block               = "0.0.0.0/0"
    gateway_id               = aws_nat_gateway.nat_gateway.id
  }

  tags = {
    Name                     = "recipe_restrict_route_table"
    Project                  = "Recipe API"
  }
}

resource "aws_route_table_association" "public_association" {
  count                      = length(var.availability_zones)
  route_table_id             = aws_route_table.public_route_table.id
  subnet_id                  = aws_subnet.public_subnets[count.index].id
}

resource "aws_route_table_association" "private_association" {
  count                      = length(var.availability_zones)
  route_table_id             = aws_route_table.private_route_table.id
  subnet_id                  = aws_subnet.private_subnets[count.index].id
}

resource "aws_route_table_association" "restrict_association" {
  count                      = length(var.availability_zones)
  route_table_id             = aws_route_table.restrict_route_table.id
  subnet_id                  = aws_subnet.restrict_subnets[count.index].id
}
