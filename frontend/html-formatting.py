import io
import json
import sys
import time

sys.path.append("")


def remove_html_tags(path_to_json_data, path_to_new_json_data):
    left_angle_bracket = "\\u0026lt;"
    right_angle_bracket = "\\u0026gt;"
    amp = "\\u0026amp;"
    quote = "\\u0026quot;"
    with io.open(path_to_json_data) as f_old:
        with io.open(path_to_new_json_data, 'w+') as f_new:
            lines = f_old.readlines()
            for i, line in enumerate(lines):
                print(len(line))
                line = line.replace(left_angle_bracket, "<").replace(right_angle_bracket, ">").replace(quote, "").replace(amp, "&")
                f_new.write(line)


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2]

    start_time = time.time()
    remove_html_tags(in_path, out_path)
    end_time = time.time()
    print(end_time - start_time)