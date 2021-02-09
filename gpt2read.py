import gpt_2_simple as gpt2


sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

while True:
	generated = gpt2.generate(sess, model_name="124M", return_as_list=True)
	single_text = generated[0]
	print(single_text)
	f = open("demo.txt", "a")
	f.write(single_text)
	f.write("\n")
	f.close()