import os
import sys
import argparse
import json
import codecs
import collections
import urllib.request

def get_target_map():
    ''' target iso-639-1 code
    https://cloud.google.com/translate/docs/languages
    '''
    target_map = {
      "Afrikaans" : "af",
      "Albanian" : "sq",
      "Amharic" : "am",
      "Arabic" : "ar",
      "Armenian" : "hy",
      "Azeerbaijani" : "az",
      "Basque" : "eu",
      "Belarusian" : "be",
      "Bengali" : "bn",
      "Bosnian" : "bs",
      "Bulgarian" : "bg",
      "Catalan" : "ca",
      "Cebuano" : "ceb (ISO-639-2)",
      "Chichewa" : "ny",
      "Chinese (Simplified)" : "zh-CN (BCP-47)",
      "Chinese (Traditional)" : "zh-TW (BCP-47)",
      "Corsican" : "co",
      "Croatian" : "hr",
      "Czech" : "cs",
      "Danish" : "da",
      "Dutch" : "nl",
      "English" : "en",
      "Esperanto" : "eo",
      "Estonian" : "et",
      "Filipino" : "tl",
      "Finnish" : "fi",
      "French" : "fr",
      "Frisian" : "fy",
      "Galician" : "gl",
      "Georgian" : "ka",
      "German" : "de",
      "Greek" : "el",
      "Gujarati" : "gu",
      "Haitian Creole" : "ht",
      "Hausa" : "ha",
      "Hawaiian" : "haw (ISO-639-2)",
      "Hebrew" : "iw",
      "Hindi" : "hi",
      "Hmong" : "hmn (ISO-639-2)",
      "Hungarian" : "hu",
      "Icelandic" : "is",
      "Igbo" : "ig",
      "Indonesian" : "id",
      "Irish" : "ga",
      "Italian" : "it",
      "Japanese" : "ja",
      "Javanese" : "jw",
      "Kannada" : "kn",
      "Kazakh" : "kk",
      "Khmer" : "km",
      "Korean" : "ko",
      "Kurdish" : "ku",
      "Kyrgyz" : "ky",
      "Lao" : "lo",
      "Latin" : "la",
      "Latvian" : "lv",
      "Lithuanian" : "lt",
      "Luxembourgish" : "lb",
      "Macedonian" : "mk",
      "Malagasy" : "mg",
      "Malay" : "ms",
      "Malayalam" : "ml",
      "Maltese" : "mt",
      "Maori" : "mi",
      "Marathi" : "mr",
      "Mongolian" : "mn",
      "Burmese" : "my",
      "Nepali" : "ne",
      "Norwegian" : "no",
      "Pashto" : "ps",
      "Persian" : "fa",
      "Polish" : "pl",
      "Portuguese" : "pt",
      "Punjabi" : "ma",
      "Romanian" : "ro",
      "Russian" : "ru",
      "Samoan" : "sm",
      "Scots Gaelic" : "gd",
      "Serbian" : "sr",
      "Sesotho" : "st",
      "Shona" : "sn",
      "Sindhi" : "sd",
      "Sinhala" : "si",
      "Slovak" : "sk",
      "Slovenian" : "sl",
      "Somali" : "so",
      "Spanish" : "es",
      "Sundanese" : "su",
      "Swahili" : "sw",
      "Swedish" : "sv",
      "Tajik" : "tg",
      "Tamil" : "ta",
      "Telugu" : "te",
      "Thai" : "th",
      "Turkish" : "tr",
      "Ukrainian" : "uk",
      "Urdu" : "ur",
      "Uzbek" : "uz",
      "Vietnamese" : "vi",
      "Welsh" : "cy",
      "Xhosa" : "xh",
      "Yiddish" : "yi",
      "Yoruba" : "yo",
      "Zulu" : "zu",
    }

    return target_map

def get_target_codes():
    targets = ['Spanish', 
               'Portuguese', 
               'Russian', 
               'German',
               'French',
               'Turkish',
               'Italian',
               'Dutch',
               'Swedish',
               'Danish'
               ]

    target_map = get_target_map()

    return [target_map[x] for x in targets]

def save_dict(d, filepath):
    str_for_save = json.dumps(d, sort_keys=True, indent=4, ensure_ascii=False)

    if not filepath:
        print(str_for_save)
        return

    with codecs.open(filepath, 'w', 'utf-8') as fw:
        fw.write(str_for_save)

def load_dict(filepath):
    if not os.path.exists(filepath):
        return {}

    with codecs.open(filepath, 'r', 'utf-8') as f:
        return json.loads(f.read())

def get_expanded_keywords(words, target_codes, expand_dict):
    for code in target_codes:
        pass            

def get_wv_model(filepath):
    import gensim

    model = gensim.models.KeyedVectors.load_word2vec_format(filepath, binary=True)
    return model

def expand_similar_words(words, model, threshold):
    sim_dict = {}

    for w in words:
        try:
            sim_dict[w] = set()
            similar_words = model.most_similar(positive=[w], topn=3)
            for sim_word in similar_words:
                if sim_word[1] >= threshold:
                    sim_dict[w].add(sim_word[0].lower())

        except KeyError as e:
            pass

    return sim_dict

def get_translate_words(words, translate_url_pattern, api_key, target_codes, curr_translate_dict):
    # get word-code pair first
    wc_pairs = []

    for word in words:
        if not word in curr_translate_dict:
            wc_pairs += [(word, code) for code in target_codes]
            continue

        for code in target_codes:
            if not code in curr_translate_dict[word]:
                wc_pairs.append((word, code))

    result_dict = {}

    for word, code in wc_pairs:
        if not word in result_dict:
            result_dict[word] = {'en': word}

        target_url = translate_url_pattern.replace('<WORD>', word)
        target_url = target_url.replace('<TARGET_CODE>', code)
        target_url = target_url.replace('<API_KEY>', api_key)

        print(target_url)

        r = urllib.request.urlopen(target_url)
        res = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
        result_dict[word][code] = res['data']['translations'][0]['translatedText']

    return result_dict

def merge_dicts(base_dict, to_merge_dict):
    for k, v in to_merge_dict.items():
        if isinstance(v, collections.Mapping):
            r = merge_dicts(base_dict.get(k, {}), v)
            base_dict[k] = r
        else:
            base_dict[k] = to_merge_dict[k]

    return base_dict

def main():
    translate_url_pattern = "https://www.googleapis.com/language/translate/v2?q=<WORD>&target=<TARGET_CODE>&source=en&key=<API_KEY>"

    parser = argparse.ArgumentParser(description='Word Expansion Tool')
    parser.add_argument("--word_list_file", help="input words separated by comma (,)")
    parser.add_argument("--word_2_vec_bin", help="word2vec bin file for expanding")
    parser.add_argument("--word_2_vec_similar_threshold", help="expanding threshold", type=float, default=0.75)
    parser.add_argument("--api_key", help="api key for querying Google Translation API")
    parser.add_argument("--load_translate_dict", help="load existing translate dict file")
    parser.add_argument("--expand_by_translate", help="expand words by loaded translated dict", action="store_true")
    parser.add_argument("--expand_by_nfd", help="expand words by unicode nfd", action="store_true")
    parser.add_argument("--output_filepath", help="output file of expanded words")

    args = vars(parser.parse_args())

    words = None
    word_list_file = args['word_list_file']
    output_filepath = args['output_filepath']
    translate_dict = {}

    if word_list_file:
        with open(word_list_file) as f:
            words = set(map(str.strip, f.read().split(',')))

    if args['word_2_vec_bin']:
        model = get_wv_model(args['word_2_vec_bin'])
        threshold = args['word_2_vec_similar_threshold']

        sim_dict = expand_similar_words(words, model, threshold)
        save_dict(result_dict, output_filepath)
        return
 
    if args['load_translate_dict']:
        translate_dict = load_dict(args['load_translate_dict'])

    if args['api_key']:
        target_codes = get_target_codes()
        diff_translate_dict = get_translate_words(words, 
                                                  translate_url_pattern, 
                                                  args['api_key'], 
                                                  target_codes, 
                                                  translate_dict)

        translate_dict = merge_dicts(translate_dict, diff_translate_dict)
        save_dict(translate_dict, output_filepath)

    if args['expand_by_translate']:
        expand_set = set(words)

        target_codes = get_target_codes()
        for word in words:
            for code in target_codes:
                expand_set.add(translate_dict[word][code].lower())
 
        print(','.join(expand_set))

        words = expand_set # for following expansion

    if args['expand_by_nfd']:
        expand_set = set(words)

        for word in words:
            expand_set |= expand_by_nfd(word)
            
        print(','.join(expand_set))


if __name__ == '__main__':
    main()
