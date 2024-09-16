from langchain_core.prompts import PromptTemplate
grammar_suggestion = PromptTemplate(
    template="Identify all sentences or words that can be improved and suggest better alternatives for each one (like Grammarly).\n{format_instructions}\n.Here is the paragraph to be corrected{paragraph}\n",
    input_variables=["paragraph"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
