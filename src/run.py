#!/usr/bin/env python3
#!/usr/bin/env bash
#Run file for milestone 1

import sys, os

def install():
    # Install dependencies from requirements.txt
    os.system(f"{sys.executable} -m pip install --break-system-packages -r {os.path.join(os.path.dirname(__file__), 'requirements.txt')}")
    print("Installed all requirements!")
    
def run_tests():
    # Run test suite
    print("Testing")
    
def process_url_file():
    # Process URL file
    # Absolute location of ASCII encoded newline-delimited set of URLs
    # Model, Dataset, and Code URLs needed
    print("Url")

def main():
    if len(sys.argv) != 2:
        print("Usage: ./run <install|<URL_FILE>|test>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    try:
        if cmd == "install":
            sys.exit(install())

        elif cmd == "test":
            sys.exit(run_tests())

        else:
            # Anything else is treated as a path to the URL file
            sys.exit(process_url_file(cmd))

    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
