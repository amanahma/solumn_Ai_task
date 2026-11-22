#!/usr/bin/env sh
# seed_data.sh — Create small deterministic plaintext files in /app/data/source/
# Used during Docker image build. Keep content minimal and deterministic.

set -e

mkdir -p /app/data/source/configs
mkdir -p /app/data/source/reports
mkdir -p /app/data/source/logs

cat > /app/data/source/configs/db.conf << 'EOF'
[database]
host = db.internal
port = 5432
name = prod_db
pool_size = 10
EOF

cat > /app/data/source/configs/app.conf << 'EOF'
[app]
debug = false
log_level = info
max_workers = 4
EOF

cat > /app/data/source/reports/daily_summary.txt << 'EOF'
Daily Summary Report
====================
Date: 2024-01-15
Total transactions: 4821
Errors: 3
Uptime: 99.94%
EOF

cat > /app/data/source/reports/audit_log.txt << 'EOF'
2024-01-15T00:01:12Z user=svc_backup action=read resource=/data/prod
2024-01-15T00:01:13Z user=svc_backup action=read resource=/data/prod/transactions
2024-01-15T06:00:00Z user=admin action=login resource=/admin/dashboard
EOF

cat > /app/data/source/logs/service.log << 'EOF'
2024-01-15T00:00:01Z [INFO] backup-service started
2024-01-15T00:00:02Z [INFO] connected to db.internal:5432
2024-01-15T00:01:00Z [INFO] health check passed
EOF

echo "[seed_data] source files created"
