#!/bin/bash
# Sylva Formalization - Olean File Verification Script
# Verifies all .olean files exist and are valid

set -e

echo "=========================================="
echo "Sylva Formalization - Olean Verification"
echo "=========================================="
echo ""

OLEAN_DIR="/root/.openclaw/workspace/sylva_formalization/.lake/build/lib/lean"
SOURCE_DIR="/root/.openclaw/workspace/sylva_formalization/SylvaFormalization"

echo "Checking for .lake/build/lib/lean directory..."
if [ ! -d "$OLEAN_DIR" ]; then
    echo "ERROR: Olean directory not found: $OLEAN_DIR"
    echo "Build may not have completed yet."
    exit 1
fi
echo "✓ Olean directory exists"
echo ""

echo "Counting .olean files..."
OLEAN_COUNT=$(find "$OLEAN_DIR" -name "*.olean" -type f 2>/dev/null | wc -l)
echo "Total .olean files found: $OLEAN_COUNT"
echo ""

echo "Checking SylvaFormalization modules..."
SYLVA_OLEANS=()
if [ -d "$OLEAN_DIR/SylvaFormalization" ]; then
    for source in "$SOURCE_DIR"/*.lean; do
        if [ -f "$source" ]; then
            filename=$(basename "$source" .lean)
            olean_path="$OLEAN_DIR/SylvaFormalization/$filename.olean"
            if [ -f "$olean_path" ]; then
                size=$(stat -c%s "$olean_path" 2>/dev/null || echo "0")
                if [ "$size" -gt 0 ]; then
                    echo "  ✓ $filename.olean ($size bytes)"
                    SYLVA_OLEANS+=("$filename")
                else
                    echo "  ✗ $filename.olean (empty file!)"
                fi
            else
                echo "  ✗ $filename.olean (missing!)"
            fi
        fi
    done
else
    echo "  SylvaFormalization olean directory not found"
fi
echo ""

echo "Checking Test.olean..."
TEST_OLEAN="$OLEAN_DIR/Test.olean"
if [ -f "$TEST_OLEAN" ]; then
    size=$(stat -c%s "$TEST_OLEAN" 2>/dev/null || echo "0")
    if [ "$size" -gt 0 ]; then
        echo "  ✓ Test.olean ($size bytes)"
    else
        echo "  ✗ Test.olean (empty file!)"
    fi
else
    echo "  ✗ Test.olean (missing!)"
fi
echo ""

if [ ${#SYLVA_OLEANS[@]} -gt 0 ]; then
    echo "Detailed file listing:"
    echo "----------------------"
    find "$OLEAN_DIR" -name "*.olean" -path "*/SylvaFormalization/*" -exec ls -lh {} \; 2>/dev/null | sort -k9
    echo ""
fi

echo "=========================================="
echo "Verification Complete"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Total .olean files: $OLEAN_COUNT"
echo "  - SylvaFormalization modules: ${#SYLVA_OLEANS[@]}"
echo ""

if [ ${#SYLVA_OLEANS[@]} -gt 0 ]; then
    echo "Modules verified:"
    for mod in "${SYLVA_OLEANS[@]}"; do
        echo "    - $mod"
    done
fi
