import os
import argparse
import openai

def review_file(file_path: str, model: str, temperature: float):
    """
    Send the contents of file_path to OpenAI for a code review and print the response.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    messages = [
        {"role": "system", "content": "You are an expert AI code reviewer. Provide concise, actionable feedback focusing on correctness, style, best practices, and potential improvements."},
        {"role": "user", "content": f"Please review the following file: {file_path}\n```\n{content}\n```"}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    review = response.choices[0].message.content.strip()
    separator = "\n" + "-" * 80 + "\n"
    print(separator)
    print(f"Review for {file_path}:")
    print(review)
    print(separator)


def traverse_and_review(root_dir: str, model: str, temperature: float, extensions: list):
    """
    Walk through root_dir, review each file with matching extensions, and pause after each.
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in sorted(filenames):
            if any(filename.endswith(ext) for ext in extensions):
                path = os.path.join(dirpath, filename)
                review_file(path, model, temperature)
                # Pause and ask user
                choice = input("Continue to next file? (y/n): ").strip().lower()
                if choice != "y":
                    print("Stopping review.")
                    return


def main():
    parser = argparse.ArgumentParser(
        description="Iterative AI-driven code review agent."
    )
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=".",
        help="Project root directory to review."
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use for reviews."
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature for the model. Lower = more deterministic."
    )
    parser.add_argument(
        "--ext",
        nargs="+",
        default=[".py", ".js", ".ts", ".java", ".go", ".yaml", ".yml"],
        help="File extensions to include in the review."
    )
    args = parser.parse_args()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    traverse_and_review(args.root_dir, args.model, args.temperature, args.ext)


if __name__ == "__main__":
    main()
