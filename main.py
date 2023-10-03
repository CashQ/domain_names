import requests
import json
import os
import openai


# Load API keys from Replit secrets manager
API_KEY = os.environ["GODADDY_API_KEY"]
API_SECRET = os.environ["GODADDY_API_SECRET"]
GPT4_API_KEY = os.environ["GPT4_API_KEY"]

headers = {
    "Authorization": f"sso-key {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json",
}

gpt4_headers = {
    "Authorization": f"Bearer {GPT4_API_KEY}",
    "Content-Type": "application/json",
}


def generate_domain_names(prompt, user_comment=None):
    openai.api_key = GPT4_API_KEY

    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates domain name suggestions."},
        {"role": "user", "content": f"Generate 5 domain name suggestions for a company with the following description: {prompt}"}
    ]

    if user_comment:
        messages.append({"role": "user", "content": f"I would like the suggestions to {user_comment}"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Replace with the appropriate GPT-4 model if different
        messages=messages,
        max_tokens=50,
        temperature=0.7
    )

    if response:
        suggestions = response.choices[0].message["content"].strip().split("\n")
        return suggestions
    else:
        print("Error generating domain names.")
        return None

def main():
    description = input("Enter your company business description: ")
    domain_zone = input("Enter your preferred domain zone (e.g., com, net, org): ")

    suggestions = generate_domain_names(description)

    if suggestions:
        print("\nDomain suggestions:")
        for suggestion in suggestions:
            print(f"{suggestion}.{domain_zone}")

        while True:
            action = input("\nEnter 'n' for the next batch of names or 'r' to register a domain: ").lower()

            if action == 'n':
                user_comment = input("Please provide a comment to adjust the domain name suggestions: ")
                suggestions = generate_domain_names(description, user_comment)
                if suggestions:
                    print("\nDomain suggestions:")
                    for suggestion in suggestions:
                        print(f"{suggestion}.{domain_zone}")
                else:
                    print("No more suggestions available.")
            elif action == 'r':
                print("Please visit https://www.godaddy.com/ to register your domain.")
                break
            else:
                print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
