from core.rag import answer

print("🤖 Type 'exit' to quit.")
while True:
    q = input("\nAsk: ").strip()
    if q.lower() == "exit":
        print("Agent: Cya! 👋🏻")
        break
    print("\nAgent Final Reply:")
    print(answer(q))



# from core.rag import answer

# print("RAG Agent ready. Type 'exit' to quit.")
# while True:
#     q = input("\nAsk: ")
#     if q.lower() == "exit":
#         print("Agent: Bye Bye")
#         break
#     print("\nAgent Final Reply:")
#     print(answer(q))