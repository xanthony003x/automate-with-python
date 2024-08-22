import pytube
import streamlit as st

class YoutubeDownloader:
  def __init__(self,url):
    self.url=url
    self.youtube=pytube.YouTube(self.url,on_progress_callback=YoutubeDownloader.onProgress)
    self.stream=None
    
  def showTitle(self):
    st.write(f'**Title:** {self.youtube.title}')
    self.showStreams()
    
  def showStreams(self):
    streams=self.youtube.streams
    stream_option=[
      f'Resolution: {stream.resolution or 'N/A'} / FPS: {getattr(stream,'fps','N/A')} / Type: {stream.mime_type}'
      for stream in streams
    ]
    choice=st.selectbox('Choose a stream option:',stream_option)
    self.stream=streams[stream_option.index(choice)]
    
  def getFileSize(self):
    file_size=self.stream.filesize/1000000
    return file_size
  
  def getPermissionToContinue(self,file_size):
    st.write(f'**Title:** {self.youtube.title}')
    st.write(f'**Author:** {self.youtube.author}')
    st.write(f'**Size:** {file_size:.2f} MB')
    st.write(f'**Resolution:** {self.stream.resolution or 'N/A'}')
    st.write(f'**FPS:** {getattr(self.stream,'fps','N/A')}')
    
    if st.button('Download'):
      self.download
      
  def download(self):
    self.stream.download()
    st.success('Completed download')
    
  @staticmethod
  def onProgress(stream=None,chunk=None,remaining=None):
    file_size=stream.filesize/1000000
    file_downloaded=file_size-remaining/1000000
    st.progress(file_downloaded/file_size)
    
if __name__=='__main__':
  st.title=('Youtube Video Downloader')
  url=st.text_input('Enter a video URL:')
  
  if url:
    downloader=YoutubeDownloader(url)
    downloader.showTitle()
    if downloader.stream:
      file_size=downloader.getFileSize()
      downloader.getPermissionToContinue(file_size)