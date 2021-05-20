import streamlit as st
import os
import json
from os.path import splitext
import SessionState
from plyer import notification
import pysftp
import paramiko
from paramiko import RSAKey
from base64 import decodebytes
st.set_page_config(layout="wide")
state = SessionState.get(n = 0, file_list=os.listdir("./paintings/images/"))
@st.cache
def create_folder(user_name):
    keydata = b"""AAAAB3NzaC1yc2EAAAABIwAAAQEAvZYcvomQbQ72DDZtV3EHXCLHzlj4oSHwtp+9qhm3H3xSWxm0mVX3xgpLkljCtWycZYtKr8G8NqK97FL42r40W++LqjRkRpOzJ8SzkV+gh365FvouGhRSChMsnuCwyiAQnhCT1wfdadxh7/6+fm3RNFjoR3MMXsjabAztD+ZXcVJzTZ1Q4yRPV79Q2wa4zp3syrda1g1+3cLMlPwVGTTaPrhZwNnDYOM+C8PDr4cr88bHNkcAp2keINV9yZUNJzJNSrWg8g9sU9/e+ffd61n9jQDZlD2hasffkCeos92HNwkVgXws5xPo+kbuisFEIcybKu5Yrbb+U8RK9JCbd/2//w=="""
    key = paramiko.RSAKey(data=decodebytes(keydata))
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.add('mt1.bsc.es', 'ssh-rsa', key) 
    with pysftp.Connection('mt1.bsc.es', username='bsc21438', password='02t8q1uV', cnopts=cnopts) as sftp:
        if not sftp.exists("/gpfs/home/bsc21/bsc21438/paintings/"+user_name+"/"):
            sftp.makedirs("/gpfs/home/bsc21/bsc21438/paintings/"+user_name+"/")
    sftp.close()

@st.cache
def upload_file(original_file, dest_file):
    keydata = b"""AAAAB3NzaC1yc2EAAAABIwAAAQEAvZYcvomQbQ72DDZtV3EHXCLHzlj4oSHwtp+9qhm3H3xSWxm0mVX3xgpLkljCtWycZYtKr8G8NqK97FL42r40W++LqjRkRpOzJ8SzkV+gh365FvouGhRSChMsnuCwyiAQnhCT1wfdadxh7/6+fm3RNFjoR3MMXsjabAztD+ZXcVJzTZ1Q4yRPV79Q2wa4zp3syrda1g1+3cLMlPwVGTTaPrhZwNnDYOM+C8PDr4cr88bHNkcAp2keINV9yZUNJzJNSrWg8g9sU9/e+ffd61n9jQDZlD2hasffkCeos92HNwkVgXws5xPo+kbuisFEIcybKu5Yrbb+U8RK9JCbd/2//w=="""
    key = paramiko.RSAKey(data=decodebytes(keydata))
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.add('mt1.bsc.es', 'ssh-rsa', key) 
    with pysftp.Connection('mt1.bsc.es', username='bsc21438', password='02t8q1uV', cnopts=cnopts) as sftp:
        sftp.put(original_file, dest_file)
    sftp.close()

name = st.sidebar.text_input("Input your name and press Enter please:","")
if (name!=''):
    work_dir = "./paintings/"+name+"/"
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)

    create_folder(name)   
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
        upload_file(work_dir+os.path.splitext(image_name)[0]+'.json',"/gpfs/home/bsc21/bsc21438/paintings/"+name+"/"+os.path.splitext(image_name)[0]+'.json')
        
    if col2.button("Next image",key = state.n):
        state.n=state.n+1
    if col2.button("Previous image",key = state.n):
        state.n=state.n-1


