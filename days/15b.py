p_input = "9,6,0,10,18,2,1"
#p_input = "0,3,6"

numbers = list(map(int, p_input.split(',')))
record_spoken = {x: [0, [None, None]] for x in numbers}
if 0 not in record_spoken:
    record_spoken[0] = [0, [None, None]]
last_spoken = None

n = 30000000
for i in range(1, n + 1):
    if i % 1000000 == 0:
        print("Iteration", i)
    x = numbers[(i - 1) % len(numbers)]

    if record_spoken[x][0] == 0:
        last_spoken = x
    elif record_spoken[last_spoken][0] == 1:
        last_spoken = 0
    else:
        last_spoken = record_spoken[last_spoken][1][0] - \
            record_spoken[last_spoken][1][1]

    if last_spoken not in record_spoken:
        record_spoken[last_spoken] = [0, [None, None]]

    record_spoken[last_spoken][0] += 1
    record_spoken[last_spoken][1][1] = record_spoken[last_spoken][1][0]
    record_spoken[last_spoken][1][0] = i
print(last_spoken)
