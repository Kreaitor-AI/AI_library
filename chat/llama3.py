from together import Together

class Llama3Client:
    def __init__(self, api_key):
        self.client = Together(api_key=api_key)

    def get_response(self, prompt, stream=False):
        if stream:
            # Streaming mode
            stream_response = self.client.chat.completions.create(
                model="meta-llama/Llama-3-70b-chat-hf",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )

            for chunk in stream_response:
                print(chunk.choices[0].delta.content or "", end="", flush=True)
        else:
            # Non-streaming mode
            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3-70b-chat-hf",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message['content']