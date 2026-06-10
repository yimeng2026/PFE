#!/bin/bash
# lake_wrapper.sh - 透明访问压缩的.olean.zst文件
# 自动解压 -> 执行lake命令 -> 可选重新压缩

set -e

LAKE_DIR="/root/.openclaw/workspace/sylva_formalization/.lake"
CACHE_DIR="$LAKE_DIR/.zst_cache"

# 确保缓存目录存在
mkdir -p "$CACHE_DIR"

# 清理函数（保留最近使用的）
cleanup_cache() {
    local max_size=${1:-1073741824}  # 默认1GB
    local current_size=$(du -sb "$CACHE_DIR" 2>/dev/null | cut -f1)
    
    if [ "$current_size" -gt "$max_size" ]; then
        # 按访问时间排序，删除最老的
        find "$CACHE_DIR" -type f -atime +1 -delete 2>/dev/null || true
    fi
}

# 查找并解压.olean文件
find_and_extract() {
    local target="$1"
    local zst_file="${target}.zst"
    
    # 如果目标已存在，直接返回
    if [ -f "$target" ]; then
        echo "$target"
        return 0
    fi
    
    # 查找对应的.zst文件
    if [ -f "$zst_file" ]; then
        local cache_path="$CACHE_DIR/$(echo "$target" | tr '/' '_')"
        
        # 如果已在缓存，直接返回
        if [ -f "$cache_path" ]; then
            cp "$cache_path" "$target"
            echo "$target"
            return 0
        fi
        
        # 解压
        echo "[wrapper] 解压: $(basename "$zst_file")" >&2
        zstd -d "$zst_file" -o "$target" --quiet
        
        # 复制到缓存
        cp "$target" "$cache_path"
        
        echo "$target"
        return 0
    fi
    
    # 找不到
    return 1
}

# 预解压常用文件（在项目目录下执行）
preheat() {
    echo "[wrapper] 预解压 Sylva 核心文件..."
    
    # 查找Sylva相关的.zst文件并解压
    find "$LAKE_DIR" -path "*/Sylva*" -name "*.olean.zst" 2>/dev/null | while read -r zst; do
        local target="${zst%.zst}"
        if [ ! -f "$target" ]; then
            zstd -d "$zst" -o "$target" --quiet 2>/dev/null && echo "  ✓ $(basename "$target")"
        fi
    done
    
    echo "[wrapper] 预解压完成"
}

# 重新压缩（可选）
recompress() {
    echo "[wrapper] 重新压缩.olean文件..."
    
    find "$LAKE_DIR" -name "*.olean" -type f ! -name "*.zst" 2>/dev/null | while read -r olean; do
        local zst="${olean}.zst"
        # 如果.zst不存在或.olean更新，重新压缩
        if [ ! -f "$zst" ] || [ "$olean" -nt "$zst" ]; then
            zstd -3 --rm "$olean" -o "$zst" --quiet 2>/dev/null && echo "  ✓ $(basename "$olean")"
        fi
    done
}

# 主逻辑
case "${1:-}" in
    preheat)
        preheat
        ;;
    recompress)
        recompress
        ;;
    find)
        find_and_extract "$2"
        ;;
    cleanup)
        cleanup_cache "${2:-1073741824}"
        ;;
    *)
        # 直接转发给真实lake，但先预解压
        preheat > /dev/null 2>&1
        echo "[wrapper] 执行: /root/.elan/bin/lake $*" >&2
        /root/.elan/bin/lake "$@"
        ;;
esac
