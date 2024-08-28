import argparse
from config import API_KEY, CHROMA_PATH, FILE_PATH, print_api_key
from utilities.document_loader import load_documents
from utilities.text_splitter import split_text
from utilities.chroma_utils import save_to_chroma
from langchain.prompts import ChatPromptTemplate
import cohere
from langchain_community.vectorstores import Chroma
from langchain_cohere import CohereEmbeddings
import os

PROMPT_TEMPLATE = """
Answer the question based only on the following context: {context}

---

Answer the question based on the above context: {question}
"""

def generate_data_store():
    print("\n\nWait a minute; Generating data store...\n\n-------------\n\n")
    documents = load_documents(FILE_PATH)
    chunks = split_text(documents)
    save_to_chroma(chunks, CHROMA_PATH, API_KEY)

def main(query_text=None):
    # generate_data_store()
    if not os.path.exists(CHROMA_PATH):
        print("Data store not found. Generating data store...\n\n-------------\n\n")
        generate_data_store()

    if query_text is None:
        parser = argparse.ArgumentParser()
        parser.add_argument("query_text", type=str, help="The query text.")
        args = parser.parse_args()
        query_text = args.query_text
    else:
        query_text = query_text

    # Prepare the DB.
    embedding_function = CohereEmbeddings(cohere_api_key=API_KEY)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    def normalize_scores(results):
        min_score = min(score for _, score in results)
        max_score = max(score for _, score in results)
        return [(doc, (score - min_score) / (max_score - min_score)) for doc, score in results]

    results = normalize_scores(db.similarity_search_with_relevance_scores(query_text, k=7))
    for i, scoree in results:
        print("scoreee", scoree)

    if len(results) == 0 or all(score < -5000 for _doc, score in results):
        print("Unable to find matching results.")
        return

    # Search the DB.

    # if len(results) == 0 or all(score < 0.7 for _doc, score in results):
    #     print("Unable to find matching results.")
    #     return

    # Process and print valid results
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    print("\n\n\n context_text\n", context_text)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print("Prompt:\n",prompt)

    # # 1. Using Cohere langchain
    # model = Cohere()#using langchain's Cohere
    # response_text = model.predict(prompt)

    # 2. Using the Cohere Chat model
    cohere_client = cohere.Client(API_KEY)  # Cohere Object
    chat = cohere_client.chat(message=prompt, model="command")

    # # 3. Using the Cohere Generate model
    # response = cohere_client.generate(
    #     model='command',  # Use the appropriate model name
    #     prompt=prompt,
    #     # max_tokens=100  # Adjust as needed
    # )
    # response_text3 = response.generations[0].text.strip()

    #View all responses

    # print("1. response_text: ", response_text)
    print("\n\n\n 2. Cohere_chat_Respose: ", chat.text, "\n\n\n")
    # print("3. response_text3:  ", response_text3)
    # print("\n modelres: ", response)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print("Formatted Response:\n", formatted_response)
    # return formatted_response
    return chat.text
    # return chat