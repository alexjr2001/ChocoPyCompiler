import scanner as sc
import RDparser as parser

def main():
    Scanner = sc.Scanner()
    Scanner.open_file("testParser2.txt")    #Testing Keywords
    Scanner.getTokens()

    Parser = parser.Parser(Scanner)
    Parser.program()


if __name__ == "__main__":
    main()

        
