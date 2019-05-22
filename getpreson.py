import itchat

itchat.login()
friends = itchat.get_friends(update=True)[0:]
print(friends)
def get_var(var):
    variable = []
    for i in friends:
        value = i[var]
        if value == '乐逍遥':
           print(i)
    return variable

NickName = get_var("NickName")
# Sex = get_var("Sex")
# Province = get_var("Province")
# City = get_var("City")
# Signature = get_var("Signature")
# qq= {'NickName' : NickName,'Sex' : Sex,'Province' : Province,'City' : City,'Signature' : Signature}
# print(qq)

