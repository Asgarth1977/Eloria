# memory_summarizer.py
from datetime import datetime
from typing import List, Dict

# -------------------------------
# Summarization Utilities
# -------------------------------

def summarize_conversation(conversation: List[Dict]) -> str:
    """
    Generate a concise summary of a conversation.
    Each entry in conversation should be a dict with:
        'role': 'user' or 'assistant'
        'content': message text
        'timestamp': ISO string
    Returns a single string summarizing key points.
    """
    if not conversation:
        return "No conversation data available to summarize."

    # Basic approach: concatenate messages and extract key points
    # Placeholder: you can replace with a more advanced summarization algorithm or LLM call
    summary_lines = []

    for entry in conversation:
        role = entry.get("role", "unknown").capitalize()
        content = entry.get("content", "").strip()
        if content:
            # Limit to first 100 characters per message for summary
            snippet = content[:100].replace("\n", " ")
            summary_lines.append(f"{role}: {snippet}")

    summary = "\n".join(summary_lines)
    return summary

# -------------------------------
# Weekly / Multi-Day Summaries
# -------------------------------

def summarize_multiple_days(memories: List[List[Dict]]) -> str:
    """
    Summarize multiple days of conversation.
    'memories' is a list of conversation lists (one per day).
    Returns a combined summary string.
    """
    combined_summary = []

    for day_memory in memories:
        day_summary = summarize_conversation(day_memory)
        combined_summary.append(day_summary)

    return "\n\n".join(combined_summary)

# -------------------------------
# Optional Helpers
# -------------------------------

def summarize_by_date(conversation: List[Dict], date: datetime) -> str:
    """
    Filter messages by a specific date and summarize them.
    Assumes each conversation entry has 'timestamp' in ISO format.
    """
    filtered = [
        entry for entry in conversation
        if entry.get("timestamp", "").startswith(date.strftime("%Y-%m-%d"))
    ]
    return summarize_conversation(filtered)
