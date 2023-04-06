import scanner as sc
def main():
    Scanner = sc.Scanner()
    Scanner.open_file("program2.txt")    #Testing Keywords

    print(Scanner.total_lines)
    Scanner.getTokens()

if __name__ == "__main__":
    main()

        
