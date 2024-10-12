character_conversion_template = """
Ensure the following dialogue is in the correct format, with each line following the format 'Speaker: Text'.
If any lines are not in this format, correct them. Then, convert the dialogue to use generic character names (Character 1, Character 2, etc.).
Identify the characters in the dialogue well.If there's character name in dialogue provide it else leave it.Don't write "charcater1 heard to character 2" etc. Provide names in dialogue only if available. in dialogue
Example input: "Ms. Dubinsky: We'd like you to join our debate team."
Example output: "Character 1: We'd like you to join our debate team."
Here is the dialogue:
{dialogue}

Make sure the number of character are {num_characters} and their gender is in sequence of {gender}, Starting with host's gender and follwed by guest's gender. The total of host and guest should be {num_characters}.
"""
