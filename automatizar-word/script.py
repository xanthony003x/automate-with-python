import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate

doc=DocxTemplate('../../../../../home/josecs/Desktop/automate-with-python/automatizar-word/src/plantilla.docx')

nombre='Jose Cabrales'
telefono='(123) 456-789'
correo='jose@gmail.com'
fecha=datetime.today().strftime('%d/%m/%Y')

constantes={'nombre':nombre,'telefono':telefono,'correo':correo,'fecha':fecha}

df=pd.read_excel('../../../../../home/josecs/Desktop/automate-with-python/automatizar-word/src/notas.xls')

for indice,fila in df.iterrows():
  contenido={
    'nombre_alumno':fila['Nombre_del_Alumno'],
    'nota_mat':fila['Mat'],
    'nota_fis':fila['Fis'],
    'nota_qui':fila['Qui']
  }
  contenido.update(constantes)
  
  doc.render(contenido)
  doc.save(f"Notas_de_{fila['Nombre_del_Alumno']}.docx")

doc.render(constantes)
doc.save(f'prueba.docx')