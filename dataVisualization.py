import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy


def open_files():
    names_of_files = ["data/rsel.csv", "data/cel-rs.csv", "data/2cel-rs.csv", "data/cel.csv", "data/2cel.csv"]
    data_tab = []
    for name in names_of_files:
        data_tab.append(numpy.genfromtxt(open(name, "rb"), delimiter=",", names=True, deletechars=''))

    return data_tab


def calculate_avg(data):
    a = [None] * len(data)
    for index in range(0, len(data)):
        a[index] = extract(data[index])
    return a


def extract(data):
    return [avg(list(elem)[2:]) for elem in data]


def avg(array):
    return sum(array) / len(array)


def column(matrix, index):
    return [row[index] for row in matrix]


def scale_x_axis(data):
    return [elem / 1000 for elem in data]


def scale_y_axis(data):
    return [elem * 100 for elem in data]


data = open_files()
data_avg = calculate_avg(data)

plt.rc('font', family='Times New Roman')
plt.figure(figsize=(6.7, 5.7))
plt.subplot(121)

names_of_algorithms = ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']
shortcuts_of_colors = ['-b', '-g', '-r', '-k', '-m']
shortcuts_of_markers = ['o', 'v', 'D', 's', 'd']
for i in range(0, len(data_avg)):
    plt.plot(scale_x_axis(column(data[i], 1)), scale_y_axis(data_avg[i]), shortcuts_of_colors[i],
             marker=shortcuts_of_markers[i], markevery=25,
             linewidth=1.0,
             markerfacecolor=colors.colorConverter.to_rgba(shortcuts_of_colors[i][1], alpha=.7),
             markeredgecolor="k",
             markeredgewidth=0.5,
             label=names_of_algorithms[i])

plt.legend(loc='lower right', numpoints=2)
plt.xlabel('Rozegranych gier(x1000)')
plt.ylabel('Odsetek wygranych gier [%]')
ax = plt.gca()
upper_axis = ax.twiny()
upper_axis.set_xticks(numpy.arange(0, 240, 40))
upper_axis.set_xlabel("Pokolenia")
upper_axis.tick_params(direction='in', top=True, right=True)
ax.tick_params(direction='in', top=True, right=True)
ax.set_xlim([0, 500])
ax.set_ylim([60, 100])
ax.grid(linestyle='dotted')

plt.subplot(122)
bp = plt.boxplot([scale_y_axis(elem[-1])[2:] for elem in data],
                 notch=True, showmeans=True)

plt.setp(bp['means'], markeredgecolor="black", marker='o', markerfacecolor="blue")
plt.setp(bp['whiskers'], linestyle=(0, (7.5, 6)), color="b")
plt.setp(bp['medians'], color="r")
plt.setp(bp['boxes'], color="b")
plt.setp(bp['fliers'], markeredgecolor="blue", marker='+')
ax2 = plt.gca()
ax2.set_ylim([60, 100])
ax2.set_xticklabels(names_of_algorithms, rotation=20)
ax2.grid(linestyle='dotted')
ax2.yaxis.tick_right()
ax2.tick_params(direction='in', top=True, right=True)

plt.show()
# plt.savefig('myplot.pdf')
plt.close()
