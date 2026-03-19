#!/usr/bin/env bash
# Usage: ./script.sh <scan-file.json>
SCAN_FILE="${1:?Usage: $0 <scan-file.json>}"

echo "## 🔍 Frontend Security Scan Results" >> $GITHUB_STEP_SUMMARY
echo "" >> $GITHUB_STEP_SUMMARY

if [ -f "$SCAN_FILE" ]; then
  echo "found=true" >> $GITHUB_OUTPUT

  # Count vulnerabilities by severity
  CRITICAL=$(jq '[.matches[] | select(.vulnerability.severity == "Critical")] | length' "$SCAN_FILE" 2>/dev/null || echo "0")
  HIGH=$(jq '[.matches[] | select(.vulnerability.severity == "High")] | length' "$SCAN_FILE" 2>/dev/null || echo "0")
  MEDIUM=$(jq '[.matches[] | select(.vulnerability.severity == "Medium")] | length' "$SCAN_FILE" 2>/dev/null || echo "0")
  LOW=$(jq '[.matches[] | select(.vulnerability.severity == "Low")] | length' "$SCAN_FILE" 2>/dev/null || echo "0")

  # Set outputs
  echo "critical=$CRITICAL" >> $GITHUB_OUTPUT
  echo "high=$HIGH" >> $GITHUB_OUTPUT
  echo "medium=$MEDIUM" >> $GITHUB_OUTPUT
  echo "low=$LOW" >> $GITHUB_OUTPUT

  echo "| Severity | Count |" >> $GITHUB_STEP_SUMMARY
  echo "|----------|-------|" >> $GITHUB_STEP_SUMMARY
  echo "| 🔴 Critical | $CRITICAL |" >> $GITHUB_STEP_SUMMARY
  echo "| 🟠 High | $HIGH |" >> $GITHUB_STEP_SUMMARY
  echo "| 🟡 Medium | $MEDIUM |" >> $GITHUB_STEP_SUMMARY
  echo "| 🟢 Low | $LOW |" >> $GITHUB_STEP_SUMMARY
  echo "" >> $GITHUB_STEP_SUMMARY

  if [ "$CRITICAL" -gt 0 ] || [ "$HIGH" -gt 0 ]; then
    echo "### Top Critical/High Vulnerabilities:" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    VULN_COUNT=$(jq '[.matches[] | select(.vulnerability.severity == "Critical" or .vulnerability.severity == "High")] | length' "$SCAN_FILE" 2>/dev/null || echo "0")
    echo "vuln_count=$VULN_COUNT" >> $GITHUB_OUTPUT
    jq -r '.matches[] | select(.vulnerability.severity == "Critical" or .vulnerability.severity == "High") | "- **\(.vulnerability.id)** (\(.vulnerability.severity)): \(.vulnerability.description // "No description")"' "$SCAN_FILE" 2>/dev/null | head -10 >> $GITHUB_STEP_SUMMARY || echo "Could not parse vulnerabilities" >> $GITHUB_STEP_SUMMARY
  else
    echo "vuln_count=0" >> $GITHUB_OUTPUT
  fi
else
  echo "found=false" >> $GITHUB_OUTPUT
  echo "❌ Scan file not found: $SCAN_FILE" >> $GITHUB_STEP_SUMMARY
fi