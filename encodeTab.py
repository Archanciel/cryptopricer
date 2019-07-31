def encodeTabbedLines():
    encodedLinesList = []
    tabMode = False
       
    with open('tabbedText.txt', 'r') as file:
        for line in file.read().splitlines():
            if '    ' in line:
                tabMode = True
                line = line.replace('    ', '[t]')
            else:
                if tabMode:
                    line = '[/t]' + line
                    tabMode = False
                   
            encodedLinesList.append(line)

    return '\n'.join(encodedLinesList)

def encodeTabbedLinesVariant():
    encodedLinesList = []
    tabMode = False
       
    with open('tabbedText.txt', 'r') as file:
        for line in file.read().splitlines():
            if '    ' in line:
                tabMode = True
                line = line.replace('    ', '[t]')
            else:
                if tabMode:
                    #line = '[/t]' + line
                    tabMode = False
                   
            encodedLinesList.append(line)

    return '\n'.join(encodedLinesList)

def encodeTabbedLinesSmarter():
    encodedLinesList = []
    tabMode = False
       
    with open('tabbedText.txt', 'r') as file:
        for line in file.read().splitlines():
            if '    ' in line and not tabMode:
                tabMode = True
                line = line.replace('    ', '[t]')
            else:
                if not '    ' in line and tabMode:
                    line = '[/t]' + line
                    tabMode = False
                else:
                    line = line.replace('    ', '')
                    
            encodedLinesList.append(line)

    return '\n'.join(encodedLinesList)

print('\ninitial\n')
print(encodeTabbedLines())
print('\nvariant\n')
print(encodeTabbedLinesVariant())
print('\nsmarter\n')
print(encodeTabbedLinesSmarter())