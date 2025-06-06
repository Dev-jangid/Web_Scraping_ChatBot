### 🔑 API Keys

1. **Groq API Key**:

   * Sign up or log in at [https://console.groq.com](https://console.groq.com)
   * Generate an API key from the dashboard



2. ###  `Web_Scraping_ChatBot`

#### command to run .py file in terminal :

python < file name.py> <web url links>   
      examples : command run in terminal
          Comamnd :   `python Web_Scraping_Chatbot.py https://www.geeksforgeeks.org/`
 

###  `Web_Scraping_ChatBot`

#### command to run .py file in terminal :

python < file name.py> <web url links>   
      examples : command run in terminal
          Comamnd :   `python Web_Scraping_Chatbot.py https://www.geeksforgeeks.org/`
 

### `Work Flow`

1. User Input. <br><br>
      `↓`
2. URL passed via command line.<br><br>
      `↓`
3.  Web Scraping Module (fetch_website_content).<br><br>
      `↓`
4.  Text Processing (process_content).<br><br>
      `↓`
5.  Groq API Interface (generate_chat_response).<br><br>
      `↓`
6.  Response Generation.<br><br>
      `↓`
7.  CLI Chat Loop.<br><br>    
      - Continues accepting user input until 'exit' or 'quit'
