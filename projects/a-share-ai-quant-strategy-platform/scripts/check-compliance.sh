#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

old_terms='会员|月票|观众票|订阅|Premium|报告会员|\bPro\b'
old_allowed='取消|不使用|不再|替代|改为|不得|禁止|检查|废弃|旧|历史|收费表达|付费包装|统一为积分|积分制度|不出现|rg -n'

positive_risk_terms='(支持|提供|开放|接入|新增|实现|返回|展示|解锁).*(荐股|喊单|带单|跟单|自动下单|券商账户|买卖点|实时信号|实盘交易|实盘自动交易|持仓明细|公开持仓|策略代码|live_trade|broker account|buy/sell)'
negative_context='不|无|禁止|不得|不能|不可|不做|不接|不支持|不保存|不实现|不展示|不返回|不输出|拒绝|拦截|检查|风险|红线|底线|边界|失败|误|异常|取消|替代|排除|不采用|不包含|不开放|只允许|不得新增|不引入|要求'

scan_globs=(
  "--glob" "*.md"
  "--glob" "*.js"
  "--glob" "*.html"
  "--glob" "!00_source_notes.md"
  "--glob" "!scripts/**"
)

fail=0

while IFS= read -r line; do
  text="${line#*:*:}"
  if [[ ! "$text" =~ $old_allowed ]]; then
    echo "old monetization term outside allowed context: $line" >&2
    fail=1
  fi
done < <(rg -n --no-heading "${scan_globs[@]}" "$old_terms" . || true)

while IFS= read -r line; do
  text="${line#*:*:}"
  if [[ ! "$text" =~ $negative_context ]]; then
    echo "positive high-risk capability wording found: $line" >&2
    fail=1
  fi
done < <(rg -n --no-heading "${scan_globs[@]}" "$positive_risk_terms" . || true)

if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

echo "check-compliance passed"
