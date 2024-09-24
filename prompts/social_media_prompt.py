from langchain.prompts import PromptTemplate

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
    },
    "FacebookContent": {
        "BrandPromotionPost": {
            "New Product": "Announce new products with vibrant visuals and enthusiastic language. Highlight the main features and benefits, and include a call to action like 'Shop Now' or 'Learn More'.",
            "Brand Story": "Share your brand's story or mission to connect emotionally with your audience. Use engaging visuals and storytelling techniques. Encourage interaction with a call to action like 'Share Your Story' or 'Join Our Community'.",
            "Customer Engagement": "Engage your audience with interactive content like polls, questions, or contests. Use visuals and language that encourage participation. Include a call to action such as 'Vote Now' or 'Comment Below'.",
            "Default": "Regularly post a variety of brand promotion content to keep your audience engaged. Mix product highlights, brand stories, and interactive posts. Always include strong visuals and clear calls to action to drive engagement."
        },
        "CustomerSuccessStory": {
            "Testimonial": "Share customer testimonials that highlight positive experiences with your product or service. Use direct quotes and high-quality images of the customer or the product in use. Include a call to action like 'Read More Stories' or 'Share Your Experience'.",
            "Case Study": "Present in-depth case studies that detail how your product or service solved a customer's problem. Use a narrative format with clear before-and-after scenarios. Include a call to action like 'Learn More' or 'See Results'.",
            "Video Testimonial": "Post video testimonials to bring customer stories to life. Ensure the video is high-quality and authentic. Include a call to action like 'Watch Now' or 'Share Your Story'.",
            "Default": "Consistently share a mix of written, visual, and video testimonials to build trust and credibility. Highlight diverse customer experiences and always include a call to action to engage your audience further."
        },
        "Ads": {
            "Product Ad": "Create ads that highlight a specific product with eye-catching visuals and a clear value proposition. Use a call to action like 'Buy Now' or 'Shop Today'.",
            "Event Ad": "Promote events with compelling images or videos, including key details like date and location. Use a call to action such as 'Register Now' or 'Save Your Spot'.",
            "Service Ad": "Advertise services by focusing on the benefits and outcomes. Use testimonials or case studies to add credibility. Include a call to action like 'Learn More' or 'Contact Us'.",
            "General": "Run ads that are broadly aimed at building brand awareness. Use strong visuals and a simple, clear message. Include a call to action like 'Learn More' or 'Follow Us'.",
            "Default": "Regularly update your ad campaigns with fresh content and visuals. Test different formats and calls to action to see what resonates best with your audience. Ensure all ads align with your overall brand message."
        },
        "PostCaption": {
            "Informative": "Craft informative post captions that provide value to your audience. Use concise language and bullet points if necessary to break down the information. Include a call to action like 'Learn More' or 'Discover Tips'.",
            "Engaging": "Write engaging captions that encourage interaction. Ask questions, use humor, or create curiosity. Include a call to action like 'Comment Below' or 'Share Your Thoughts'.",
            "Inspirational": "Create inspirational captions that resonate emotionally with your audience. Use quotes, stories, or motivational language. Include a call to action like 'Get Inspired' or 'Join the Movement'.",
            "Default": "Maintain a balance of informative, engaging, and inspirational captions in your posts. Tailor the tone and content to match the accompanying visuals and always include a clear call to action."
        },
        "PostCaption": {
            "Informative": "Craft informative post captions that provide value to your audience. Use concise language and bullet points if necessary to break down the information. Include a call to action like 'Learn More' or 'Discover Tips'.",
            "Engaging": "Write engaging captions that encourage interaction. Ask questions, use humor, or create curiosity. Include a call to action like 'Comment Below' or 'Share Your Thoughts'.",
            "Inspirational": "Create inspirational captions that resonate emotionally with your audience. Use quotes, stories, or motivational language. Include a call to action like 'Get Inspired' or 'Join the Movement'.",
            "Default": "Maintain a balance of informative, engaging, and inspirational captions in your posts. Tailor the tone and content to match the accompanying visuals and always include a clear call to action."
        },
        "PostImage": {
            "High-Quality Visuals": "Use high-quality images that are visually appealing and relevant to the post content. Ensure images are well-lit, in focus, and high resolution to attract and retain attention.",
            "Branded Content": "Incorporate your brand’s colors, logo, or elements into images to maintain consistency. Use branded templates or frames to make your posts easily recognizable.",
            "Infographics": "Share infographics that convey information quickly and effectively. Use clear and simple graphics to highlight key points and make data easily digestible. Ensure text is legible even on smaller screens.",
            "Default": "Regularly update your visuals to keep your content fresh and engaging. Use a variety of image types including high-quality photos, branded content, and infographics. Ensure all visuals align with your brand’s aesthetic and message."
        }
    },
    "YouTubeContent": {
        "VideoDescription": {
            "FromPoints": "Craft video descriptions that expand on key points covered in the video. Include timestamps for easy navigation and relevant links for more information. Use keywords to improve searchability and a call to action like 'Subscribe' or 'Leave a Comment'.",
            "ThumbnailDescription": "Write concise descriptions for video thumbnails that are catchy and relevant to the content. Ensure the text is readable and complements the visual elements. Include keywords and a call to action like 'Watch Now'.",
            "ChannelDescription": "Create a channel description that clearly explains what your channel is about, the type of content you produce, and the value it offers to viewers. Include information about your posting schedule and a call to action like 'Subscribe for Updates'.",
            "Default": "Regularly update your video descriptions with new keywords and relevant links. Maintain a consistent format that includes key points, timestamps, and calls to action. Ensure descriptions align with your overall channel branding."
        },
        "VideoIdeas": {
            "Educational": "Generate video ideas that provide value through education, such as 'How-to' guides, tutorials, and explainer videos. Focus on trending topics or common questions in your niche.",
            "Entertainment": "Develop ideas for entertaining content like challenges, behind-the-scenes footage, or vlogs. Consider what’s currently popular with your audience and how you can put your own unique spin on it.",
            "Product Reviews": "Plan video reviews of popular or new products in your industry. Provide honest, detailed evaluations and comparisons to help your audience make informed decisions.",
            "Interviews": "Schedule interviews with industry experts, influencers, or interesting personalities. Prepare engaging questions that will provide valuable insights for your audience.",
            "Default": "Maintain a diverse mix of video ideas to keep your content fresh and engaging. Regularly review performance metrics to refine and improve your content strategy."
        },
        "VideoScripts": {
            "GivenPointers": "Develop scripts that follow the key pointers for the video. Start with a strong hook to grab attention, followed by an introduction that outlines what the video will cover. Expand on each point in a clear, logical sequence, and conclude with a summary and a call to action like 'Subscribe' or 'Visit Our Website'.",
            "Detailed": "Write detailed scripts that include camera directions, dialogue, and timing cues. Ensure the script flows naturally and maintains viewer interest throughout. Include prompts for visual aids or on-screen text where necessary.",
            "Default": "Create a standard template for your video scripts to ensure consistency. Include key sections such as the hook, introduction, main content, and conclusion. Regularly update the template based on viewer feedback and performance data."
        },
        "CoverPicture": {
            "DesignTips": "Create cover pictures (thumbnails) that are visually striking and relevant to the video content. Use bright colors, clear text, and high-contrast images to stand out. Ensure the design aligns with your channel’s branding.",
            "Tools": "Utilize design tools like Canva, Adobe Spark, or Photoshop to create professional-quality thumbnails. Leverage templates to maintain consistency across your videos.",
            "BestPractices": "Follow best practices such as keeping text short and readable, focusing on faces or key visuals, and ensuring the thumbnail looks good at various sizes. A/B test different designs to see what resonates best with your audience.",
            "Default": "Regularly update your cover picture design strategy based on performance metrics and viewer feedback. Ensure all thumbnails maintain a consistent look and feel that represents your brand."
        },
        "ThumbnailGenerator": {
            "AutomatedTools": "Use automated thumbnail generator tools like TubeBuddy or Canva to quickly create thumbnails. Ensure these tools are set up with your brand’s colors and fonts for consistency.",
            "Customization": "Customize generated thumbnails to add unique touches that reflect the video’s content. Adjust elements like text size, placement, and image cropping to optimize visual appeal.",
            "Review": "Review the automatically generated thumbnails to ensure they meet your quality standards. Make manual adjustments as needed to enhance clarity and attractiveness.",
            "Default": "Integrate thumbnail generators into your content creation workflow to save time while maintaining high-quality visuals. Regularly review and update settings to align with your evolving brand style."
        }
    },
    "InstagramContent": {
        "InstagramPostCaption": {
            "Witty": "Craft witty captions that incorporate humor or clever wordplay. Example: 'Life isn’t perfect, but your outfit can be! 😎 #FashionGoals'",
            "Philosophical": "Write captions that provoke thought or contemplation. Example: 'In the end, we only regret the chances we didn’t take. ✨ #CarpeDiem'",
            "Inspiring": "Create captions that uplift and motivate your audience. Example: 'Believe you can, and you're halfway there. 💪 #MondayMotivation'",
            "Default": "Mix up your caption styles to cater to different audience preferences. Always include relevant hashtags and a call to action."
        },
        "PostImage": {
            "High-Quality Visuals": "Share visually appealing images that capture attention and represent your brand aesthetic.",
            "Branded Content": "Incorporate your brand's colors, logo, or elements into images to maintain brand consistency and recognition.",
            "Variety of Content": "Diversify your image posts with a mix of product shots, lifestyle images, user-generated content, and behind-the-scenes shots.",
            "Default": "Regularly update your image content to keep your feed fresh and engaging. Ensure all images align with your brand identity and messaging."
        },
        "Ad": {
            "Image": "Create visually compelling ads that showcase your product or service. Use eye-catching imagery and clear messaging to drive engagement and conversions.",
            "Default": "Consistently monitor and optimize your ad performance to maximize ROI. Test different ad formats, targeting options, and creatives to find what works best for your audience."
        },
        "ReelIdeas": {
            "Trendy Challenges": "Participate in popular challenges or trends within your niche. Put your own unique spin on it to stand out.",
            "Educational Tutorials": "provide idead in point for instagram reels.Share quick and informative tutorials related to your industry or niche. Provide value to your audience while showcasing your expertise.",
            "Behind-the-Scenes": "Give your audience a glimpse behind the scenes of your business or creative process. Humanize your brand and build authenticity.",
            "Comedic Skits": "Create short comedic skits or sketches that entertain your audience while still aligning with your brand identity.",
            "Default": "Stay up-to-date with current trends and leverage them to create engaging Reels content. Experiment with different formats and styles to find what resonates with your audience."
        },
        "PromotionalPost": {
            "New Product": "Promote new products with visually appealing content and compelling messaging. Highlight key features and benefits to entice your audience.",
            "Limited-Time Offers": "Create urgency with promotions and discounts that are available for a limited time only. Use persuasive language to encourage immediate action.",
            "Collaboration Deals": "Partner with influencers or other brands for collaborative promotions. Leverage their audience to expand your reach and credibility.",
            "Default": "Ensure promotional posts are aligned with your brand voice and values. Provide clear and concise information along with a strong call to action."
        },
        "ReelAudio": {
            "Enabling 30-Second Audio": "Utilize the 30-second audio feature when available to add a dynamic element to your Reels. Choose music or sound effects that enhance the mood or message of your content.",
            "Default": "Incorporate audio into your Reels to make them more engaging and memorable. Experiment with different tracks and audio effects to find the perfect fit for your content."
        }
    },
    "TikTokContent": {
        "Captions": {
            "Short": "Write brief, catchy captions that complement your video content. Example: 'New hack! 👀 #LifeHack'",
            "Engaging": "Encourage viewers to interact with your video by asking questions or using call to actions. Example: 'What's your favorite trick? Let us know! 💡'",
            "Informative": "Provide key information or context for your video. Example: '3 easy steps to perfect pancakes! 🥞 #CookingTips'",
            "Humorous": "Add a touch of humor to your captions to make them more relatable. Example: 'When you finally get it right... 😂 #NailedIt'",
            "Witty": "Infuse your captions with clever wordplay or witty remarks to entertain your audience. Example: 'Life's a beach, and I'm just playing in the sand. 🏖️ #SummerVibes'",
            "Philosophical": "Share thought-provoking insights or philosophical reflections in your captions. Example: 'In a world full of noise, find your inner peace. 🧘 #Mindfulness'",
            "Inspiring": "Motivate and inspire your audience with uplifting messages in your captions. Example: 'Dream big, work hard, stay focused. You've got this! 💪 #Inspiration'",
            "Default": "Use a variety of caption styles to keep your content fresh. Include relevant hashtags to boost discoverability."
        },
        "VideoIdeas": {
            "Tutorials": "Create step-by-step guides for popular or trending topics. Example: 'Learn how to make DIY face masks at home! #DIYBeauty'",
            "Challenges": "Participate in or create new challenges. Example: 'Can you do this dance? Show us! #DanceChallenge'",
            "BehindTheScenes": "Share behind-the-scenes footage of your brand or creative process. Example: 'A day in the life at our studio. #BTS'",
            "Product Demos": "Show your product in action. Example: 'Check out our new gadget! Here's how it works. #TechDemo'",
            "User-Generated Content": "Feature content created by your followers. Example: 'We love your creativity! Keep sharing with #MyBrandChallenge'",
            "Ideas on the topic": "Brainstorm creative video ideas related to your niche or industry. Example: 'Exploring new trends in fashion. What's hot this season?'",
            "Ideas for a business": "Generate video ideas that promote your business or brand. Example: 'Showcasing our latest collection. Which piece is your favorite?'",
            "Default": "Keep up with TikTok trends and tailor your content to fit your brand voice. Use a mix of video ideas to engage your audience."
        },
        "Scripts": {
            "Hook": "Start with a strong hook to grab attention in the first few seconds. Example: 'Did you know you can do this with a paperclip? #LifeHacks'",
            "Introduction": "Briefly introduce what your video is about. Example: 'Today, we're showing you three easy workouts you can do at home.'",
            "Main Content": "Present the main content in a clear, engaging manner. Example: 'First, you'll need a rubber band. Here's how to use it...'",
            "Call to Action": "End with a call to action to encourage interaction. Example: 'Try it out and tag us in your videos! #TryItYourself'",
            "Tik Tok Script": "Develop scripts tailored for TikTok videos, ensuring they are concise and engaging. Example: 'Let's dive into the world of beauty hacks! Here's a quick tip for flawless skin.'",
            "Default": "Ensure your scripts are concise and engaging. Adapt your script style to fit the video format and audience."
        },
        "Descriptions": {
            "FromPoints": "Expand on key points covered in the video. Example: '3 tips for better sleep: 1. Stick to a schedule 2. Create a restful environment 3. Avoid screens before bed. #BetterSleep'",
            "Engaging": "Create descriptions that encourage viewers to watch and interact. Example: 'Can you believe this trick actually works? Watch to find out! #MagicTrick'",
            "Informative": "Provide detailed information relevant to the video content. Example: 'Here's a quick guide to organizing your workspace for maximum productivity. #WorkFromHome'",
            "Ideas on the topic": "Write informative video descriptions that expand on the topic discussed in the video. Example: 'Exploring sustainable fashion and its impact on the environment. Learn more in this eye-opening video!'",
            "Ideas for a business": "Craft engaging video descriptions that promote your business or products. Example: 'Discover the secret behind our bestselling skincare line. Watch now to reveal flawless skin!'",
            "Default": "Use keywords and hashtags to improve searchability. Keep descriptions relevant and engaging."
        },
        "Hashtags": {
            "Trending": "Use trending hashtags to increase visibility. Example: '#ForYou #ViralVideos'",
            "Branded": "Create and use branded hashtags to promote your brand. Example: '#MyBrandLife #BrandChallenge'",
            "Niche": "Include niche-specific hashtags to reach your target audience. Example: '#FitnessTips #HealthyLiving'",
            "Business-specific": "Incorporate hashtags related to your business or industry to attract relevant viewers. Example: '#FashionTech #BeautyHacks'",
            "Default": "Mix trending, branded, niche, and business-specific hashtags to optimize reach and engagement. Research popular hashtags in your niche regularly."
        }
    },
    "PinterestContent": {
        "Pins": {
            "Product Pins": "Create high-quality images that showcase your product. Include a detailed description and a call to action like 'Shop now'. Example: 'Our new eco-friendly tote is perfect for summer! 🌿 #EcoFriendly'",
            "Recipe Pins": "Share visually appealing images of your recipes. Include the recipe name, ingredients, and a link to the full recipe. Example: 'Delicious vegan chocolate cake! 🍫 Find the recipe at the link. #VeganRecipes'",
            "DIY Pins": "Post step-by-step images of DIY projects. Include a brief description and link to a detailed tutorial. Example: 'DIY terrarium tutorial – easy and fun! 🌱 #DIYHome'",
            "Infographic Pins": "Design infographics with valuable information. Use clear headings and concise text. Include your brand logo and a link. Example: '10 tips for better sleep. 😴 Click for more! #HealthTips'",
            "Travel Pins": "Share beautiful images of travel destinations. Include tips and must-see attractions. Example: 'Top 10 places to visit in Italy! 🇮🇹 #TravelGoals'",
            "Product Description": "Craft compelling descriptions that highlight the unique features and benefits of your product. Example: 'Our eco-friendly tote is made from sustainable materials, perfect for the environmentally conscious fashionista. Click to shop now! 🌎'",
            "Promotional Post": "Create engaging posts to promote special offers or discounts. Use eye-catching visuals and clear messaging. Example: 'Flash sale alert! Get 20% off our entire summer collection for a limited time. Shop now! ☀️'",
            "How-to guide": "Provide step-by-step instructions for completing a task or project. Use clear visuals and concise language. Example: 'DIY guide: How to create your own terrarium in 5 easy steps! 🌿 #DIYProject'",
            "Default": "Ensure all pins have high-quality images and detailed descriptions. Include keywords and a call to action."
        },
        "Boards": {
            "Themed Boards": "Create boards around specific themes relevant to your brand. Example: 'Healthy Recipes', 'Home Decor Ideas'. Include high-quality pins and organize them logically.",
            "Product Collections": "Showcase collections of your products. Include detailed descriptions and links to purchase pages. Example: 'Summer Collection', 'Best Sellers'.",
            "Inspirational Boards": "Curate boards with inspirational content. Example: 'Motivation', 'Success Stories'. Include motivational quotes and stories.",
            "Educational Boards": "Provide educational content. Example: 'Marketing Tips', 'DIY Projects'. Include infographics and how-to guides.",
            "Collaborative Boards": "Invite users or influencers to contribute. Example: 'Collaborations', 'Community Favorites'. This can increase engagement and reach.",
            "Default": "Regularly update boards with fresh content. Ensure each board has a clear focus and is well-organized."
        },
        "Descriptions": {
            "SEO Optimized": "Write descriptions with relevant keywords. Example: 'Discover how to create a beautiful DIY garden. #DIY #Gardening'. Provide clear and concise information.",
            "Storytelling": "Craft descriptions that tell a story or share an experience. Example: 'This recipe brings back memories of my grandmother's kitchen. #FamilyRecipe'.",
            "Informative": "Include detailed information about the pin. Example: 'Learn the top 10 tips for creating a productive home office. #WorkFromHome'. Provide tips or interesting facts.",
            "Call to Action": "Encourage viewers to take action. Example: 'Click the link for the full tutorial and start your project today! #Crafting'.",
            "Product Description": "Craft compelling descriptions that highlight the unique features and benefits of your product. Example: 'Our eco-friendly tote is made from sustainable materials, perfect for the environmentally conscious fashionista. Click to shop now! 🌎'",
            "Promotional Post": "Create engaging posts to promote special offers or discounts. Use eye-catching visuals and clear messaging. Example: 'Flash sale alert! Get 20% off our entire summer collection for a limited time. Shop now! ☀️'",
            "How-to guide": "Provide step-by-step instructions for completing a task or project. Use clear visuals and concise language. Example: 'DIY guide: How to create your own terrarium in 5 easy steps! 🌿 #DIYProject'",
            "Default": "Maintain a consistent tone and style. Use a mix of storytelling, informative, and call-to-action elements."
        },
        "Marketing": {
            "Promoted Pins": "Invest in promoted pins to reach a larger audience. Example: 'Try our new summer collection! Click to shop. #SummerStyle'. Target based on interests and demographics.",
            "Seasonal Campaigns": "Run campaigns around seasonal events. Example: 'Holiday Gift Ideas', 'Summer Activities'. Create themed pins and boards.",
            "Partnerships": "Collaborate with influencers or brands. Example: 'Partnered with @influencer for a special project! #BrandCollab'. Highlight partnership benefits.",
            "Content Series": "Develop a series of related pins. Example: '30 Days of Healthy Eating', 'Weekly DIY Projects'. Use consistent branding.",
            "Engagement Campaigns": "Run campaigns that encourage interaction. Example: 'Share your DIY project with #YourBrandDIY for a chance to be featured!'.",
            "Default": "Align marketing initiatives with your brand strategy. Use a mix of organic and promoted content."
        },
        "Titles": {
            "Direct": "Write clear and direct titles. Example: '10 Easy DIY Home Decor Ideas'. Use strong keywords.",
            "Intriguing": "Craft titles that pique curiosity. Example: 'You Won't Believe These Home Organization Hacks!'.",
            "SEO Focused": "Include relevant keywords. Example: 'Best Vegan Recipes for Healthy Living'.",
            "Instructional": "Highlight instructional content. Example: 'How to Create a Stunning Garden on a Budget'.",
            "Default": "Ensure titles are concise, engaging, and relevant. Use a mix of styles."
        },
        "Project Ideas": {
            "Seasonal Projects": "Align projects with current seasons or holidays. Example: 'DIY Christmas Decorations', 'Summer Outdoor Projects'.",
            "Challenges": "Encourage participation and engagement. Example: '30-Day Fitness Challenge', 'Weekly Craft Projects'.",
            "Collaborative Projects": "Partner with other creators or brands. Example: 'Collaborative Recipe Series', 'Co-Hosted DIY Tutorials'.",
            "Educational Series": "Provide educational content. Example: 'Beginner's Guide to Gardening', 'Advanced Cooking Techniques'.",
            "Interactive Projects": "Involve user interaction. Example: 'Share Your Best Travel Photos', 'DIY Contest with Prizes'.",
            "Default": "Regularly brainstorm new project ideas. Ensure projects align with brand values and audience interests."
        }
    }
},
Tone = {
    "Default": "Use voicing according to the content",
    "Funny": "Incorporate humor through jokes, witty remarks, or playful visuals. Keep it light-hearted and relatable to your audience, avoiding controversial or sensitive topics.",
    "Nostalgic": "Evoke memories of the past by referencing popular trends, personal milestones, or historical events. The tone should be warm and inviting, aiming to create a sentimental connection with the audience.",
    "Angry": "Express displeasure or frustration about specific situations or injustices. Keep the language controlled and focused, using this tone to draw attention to important issues and call for action without alienating the audience.",
    "Empathetic": "Show understanding and compassion towards issues or personal stories shared by your audience. Use a caring and supportive language to foster a sense of community and trust.",
    "Sarcastic": "Use irony and sharp wit to make a point or criticize something. Ensure the sarcasm is evident and does not come off as malicious or offensive, maintaining a balance between humor and message clarity.",
    "Sad": "Use a sensitive and sincere tone to discuss serious issues or events that may evoke sadness. This approach should be used to connect on a deeper emotional level or to show solidarity during tough times.",
}

def social_media_prompt(query, summary, socialmedia, post_topic, sub_topic, tone, words):
    # If socialmedia is a tuple, extract the first element (platform name)
    if isinstance(socialmedia, tuple):
        socialmedia = socialmedia[0]

    # Retrieve content for the specified social media platform, post topic, and sub-topic
    platform_content = SocialMedia.get(socialmedia, {}).get(post_topic, {})
    post_content = platform_content.get(sub_topic, "Default")  # Fallback if not found

    return PromptTemplate(
        template=f"""
        Create a social media post on: {query}
        Use this as contextual information: {summary}

        Post Content: {post_content}
        Tune it for: {socialmedia}

        Use this tone for writing and delivery: {tone}
        Word length: Try to use around {words} words.

        Don't provide outdated data.
        """,
        input_variables=["query", "summary"],
        partial_variables={
            "socialmedia": socialmedia,
            "tone": tone,
            "words": words,
            "post_content": post_content  # Include the content of the post in the partial variables
        }
    )
