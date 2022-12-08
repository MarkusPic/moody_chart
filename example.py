from moody_chart import moody_chart


if __name__ == '__main__':
    fig, ax = moody_chart()
    fig.set_size_inches(7, 5)
    fig.savefig('moody_chart.png')
