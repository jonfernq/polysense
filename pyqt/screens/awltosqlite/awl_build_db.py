

def chunk(seq, step):
    chunked = [seq[i:i+step] for i in range(0,len(seq),step)]
    return chunked 

def file_to_lines_list(filename):
    with open(filename, 'rt', encoding='utf-8') as f:
        lines = []
        for line in f:
            if line.strip() == '':
                continue 
            lines.append(line.strip()) 
        return lines 
        


# derivative words provide a list of the raw words (set for inclusion check, used for) 

awl_derivative_words = file_to_lines_list('awl_derivative_words.txt')
awl_eng_thai = file_to_lines_list('awl_eng_thai.txt')

recs = chunk(awl_eng_thai, 4)
print(len(recs))   
print(recs) 
quit() 






        

