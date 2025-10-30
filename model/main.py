from agents.json_parser import parse_user_profile
from agents.assistant_json import assistant_json_formatter
from agents.summary_gen import generate_summary
from agents.career_recommender import recommend_career
from agents.rec_newbie_career import rec_newbie_career

def main():
    print("👋 Welcome to the Career Recommender System (Interactive Mode)\n")
    print("💬 Type 'done' when you finish chatting.\n")

    conversation = []
    
    # Step 1 — Gather conversation-like input
    while True:
        user_input = input("🧑 You: ")
        if user_input.lower().strip() == "done":
            break

        conversation.append({"role": "user", "content": user_input})

        # AI (simulated) — generate next question or response
        ai_response = rec_newbie_career("\n".join([f"{m['role']}: {m['content']}" for m in conversation]))
        conversation.append({"role": "assistant", "content": ai_response})

        print(f"🤖 AI: {ai_response}\n")

    print("\n✅ Conversation complete! Generating portfolio...\n")

    # Combine all user messages into one profile text
    combined_user_input = " ".join([m['content'] for m in conversation if m['role'] == "user"])

    # Step 2 — Parse user profile
    user_json = parse_user_profile(combined_user_input)
    formatted_json = assistant_json_formatter(user_json)
    print("🧾 User Portfolio JSON:\n", formatted_json)

    # Step 3 — Generate a summary
    summary = generate_summary(formatted_json)
    print("\n🪶 Session Summary:\n", summary)

    # Step 4 — Recommend careers
    recommendations = recommend_career(formatted_json)
    print("\n💼 Career Recommendations:\n", recommendations)

    print("\n🎉 Done! You can now use this profile for trends or course recommendations.")

if __name__ == "__main__":
    main()

