-include $(VAR_DIR)/profile/prod.mk

# API Gateway Route53
TF_VAR_dos_integration_sub_domain_name := $(PROJECT_ID)-$(ENVIRONMENT)

# API Gateway Route53
TF_VAR_dos_integration_sub_domain_name := $(PROGRAMME)-$(TEAM_ID)-$(ENVIRONMENT)
DOS_INTEGRATION_URL := $(TF_VAR_dos_integration_sub_domain_name).$(TEXAS_HOSTED_ZONE)
