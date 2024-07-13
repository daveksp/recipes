data "template_file" "swagger" {
  template = "${file("resources/swagger_recipe.yaml")}"

  #vars = {
  #  request_template = "${local.request_template}"
  #}
}



resource "aws_api_gateway_rest_api" "recipe_api" {
  name                       = "recipe_gw"
  description                = "Proxy to handle requests related to the recipe API"
  body                       = "${data.template_file.swagger.rendered}"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}


resource "aws_api_gateway_deployment" "recipe_deployment" {
  rest_api_id                = aws_api_gateway_rest_api.recipe_api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_rest_api.recipe_api.body
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_api_gateway_stage" "test_stage" {
  deployment_id              = aws_api_gateway_deployment.recipe_deployment.id
  rest_api_id                = aws_api_gateway_rest_api.recipe_api.id
  stage_name                 = "TEST"

  #depends_on = [aws_cloudwatch_log_group.gateway_logs]
}


resource "aws_api_gateway_base_path_mapping" "stage-domain-mapping" {
  api_id      = aws_api_gateway_rest_api.recipe_api.id
  stage_name  = aws_api_gateway_stage.test_stage.stage_name
  domain_name = aws_api_gateway_domain_name.api_domain_name.domain_name
}
