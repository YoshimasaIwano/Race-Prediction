import os
def split_url_file():
    horse_url_dir = "../data/horse_url/"
    horse_url_file = horse_url_dir + "horse.txt"
    if os.path.isfile(horse_url_file):
        with open(horse_url_file, mode='r') as f:
            num_horse_url_file =  len(f.readlines()) // 1000
        f.close()
        with open(horse_url_file, mode='r') as f:
            for i in range(num_horse_url_file+1):
                new_horse_url_file = horse_url_dir + "horse_" + str(i) + ".txt"
                with open(new_horse_url_file, mode='a+') as fw:
                    for j in range(1000):
                        url_line = f.readline()
                        fw.write(url_line)
                    fw.close()

        f.close()

