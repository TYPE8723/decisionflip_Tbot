count = 0
unique_users = []
dict = {}
with open("./userlogs.txt","r") as log_file:
    for line in log_file.readlines():
            count = count+1
            user_name = line.split(' ')[0]
            user_name_cut = user_name[0]+'***'+user_name[-1]
            if user_name_cut in unique_users :
                dict[user_name_cut] = dict[user_name_cut]+1
                pass
            else:
                dict[user_name_cut] = 0
                unique_users.append(user_name_cut)
print('hits : '+str(count))
#print('unique_users('+str(len(unique_users))+') : '+str(unique_users ))
print('usr hits : ',dict)