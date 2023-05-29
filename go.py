import subprocess

def main():
    print("Hello, welcome to the interactive command line tool.\n")
    
    # Ask the user questions
    is_post = input("Would you like to make a new post (yes/no)? ")
    post_name = input("What's the post called? ")

    if is_post.lower() != 'yes':
        print("Goodbye!")
        return
    
    post_filename = "post/" + post_name.lower().replace(" ", "-") + ".md"
    subprocess.run(["hugo", "new", post_filename]) 
   
if __name__ == "__main__":
    main()
