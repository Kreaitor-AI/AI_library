from langchain.prompts import PromptTemplate

def email_prompt(user_input, post_body, tone, words):
    """
    Constructs a PromptTemplate for generating email content.

    Args:
        user_input (str): The topic or subject of the email.
        post_body (str): The body content of the email.
        tone (str): The tone to be used in the email.
        words (str): The desired word count for the email.

    Returns:
        PromptTemplate: The formatted prompt template.
    """
    return PromptTemplate(
        template=f"""
        Create an email on: {user_input}
        Post type: {post_body}

        Use this tone for writing and delivery: {tone}
        Word length: Try to use around {words} words.
        """,
        input_variables=["user_input"],
        partial_variables={
            "post": post_body,
            "tone": tone,
            "words": words
        }
    )
