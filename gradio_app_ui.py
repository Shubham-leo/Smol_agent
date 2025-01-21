from smolagents import CodeAgent, HfApiModel
from smolagents import tool, Tool
from huggingface_hub import InferenceClient
from huggingface_hub import list_models
import gradio as gr
from dotenv import load_dotenv
import PIL.Image

# Load environment variables from the .env file
load_dotenv()

@tool
def model_download_tool(task: str) -> str:
    """
    This tool retrieves the most downloaded model for a given task from the Hugging Face Hub.

    Args:
        task (str): The task for which to fetch the most downloaded model (e.g., 'text-to-image').

    Returns:
        str: The ID of the most downloaded model for the specified task.
        
    Example:
        model_download_tool("text-to-image") 
        # Returns the model ID of the most downloaded text-to-image model.
    """
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
    return most_downloaded_model.id

class TextToImageTool(Tool):
    """
    A custom tool that generates images based on text descriptions using the Hugging Face Inference API.
    """
    description = "This tool creates an image according to a prompt, which is a text description."
    name = "image_generator"
    inputs = {
        "prompt": {
            "type": "string", 
            "description": "The image generator prompt. Add details to improve the image quality (e.g., 'high-res', 'photorealistic')."
        },
        "model": {
            "type": "string",
            "description": "The Hugging Face model ID to use for image generation. Defaults to the current model if not specified."
        }
    }
    output_type = "image"
    current_model = "black-forest-labs/FLUX.1-schnell"  # Default model for image generation

    def forward(self, prompt, model):
        """
        Generates an image based on the provided prompt using the selected model.

        Args:
            prompt (str): The text description of the image.
            model (str, optional): The model ID to use for generation. Defaults to `current_model` if not provided.

        Returns:
            str: A message indicating the success of the image generation, including the prompt and model used.
        
        Example:
            forward("A futuristic city at night")
            # Generates the image and returns a success message indicating the prompt and model used.
        """
        if model:
            if model != self.current_model:
                self.current_model = model
                self.client = InferenceClient(model)
        if not hasattr(self, "client"):
            self.client = InferenceClient(self.current_model)
            
        image = self.client.text_to_image(prompt)
        image.save("image.png")
            
        return f"Successfully saved image with this prompt: {prompt} using model: {self.current_model}"

def generate_image(prompt):
    """
    Function to handle Gradio interface interaction, improve the prompt, and generate an image.

    Args:
        prompt (str): The initial text prompt provided by the user.

    Returns:
        tuple: The generated image and the agent's response.
        
    Example:
        generate_image("A peaceful garden with butterflies")
        # Generates the image and returns the generated image along with the agent's response.
    """
    image_generator = TextToImageTool()
    agent = CodeAgent(tools=[image_generator, model_download_tool], model=HfApiModel())
    
    # Run the agent with the provided prompt
    result = agent.run(
        f"Improve this prompt, then generate an image of it. Prompt: {prompt}. Get the latest model for text-to-image from the Hugging Face Hub."
    )
    
    # Load and return the generated image along with the result text
    generated_image = PIL.Image.open("image.png")
    return generated_image, result

# Create Gradio interface
demo = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(
            label="Enter your image prompt",
            placeholder="Example: A cat wearing a hazmat suit in contaminated area"
        )
    ],
    outputs=[
        gr.Image(label="Generated Image"),
        gr.Textbox(label="Agent Response")
    ],
    title="AI Image Generator",
    description="Enter a prompt and the AI will improve it and generate an image using the latest text-to-image model.",
    examples=[
        ["A cat wearing a hazmat suit in contaminated area"],
        ["A peaceful garden with butterflies"],
        ["A futuristic city at night"]
    ]
)

# Launch the interface
if __name__ == "__main__":
    demo.launch()

# Tips:
# - Provide detailed prompts to achieve better image generation results, such as including terms like 'high-res' or 'photorealistic'.
# - The agent will automatically improve the prompt before generating an image, enhancing the results.
# - You can try various text descriptions, from simple to complex, for a wide range of image generation outputs.
# - Experiment with different models for potentially better or specialized outputs.
