
'''
confusablesSummary.txt
http://www.unicode.org/Public/security/10.0.0/confusablesSummary.txt
'''

class HomoglyphUtility(object):
    @staticmethod
    def is_target_homo_char(c):
        c_ord = ord(c)

        # Only target on alpha
        if (c_ord >= ord('A') and c_ord <= ord('Z')) or\
           (c_ord >= ord('a') and c_ord <= ord('z')):
            return True

        return False

    @staticmethod
    def get_homo_map(summary_filepath, for_recover=True):
        '''
        file format dependent
        '''
        homo_map = {}

        with open(summary_filepath) as f:
            for line in f:
                if line.startswith('#'):
                    parts = line.strip().split()
                    try:
                        key = parts[1]
                        key_ord = ord(key)

                        if not HomoglyphUtility.is_target_homo_char(key):
                            continue

                        for c in parts[2:]:
                            # ascii is not our target
                            if ord(c) <= 255:
                                continue

                            if for_recover:
                                homo_map[ord(c)] = key
                            else:
                                if not key in homo_map:
                                    homo_map[key] = []

                                homo_map[key].append(c)
                    except Exception as ex:
                        pass

        return homo_map

if __name__ == '__main__':
    print(HomoglyphUtility.get_homo_map('data/confusablesSummary.txt', for_recover=True))
    print(HomoglyphUtility.get_homo_map('data/confusablesSummary.txt', for_recover=False))

