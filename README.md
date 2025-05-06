###  `Web_Scraping_ChatBot`

#### command to run .py file in terminal :

python < file name.py> <web url links>   
      examples : command run in terminal
          Comamnd :   `python Assessment.py https://www.geeksforgeeks.org/`
 

User Input 
      ↓
[1] URL passed via command line
      ↓
[2] Web Scraping Module (fetch_website_content)
      - Uses requests to fetch the HTML
      - Uses BeautifulSoup to extract <p> and <h1>–<h6> content
      ↓
[3] Text Processing (process_content)
      - Cleans and trims the text to 28,000 characters
      ↓
[4] Groq API Interface (generate_chat_response)
      - Uses LLaMA 3 (llama3-70b-8192)
      - Sends cleaned text as system context
      - Sends user question as input
      ↓
[5] Response Generation
      - Returns the model's reply based on the context only
      ↓
[6] CLI Chat Loop
      - Continues accepting user input until 'exit' or 'quit'
