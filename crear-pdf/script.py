#Dentro de la carpeta con el archivo .py
#   streamlit run script.py

import streamlit as st
from fpdf import FPDF

class PDF(FPDF):
  def header(self):
    if hasattr(self,'document_title'):
      self.set_font('Arial','B',12)
      self.cell(0,10,self.document_title,0,1,'C')
      
  def footer(self):
    self.set_y(-15)
    self.set_font('Arial','I',8)
    self.cell(0,10,f'Page {self.page_no()}',0,0,'C')
    
  def chapter_title(self,title,font='Arial',size=12):
    self.set_font(font,'B',size)
    self.cell(0,10,title,0,1,'L')
    self.ln(10)
    
  def chapter_body(self,body,font='Arial',size=12):
    self.set_font(font,'',size)
    self.multi_cell(0,10,body)
    self.ln()
    
def create_pdf(filename,document_title,author,chapters,image_path=None):
  pdf=PDF()
  pdf.document_title=document_title
  pdf.add_page()
  if author:
    pdf.set_author(author)
    
  if image_path:
    pdf.image(image_path,x=10,y=25,w=pdf.w-20)
    pdf.ln(120)
    
  for chapter in chapters:
    title,body,font,size=chapter
    pdf.chapter_title(title,font,size)
    pdf.chapter_body(body,font,size)
    
  pdf.output(filename)
  
def main():
  st.title('Python PDF Generator')
  st.header('Document Configuration')
  document_title=st.text_input('Document Title','Document Title')
  author=st.text_input('Author','')
  upload_image=st.file_uploader('Upload an image for document (optional)',type=['jpg','png'])
  
  st.header('Document Chapters')
  chapters=[]
  chapter_count=st.number_input('Chapters Number',min_value=1,max_value=10,value=1)
  
  for i in range(chapter_count):
    st.subheader(f'Chapter {i+1}')
    title=st.text_input(f'Title of Chapter {i+1}',f'Title of Chapter {i+1}')
    body=st.text_area(f'Body of Chapter {i+1}',f'Content of Chapter {i+1}')
    font=st.selectbox(f'Font of Chapter {i+1}',['Arial','Courier','Times'])
    size=st.slider(f'Font Size of Chapter {i+1}',8,24,12)
    chapters.append((title,body,font,size))
    
  if st.button('Generate PDF'):
    image_path=upload_image.name if upload_image else None
    if image_path:
      with open(image_path,'wb') as f:
        f.write(upload_image.getbuffer())
        
    create_pdf('filegenerated.pdf',document_title,author,chapters,image_path)
    
    with open('filegenerated.pdf','rb') as pdf_file:
      PDFbyte=pdf_file.read()
      
    st.download_button(
      label='Download PDF',
      data=PDFbyte,
      file_name='output_fpdf.pdf',
      mime='application/octet-stream'
    )
    
    st.success('PDF successfully generated')
    
  
if __name__=='__main__':
  main()