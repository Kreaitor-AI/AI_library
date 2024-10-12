podcast_text_prompt = """
Generate a podcast script on the topic: '{topic}', with the context: {summary_result}.

Requirements:
1. The script must feature exactly the characters listed: {names}, including the host. No additional characters should be added. 
2. Use the provided names exactly as given in {names}. The first name is for the host, followed by the guest names in sequence.
3. The script must be exactly {length_words} words long. Ensure the total word count is precise.
4. Avoid adding emotions, commentary, or additional content. Stick strictly to the script.
5. Do not use asterisks or special formatting (e.g., *Ben:*). Begin the script directly with dialogue.

Example with names Aisha, Rahul, Priya:
Host: Welcome to our podcast, where we discuss all things related to sports. Today's topic is India at the Olympics. I'm your host, Aisha, and joining me are our sports experts – Rahul and Priya.

Rahul: India has a long history at the Olympics, starting in 1900 when Norman Pritchard won two silver medals. Since then, India has been a regular participant, with the Men's Field Hockey Team dominating between 1928 and 1980.

Example with names Aisha, Rahul:
Host: Welcome to our podcast on sports. Today’s topic is India at the Olympics. I'm your host, Aisha, and with me is our guest, Rahul.

Rahul: India’s Olympic journey began in 1900, with Norman Pritchard winning two silver medals. India has been a regular participant since then, especially excelling in field hockey.
"""
