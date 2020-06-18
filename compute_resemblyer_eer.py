similarity_results = {'1':[], '0':[]}

with open("resemblyser_sim_test.txt") as file:
    for line in file:
        splitted = line.split()
        similarity_results[splitted[0]].append(float(splitted[1]))

similarity_results['1'].sort()
similarity_results['0'].sort(reverse=True)

#print(len(similarity_results['1']))
#print(len(similarity_results['0']))

threshold = None

for i in range(len(similarity_results['1'])):
    if similarity_results['1'][i] >= similarity_results['0'][i] :
        threshold = similarity_results['1'][i]
        break

print("Threshold = " + str(threshold))

total_exs = len(similarity_results['1'])
correct_exs = 0
for res in similarity_results['1']:
    if res >= threshold:
        correct_exs += 1
print(correct_exs)
print(correct_exs / total_exs)

total_exs = len(similarity_results['0'])
correct_exs = 0
for res in similarity_results['0']:
    if res < threshold:
        correct_exs += 1
print(correct_exs)
print(correct_exs / total_exs)