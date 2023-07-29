import subprocess

import re


def main():
    print("Hello, welcome to the interactive command line tool.\n")

    # Ask the user questions
    is_post = input("Would you like to make a new post (yes/no)? ")
    post_name = input("What's the post called? ")

    if is_post.lower() != "yes":
        print("Goodbye!")
        return

    # Clean the title to be a good filename
    post_local_filename = re.sub(r"[^a-zA-Z0-9 ]+", "", post_name)
    post_local_filename = post_local_filename.lower().replace(" ", "-")
    post_filename = "posts/" + post_local_filename + ".md"

    subprocess.run(["hugo", "new", post_filename])


if __name__ == "__main__":
    main()
