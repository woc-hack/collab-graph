import io

sample_n = 100000
path_to_p2a_table = "/home/elena/p2a_table"
with io.open(path_to_p2a_table, encoding="latin-1") as data_file:
    first_n_rows = [next(data_file) for x in range(sample_n)]
sample_data = "".join(first_n_rows)
with io.open("data/sample-data.txt", "w") as sample_data_file:
    sample_data_file.write(sample_data)
