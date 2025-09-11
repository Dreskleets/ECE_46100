from huggingface import select_model, chat_with_model, get_inference_client

#UI Menu Layout

#1.) Reviews
    #SQL lite (6 DB)
        #User Reviews (1-10)
        #Average Runtime (per chat)
#2.) Chat (HF)
#3.) Performance (Testing / Runtime)

#Hugging Face Menu (2)
client = get_inference_client()
model = select_model()
if model:
    chat_with_model(model, client)
