character_conversion_template = """
Ensure the following dialogue is in the correct format, with each line following the format 'Speaker: Text'.
If any lines are not in this format, correct them. Then, convert the dialogue to use the provided character names.

Use the names exactly as provided in {names}. Do not replace any names with generic labels (e.g., Character 1, Character 2). Only include names in the dialogue if they are present, and ensure the dialogue matches the structure 'Speaker: Text'. 

Do not write lines such as 'Character 1 heard Character 2', or similar, unless specified in the dialogue.

Example input: "Ms. Dubinsky: We'd like you to join our debate team."
Example output: "Aisha: We'd like you to join our debate team."

Here is the dialogue:
{dialogue}

Make sure the characters are exactly as provided in {names}.
"""
