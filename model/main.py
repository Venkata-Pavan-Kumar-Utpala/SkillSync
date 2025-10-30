from agents.json_parser import parse_user_profile
from agents.assistant_json import assistant_json_formatter
from agents.summary_gen import generate_summary
from agents.career_recommender import recommend_career

def main():
    print("👋 Welcome to the Career Recommender System\n")

    # Step 1 — Get user data
    user_input = input("Tell me about your skills, experience, and education: ")
    user_json = parse_user_profile(user_input)

    # Step 2 — Format the JSON neatly
    formatted_json = assistant_json_formatter(user_json)
    print("\n🧾 User Portfolio JSON:\n", formatted_json)

    # Step 3 — Generate a summary
    summary = generate_summary(formatted_json)
    print("\n🪶 Session Summary:\n", summary)

    # Step 4 — Recommend careers
    recommendations = recommend_career(formatted_json)
    print("\n💼 Career Recommendations:\n", recommendations)

if __name__ == "__main__":
    main()
