from os import link
import requests

coins_list = [ "", "CHF", "CAD", "EUR", "GBP",  "JP", "NZD", "USD"]
#special cases due to the length of the number or :
'''
    1. XBT
    2. XAU
    3. XAG
'''


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

    the number of pairs: C(7, 2) = 42 pairs
'''


if __name__ == "__main__":

    fin = open("pair_currencies.txt", "r")
    a = fin.readlines()
    fin.close()
    links = []
    links.append('\0')
    for i in a:
        links.append( i[: len(i) - 1]  )
    
    with open("currencies.txt", "w") as currencies:
        for i in range( 1, len(coins_list) ):
            for j in range(1, len(coins_list) ):
                if i!=j:
                    cnt = 13*(i-1) + j
                    if i < j:
                        cnt -= 1
                    page_url = links[ cnt ]

                    r = requests.get(page_url)
                    links_html = r.content
                    links_html = str(links_html)
                    bullshit_skipping = len("result__BigRate-sc-1bsijpp-1 iGrAod") + 2
                    first = links_html.find("result__BigRate-sc-1bsijpp-1 iGrAod")
                    #--------------------------------------------------------------------
                    start_position = first + bullshit_skipping
                    finish_position = links_html.find("<", start_position)
                    first_part_of_currency = links_html[start_position: finish_position]


                    bullshit_skipping = len("faded-digits") + 2
                    start_position = links_html.find("faded-digits", finish_position-1) + bullshit_skipping
                    finish_position = start_position + 4
                    second_part_of_currency = links_html[start_position: finish_position]
                    result = first_part_of_currency + second_part_of_currency

                    #currencies.write(coins_list[i]+" -> "+coins_list[j]+" = "+result+"\n")
                    currencies.write(result + "\n")