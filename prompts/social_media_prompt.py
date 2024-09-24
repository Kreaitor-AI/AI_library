from langchain.prompts import PromptTemplate

def social_media_prompt(query, summary, platform_key, post_topic, post_subtopic, tone_key, words):
    
    
    SocialMedia = {
        "TwitterContent": {
            "Ad": {
                "Product Highlight": "Feature a product with a high-quality image or short video that showcases the product in action. Focus on one key benefit of the product and explain it in a compelling manner within the tweet. Include a direct call to action such as 'Shop now' with a link to the purchase page.",
                "Event Promotion": "Promote events by focusing on the unique selling points of the event—be it speakers, activities, or potential benefits. Use an event-specific hashtag to track conversations and engagement. A countdown to the event date can build anticipation, with periodic tweets reminding your audience of the event timeline.",
                "Service Showcase": "Highlight services by explaining how they solve common problems or improve situations for your target audience. Include client testimonials or case study snippets where possible. Short video clips or GIFs that demonstrate service benefits can be very effective.",
                "Default": "General advertisements should clearly state what is being offered and its value, accompanied by a strong visual or video. Always end with a straightforward call to action, directing followers to learn more, buy now, or get involved."
            },
            "Marketing": {
                "Teaser": "Craft teasers that build anticipation without giving away too much detail. Use suggestive language and visually engaging media to hint at new releases or upcoming announcements. Encourage followers to guess or speculate in replies to foster interaction and engagement.",
                "Call to Action": "Use persuasive language in your calls to action, making it clear what you want the user to do next. Ensure any links are accompanied by enticing reasons to click through, such as exclusive content, special offers, or more detailed information.",
                "Cross-Promotion": "When cross-promoting, tag partner brands and use a common hashtag to unify the campaign. Share benefits clearly so followers from both sides understand the value of the partnership. Highlight how both audiences can benefit from the collaboration.",
                "Default": "Ensure all marketing tweets align with your overall brand strategy and are tailored to your audience's interests and needs. Mix direct calls to action with engaging, informative content to keep your followers interested and active."
            },
            "Products": {
                "Feature Focus": "Highlight a single feature of your product in each tweet. Describe its benefits succinctly and how it solves a problem or enhances the user's experience. Use compelling visuals or videos to illustrate the feature's impact.",
                "Comparison": "When comparing products, be clear about the advantages using factual data and direct comparisons. Graphs or charts can be effective here. Always be respectful and professional to avoid the appearance of disparaging competitors.",
                "Default": "Regularly feature different aspects of your products, alternating focus between features, benefits, and comparisons. Keep the content fresh and engaging by using varied formats such as images, videos, and quick facts."
            },
            "DiscussionThreads": {
                "DiscussionStarter": "Initiate a discussion by posing a thought-provoking question or statement that is relevant to your industry or a trending topic. Provide some context or background information to encourage deeper understanding. Share your own perspective or opinion on the topic and invite others to do the same. Respond to comments and engage with participants by asking follow-up questions or acknowledging their contributions. Finally, summarize key points discussed in the thread and thank participants for their engagement.",
                "Debate": "Start a debate by introducing a controversial or divisive topic that is relevant to your industry or audience. Present two contrasting viewpoints on the topic, each in its own tweet. Encourage followers to choose a side or share their own perspective. Engage with participants by responding to their arguments and encouraging respectful debate. Offer your own insights or conclusions based on the discussion and thank participants for their contributions.",
                "Q&A": "Host a Q&A session with a specific theme or focus by announcing it in a tweet and inviting followers to ask questions. Share a question posed by a follower along with your answer, providing detailed information or insights. Continue responding to questions from other followers, keeping the conversation flowing. Encourage more participation by reminding followers that the Q&A session is ongoing. Finally, wrap up the thread by summarizing key questions and answers, and express gratitude to participants for their engagement."
            },
            "Crypto": {
                "Market Updates & Analysis": "Timely updates on cryptocurrency prices and trends, supported by visual aids.",
                "Educational Insights": "Simplifying blockchain concepts and educating on safeguarding crypto assets.",
                "Industry Trends & Developments": "Offering insights and predictions on crypto developments, updates on decentralized finance platforms, and coverage of NFT drops, auctions, and sales.",
                "Regulatory & Environmental Focus": "Tracking global crypto regulations and discussing crypto mining sustainability.",
                "Upcoming Events & Innovations": "Providing insights into upcoming ICOs and token sales.",
                "Default": "Ensuring followers stay informed with a mix of market updates, educational insights, and industry trends, using various formats to cater to different preferences and enhance engagement."
            },
            "Stock": {
                "Market Trends Analysis": "In-depth examination of current stock market trends and sector performance.",
                "Stock Spotlight": "Highlighting top-performing stocks and significant market movers together with tips for portfolio management and risk mitigation.",
                "Financial Insights": "Analyzing earnings reports, dividend updates, and financial impacts.",
                "Investor Sentiment Tracking": "Monitoring market sentiment, analyst ratings, and investor behavior.",
                "Corporate Events Coverage": "Updates on IPOs, mergers, acquisitions, and corporate developments.",
                "Default": "Providing a comprehensive blend of market analysis, stock updates, and financial insights to maintain engagement and inform followers."
            },
            "News": {
                "Breaking News Updates": "Quick updates on significant events with visuals.",
                "In-Depth Analysis": "In-depth analysis and opinion pieces on significant events and stories.",
                "Feature Stories": "Human interest stories, influential figures' profiles, and global events coverage.",
                "Interactive Engagement": "Engaging polls, satire, humor, and insights on technology innovations.",
                "Political & Economic Analysis": "Analysis of political events, legislative changes, and economic updates.",
                "Default": "A comprehensive mix of news content to cater to diverse audience preferences and increase engagement."
            },
            "Sports": {
                "Game Highlights": "Recap of recent games, including thrilling moments and standout performances.",
                "Player Profiles": "In-depth features on athletes, highlighting their achievements and personal stories.",
                "Event Previews": "Promotional content for upcoming sports events, detailing schedules and key matchups.",
                "Behind-the-Scenes Insights": "Exclusive glimpses into athlete dynamics, team preparations, and off-field stories.",
                "Fan Engagement Hub": "Interactive polls, fan submissions, and community-driven content to engage sports enthusiasts.",
                "Sports Updates Central": "Real-time updates on injuries, transfers, and emerging talents across various sports.",
                "Default": "A comprehensive mix of sports content to cater to diverse audience preferences and increase engagement."
            },
            "Post and Variation": {
                "Announcement": "Create multiple variations of an announcement to test what resonates best with your audience. Vary the phrasing, use different hashtags, and include various calls to action. Track the performance of each variation to determine the most effective messaging.",
                "Engagement": "Craft different versions of engagement posts to see which generates the most interaction. Ask different questions, use various formats (polls, questions, prompts), and experiment with hashtags. Analyze the results to optimize future engagement strategies.",
                "Informational": "Share the same informational content in multiple formats, such as text-only, with images, or in a thread. Experiment with different styles of presenting the information to see which format your audience prefers. Monitor engagement and adjust accordingly.",
                "Default": "Diversify your posts by creating variations of each type of content. Regularly test different approaches to see what works best for your audience. Keep track of performance metrics to continually refine your content strategy."
            }
        },
        "LinkedInContent": {
            "Ad": {
                "B2B": "Create ads that speak directly to business decision-makers. Highlight how your product or service can improve efficiency, reduce costs, or drive growth. Use professional language and include data or case studies to back up your claims. Encourage clicks with a strong call to action, such as 'Learn More' or 'Request a Demo'.",
                "Professional Services": "Promote your professional services by showcasing your expertise and experience. Use testimonials and client success stories to build trust. Highlight any certifications or awards to add credibility. Make it easy for potential clients to reach out with a clear call to action like 'Contact Us' or 'Schedule a Consultation'.",
                "Event Promotion": "Advertise events by focusing on the key benefits for attendees, such as networking opportunities, learning from industry experts, or gaining valuable insights. Use compelling visuals and include all necessary details like date, time, and location. Add a call to action like 'Register Now' or 'Save Your Seat'.",
                "Default": "Ensure all ads are targeted and relevant to your audience. Use professional imagery and clear, concise messaging. Include a call to action to guide the viewer to the next step, whether it's learning more, signing up, or contacting your team."
            },
            "Headlines": {
                "Direct": "Write headlines that get straight to the point, perfect for job postings or product launches. Use strong, clear language to convey the main message, such as 'Hiring Now: Senior Software Engineer' or 'New Product Launch: AI-Powered Analytics'.",
                "Indirect": "Craft headlines that spark curiosity and encourage further reading, ideal for articles or thought leadership pieces. Examples include 'Why This Trend is Changing the Industry...' or 'The Secret to Improving Your Productivity'.",
                "Default": "Develop headlines that capture attention and encourage engagement. Whether direct or indirect, ensure they align with the content and provide a clear indication of what the reader can expect."
            },
            "TalkingAbout": {
                "Industry Trends": "Share insights on the latest trends in your industry. Provide your analysis and predictions to position yourself as a thought leader. Engage with your audience by asking for their opinions or experiences related to the trend.",
                "Company Culture": "Showcase your company culture by sharing behind-the-scenes content, employee stories, or details about company events. Highlight what makes your workplace unique and appealing to potential hires and partners.",
                "Expert Advice": "Provide valuable advice and tips relevant to your industry. Share your expertise to help your audience solve common problems or improve their skills. This positions your brand as a helpful resource and thought leader.",
                "Default": "Maintain a consistent posting schedule that includes a mix of industry trends, company culture, and expert advice. Engage with your audience by encouraging comments and discussions, and always respond to interactions to foster a community."
            },
            "PromotionalPost": {
                "Product Launch": "Announce new products with excitement and enthusiasm. Highlight the key features and benefits, and explain how it addresses a specific need or problem. Use high-quality visuals and include a call to action such as 'Learn More' or 'Buy Now'.",
                "Service Highlight": "Promote a particular service by explaining how it can benefit your audience. Use real-life examples or case studies to illustrate its effectiveness. Include a call to action like 'Contact Us' or 'Get Started'.",
                "Special Offer": "Advertise special promotions or discounts to create a sense of urgency. Clearly state the offer details and deadline. Use compelling language and visuals to encourage immediate action, and include a call to action like 'Shop Now' or 'Claim Your Discount'.",
                "Default": "Regularly update your audience with promotional posts that highlight your products or services. Use a variety of formats, including images, videos, and testimonials, to keep the content engaging. Always include a clear call to action."
            },
            "JobPostings": {
                "General": "Create job postings that clearly outline the role, responsibilities, and qualifications. Highlight what makes your company a great place to work and any unique benefits or perks. Include a straightforward call to action like 'Apply Now' or 'Submit Your Resume'.",
                "Internships": "Advertise internship opportunities by emphasizing the learning and growth potential. Detail the skills and experience interns will gain, and what makes your internship program unique. Use a call to action like 'Apply for Internship' or 'Start Your Career With Us'.",
                "Executive": "For executive roles, focus on the strategic impact and leadership opportunities. Highlight the key challenges and opportunities the role presents. Use professional, high-level language and a call to action like 'Join Our Leadership Team' or 'Apply for Executive Role'.",
                "Default": "Ensure all job postings are clear and concise, providing essential information about the role and your company. Use engaging language to attract top talent, and include a call to action to encourage applications."
            }
        }
        
    }
    Tone = {
    "Default": "Use voicing according to the content",
    "Funny": "Incorporate humor through jokes, witty remarks, or playful visuals. Keep it light-hearted and relatable to your audience, avoiding controversial or sensitive topics.",
    "Nostalgic": "Evoke memories of the past by referencing popular trends, personal milestones, or historical events. The tone should be warm and inviting, aiming to create a sentimental connection with the audience.",
    "Angry": "Express displeasure or frustration about specific situations or injustices. Keep the language controlled and focused, using this tone to draw attention to important issues and call for action without alienating the audience.",
    "Empathetic": "Show understanding and compassion towards issues or personal stories shared by your audience. Use a caring and supportive language to foster a sense of community and trust.",
    "Sarcastic": "Use irony and sharp wit to make a point or criticize something. Ensure the sarcasm is evident and does not come off as malicious or offensive, maintaining a balance between humor and message clarity.",
    "Sad": "Use a sensitive and sincere tone to discuss serious issues or events that may evoke sadness. This approach should be used to connect on a deeper emotional level or to show solidarity during tough times.",
    }
    
       
    # Retrieve platform-specific content from SocialMedia
    platform_content = SocialMedia.get(platform_key, {})

    # Check if the platform has the specified post_topic
    if post_topic not in platform_content:
        return f"Error: Post topic '{post_topic}' not found in platform '{platform_key}'."

    # Retrieve post content from the topic and subtopic
    topic_content = platform_content.get(post_topic, {})
    post_content = topic_content.get(post_subtopic, topic_content.get("Default", "General Update"))

    # Retrieve the tone description from Tone
    tone_description = Tone.get(tone_key, Tone.get("Default"))

    # Create and return the PromptTemplate
    return PromptTemplate(
        template=f"""
        Create a social media post on: {query}
        Use this as contextual information: {summary}
        Post content: {post_content}
        Use this tone: {tone_description}
        Try to keep the word count around {words}.
        """,
        input_variables=["query", "summary"],
        partial_variables={
            "post_content": post_content,
            "tone_description": tone_description,
            "words": words
        }
    )

