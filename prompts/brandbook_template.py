brandbook_template = """
    We are creating a brand book for a company. Based on the following details, generate a brand book in dictionary format with the keys: Slogan, Brand Values, Vision, Voice, Product/Service, and Color Palate.
    Each section should be detailed and comprehensive, providing a full and descriptive overview. Use the following format:
    - Slogan: One-liner (e.g., 'dar ke agge jit hai')

      Brand Values: An array of 6 points, each structured as follows:

        "Brand Values": [
        {{
            "heading": "...",
            "subHeading": "...",
            "description": "..."
        }},
        {{
            "...": "..."
        }}
      ],
      "Vision": {{
        "oneLiner": "Your concise vision statement",
        "description": "description in exactly 300 words"
      }},
      "Voice": {{
        "oneLiner": "Your concise voice statement",
        "description": "description in exactly 300 words"
      }},
      "Product/Service": [
        "One Liner (30 words)",
        "Point 1 (10-15 words)",
        "Point 2 (10-15 words)",
        "Point 3 (10-15 words)"
      ],
      "Color Palatte": [
        "#8378bd",
        "#8378bd",
        "#8378bd",
        "#8378bd",
        "#8378bd",
        "#8378bd"
      ],
      "Suggested Icon": "Your suggested icon",
      "Suggested Font": "Your suggested font"
    }}

    Company Name: {company_name}
    Description/Prompt: {description}
    Industry: {industry}
    Sector: {sector}
    Service Description / Product Description: {service_description}
    Color Palate: {color_palate}
    Targeted Audience: {targeted_audience}
    Gender: {gender}
    Age: {age}
    Location: {location}

        One icon to be suggested from this only, based on  {industry}:
    -Computers & Devices
    -Crypto
    -Lifestyle
    -Productivity
    -Social Media
    -Medical/Medico
    -Finance
    -Video,Audio,Image
    -Food
    -Money

   One Font to be suggested from this:
   -Roboto
   -Open Sans
   -Lato
   -Montserrat
   -Oswald
   -Raleway
   -PT Sans
   -PT Serif
   -Merriweather
   -Source Sans Pro
   -Poppins
   -Nunito
   -Josefin Sans
   -Roboto Condensed
   -Work Sans
   -Playfair Display
   -Quicksand
   -Bebas Neue
   -Libre Baskerville
   -Cormorant Garamond


    example for vision description:"At Kreaitor AI Company, our vision is to revolutionize the way businesses and individuals create content by leveraging the power of artificial intelligence. We aspire to become the global leader in AI-driven content creation tools, enabling users to produce high-quality, engaging content with ease and efficiency. Our vision is grounded in the belief that AI can significantly enhance creativity and productivity, allowing users to focus on their core strengths while our tools handle the repetitive and time-consuming tasks. We aim to build a future where AI-powered content creation is accessible to everyone, regardless of technical expertise, and is seamlessly integrated into everyday workflows. By continuously innovating and improving our products, we strive to stay ahead of the curve and anticipate the evolving needs of our users. Our commitment to ethical AI practices ensures that our solutions are not only powerful but also trustworthy and transparent. Through collaboration with our users and partners, we seek to foster a vibrant community of creators who are empowered by our technology to achieve their goals and realize their full potential. Ultimately, our vision is to transform the content creation landscape, making it more efficient, enjoyable, and impactful for all."
    example for voice description:"At Kreaitor AI Company, our voice is characterized by clarity, approachability, and inspiration. We communicate with our audience in a way that is both informative and engaging, ensuring that complex AI concepts are accessible to all. Our tone is friendly and supportive, reflecting our commitment to customer success and satisfaction. We strive to inspire our users by showcasing the potential of AI in content creation, and we maintain a conversational style that encourages interaction and feedback. Our communications are underpinned by transparency and honesty, as we believe in building trust with our audience through open and straightforward dialogue. Whether we are providing product updates, sharing industry insights, or offering support, our voice remains consistent, reinforcing our brand values and fostering a sense of community among our users. We aim to be not just a service provider but a partner in our users' creative journeys, guiding them with expertise and enthusiasm."
    example for Product/Service: [
    "One Liner:" Our AI-powered tools revolutionize content creation, enabling businesses and individuals to generate high-quality, engaging, and impactful content efficiently, effectively, and with ease. These tools transform digital presence, drive significant growth, and provide unparalleled value, making content creation simpler and more effective than ever before",
    "Point 1: Intuitive user interface designed for a seamless, user-friendly experience that simplifies complex tasks and increases productivity.",
    "Point 2: Real-time collaboration features that enhance teamwork, streamline workflows, and facilitate efficient project management for maximum efficiency and output.",
    "Point 3: Advanced AI algorithms analyze, optimize content quality, provide insights, and ensure exceptional results that meet the highest standards."


]
"""