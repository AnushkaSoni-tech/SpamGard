import os 
import pandas as pd

from pipeline.chain import get_chain


# =====================
# 3. Wrapper function
# =====================
def classify_message(message):
    chain, format_instructions = get_chain()
    return chain.invoke({
        "format_instructions": format_instructions,
        "message": message
    })



def classify_batch(messages):
    """
    Simple batch classification using LangChain's .batch().
    Returns a DataFrame with one row per message.
    """
    chain, format_instructions = get_chain()  # cached; cheap

    # Prepare inputs
    inputs = [
        {"format_instructions": format_instructions, "message": msg}
        for msg in messages
    ]

    # Run batch
    outputs = chain.batch(inputs)

    # Build DataFrame
    results = []
    for i, (msg, out) in enumerate(zip(messages, outputs), start=1):
        try:
            results.append({
                "Message #": i,
                "Message": msg,
                "Label": out.label,
                "Risk Score": out.risk_score,
                "Reasons": "; ".join(out.reasons),
                "Red Flags": "; ".join(out.red_flags),
                "Suggested Action": out.suggested_action
            })
        except Exception as e:
            results.append({
                "Message #": i,
                "Message": msg,
                "Label": "Error",
                "Risk Score": "Error",
                "Reasons": "Error",
                "Red Flags": "Error",
                "Suggested Action": "Error"
            })
    return pd.DataFrame(results)