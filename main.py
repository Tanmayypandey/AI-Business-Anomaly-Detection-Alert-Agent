"""
Main entry point for the AI Business Anomaly Detection & Alert Agent.

This file launches the existing AI business analysis pipeline.
"""

import runpy


if __name__ == "__main__":

    print("=" * 70)
    print("🤖 AI BUSINESS ANOMALY DETECTION & ALERT AGENT")
    print("=" * 70)

    print("\n🚀 Starting complete business analysis pipeline...\n")

    runpy.run_module(
        "src.ai_business_report",
        run_name="__main__"
    )

    print("\n" + "=" * 70)
    print("🎉 MAIN PIPELINE EXECUTION FINISHED")
    print("=" * 70)