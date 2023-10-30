from parser.keywords.main import KeyWord

keys = KeyWord('./keyword.db')
key = keys.get_key('en', [1,10])
print(key)