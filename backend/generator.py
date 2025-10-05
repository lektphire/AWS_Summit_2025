import time
import boto3
import json

# Setup bedrock
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

def generate_conversation(model_id, system_prompts, messages):
    print(f"Generating with model {model_id}")
    
    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig={"temperature": 0.5}
    )
    
    return response["output"]["message"]["content"][0]["text"]

def summarize_text(text):
    system_prompts = [{"text": "You are an app that creates summaries of text in 50 words or less."}]
    messages = [{"role": "user", "content": [{"text": f"Summarize the following text: {text}."}]}]
    return generate_conversation("us.amazon.nova-pro-v1:0", system_prompts, messages)

def sentiment_analysis(text):
    system_prompts = [{"text": "You are a bot that takes text and returns a JSON object of sentiment analysis."}]
    messages = [{"role": "user", "content": [{"text": f"{text}"}]}]
    return generate_conversation("us.amazon.nova-pro-v1:0", system_prompts, messages)

def perform_qa(question, text):
    system_prompts = [{"text": f"Given the following text, answer the question. If the answer is not in the text, 'say you do not know'. Here is the text: {text}"}]
    messages = [{"role": "user", "content": [{"text": f"{question}"}]}]
    return generate_conversation("us.amazon.nova-pro-v1:0", system_prompts, messages)

def summarize_emails(text):
    system_prompts = [{"text": """
                       You are an email assistant that creates concise summaries of email content. 
                       Focus on key actions, deadlines, and important information. 
                       Group related emails together.
                       If there is no email content, say 'No recent email content'.
                       If there is no summary, say 'No summary'.
                       Ignore obvious spam.
                       Categorize emails urgent, updates, subscribed emails, communications, and low-priority.
                       Do not exceed 100 words per section.
                       """}]
    messages = [{"role": "user", "content": [{"text": f"Summarize this email: {text}"}]}]
    return generate_conversation("us.amazon.nova-pro-v1:0", system_prompts, messages)


if __name__ == "__main__":
    # Sample text for summarization
    text = "Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Luma, Meta, Mistral AI, poolside (coming soon), Stability AI, and Amazon through a single API, along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI. Using Amazon Bedrock, you can easily experiment with and evaluate top FMs for your use case, privately customize them with your data using techniques such as fine-tuning and Retrieval Augmented Generation (RAG), and build agents that execute tasks using your enterprise systems and data sources. Since Amazon Bedrock is serverless, you don't have to manage any infrastructure, and you can securely integrate and deploy generative AI capabilities into your applications using the AWS services you are already familiar with"

    print("\n=== Summarization Example ===")
    summary = summarize_text(text)
    print(f"Summary:\n{summary}")
    time.sleep(2)

    print("\n=== Sentiment Analysis Example ===")
    sentiment_analysis_json = sentiment_analysis(text)
    print(f"Sentiment_Analysis JSON:\n{sentiment_analysis_json}")
    time.sleep(2)

    print("\n=== Q&A Example ===")

    q1 = "How many companies have models in Amazon Bedrock?"
    print(q1)
    answer = perform_qa(q1, text)
    print(f"Answer: {answer}\n")
    time.sleep(2)

    q2 = "Can Amazon Bedrock support RAG?"
    print(q2)
    answer = perform_qa(q2, text)
    print(f"Answer: {answer}\n")
    time.sleep(2)

    q3 = "When was Amazon Bedrock announced?"
    print(q3)
    answer = perform_qa(q3, text)
    print(f"Answer: {answer}\n")
