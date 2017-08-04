class PRTC:

    def __init__(self):
        print("init")

        with open('suite_all.dat') as f1:
            case_list = []
            for case_section in f1.read().split('['):
                if 'CASEID' in case_section :
                    case_lines = case_section.split('\n')
                    case = case_lines[0].strip(']')
                    case_id = ''
                    argument_id = ''
                    function_name = ''
                    argument_content = ''
                    for c_line in case_lines[1:]:
                        if '#' not in c_line:
                            argument_content += c_line + '\n'
                            if 'CASEID' in c_line:
                                case_id = c_line.split('=')[1].strip()
                            elif 'ARGUMENTS' in c_line:
                                argument_id = c_line.split('=')[1].strip()
                            elif 'FUNCTIONNAME' in c_line:
                                function_name = c_line.split('=')[1].strip()
                    case_list.append([case, case_id, argument_id, function_name, argument_content.strip(), 'X', ''])

        with open('suite_all.dat') as f2:
            for case_in_use in f2.readlines():
                if 'CASESECTION' in case_in_use and '#' not in case_in_use:
                    case_in_use_id = case_in_use.split('=')[1].strip()
                    for idx, item in enumerate(case_list):
                        if case_in_use_id.lower() == item[0].lower():
                            case_list[idx][5] = 'O'


        with open('.\\testlogs\TPAFInfo_.log') as f:
            test_result = []
            for logs in f.readlines():
                if '> in Module {MAIN}]' in logs:
                    log = logs.split('][')
                    for case_content in case_list:
                        if log[1].lower() == case_content[1].lower() and log[4].split('<')[1].split('>')[0].lower() == case_content[3].lower():
                            for idx, item in enumerate(case_list):
                                if case_content[0].lower() == item[0].lower():
                                    case_list[idx][6] = log[2]


        with open('case.dat') as f:
            argument_list = []
            for argument_data in f.read().split('['):
                if 'Expected' in argument_data:
                    argument_lines = argument_data.split('\n')
                    case_argument_id = argument_lines[0].strip('[ ]\t\r\n')
                    case_argument_input = ''
                    case_argument_except =''
                    for argu_line in argument_lines[1:]:
                        if '#' not in argu_line and argu_line != '':
                            if 'Expected' in argu_line:
                                case_argument_except += argu_line + '\n'
                            else:
                                case_argument_input += argu_line + '\n'
                    argument_list.append([case_argument_id, case_argument_input.strip(), case_argument_except.strip()])


        with open('result.xls', 'w') as xls:
            xls.write('Case\tArgument\tIn use\tResult\tInput\tExcepted\n')
            for case in case_list:
                r3 = ''
                r4 = ''
                for argument in argument_list:
                    if case[2].lower() == argument[0].lower():
                        r3 = argument[1]
                        r4 = argument[2]
                # result.append([case[0],case[1],case[2],r3,r4])
                xls.write(case[0] +'\t\"'+ case[4] +'\"\t\"'+ case[5] +'\"\t\"'+ case[6] +'\"\t\"'+ r3 +'\"\t\"'+ r4 + '\"\n')

        print()





if __name__ == '__main__':
    PRTC()
