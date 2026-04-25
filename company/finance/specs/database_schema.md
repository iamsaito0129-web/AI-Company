# 🗄️ 資産管理システム：データスキーマ定義 (Database Schema v2)

本スキーマは、行動経済学に基づいた「認知的負荷の最小化」と、プロアクティブな「Safe-to-Spend（今、使えるお金）」の算出を可能にする構造を定義する。

---

## 1. 支出・収入・振替トランザクション (`transactions.json`)
日々の現金の出入りを記録する。

```json
[
  {
    "id": "tx_abc123",
    "date": "2026-04-15",
    "type": "expense",         // expense, income, transfer
    "category": "変動費",      // 認知負荷低減のため、以下に集約を推奨：
                               // [固定費, 変動費, 自己投資, 特別支出, その他]
    "item_name": "Amazon Prime",
    "amount": 300,
    "source": "PayPay",
    "note": "",
    "is_imported": true
  }
]
```

## 2. 月末監査 & 予算設定 (`financial_status.json`)
実測残高の監査記録と、Safe-to-Spend算出のための予算設定を統合。

```json
{
  "monthly_budgets": {
    "2026-04": {
      "budget_limit": 100000,    // 変動費の月間予算
      "savings_goal": 50000      // 貯金目標
    }
  },
  "snapshots": [
    {
      "month": "2026-04",
      "snapshot_date": "2026-04-30",
      "actual_assets": {
        "bank_main": 150000,
        "paypay": 5000,
        "wallet_cash": 15000
      },
      "reconciliation": {
        "theoretical": 173000,
        "actual": 170000,
        "unaccounted": -3000,
        "threshold_met": false,   // 誤差が許容範囲内か
        "act_penalty": -100
      }
    }
  ]
}
```

## 3. 給与明細データ (`salary_slips.json`)
教職員給与規定に基づいた監査対応スキーマ。

```json
[
  {
    "month": "2026-04",
    "payment_date": "2026-04-17",
    "allowances": {
      "basic_salary": 250000,
      "teaching_special": 10000,
      "regional": 20000,
      "transport": 15000
    },
    "deductions": {
      "mutual_aid_pension": 25000,
      "health_insurance": 12000,
      "income_tax": 6000,
      "resident_tax": 0
    },
    "net_pay": 251000,
    "is_audited": true
  }
]
```

## 4. 報酬システムログ (`act_ledger.json`)
ACTの獲得・消費履歴。行動変容のエビデンス。

```json
[
  {
    "date": "2026-04-30",
    "action": "Consolidated Audit Success",
    "points": 50,
    "balance": 950
  }
]
```

---
承認日: 2026-04-25
設計者: Antigravity (v2)
