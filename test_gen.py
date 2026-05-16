import json

from generator import generate_prd, evaluate_prd

EXAMPLE_IDEA = "a tool that helps remote engineering teams run async standups via Slack"

if __name__ == "__main__":
    print("=== Generating PRD ===")
    prd = generate_prd(EXAMPLE_IDEA)
    print(json.dumps(prd, indent=2))

    print("\n=== Evaluating PRD ===")
    evaluation = evaluate_prd(prd)
    print(json.dumps(evaluation, indent=2))
