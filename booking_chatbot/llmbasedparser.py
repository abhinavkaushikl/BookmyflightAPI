from transformers import pipeline

# Use a smaller model that's more likely to work
generator = pipeline('text-generation', model='distilgpt2', max_length=200)

def parse_travel_query_free_llm(user_query):
    prompt = f"""Extract the following travel details from the user query:
- destination city or location
- departure date (YYYY-MM-DD)
- return date (YYYY-MM-DD)
- travel preferences (e.g., beach, desert, mountain)

If some info is missing, return null for those fields.

Return the output strictly as a JSON object like this:
{{
  "destination": "city or location",
  "departure_date": "YYYY-MM-DD or null",
  "return_date": "YYYY-MM-DD or null",
  "preferences": "preference keyword or null"
}}

Example input:
"Want to book for delhi and date will be '2025-06-04' and '2025-06-09' and desert i will prefer"

Example output:
{{
  "destination": "Delhi",
  "departure_date": "2025-06-04",
  "return_date": "2025-06-09",
  "preferences": "desert"
}}

User query:
\"\"\"{user_query}\"\"\"
"""
    # Generate completion
    outputs = generator(prompt, do_sample=False)
    generated_text = outputs[0]['generated_text']
    
    # Extract JSON substring from generated text (simplistic)
    import re, json
    match = re.search(r"\{.*\}", generated_text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("Failed to parse JSON.")
            return None
    else:
        print("No JSON found in output.")
        return None

if __name__ == "__main__":
    query = "want to book for delhi and date will be '2025-06-04' and '2025-06-09' and desert i will prefer"
    result = parse_travel_query_free_llm(query)
    print("Free LLM Parsed Info:", result)
