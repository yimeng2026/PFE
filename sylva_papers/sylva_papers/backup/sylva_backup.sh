#!/bin/bash
# SYLVA 实时备份脚本
# 用法: ./sylva_backup.sh [incremental|full]

BACKUP_DIR="/root/.openclaw/workspace/sylva_papers/backup"
SOURCE_DIRS=(
    "/root/.openclaw/workspace/alpha_derivation"
    "/root/.openclaw/workspace/sylva_formalization"
    "/root/.openclaw/workspace/agent_writing_system"
    "/root/.openclaw/workspace/问题库"
)

TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
TODAY=$(date +%Y-%m-%d)

# 创建日期目录
mkdir -p "$BACKUP_DIR/$TODAY"

# 执行备份
for dir in "${SOURCE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        cp -r "$dir" "$BACKUP_DIR/$TODAY/" 2>/dev/null
    fi
done

# 更新latest软链接
rm -f "$BACKUP_DIR/latest"
ln -s "$BACKUP_DIR/$TODAY" "$BACKUP_DIR/latest"

# 更新清单
cat > "$BACKUP_DIR/manifest.json" << EOF
{
  "backup_id": "$TIMESTAMP",
  "timestamp": "$(date -Iseconds)",
  "type": "${1:-incremental}",
  "source_dirs": $(printf '%s\n' "${SOURCE_DIRS[@]}" | jq -R . | jq -s .),
  "backup_location": "$BACKUP_DIR/$TODAY",
  "latest_link": "$BACKUP_DIR/latest"
}
EOF

echo "[$(date -Iseconds)] Backup completed: $TIMESTAMP"
