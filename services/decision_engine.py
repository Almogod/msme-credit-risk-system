def risk_based_decision(pd: float):
    if pd > 0.7:
        return "Reject"
    elif pd > 0.4:
        return "Conditional Approval"
    return "Approve"
