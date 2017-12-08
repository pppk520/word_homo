from util.homoglyph_utility import HomoglyphUtility

def recover_homo_word(word, homo_map):      
    ord_list = list(map(ord, word))
                                                                                
    w = []                                                                      
    for i in range(len(ord_list)):                                              
        if ord_list[i] in homo_map:                                      
            w.append(homo_map[ord_list[i]])                              
        else:                                                                   
            w.append(word[i])                                                   
                                                                                
    return ''.join(w) 

def is_target_homo_word(word, homo_map):
    if len(word) == 0:      
        return False                                                            
                                                            
    ord_list = list(map(ord, word))

    ascii_count = 0                                                             
    target_count = 0                                                            
    outlier_cont = 0

    for i in range(len(ord_list)):                                           
        if ord_list[i] >= ord('A') and ord_list[i] <= ord('Z') or \
           ord_list[i] >= ord('a') and ord_list[i] <= ord('z'):                 
                ascii_count += 1                                                
        elif ord_list[i] in homo_map:                                    
            target_count += 1                                                   
        else:                                                                   
            outlier_cont += 1                                                   
                                                                                
    hit = target_count == 1 and ascii_count >= 2 and outlier_cont == 0          
                                                                                
    return hit  


def main():
    confusable_path = 'data/confusablesSummary.txt'
    test_words_path = 'data/input_test_words.txt'

    homo_map = HomoglyphUtility.get_homo_map(confusable_path, for_recover=True)

    with open(test_words_path) as f:
        for line in f:
            word = line.strip()

            if is_target_homo_word(word, homo_map):
                print('{} [suspicious]'.format(word))
            else:           
                print(word) 


if __name__ == '__main__':
    main()

