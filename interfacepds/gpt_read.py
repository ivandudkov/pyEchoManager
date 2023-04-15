import struct


def read_gpt(input, output):
    """pds .gpt file conertion to latlon .txt table

    Parameters
    ----------
    input :
        path to input file .gpt
    output :
        path to save .txt table
    """
    with open(input, '+br') as file:
        
        buffer_pos = 0
        buffer = file.read()
        
        lat = []
        lon = []
        while buffer_pos != len(buffer) - 1:
            if buffer_pos <= 3:
                print(hex(buffer[buffer_pos]))
                buffer_pos += 1

            elif (len(buffer) - 1 - buffer_pos) < 8:
                print(f'ENND {buffer_pos} from {len(buffer)}')
                # lat.append(struct.unpack('8d', buffer[buffer_pos:buffer_pos+64]))
                # buffer_pos += 64
                # lon.append(struct.unpack('8d', buffer[buffer_pos:-1]))
                # buffer_pos += 64
                # print(f'{buffer_pos} from {len(buffer)}')
                break
            else:
                lat.append(struct.unpack('d', buffer[buffer_pos:buffer_pos+8])[0])
                buffer_pos += 8
                lon.append(struct.unpack('d', buffer[buffer_pos:buffer_pos+8])[0])
                buffer_pos += 8
                print(f'{buffer_pos} from {len(buffer)}')
        with open(output, 'w') as file2:
            
            for idx in range(len(lon)):
                print(f'{idx} {lat[idx]} {lon[idx]}')
                file2.write(f'{idx},{lat[idx]},{lon[idx]}\n')
            
        
read_gpt(r'C:\Users\IvanDudkov\Desktop\ABP50_TTR021-20220809-230803-L_B09p2.0.gpt',r'C:\Users\IvanDudkov\Desktop\ABP50_TTR021-20220809-230803-L_B09p2.0.txt')
