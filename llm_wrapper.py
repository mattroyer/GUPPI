class LLMWrapper:
  def __init__(self, llm_type, model_name):
    self.llm_type = llm_type
    self.model_name = model_name
    self.llm_client = self._initialize_llm()

  def _initialize_llm(self):
    if self.llm_type == 'openai':
      from openai import OpenAI
      import os
      api_key = os.getenv('OPENAI_API_KEY')
      return OpenAI(api_key=api_key)
    elif self.llm_type == 'ollama':
      import ollama
      return ollama
    else:
      raise ValueError("Unsupported LLM type")

  def send_message(self, messages, stream=True):
    if self.llm_type == 'openai':
      completion = self.llm_client.chat.completions.create(model=self.model_name, messages=messages, stream=stream)
      for chunk in completion:
        choice = chunk.choices[0]
        content = choice.delta.content
        role = 'assistant'
        done = choice.finish_reason == 'stop'
        yield {
          'content': content,
          'role': role,
          'done': done
        }
    elif self.llm_type == 'ollama':
      stream = self.llm_client.chat(model=self.model_name, messages=messages, stream=stream)
      for chunk in stream:
        yield {
          'content': chunk['message']['content'],
          'role': chunk['message']['role'],
          'done': chunk.get('done', False)
        }
