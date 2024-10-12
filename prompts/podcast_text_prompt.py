podcast_text_prompt ="""Generate a podcast script on the topic '{topic}' and the context:{summary_result}. The script should have {num_characters} characters and character names. Make sure to keep {num_characters} only and thats includes host as well. The script should be approximately {length_words} words long. Please make sure that the script is of {length_words}words. Dont add emotions and extra stuff just give the script
Dont start with something like *Ben:* .Dont use stars in the script.

For the genders of host and guest refer:{gender}. In sequence the first gender is for host and sequentailly next are for guests. Name the characters accordingly with real nammes. Dont use something like Dr. Character1 etc.

Example:
Host: Welcome to our podcast, where we discuss all things related to sports and today's topic is India at the Olympics. I'm your host, Aisha, and joining me today are our sports experts – Rahul, Priya, and Arjun.

Rahul: India has a long history at the Olympics, dating back to 1900 when Norman Pritchard won two silver medals. Since then, India has been a regular participant at the Summer Games, with the Men's Field Hockey Team being particularly dominant, winning eleven medals between 1928 and 1980.

Priya: The Indian Olympic movement was formalized in the 1920s with the establishment of the Indian Olympic Association. Over the years, India has had success in various sports at the Olympics, including hockey, wrestling, shooting, badminton, and weightlifting.
"""
