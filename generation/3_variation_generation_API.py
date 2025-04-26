import pandas as pd
import openai
import os
import textwrap

# Set your OpenAI API Key
os.environ["OPENAI_API_KEY"] = "Your_key"
client = openai.OpenAI()

# Constants
MAX_PROBLEMS = 5583  # Limit the number of problems to process
MODEL_NAME = "gpt-4o-mini"  # Model for text generation

def wrap_text(text, width=80):
    """Wrap text to the specified width."""
    return '\n'.join(textwrap.wrap(text, width))

def generate_variations(problem_statement):
    try:
        # Define the different prompts for variation generation
        prompts = {
            "Fictional Stories": (
                f"Convert the following mathematical problem into a fictional story. "
                f"Retain the mathematical core and keep the resulting statement "
                f"approximately similar in length. Return just the problem statement. "
                f"Problem: {problem_statement}"
            ),
            "Adversarial Information": (
                f"Inject unrelated numerical information into this mathematical problem. "
                f"Retain the mathematical core and keep the resulting statement "
                f"approximately similar in length. Return just the problem statement. "
                f"Problem: {problem_statement}"
            ),
            "Contextual Disguise": (
                f"Place this mathematical problem in an unrelated context. "
                f"Retain the mathematical core and keep the resulting statement "
                f"approximately similar in length. Return just the problem statement. "
                f"Problem: {problem_statement}"
            ),
        }

        # Define a dictionary to store the variations
        variations = {}

        # Use the API to generate variations for each prompt
        for key, prompt in prompts.items():
            conversation = [
                {"role": "user", "content": prompt}
            ]
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=conversation
            )
            # Extract and wrap the response text for each variation
            text_response = response.choices[0].message.content.strip()
            variations[key] = wrap_text(text_response)

        return variations
    except Exception as e:
        print(f"Error during variation generation: {e}")
        return {
            "Fictional Stories": "-",
            "Adversarial Information": "-",
            "Contextual Disguise": "-"
        }

def main():
    # Read the dataset
    df = pd.read_parquet('combinatorics5.parquet')
    df = df.head(MAX_PROBLEMS)  # Limit the number of problems for processing

    # Create lists to store variations
    fiction_stories = []
    adversarial_info = []
    contextual_disguise = []

    for index, row in df.iterrows():
        problem_statement = row['problem']

        # Generate variations for the problem statement
        variations = generate_variations(problem_statement)

        # Append variations to corresponding list
        fiction_stories.append(variations["Fictional Stories"])
        adversarial_info.append(variations["Adversarial Information"])
        contextual_disguise.append(variations["Contextual Disguise"])

        # Print the variations for each problem with wrapping
        print(f"  Original problem {index + 1}:\n{wrap_text(problem_statement)}\n")
        print(f"Problem {index + 1} Variations:")
        print(f"  Fictional Stories:\n{variations['Fictional Stories']}\n")
        print(f"  Adversarial Information:\n{variations['Adversarial Information']}\n")
        print(f"  Contextual Disguise:\n{variations['Contextual Disguise']}\n")

    # Append new columns to the DataFrame
    df['fictional'] = fiction_stories
    df['adversarial'] = adversarial_info
    df['contdis'] = contextual_disguise

    # Save the new DataFrame to a new parquet file
    df.to_parquet('combinatorics5_variations_test_5583.parquet')

    # Also save the DataFrame to a json file
    df.to_json('combinatorics5_variations_test_5583.json', orient='records', lines=True)

if __name__ == "__main__":
    main()
