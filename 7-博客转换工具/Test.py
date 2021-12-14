import markdown

with open('打造正则引擎[1]--正则表达式的介绍.md', 'r') as f:
    text = f.read()
    html = markdown.markdown(text)

with open('打造正则引擎[1]--正则表达式的介绍.html', 'w') as f:
    f.write(html)