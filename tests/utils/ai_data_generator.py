"""
AI-powered test data generator.

Uses Claude to generate realistic user data for tests. Each call returns 
a unique, plausible user profile — real-looking names, valid-format emails, 
strong-looking passwords.

Why AI instead of hardcoded data?
- Real users have unpredictable input patterns; hardcoded "John Doe" 
  values create false consistency
- Fresh accounts per test run means no test interference
- Demonstrates AI + Playwright integration for the portfolio
"""

import json
import os
import random
import string
from dataclasses import dataclass
from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()
_client = Anthropic()


@dataclass
class TestUser:
    """A generated test user profile."""
    name: str
    email: str
    password: str
    first_name: str
    last_name: str
    company: str
    address: str
    city: str
    state: str
    zipcode: str
    mobile: str
    country: str = "United States"


def _random_suffix(length: int = 8) -> str:
    """Adds uniqueness to emails so we don't get 'email already exists' errors."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_test_user(model: str = "claude-haiku-4-5") -> TestUser:
    """
    Generates a single test user with realistic data via Claude.
    
    Returns a TestUser with fields for both signup and checkout flows.
    Uses Haiku for speed/cost — this is quick structured generation.
    """
    prompt = """Generate a realistic test user profile. Respond with ONLY valid JSON, no other text.

The JSON must have exactly these fields:
{
  "first_name": "<realistic first name>",
  "last_name": "<realistic last name>",
  "company": "<plausible company name>",
  "address": "<realistic street address>",
  "city": "<real US city>",
  "state": "<US state name, full>",
  "zipcode": "<5-digit US zip code>",
  "mobile": "<10-digit US phone, digits only, no formatting>"
}

Make the data varied and realistic - not "John Doe" or "Jane Smith" clichés."""

    response = _client.messages.create(
        model=model,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    
    text = response.content[0].text.strip()
    # Strip common markdown wrappers if the model adds them
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    
    data = json.loads(text)
    
    # Build the full TestUser
    first_name = data["first_name"]
    last_name = data["last_name"]
    full_name = f"{first_name} {last_name}"
    
    # Add unique suffix to email so we don't collide with existing accounts
    email = f"{first_name.lower()}.{last_name.lower()}.{_random_suffix()}@testmail.com"
    
    # Generate a strong password (Claude doesn't need to do this)
    password = f"Test_{_random_suffix(12)}!"
    
    return TestUser(
        name=full_name,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        company=data["company"],
        address=data["address"],
        city=data["city"],
        state=data["state"],
        zipcode=data["zipcode"],
        mobile=data["mobile"],
    )


if __name__ == "__main__":
    # Quick manual test - run this file directly to see generation in action
    user = generate_test_user()
    print(f"Generated user:")
    print(f"  Name:     {user.name}")
    print(f"  Email:    {user.email}")
    print(f"  Password: {user.password}")
    print(f"  Company:  {user.company}")
    print(f"  Address:  {user.address}")
    print(f"  City:     {user.city}, {user.state} {user.zipcode}")
    print(f"  Mobile:   {user.mobile}")