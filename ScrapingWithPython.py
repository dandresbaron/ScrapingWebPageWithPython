#Import the libraries
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from deep_translator import GoogleTranslator

#Creation of a function to scrape a web page and translate the HTML content from english to hindi
def functionScraping (url, file_name, input_language, output_language):

    # Initialize a session
    session = requests.Session()
    # Set the User-agent as a regular browser
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

    #Get the HTML content
    html = session.get(url).content

    # Parse HTML using beautiful soup
    soup = bs(html, "html.parser")

    #Convert file  HTML to String
    soup_string = str(soup)

    #Obtener el texto del HTML
    text_html = soup.get_text()

    #list comprenhension
    #Separate by line breaks and remove blanks
    nw_text_html = [x.replace(' ', '#') for x in text_html.split('\n') if x != '' ]
    
    #Translate to the languages you enter as input parameters
    translator = GoogleTranslator(source= input_language, target=output_language)
    lines_translated = []
    for item in tqdm(nw_text_html):
        if not item.isnumeric():
            lines_translated.append((item, translator.translate(item)))

    #Replace with the corresponden translation
    for item in lines_translated:
        if item[1] != None and item[0].lower() not in ['html', 'or']:
            soup_string =soup_string.replace(item[0].replace('#', ' '), item[1].replace('#', ' '))

    #Save the file
    with open(file_name +'.html', 'w') as file:
        file.write(soup_string)

    return soup, soup_string 



main_html, main_html_text  = functionScraping("https://www.classcentral.com/", "index", "en", "hi") 


#Get the url's in a list 
urls = [link.get('href') for link in main_html.findAll('a')]



sentence = "https://www.classcentral.com"
list_tuple=[]
for url in tqdm(urls):
    file_name = 'files/' + url.replace('/', '_')
    url_scraping = sentence + url if sentence not in url else url 
    if url_scraping != sentence + '/' and not os.path.exists(file_name):
        functionScraping(url_scraping, file_name, "en", "hi")
        list_tuple.append([('href="{}"'.format(url_scraping), 'href="file://{}"'.format(file_name))])

for item in  list_tuple:
    main_html_text  = main_html_text.replace(item[0], item[1])
            