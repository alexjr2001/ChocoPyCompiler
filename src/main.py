import scanner as sc
def main():
    Scanner = sc.Scanner()
    Scanner.open_file("testKeywords.txt")    #Testing Keywords

    print(Scanner.total_lines)
    Scanner.getTokens()

if __name__ == "__main__":
    main()

        
