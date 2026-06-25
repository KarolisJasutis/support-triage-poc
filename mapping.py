TEAM_CATEGORIES = {
    "Integration Support": [
        "webhook_issue",
        "api_error",
        "sdk_integration",
        "sandbox_environment",
        "documentation_question"
    ],
    "Payments Support": [
        "payment_status",
        "transaction_failure",
        "settlement_question",
        "refund_request",
        "chargeback_question"
    ],
    "Account Support": [
        "authentication_issue",
        "api_key_issue",
        "permission_access",
        "account_configuration"
    ],
    "Compliance Support": [
        "kyc_question",
        "aml_review",
        "account_verification",
        "compliance_request"
    ]
}

SAMPLE_SUPPORT_MESSAGES = [
    "We receive 401 responses from our webhook endpoint.",
    "api not working",
    #"We cannot generate API keys.",
    #"The integration is not working.",
    #"Our payment settlement is delayed and we need help.",
    #"The API returns a 500 error when creating a customer.",
    #"Our account verification request is stuck in review.",
    #"We need clarification on sandbox environment behavior.",
    #"I am unable to access the dashboard after logging in.",
    #"What do we need to do to comply with KYC requirements?"
]
