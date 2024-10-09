regenerate_brandbook_template = """
Based on the current output of the {section} section, regenerate the {section} section using the following context:

Current Section Content:
{current_section_content}

Prompt:
{prompt}

The format will be:
{format_example}

The response should be a valid JSON object representing the {section} section. Instructions:

One icon to be suggested from this only:
- Computers & Devices
- Crypto
- Lifestyle
- Productivity
- Social Media
- Medical/Medico
- Finance
- Video, Audio, Image
- Food
- Money

One font to be suggested from this only:
- Roboto
- Open Sans
- Lato
- Montserrat
- Oswald
- Raleway
- PT Sans
- PT Serif
- Merriweather
- Source Sans Pro
- Poppins
- Nunito
- Josefin Sans
- Roboto Condensed
- Work Sans
- Playfair Display
- Quicksand
- Bebas Neue
- Libre Baskerville
- Cormorant Garamond
"""