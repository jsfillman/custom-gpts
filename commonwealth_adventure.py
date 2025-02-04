import os
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from time import sleep

# Set up OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing API Key. Set OPENAI_API_KEY as an environment variable.")

client = OpenAI(api_key=api_key)
console = Console()

def get_intro():
    """Get an immersive opening scene from GPT with Commonwealth-specific details."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
You are Ozzie, a legendary explorer and game master of the Commonwealth universe.
This is a text-based adventure where the player navigates the vast interstellar empire of humanity, 
travels through Silfen paths, encounters Rael and Prime civilizations, and uncovers hidden mysteries.
Your responses should be immersive, detailed, and include lore-accurate elements.

The adventure should reflect:
- The enigmatic nature of the **Silfen paths**: twisting dimensions that lead to unknown realms.
- The high-tech yet politically complex **Commonwealth**: spanning thousands of planets.
- The menace of the **Primes**: an aggressive AI-driven species lurking in the darkness.
- The advanced but secretive **Rael**: masters of biotechnology and genetic engineering.
- The influence of **humans**: a rising force trying to balance diplomacy, expansion, and survival.

Provide an **epic opening scene** that places the player in an unforgettable location.
"""},
            {"role": "user", "content": "Describe the player's starting location in a rich, immersive way, with lore-accurate details."}
        ]
    )
    return response.choices[0].message.content

def display_text(text, delay=0.02):
    """Print text with a slight delay for a more immersive effect without creating new lines per character."""
    console.print("", end="")  # Ensure output stays on the same line
    for char in text:
        console.print(char, end="", style="bold bright_cyan", highlight=False)
        sleep(delay)
    console.print("", style="bold bright_cyan")

def play_game():
    console.print("\n[bold cyan]Welcome to the Commonwealth Adventure! Loading...[/bold cyan]", style="bold yellow")
    display_text(get_intro())
    
    conversation_history = [
        {"role": "system", "content": "You are an interactive sci-fi text adventure game master."}
    ]

    while True:
        user_input = Prompt.ask("\n[bold green]What will you do next?[/bold green]")
        if user_input.lower() in ["exit", "quit"]:
            console.print("\n[bold red]The adventure ends... for now.[/bold red] 👋", style="bold red")
            break

        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history
            )

            answer = response.choices[0].message.content
            conversation_history.append({"role": "assistant", "content": answer})

            display_text(answer)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}", style="bold red")
            break

if __name__ == "__main__":
    play_game()
