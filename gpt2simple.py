import gpt_2_simple as gpt2
import os
import requests

model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/


file_name = "input.txt"

sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              file_name,
              model_name=model_name,
              steps=1000)   # steps is max number of training steps

while True:
	generated = gpt2.generate(sess, return_as_list=True)
	single_text = generated[0]
	print(single_text)
	f = open("demofile2.txt", "a")
	f.write(single_text)
	f.write("\n")
	f.close()