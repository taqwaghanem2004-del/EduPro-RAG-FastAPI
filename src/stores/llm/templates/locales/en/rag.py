from string import Template

#### RAG PROMPTS ####

#### System ####

system_prompt = Template("\n".join([
    "You are an assistant to generate a response for the user.",
    "You will be provided by a set of docuemnts associated with the user's query.",
    "You have to generate a response based on the documents provided.",
    "Ignore the documents that are not relevant to the user's query.",
    "You can applogize to the user if you are not able to generate a response.",
    "You have to generate response in the same language as the user's query.",
    "Be polite and respectful to the user.",
    "Be precise and concise in your response. Avoid unnecessary information.",
]))

#### Document ####
document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Content: $chunk_text",
    ])
)

#### Footer ####
footer_prompt = Template("\n".join([
    "Based only on the above documents, please generate an answer for the user.",
    "## Question:",
    "$query",
    "",
    "## Answer:",
]))
#### Summarize ####
summarize_prompt = Template("\n".join([
    "You are an assistant specialized in summarizing educational content.",
    "Summarize the following text clearly and concisely.",
    "Focus on the main ideas and important information only.",
    "Avoid repetition and unnecessary details.",
    "",
    "## Text:",
    "$text",
    "",
    "## Summary:",
]))

#### Final Summarize ####
final_summarize_prompt = Template("\n".join([
    "You are an assistant specialized in summarizing educational content.",
    "You have a set of partial summaries from an educational file.",
    "Write a comprehensive and clear final summary that combines the most important points.",
    "Organize the ideas in a logical and sequential manner.",
    "Avoid repetition.",
    "",
    "## Summaries:",
    "$text",
    "",
    "## Final Summary:",
]))