import re

with open('bib.txt', 'r', encoding='utf-8') as file:
    bib_data = file.read()
    # 調整正則表達式來匹配被大括號包裹或未包裹的 title
    title_match = re.search(r'title\s*=\s*{+(.+?)}+', bib_data)
    if title_match:
        title = title_match.group(1)
        words = title.split()
        # 定義小寫的單字集合
        lowercase_words = {'of', 'a', 'the', 'in', 'on', 'at', 'for', 'and', 'to', 'with'}
        # 檢查格式
        formatted_correctly = True
        for word in words:
            if word.lower() in lowercase_words and word.islower():
                continue
            elif word.lower() not in lowercase_words and word[0].isupper() and word[1:].islower():
                continue
            else:
                formatted_correctly = False
                break
        if formatted_correctly:
            print("Title 格式正確")
        else:
            print("Title 格式不正確")
    else:
        print("未找到 title 欄位")