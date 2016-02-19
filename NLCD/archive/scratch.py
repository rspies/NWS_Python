

txt_file = open('temp.txt', 'w')
'''
a = 0
while a < 256:
    txt_file.write("'" + '%' + str(a) + ',' + "'" + ' + ')
    a += 1
txt_file.close()
'''

'''
a = 0
while a < 256:
    txt_file.write("_" + str(a) + '=' + "[]" + '\n')
    a += 1
txt_file.close()
'''

'''
a = 0
while a < 256:
    txt_file.write(str('if Value == ' + "'" + str(a) + "'" + ':' '\n' + \
                       '    ' + "_" + str(a)) + '.append(count)' + '\n' + \
                       '    ' + 'Count.append(count)' + '\n')
    a += 1
txt_file.close()
'''

'''
a = 0
while a < 256:
    txt_file.write('_' + str(a) + 'sum' + ' = ' + 'numpy.sum(' + "_" + str(a) + ')' + '\n')
    a += 1
txt_file.close()
'''

'''
a = 0
while a < 256:
    txt_file.write("_" + str(a) + 'percent' + ' = ' + 'float(' + "_" + str(a) + 'sum' + '/Count_sum*100' + ')' + '\n')
    a += 1
txt_file.close()
'''


a = 0
while a < 256:
    txt_file.write('str(' + "_" + str(a) + 'percent' + ')' + ' + ' + "','" + ' + ')
    a += 1
txt_file.close()

