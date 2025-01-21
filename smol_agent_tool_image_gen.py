"""
This script demonstrates advanced usage of Smol Agent with custom tools for downloading models and generating images.
It integrates the Hugging Face API to fetch the most downloaded model for a specific task and uses a custom text-to-image
tool to create high-quality images based on user prompts.

Requirements:
- Install the `smolagents` library and required dependencies.
- Set up an environment variable `HF_API_TOKEN` with your Hugging Face API token.
"""

from smolagents import CodeAgent, HfApiModel
from smolagents import tool, Tool
from huggingface_hub import InferenceClient, list_models
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@tool
def model_download_tool(task: str) -> str:
    """
    Retrieves the most downloaded model for a specific task from the Hugging Face Hub.

    Args:
        task: The task (e.g., "text-to-image") for which to fetch the most downloaded model.

    Returns:
        The model ID of the most downloaded checkpoint.
    """
    # Get the most downloaded model for the specified task
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
    return most_downloaded_model.id

class TextToImageTool(Tool):
    """
    A custom tool for generating images based on text prompts using the Hugging Face Inference API.
    """
    description = (
        "Generates an image based on a provided text prompt. For best results, include detailed descriptions "
        "in the prompt, such as 'high-res' or 'photorealistic'."
    )
    name = "image_generator"
    inputs = {
        "prompt": {
            "type": "string",
            "description": "The text description for the image. Detailed prompts yield better results."
        },
        "model": {
            "type": "string",
            "description": "The Hugging Face model ID for image generation. Defaults to the current model if not specified."
        }
    }
    output_type = "image"
    current_model = "black-forest-labs/FLUX.1-schnell"  # Default model for image generation

    def forward(self, prompt, model=None):
        """
        Generates an image using the specified model and prompt.

        Args:
            prompt: The text description for the image.
            model: Optional. The Hugging Face model ID to use. Defaults to `current_model`.

        Returns:
            A success message indicating the prompt and model used for image generation.
        """
        # Update the model if a new one is provided
        if model and model != self.current_model:
            self.current_model = model
            self.client = InferenceClient(model)
        
        # Initialize the client if not already done
        if not hasattr(self, "client"):
            self.client = InferenceClient(self.current_model)
        
        # Generate the image and save it locally
        image = self.client.text_to_image(prompt)
        image_path = "image.png"
        image.save(image_path)
        return f"Image saved as {image_path}. Prompt: '{prompt}'. Model: '{self.current_model}'."

# Instantiate the custom text-to-image tool
image_generator = TextToImageTool()

# Initialize the Smol Agent with the custom tools
agent = CodeAgent(
    tools=[image_generator, model_download_tool],  # Add the tools
    model=HfApiModel()                            # Use Hugging Face API for language processing
)

# Run a query that uses both tools
response = agent.run(
    "Improve this prompt, then generate an image of it. "
    "Prompt: A cat wearing a hazmat suit in a contaminated area. "
    "Get the latest model for text-to-image from the Hugging Face Hub."
)

# Print the response from the agent
print(response)

# Tips:
# - Use `model_download_tool` to dynamically fetch the most popular models for any task.
# - Combine tools to chain actions, such as downloading a model and using it for a task.
# - Refine prompts iteratively for better results in text-to-image generation.
