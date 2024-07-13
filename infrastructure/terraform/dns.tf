data "aws_route53_zone" "primary" {
  name                       = var.primary_dns
}

resource "aws_acm_certificate" "api-certificate" {
  provider                   = aws
  domain_name                = "test.${var.primary_dns}"
  validation_method          = "DNS"

  lifecycle {
    create_before_destroy    = true    # when updating we first create a new resource, then delete the old one
  }

  tags = {
    Environment              = "production"
    Name                     = "test-website-certificate"
    Project                  = "test"
  }
}

resource "aws_route53_record" "api-cert-dns-validation" {
  provider                   = aws
  allow_overwrite            = true

  name                       = tolist(aws_acm_certificate.api-certificate.domain_validation_options)[0].resource_record_name
  records                    = [tolist(aws_acm_certificate.api-certificate.domain_validation_options)[0].resource_record_value]
  type                       = tolist(aws_acm_certificate.api-certificate.domain_validation_options)[0].resource_record_type
  zone_id                    = data.aws_route53_zone.primary.id
  ttl                        = 60
}

resource "aws_acm_certificate_validation" "api-certificate-validation" {
  provider                   = aws
  certificate_arn            = aws_acm_certificate.api-certificate.arn
  validation_record_fqdns    = [aws_route53_record.api-cert-dns-validation.fqdn]
}

resource "aws_api_gateway_domain_name" "api_domain_name" {
  certificate_arn            = aws_acm_certificate_validation.api-certificate-validation.certificate_arn
  domain_name                = "test.${var.primary_dns}"
}

resource "aws_route53_record" "api-dns-record" {
  name                       = "test.${var.primary_dns}"
  type                       = "A" # it worked as a CNAME
  zone_id                    = data.aws_route53_zone.primary.zone_id

  alias {
    name                     = aws_api_gateway_domain_name.api_domain_name.cloudfront_domain_name
    zone_id                  = aws_api_gateway_domain_name.api_domain_name.cloudfront_zone_id
    evaluate_target_health   = false
  }
}
