# -*- coding: utf-8 -*-
"""
Master Launcher — Supabase config + tool catalogue.
"""

SUPABASE_URL = "https://oewdqhwdliaqmcqdsyll.supabase.co"
SUPABASE_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ld2RxaHdkbGlhcW1jcWRzeWxsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc3MjY5NzcsImV4cCI6MjA5MzMwMjk3N30"
    ".7nO8V59r_Mw3KmPZE7W1u2Iap_X9qLHqsmj_f96eYSw"
)
EDGE_BASE = f"{SUPABASE_URL}/functions/v1"

# Master launcher version (separate from individual tool versions)
MASTER_TOOL_SLUG = "master"
CURRENT_VERSION = "1.0.0"
REQUEST_TIMEOUT = 15

# ── Tool catalogue ────────────────────────────────────────────────────────────
# Prices shown here are fallback defaults only.
# Real prices are fetched live from Supabase via get-payment-config.
TOOLS = [
    {
        "slug": "loan_software",
        "name": "Fasal Rin Loan Automation",
        "short_desc": (
            "Automates new loan application filing on the Fasal Rin portal. "
            "Reads applicant data from Excel and fills the online form automatically."
        ),
        "icon": "\U0001f4bc",   # briefcase
        "price_fallback": 2500,
        "exe_name": "FasalRinAutomation.exe",
    },
    {
        "slug": "loan_discrepancy",
        "name": "Loan Discrepancy Management",
        "short_desc": (
            "Handles loan discrepancy resolution on the portal. "
            "Reads discrepancy records from Excel and submits corrections automatically."
        ),
        "icon": "\U0001f4cb",   # clipboard
        "price_fallback": 2000,
        "exe_name": "DiscrepancyAutomation.exe",
    },
    {
        "slug": "is_claim_discrepancy",
        "name": "IS Claim Discrepancy",
        "short_desc": (
            "Automates IS claim discrepancy submission on the Fasal Rin portal. "
            "Processes discrepancy claims in bulk from an Excel sheet."
        ),
        "icon": "\U0001f4dd",   # memo
        "price_fallback": 2000,
        "exe_name": "ISClaimDiscrepancyAutomation.exe",
    },
    {
        "slug": "is_automation",
        "name": "IS Claim Automation",
        "short_desc": (
            "Automates IS claim filing on the Fasal Rin portal. "
            "Handles bulk claim submissions from Excel with captcha assistance."
        ),
        "icon": "\U0001f916",   # robot
        "price_fallback": 2000,
        "exe_name": "ISClaimAutomation.exe",
    },
]
