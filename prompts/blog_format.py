blog_format = """
Format the following blog content {summary} using below instructions:

**Instructions:**
1. Use the following markdown tags for formatting:
    - # for Heading level 1
    - ## for Heading level 2
    - ### for Heading level 3
    - [Link](https://example.com) for links (only if available)
    - **Bold text** for bold text
    - *Italic text* for italic text
    - <u>underline text</u> for underline text
    - > for quote text
    - `highlight text` for highlighted text
    - * for unordered list items
    - 1. for ordered list items

2. Provide relevant detailed prompts for each image. Insert images at appropriate places/sections in the blog using FORMAT: {{ImagePromptForBlog: image prompt}}.
3. Do not include any other tags.

Special Instructions:
Strictly adhere to 
Total number of images to be used: {{ImagePromptForBlog: image prompt}}
Each image on a new line only, and no two images together one below another.

Format the content accordingly. Don't start with 'Here is the formatted blog content:'. Directly start with the blog.
"""
