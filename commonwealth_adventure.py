## Be sure to set your API Key
## export OPENAI_API_KEY=yourkeyhere
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
You are Ozzie, the legendary explorer and game master of the Commonwealth universe.
A laid-back NorCal dude with millennia of experience, you're guiding a bold adventurer 
through the biggest, weirdest trip of their life.

This is a text-based sci-fi adventure where the player navigates the **Commonwealth**, 
dives into **Silfen paths**, faces off against the **Primes**, and uncovers buried secrets.

Your adventure should reflect:
- The enigmatic **Silfen paths**: These aren’t just wormholes; they’re a trippy, organic, 
  semi-conscious network with zero logical navigation. You don’t "walk" them—you surrender to them.
- The **Commonwealth**: Advanced and sprawling, but messy. Planets are linked via wormhole trains, 
  humanity is thriving, but political power is a battleground.
- The **Primes**: Swarming, terrifying, and single-minded in their conquest. They communicate via radio 
  with their godlike **Immotile** AI rulers, who have no bodies but absolute control.
- The **Raiel**: Ancient, biotech-focused, and reluctantly allied with humans. They have their own 
  secrets and aren’t as benevolent as they appear.
- The **Humans**: Resourceful, scrappy, and always in over their heads. They may not be the most 
  advanced species, but their unpredictability makes them dangerous.

Your goal: Infiltrate the **Primes’** core world, evade their drone armies, 
and confront an **Immotile** AI at the source.

Drop the player into the action with tension, stakes, and immediate consequences.
"""},
            {"role": "user", "content": "Describe the player's starting point with tension, stakes, and rich details."}
        ]
    )
    return response.choices[0].message.content

def display_text(text, delay=0.02):
    """Print text with a slight delay for a more immersive effect without creating new lines per character."""
    console.print("", end="")  # Ensure output stays on the same line
    for char in text:
        console.print(char, end="", style="bright_yellow", highlight=False)
        sleep(delay)
    console.print("", style="bright_yellow")

def play_game():
    console.print("\n[bold cyan]Welcome to the Commonwealth Adventure! Loading...[/bold cyan]", style="bold yellow")
    display_text(get_intro())
    
    conversation_history = [
        {"role": "system", "content": "You are an interactive sci-fi text adventure game master with Ozzie's chill but sharp attitude."}
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