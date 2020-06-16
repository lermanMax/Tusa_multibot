def equally(users):

    fullbank = sum([users[i] for i in users]) #сколько всего потрачено
    selfbank = int(fullbank/len(users)) #сколько потратил каждый. без дробной части

    debt = {} # долг
    # число-сколько должен каждый. отрицательное-займодатель, положительное-заёмщик
    for i in users: debt[i] = selfbank - users[i]

    transactions = {}

    while debt[max(debt, key=lambda x:debt[x])] != 0: # ждем, когда не останется должников
        name_min = min(debt, key=lambda x:debt[x]) # самый большой займодатель
        name_max = max(debt, key=lambda x:debt[x]) # самый большой заёмщик
        # вычиление транзакции
        # t = (abs(debt[name_max])+abs(debt[name_min])-abs(debt[name_max]+debt[name_min]))/2
        t = min(abs(debt[name_max]),abs(debt[name_min]))
        transactions[name_max+' to '+name_min] = t
        debt[name_max] -= t
        debt[name_min] += t

    victim = min(debt, key=lambda x:debt[x]) # жертва округления. тот, кто недополучит
    if debt[victim] != 0: transactions[victim +', тебя обманули на'] = debt[victim] # если долг не равен 0, записать

    return transactions
