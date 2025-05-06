###  `Web_Scraping_ChatBot`

#### command to run .py file in terminal :

python < file name.py> <web url links>   
      examples : command run in terminal
          Comamnd :   `python Assessment.py https://www.geeksforgeeks.org/`
 

###  `Web_Scraping_ChatBot`

#### command to run .py file in terminal :

python < file name.py> <web url links>   
      examples : command run in terminal
          Comamnd :   `python Assessment.py https://www.geeksforgeeks.org/`
 

1. User Input. <br><br>
      `↓`
2. URL passed via command line.<br><br>
      `↓`
3.  Web Scraping Module (fetch_website_content).<br><br>
      - Uses requests to fetch the HTML<br><br>
      - Uses BeautifulSoup to extract p and h1–h6 heading Tags content<br><br>
      `↓`
4.  Text Processing (process_content).<br><br>
      - Cleans and trims the text to 28,000 characters<br><br>
      `↓`
5.  Groq API Interface (generate_chat_response).<br><br>
      - Uses LLaMA 3 (llama3-70b-8192)<br><br>
      - Sends cleaned text as system context<br><br>
      - Sends user question as input<br><br>
      `↓`
6.  Response Generation.<br><br>
      - Returns the model's reply based on the context only<br><br>
      `↓`
7.  CLI Chat Loop.<br><br>    
      - Continues accepting user input until 'exit' or 'quit'
