import scanner as sc
import RDparser as parser

def main():
    Scanner = sc.Scanner()
    Scanner.open_file("program1.txt")    #Testing Keywords
    Scanner.getTokens()

    Parser = parser.Parser(Scanner)


if __name__ == "__main__":
    main()

        
