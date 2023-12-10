# 安装分割文件的包、OS包，random包
from filesplit.split import Split
import os, random, pandas
from google.cloud import storage

def file_split(input_filename: str):
    filename = os.path.basename(input_filename) #获取输入文件名
    filepath = os.path.dirname(input_filename) #获取文件绝对路径
    
    #生成文件名+随机字符串的子文件夹
    alphabet = "zyxwvutsrqponmlkjihgfedcba"
    outputdir = input_filename+''.join(random.sample(alphabet,5))
    os.makedirs(outputdir)

    #按50MB分割文件
    split = Split(input_filename, outputdir)
    split.bysize(size=1024*1024*50)

    #返回分割文件的存放文件夹
    return outputdir


def file_upload(source_filename, target_bucket):
    workdir = file_split(source_filename)

    #获取拆分的文件列表并转化为blob
    source = []
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_bucket)
    df = pandas.read_csv(workdir+'/'+'manifest')
    for file in df['filename']:
        print (workdir+'/'+file)
        source.append(bucket.blob(workdir+'/'+file))
    
    #设置目标文件
    filename = os.path.basename(source_filename) #获取输入文件名
    destination = bucket.blob(filename)
    destination.content_type = "text/plain"

    #上传文件
    destination_generation_match_precondition = 0
    destination.compose(source, if_generation_match=destination_generation_match_precondition)






   # print (workdir)

    #获取拆分的文件列表并转化为blob



    
#
#   outputfilelist=[]
#   df = pandas.read_csv(outputdir+'/'+'manifest')
#   for file in df['filename']:
#       outputfilelist.append(file)
#
#
#
#
#   #print (df["filename"])
#   print (*outputfilelist, sep = "\n")






#split = Split("/home/gcpvm/py/file/demofile01_1", "/home/gcpvm/py/file")
#split.bysize(size=1024*1024*50)


file_upload("/home/gcpvm/py/file/demofile01", "hy-gcs-003")
