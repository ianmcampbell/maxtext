python3 MaxText/train.py MaxText/configs/base.yml run_name=rwitten_20230703_2_rep1 base_output_directory="gs://maxtext-experiments-multipod/" dataset_path="gs://maxtext-dataset/" number_of_repetitions=1 steps=17000 warmup_steps=1700 learning_rate="1.e-3"
python3 MaxText/train.py MaxText/configs/base.yml run_name=rwitten_20230703_2_rep2 base_output_directory="gs://maxtext-experiments-multipod/" dataset_path="gs://maxtext-dataset/" number_of_repetitions=2 steps=17000 warmup_steps=1700 learning_rate="1.e-3"
python3 MaxText/train.py MaxText/configs/base.yml run_name=rwitten_20230703_2_rep4 base_output_directory="gs://maxtext-experiments-multipod/" dataset_path="gs://maxtext-dataset/" number_of_repetitions=4 steps=17000 warmup_steps=1700 learning_rate="1.e-3"
python3 MaxText/train.py MaxText/configs/base.yml run_name=rwitten_20230703_2_layers16 base_output_directory="gs://maxtext-experiments-multipod/" dataset_path="gs://maxtext-dataset/" number_of_repetitions=1 steps=17000 warmup_steps=1700 learning_rate="1.e-3"  base_num_decoder_layers=16
python3 MaxText/train.py MaxText/configs/base.yml run_name=rwitten_20230703_2_layers32 base_output_directory="gs://maxtext-experiments-multipod/" dataset_path="gs://maxtext-dataset/" number_of_repetitions=1 steps=17000 warmup_steps=1700 learning_rate="1.e-3" base_num_decoder_layers=32

