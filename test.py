import pickle

with open('test.dat', 'wb') as file:
    pickle.dump([0, 1, 2, 3, 4, 5, 6, 7], file)

with open('test.dat', 'rb') as file:
    x = pickle.load(file)
    queue_list = [item for item in x if item != 3]  # Corrected the condition here

with open('test.dat', 'wb') as file:
    pickle.dump(queue_list, file)

with open('test.dat', 'rb') as file:
    x = pickle.load(file)

print(x)
