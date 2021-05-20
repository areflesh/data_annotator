import streamlit as st
import os
import json
from os.path import splitext
import SessionState
from plyer import notification
import pysftp
import paramiko
st.set_page_config(layout="wide")
state = SessionState.get(n = 0, file_list=os.listdir("./paintings/images/"))
@st.cache
def dir_creation(): 
    with pysftp.Connection('mt1.bsc.es', username='bsc21438', password='02t8q1uV') as sftp:
        if not sftp.exists("/gpfs/home/bsc21/bsc21438/paintings/"+name+"/"):
            sftp.makedirs("/gpfs/home/bsc21/bsc21438/paintings/"+name+"/")
    sftp.close()
name = st.sidebar.text_input("Input your name and press Enter please:","")
if (name!=''):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('mt1.bsc.es', username='bsc21438', password='02t8q1uV')
    file_sftp = ssh.open_sftp()

    work_dir = "./paintings/"+name+"/"
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)

    dir_creation()    
    
    try:
        image_name = state.file_list[state.n]
    except: 
        notification.notify(
                    title = "Annotation is finished",
                    message = "All images are annotated",  
                    timeout  = 15)
        state.n = 0
        image_name = state.file_list[state.n]
    
    if os.path.exists("./paintings/"+name+"/"+os.path.splitext(image_name)[0]+'.json'):
        with open("./paintings/"+name+"/"+os.path.splitext(image_name)[0]+'.json','r') as json_file:
            provided_meta_data = json.load(json_file)
        provided_des = provided_meta_data[name]
    else:
        provided_des="None"
    
    col1,col2 = st.beta_columns(2)
    col1.markdown('# Image')
    col1.markdown("** File name: **" + image_name)
    col1.image("./paintings/images/"+image_name)
    
    with open("./paintings/descriptions/"+os.path.splitext(image_name)[0]+'.json','r') as json_file:
        meta_data = json.load(json_file)
    
    col2.markdown('# Annotation')
    col2.markdown("** Original caption: **"+meta_data["annot"])
    col2.markdown("** Provided caption: **"+provided_des)
    
    annotation = col2.text_input("Input annotation:")
    if annotation:
        col2.markdown(" ** BLEU Score: **"+str(len(annotation)))
    
    if col2.button("Save data"):   
        print(image_name)
        print(annotation)
        
        annot = {"File":image_name}
        annot[name]=annotation

        with open(work_dir+os.path.splitext(image_name)[0]+'.json', 'w') as json_file:
            json.dump(annot, json_file)
        with file_sftp.open("/gpfs/home/bsc21/bsc21438/paintings/"+name+"/"+os.path.splitext(image_name)[0]+'.json', 'w') as outfile:
            json.dump(annot, outfile)
    if col2.button("Next image",key = state.n):
        state.n=state.n+1
    if col2.button("Previous image",key = state.n):
        state.n=state.n-1
    ssh.close()

