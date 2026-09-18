import sys

def run(source):
    print(source)
    print("Scanner Not Implemented")

def run_file(filename):
    with open(filename, "r") as file:
        source = file.read()
    run(source)

def run_prompt():
    print(">>>>> JoshLang REPL <<<<<")
    while True:
        try:
            source = input(">>> ")
            run(source)
        except KeyboardInterrupt:
            print()
            break

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        run_prompt()
    elif len(args) == 1:
        run_file(args[0])
    else:
        print("Usage: python src/JoshLang.py [script]")

if __name__ == "__main__":
    main()