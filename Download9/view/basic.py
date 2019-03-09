def bytes_to_maxunit(size):
    if (size < 1024):
        return str(size) + str('B')
    elif (size < 1024 * 1024):
        return str('%.2f' % (size / 1024)) + 'KB'
    elif (size < 1024 * 1024 * 1024):
        return str('%.2f' % (size / 1024 / 1024)) + 'MB'
    else:
        return str('%.2f' % (size / 1024 / 1024 / 1024)) + 'GB'

def seconds_to_hms(remain, v):
    if (v == 0):
        return '00:00:00'
    ftime = int(remain / v)
    if (int(ftime / 100) > 100):
        return '99:59:59'
    else:
        return str('%.2d' % (ftime / 3600)) + ":" + str('%.2d' % (ftime % 3600 / 60)) + ":" + str('%.2d' % (ftime % 60))