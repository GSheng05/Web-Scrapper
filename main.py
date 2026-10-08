import sys

def main():
    # Check number of arguments (sys.argv[0] is the script name)
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        base_url = sys.argv[1]
        print(f"starting crawl of: {base_url}")


if __name__ == "__main__":
    main()
