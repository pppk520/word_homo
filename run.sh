# download homoglyph mappings
CONF_SUMM_FILE=data/confusablesSummary.txt

if [ ! -f $CONF_SUMM_FILE ]; then
    wget http://www.unicode.org/Public/security/10.0.0/confusablesSummary.txt -O $CONF_SUMM_FILE
fi

python tool-detect-homo.py
