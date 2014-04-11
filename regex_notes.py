import re

# p_compile (find protocol) summary:
# find a word \w, follow by digit \d, which may or may not be present (?) (\w\d?)
# if preceeded by a space (?<=\s)
# if followed by(?=) multiple blank spaces \s+, and a digit (?<=\s+d)
# or (|), find a word, space, word(multiple) and optional digit (\w\s\w+\d?)
# if preceeded by a space (?<=\s)
# if followd by one or more spaces, one or more digits and a . (?=\s+\d+\.)
p_compile = re.compile(r'(?<=\s)((\w\d?)|(\w\s\w+\d?)|(\w+?\*))(?=\s+\d+\.)')

# rp_compile (find route/prefix) summary
# find one to three digits, followed by a (.) period, and match the pattern up to three times
# then, find a one to three digits one time, followed by (/) and one to two digits.
# only if followed by optional one or more spaces and a mandatory open bracket
# or (|)
# followed by optional one or more spaces and a word
rp_compile = re.compile(r'((\d{1,3}\.){3}(\d{1,3}){1}(/\d{1,2})|(\d{1,3}\.){3}(\d{1,3}){1}(?=\s?\[))')
