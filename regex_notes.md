### p_compile (find protocol) summary:
* 
* (?<=\s)((\w)|(\w\s\w+\d?)|(\w+?\*))(?=\s+\d+\.)

rp_compile (find route/prefix) summary
find one to three digits, followed by a (.) period, and match the pattern up to three times
then, find a one to three digits one time, followed by (/) and one to two digits.
only if followed by optional one or more spaces and a mandatory open bracket
or (|)
followed by optional one or more spaces and a word

(r'((\d{1,3}\.){3}(\d{1,3}){1}(/\d{1,2})|(\d{1,3}\.){3}(\d{1,3}){1}(?=\s?\[))')
