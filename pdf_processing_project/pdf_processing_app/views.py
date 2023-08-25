from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadPDFForm

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

import tempfile

# Create your views here.

def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
                for chunk in pdf_file.chunks():
                    temp_pdf_file.write(chunk)

            loader = PyPDFLoader(temp_pdf_file.name)

            docs = loader.load()

            temp_pdf_file.close()

            llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
            chain = load_summarize_chain(llm, chain_type="stuff")

            chain.run(docs)

            # Define prompt
            prompt_template = """Write a detailed summary of the following:
            "{text}"
            CONCISE SUMMARY:"""
            prompt = PromptTemplate.from_template(prompt_template)

            # Define LLM chain
            llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo-16k")
            llm_chain = LLMChain(llm=llm, prompt=prompt)

            # Define StuffDocumentsChain
            stuff_chain = StuffDocumentsChain(
                llm_chain=llm_chain, document_variable_name="text"
            )

            docs = loader.load()
            processed_result = stuff_chain.run(docs)
            return render(request, 'result.html', {'result': processed_result})
    else:
        form = UploadPDFForm()
    return render(request, 'upload.html', {'form': form})
