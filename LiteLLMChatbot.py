from smolagents import CodeAgent,LiteLLMModel

model = LiteLLMModel("openai/gpt-3.5-turbo",temperature=0.2)

message = []

while True:
    user_input = input("Enter your message: ")

    if user_input == "exit":
        break

    message.append({"role":"user","content":user_input})

    response = model(message,max_tokens=500)
    assistant_response = response.content

    print("Assistant:",assistant_response)
    message.append({"role":"assistant","content":assistant_response})
