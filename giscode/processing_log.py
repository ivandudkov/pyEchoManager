class ProcessingLog:
    """A class for proc log"""
    
    def __init__(self):
        self.metadata_header = {'Cruise':None, 
                                 'Vessel':None, 
                                 'Date':None, 
                                 'MBES':None, 
                                 'PositioningSystem':None}
        self.header = None
        self.lines = []
        
    def read_log(self, path):
        
        fs_position = None
        with open(path, 'r') as file:
            for num, line in enumerate(file):
                
                parsed_content = line.split(sep='\n')[0].split(sep='\t')
                log_line = ProcessingLogLine()
                
                if num == 0:
                    log_line.name = 'header'
                    log_line.content = parsed_content
                    self.header = log_line
                    
                    count = 0
                    for element in parsed_content:
                        if "Fileset" in element:
                            fileset_position = count
                            break
                        count += 1
                    
                else:
                    log_line.name = parsed_content[fileset_position]
                    log_line.content = parsed_content
                    self.lines.append(log_line)
        
        
        
        

class ProcessingLogLine:
    """bla bla"""
    
    def __init__(self):
        self.name = None
        self.content = None
        
    def __str__(self):
        BLUE ='\033[94m'
        END = '\033[0m'
        return f'Log line is referred to {BLUE}{self.name}{END}\nContent is {BLUE}{self.content}{END}'
        