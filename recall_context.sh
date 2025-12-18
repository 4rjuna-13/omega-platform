#!/bin/bash
echo "=== JAIDA CONTEXT ==="
cat JAIDA_CONTEXT.txt 2>/dev/null || echo "Context file not found"
echo "=== END CONTEXT ==="
