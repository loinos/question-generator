import openai
import json
openai.api_key = "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"

def get_questions(n,text):
    messages = []
    message = r"user: составь json файл формата {'questions':[{'question':'*',options[*,*,*,*],'answer':'*номер правильного ответа*'},...]}  на" + str(n) + "вопросов по вот этому тексту :"+str(text)  # вводим сообщение 
    messages.append({"role": "user", "content": message})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
    reply = chat.choices[0].message.content
    return reply


s = get_questions(5,"граждане и гражданки советского союза советское правительство и его глава товарищ сталин поручили мне сделать следующее заявление сегодня в четыре часа утра без предъявления каких-либо претензий к советскому союзу без объявления войны германские войска напали на нашу страну атаковали наши границы во многих местах и подвергли бомбёжке со своих самолётов наши города житомир киев севастополь каунас и некоторые другие причём убито и ранено более двухсот человек налёты вражеских самолётов и артиллерийский обстрел были совершены также с румынской и финляндской территории это неслыханное нападение на нашу страну является беспримерным в истории цивилизованных народов произведено несмотря на то что между ссср и германией заключён договор о ненападении и советское правительство со всей добросовестностью выполняло все условия этого договора я ответственность за это разбойничье нападение на советский союз их правителей правительство советского союза выражает непоколебимую уверенность в том что наши доблестные армия и флот и смелые соколы советской авиации честью выполнят долг перед родиной перед советским народом и нанесут сокрушительный удар агрессору наше дело правое враг будет разбит победа будет за нами")
print(s)