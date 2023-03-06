-include $(VAR_DIR)/platform-texas/v1/account-live-k8s-nonprod.mk

# ==============================================================================
# Service variables

LOG_LEVEL:= DEBUG

DB_SERVER_NAME := uec-core-dos-performance2-db-12
DB_ROUTE_53 := uec-core-dos-performance2-primary.dos-db-sync-rds
DB_REPLICA_SERVER_NAME := uec-core-dos-performance2-db-12-replica-di
DB_REPLICA_53 := uec-core-dos-performance2-di-ro.dos-db-sync-rds
DB_PORT := 5432
DB_NAME := pathwaysdos
DB_SCHEMA := pathwaysdos
DOS_DB_SG_NAME := live-lk8s-nonprod-core-dos-db-rds-postgres-sg
DOS_DB_REPLICA_SG_NAME := uec-core-dos-performance2-db-12-replica-di-sg

DB_SECRET_NAME := core-dos-dev/deployment
DB_SECRET_KEY := DB_DI_READWRITE_PASSWORD
DB_USER_NAME_SECRET_NAME = uec-dos-int-dev/deployment
DB_USER_NAME_SECRET_KEY = DOS_DB_DI_USERNAME

DB_REPLICA_SECRET_NAME := core-dos-dev/deployment
DB_REPLICA_SECRET_KEY := DB_DI_READWRITE_PASSWORD
DB_READ_ONLY_USER_NAME_SECRET_NAME = uec-dos-int-dev/deployment
DB_READ_ONLY_USER_NAME_SECRET_KEY = DOS_DB_DI_USERNAME

TF_VAR_ip_address_secret := uec-dos-int-dev-ip-addresses-allowlist
SLACK_WEBHOOK_SECRET_NAME = uec-dos-int-dev/deployment
SLACK_WEBHOOK_SECRET_KEY = SLACK_WEBHOOK
SLACK_ALERT_CHANNEL := dos-integration-dev-status

TAG_SECRET_MANAGER := uec-dos-int-dev/deployment
