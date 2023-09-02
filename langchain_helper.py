from dotenv import load_dotenv,find_dotenv
from langchain.document_loaders.base import Document
from langchain.utilities import ApifyWrapper
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


load_dotenv(find_dotenv())


apify = ApifyWrapper()
chat = ChatOpenAI(model_name="gpt-4",temperature=0.3)
chain = load_qa_chain(chat, chain_type="stuff")

def mail_personalizado(empresa, prospecto, url):
    crawl_input={"crawlerType": "playwright:firefox",
                 "excludeUrlGlobs": [],
                 "maxCrawlDepth": 20,
                 "maxCrawlPages": 1,
                 "initialConcurrency": 0,
                 "maxConcurrency": 200,
                 "initialCookies": [],
                 "dynamicContentWaitSecs": 10,
                 "maxScrollHeightPixels": 5000,
                 "htmlTransformer": "readableText",
                 "readableTextCharThreshold": 100,
                 "maxResults": 9999999,
                 "startUrls": [{"url": url}]
                 }
    
    loader = apify.call_actor(
        actor_id="apify/website-content-crawler",
        run_input=crawl_input,
        dataset_mapping_function=lambda item: Document(
            page_content=item["text"] or "", metadata={"source": item["url"]}
            ),)
    docs=loader.load()

    q='Formula un correo corto de 5-8 lineas para ' + prospecto + \
        ' ofreciendole el servicio de generación de leads para ' + empresa + \
            '. El correo debe mencionar las soluciones de ' + empresa + \
                ' y como se pueden beneficiar a traves de la generación de leads, además de hacerle a '+ prospecto + ' un cumplido.'
    email=chain.run(input_documents=docs, question=q)

    response = {'correo':email}
    return response
