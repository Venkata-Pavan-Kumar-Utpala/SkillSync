from utils.shivaay_api import call_shivaay_agent

def parse_user_profile(user_input):
    system_prompt = (
        "You are JSONParser. Ask for and extract user details such as: "
        "5 highlighted skills, 2 previous work experiences, education, projects worked on, "
        "LinkedIn profile, and contact number. "
        "Return this as a valid JSON object."
    )
    return call_shivaay_agent(system_prompt, user_input)
