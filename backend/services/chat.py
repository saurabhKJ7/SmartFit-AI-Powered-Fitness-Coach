from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def chat_with_llm(query):
    llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0,
    max_tokens=200
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant .",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
chain.invoke(
    {
        "input": "{input}"
    }
)
