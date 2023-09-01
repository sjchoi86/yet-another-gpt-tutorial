### Yet Another GPT Tutorial

This repo contains simple usages for utilizing GPT API provided by OpenAI. 
- [GPT API usage](https://github.com/sjchoi86/yet-another-gpt-tutorial/blob/main/code/demo_gpt_01_chat.ipynb)
: Basic OpenAI API usage for using [GPT](https://openai.com/gpt-4)
- [Wiki Summarize](https://github.com/sjchoi86/yet-another-gpt-tutorial/blob/main/code/demo_webcrawl_01_wiki.ipynb)
: [Wikipedia](https://www.wikipedia.org/) Web crawling using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) + Summarization using GPT
- [Retrieval-Augmented Generation](https://github.com/sjchoi86/yet-another-gpt-tutorial/blob/main/code/demo_gpt_02_rag.ipynb)
: A minimal implementation of RAG using Wikipedia. Given the user's question, GPT first suggests entities for searching Wikipedia. Then, GPT summarizes the queried pages and the summarized sentences and the given question are combined and given to GPT to answer.
- [Qaulity-Diversity Wiki Sampling](https://github.com/sjchoi86/yet-another-gpt-tutorial/blob/main/code/demo_webcrawl_03_qd.ipynb): A quality-diversity based sampling using determinantal point processes where the kernel matrix is constructed from BERT distance measure. The initial sample is deterministically selected using the same BERT distance.
- [GPT Fine-Tuning](https://github.com/sjchoi86/yet-another-gpt-tutorial/blob/main/code/demo_gpt_03_finetune.ipynb): Fine-tune GPT model using OpenAI API. 

### Contact
sungjoon dash choi at korea dot ac dot kr
