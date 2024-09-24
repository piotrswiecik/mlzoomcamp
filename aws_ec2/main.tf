provider "aws" {
  region  = "eu-central-1"
  profile = "ai"
}

resource "aws_instance" "ml_zoomcamp_instance" {
  ami               = "ami-0724e2337a36ed1b2" # Custom Ubuntu 24.04 LTS x86_64
  instance_type     = "t2.micro"
  availability_zone = "eu-central-1a"
  key_name          = "ml_zoomcamp_key"
  subnet_id = aws_subnet.ml_zoomcamp_vpc_main_subnet.id

  vpc_security_group_ids = [
    aws_security_group.ml_zoomcamp_sg_allow_ssh.id,
    aws_security_group.ml_zoomcamp_sg_allow_egress.id
  ]

  root_block_device {
    delete_on_termination = true
    volume_size           = 30
    volume_type = "gp3"
  }

  tags = {
    Name    = "ml_zoomcamp_instance"
    Project = "ml_zoomcamp"
  }
}

resource "aws_key_pair" "ml_zoomcamp_key" {
  key_name   = "ml_zoomcamp_key"
  public_key = file("~/.ssh/ml_zoomcamp_key.pub")

}

resource "aws_vpc" "ml_zoomcamp_vpc" {
  cidr_block = "172.16.0.0/16"

  tags = {
    Name    = "ml_zoomcamp_vpc"
    Project = "ml_zoomcamp"
  }
}

resource "aws_subnet" "ml_zoomcamp_vpc_main_subnet" {
  vpc_id                  = aws_vpc.ml_zoomcamp_vpc.id
  cidr_block              = "172.16.0.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name    = "ml_zoomcamp_vpc_main_subnet"
    Project = "ml_zoomcamp"
  }
}

resource "aws_security_group" "ml_zoomcamp_sg_allow_ssh" {
  name   = "allow_ssh"
  vpc_id = aws_vpc.ml_zoomcamp_vpc.id

  tags = {
    Name    = "ml_zoomcamp_sg_allow_ssh"
    Project = "ml_zoomcamp"
  }
}

resource "aws_security_group" "ml_zoomcamp_sg_allow_egress" {
  name   = "allow_egress"
  vpc_id = aws_vpc.ml_zoomcamp_vpc.id

  tags = {
    Name    = "ml_zoomcamp_sg_allow_egress"
    Project = "ml_zoomcamp"
  }
}

resource "aws_vpc_security_group_ingress_rule" "ml_zoomcamp_sg_allow_ssh" {
  security_group_id = aws_security_group.ml_zoomcamp_sg_allow_ssh.id
  cidr_ipv4 = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 22
  to_port           = 22
}

resource "aws_internet_gateway" "ml_zoomcamp_igw" {
  vpc_id = aws_vpc.ml_zoomcamp_vpc.id

  tags = {
    Name    = "ml_zoomcamp_igw"
    Project = "ml_zoomcamp"
  }
}

resource "aws_vpc_security_group_egress_rule" "ml_zoomcamp_sg_allow_all" {
  security_group_id = aws_security_group.ml_zoomcamp_sg_allow_egress.id
  cidr_ipv4 = "0.0.0.0/0"
  ip_protocol       = "-1"
  from_port = 0
  to_port = 0
}

resource "aws_route_table" "ml_zoomcamp_rt" {
  vpc_id = aws_vpc.ml_zoomcamp_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.ml_zoomcamp_igw.id
  }
}

resource "aws_route_table_association" "ml_zoomcamp_rta" {
  subnet_id      = aws_subnet.ml_zoomcamp_vpc_main_subnet.id
  route_table_id = aws_route_table.ml_zoomcamp_rt.id
}