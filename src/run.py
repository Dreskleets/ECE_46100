#Run file for milestone 1

import sys, os

def install():
    
    print("Install")
    
def run_tests():
    
    print("Testing")
    
def process_url_file():
    
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