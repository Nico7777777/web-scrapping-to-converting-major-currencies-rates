from os import link
import requests

coins_list = [ "", "CHF", "CAD", "EUR", "GBP",  "JPY", "NZD", "USD"]
link_root = "https://www.xe.com/currencyconverter/convert/?Amount=1&From="
n = len(coins_list)
cnt = 1
#special cases due to the length of the number or :
'''
    1. XBT # these three
    2. XAU # are going to
    3. XAG # be added
'''
extension_list = ["XBT", "XAU", "XAG"]
# the plan behind the programme
'''
    the currencies Ima use in this banking system
    1.The 7 Major Currencies:
        CHF - Swiss Franc
        CND - Canadian Dollar
        EUR - Euro
        GBP - Great Britan Pound
        JPY - Japanese Yen
        NZD - New Zeeland Dollar
        USD - United States Dollar
    ---------------------------------

    TOTAL COINS USED: 7

    the number of pairs: C(7, 2) = 21 pairs
'''

def seed_file():
    with open("pair_currencies.txt", "w") as f:
        f.write("") # to empty the file if it exists and maybe already has data
    with open("pair_currencies.txt", "a") as f:
        for i in range(1, n):
            for j in range(i+1, n):
                f.write( link_root + coins_list[i] + "&To=" + coins_list[j] + "\n")

def turn_the_file_to_list()->list:
        fin = open("pair_currencies.txt", "r")
        a = fin.readlines() # list of web links to be scrapped on unprocessed(with \n at the back)
        fin.close()
        links = []
        links.append('\0')
        for i in a:
            links.append( i[: len(i) - 1]  ) # this will be a list of links starting with the count at 1 and w.o. /n at the back, which makes it easier
        return links

if __name__ == "__main__":
    seed_file()
    links = turn_the_file_to_list()

    with open("currencies.txt", "w") as currencies:
        for i in range( 1, n ): #loop throuh the coins
            for j in range(i+1, n ): # from the list 'coins_list'
                    page_url = links[ cnt ]
                    cnt += 1

                    r = requests.get(page_url)
                    links_html = r.content
                    links_html = str(links_html)
                    bullshit_skipping = len("result__BigRate-sc-1bsijpp-1 iGrAod") + 2 # the two characters are '">' at the end of html tag
                    first = links_html.find("result__BigRate-sc-1bsijpp-1 iGrAod")
                    #--------------------------------------------------------------------
                    start_position = first + bullshit_skipping
                    finish_position = start_position
                    while links_html[finish_position].isdigit() or links_html[finish_position]=='.':
                        finish_position += 1
                    first_part_of_currency = links_html[start_position: finish_position]


                    bullshit_skipping = len("faded-digits") + 2
                    start_position = links_html.find("faded-digits", finish_position-1) + bullshit_skipping
                    finish_position = start_position
                    while links_html[finish_position].isdigit() or links_html[finish_position]=='.':
                        finish_position += 1
                    second_part_of_currency = links_html[start_position: finish_position]
                    result = first_part_of_currency + second_part_of_currency

                    currencies.write("by selling 1"+coins_list[i]+" you can buy "+result+coins_list[j]+"\n")
