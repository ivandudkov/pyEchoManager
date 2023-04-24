import os
from datetime import datetime, timezone
from numpy import pi, cos, sin, log, exp, arccos, tan, arctan, tanh, arctanh
import numpy as np
import matplotlib.pyplot as plt

# Based on GEBCO 17th Year Training Program
# ESCI_OE_774_874 JHC and Semme Dijkstra, CCOM, UNH

class SSP:
    """A Class for handling Sound Speed Profile data"""

    def __init__(self):

        # The data attributes
        self.obs_time = None
        self.log_time = None
        self.obs_latitude = None
        self.obs_longitude = None
        self.vessel_latitude = None
        self.vessel_longitude = None
        self.obs_sample = list()
        self.obs_depth = list()
        self.obs_ss = list()
        self.proc_depth = np.array([])
        self.proc_ss = np.array([])
        self.g = np.array([])
        self.proc_ss = np.array([])
        self.twtt_layer=np.array([])
        self.vessel_speed = None
        self.bot_depth = None

        self.metadata = dict()
        self.metadata["units"] = "rad"
        self.metadata["count"] = None
        self.metadata["geoid"] = None
        self.metadata["ellipsoid"] = None
        self.metadata["chart_datum"] = None
        self.metadata["time_basis"] = "UTC"
        self.metadata["name"] = None
        self.metadata["Source File"] = None
        
    def read_jhc_file(self, fullpath):
        """Read John's Sound Velocity Profiles,
        see data format in data/jhc_svp folder"""
        
        # Check to see whether data already exists in the object
        if self.obs_depth:
            raise RuntimeError('SSP object already contains a profile')
            
        # Check the File's existence
        if os.path.exists(fullpath):
            self.metadata["Source File"] = fullpath
            print('Opening sound speed profile data file:' + fullpath)
        else:  # Raise a meaningful error
            raise RuntimeError('Unable to locate the input file' + fullpath)

        # Open, read and close the file
        svp_file = open(fullpath)
        svp_content = svp_file.read()
        svp_file.close

        # Tokenize the contents
        svp_lines = svp_content.splitlines()
        self.obs_time = datetime.fromtimestamp(
            float(svp_lines[1].split()[0]), timezone.utc)
        self.log_time = datetime.fromtimestamp(
            float(svp_lines[2].split()[0]), timezone.utc)
        self.obs_latitude = float(svp_lines[3].split()[0])
        self.obs_longitude = float(svp_lines[3].split()[1])
        self.vessel_latitude = float(svp_lines[4].split()[0])
        self.vessel_longitude = float(svp_lines[4].split()[1])
        self.metadata["count"] = int(svp_lines[5].split()[0])

        count = 0  # initialize the counter for the number of rows read

        for svp_line in svp_lines[16:]:
            observations = svp_line.split()  # Tokenize the stringS
            self.obs_sample.append(float(observations[0]))
            self.obs_depth.append(float(observations[1]))
            self.obs_ss.append(float(observations[2]))
            count += 1

        if self.metadata["count"] != count:
            raise RuntimeError('Nr of Samples read ('+str(count) +
                               ') does not match metadata count (' +
                               str(self.metadata["count"])+')')
        
        ####### LAB_B
        
    def read_mvp_file(self, fullpath):
        """Read MVP file. See data/mvp for profile example"""
        # Check to see whether data already exists in the object

        if self.obs_depth:
            raise RuntimeError('SSP object already contains a profile')

        # Check the File's existence
        if os.path.exists(fullpath):
            self.metadata["Source File"] = fullpath
            print('Opening sound speed profile data file:' + fullpath)
        else:  # Raise a meaningful error
            raise RuntimeError('Unable to locate the input file' + fullpath)

        # Open, read and close the file
        svp_file = open(fullpath)
        svp_content = svp_file.read()
        svp_file.close

        # Save the file name as meta data

        self.metadata["name"] = os.path.basename(fullpath)

        # Tokenize the contents
        svp_lines = svp_content.splitlines()

        # Create a Position object
        pos = Position()

        n_lines = 0
        for line in svp_lines:
            print(line)
            n_lines += 1
            
            # B.0.2.0 Find the end of The Header
            if line == '':
                break            

            # B.0.2.1 Find the Time
            # Parse the time
            if line[0:8] == "GPS Time":
                # Extract the ZDA record
                obs = line.split()
                # Extract the UTC time string
                self.obs_time = ParseNMEA0183_ZDA(obs[2])

            # B.0.2.2 Find the Position
            # Parse the position            
            if line[0:12] == "GPS Position":
                # Extract the GPS record
                obs = line.split()
                # Extract the GGA position string
                _,self.obs_latitude,self.obs_longitude,_,_,_,_,_,_,_ = ParseNMEA0183_GGA(obs[2])

            # B.0.2.3 Find the Bottom Depth
            # Parse the Depth
            if line[0:13] == "Bottom Depth:":
                obs = line.split()
                self.bot_depth=float(obs[2])

            # B.0.2.4 Find the Vessel Speed
            # Parse the Vessel Speed
            if line[0:11] == "Ship Speed:":
                obs = line.split()
                self.vessel_speed=float(obs[2])/1.852


        # B.0.2.5 Parsing the Record Identifier Line
        print(n_lines)
        rec_type = svp_lines[n_lines].split(',')
        
        # Find the index of the Dpth(m) records
        index_depth = rec_type.index('Dpth(m)')
        
        # Find the index of the Sound Speed records
        index_ss = rec_type.index('SV(m/s)')
        
        # B.0.2.6 Parsing the Records
        for line in svp_lines[ n_lines + 1:]:
            obs = line.split(',')
            self.obs_depth.append( float(obs[index_depth]))
            self.obs_ss.append( float(obs[index_ss]))
            
        # B.0.2.7 Sorting the Records
        temp = sorted(zip(self.obs_depth, self.obs_ss), key=lambda x: x[0])
        self.obs_depth, self.obs_ss = map(list, zip(*temp))
        
        # B.0.2.8 Removing the Duplicates
        # Remove any duplicate depths with associated sound speeds
        d_p=self.obs_depth[0]            # previous depth value analyzed (we will start
                                         # looking at the 2nd depth)
        unwanted = []                    # indexes of the duplicate depths that are unwanted

        # Loop through the observations starting at the 2nd depth
        index = 0
        for d in self.obs_depth[1:]:
            index += 1                   # The index of the depth currently analyzed
            if d == d_p:
                unwanted.append(index)   # Current depth is the same a the previous depth, 
                                         # store its index 
            d_p = d                      # Done the current depth store as previous depth 
                                         # for next iteration

        for e in sorted( unwanted, reverse = True):
            del self.obs_depth[ e]       # Remove the last unwanted depth
            del self.obs_ss[ e]          # Remove the associated sound speed observation
            
        # B.0.2.9 Creating numpy Arrays to hold the depths and sound speeds
        self.d = np.array(self.obs_depth)
        self.c = np.array(self.obs_ss)
        
        # B.0.2.10 Extending the profiles to the Surface
        if self.d[0] > 0:
            self.d = np.insert(self.d,0,0)
            self.c = np.insert(self.c,0,self.c[0])
            
        # B.0.2.11 Calculating the Sound Speed Gradients
        self.g = (self.c[1:] - self.c[0:-1])/(self.d[1:] - self.d[0:-1])
        # B.0.2.12 Expanding the Profiles to Full Ocean Depth
        if self.d[-1] < 12000:
                self.d = np.append(self.d,12000)
                self.c = np.append(self.c,self.c[-1]+0.017*(12000-self.d[-2]))
                self.g = np.append(self.g,0.017)
                
        # B.0.2.13 Replacing Zero Gradients
        self.g[self.g == 0] = 0.0001
        
        # B.0.2.14 Updating the profile
        # Recalculate the sound speed profile
        for i in range(1,len(self.g)):
            self.c[i]=self.c[i-1]+(self.d[i] - self.d[i-1])*self.g[i-1]

            
            
    def determine_c( self, d):
        """Determine... ???"""
        layer = sum( d >= self.d) - 1
        ss = self.c[layer]+(d-self.d[layer])*self.g[layer]
        return ss
    
    
    def determine_depth(self, d_start, th_start, ss_start, twtt):
        """???"""
        # B1.3.0.0 Initialization
        depth=0
        rad_dist=0
        layer_s=0
        layer_e=0
        
        # Deal with angles of incidence greater than 90 degrees
        swap=False
        if th_start > pi/2:
            swap = True
            th_start = pi - th_start

        # B.1.3.0.1 Determine the start layer
        layer_s = sum(d_start >= self.d) - 1
        
        # B.1.3.0.2 Determine the Ray Constant
        ray_c = cos(th_start)/ss_start
        self.ray_constant = ray_c
        
        
        # B.1.3.0.3 Calculate Ray Path Properties for Each Layer  
        delta_d = (self.d[1:] - self.d[0:-1])
        r_curve = -1/(self.g[0:]*ray_c)
        th = arccos(self.c[0:]*ray_c)

        dx = r_curve * (sin(th[1:]) - sin(th[0:-1]))
        dz = delta_d     
        hm = 2/self.g*log(self.c[1:]/self.c[0:-1])
        dt = hm+2/self.g*log((1+sin(th[0:-1]))/(1+sin(th[1:])))      
        
        
        # B.1.3.0.4 Determine properties for start layer from the top to the start
        dx_init = r_curve[layer_s]*(sin(th_start)-sin(th[layer_s]))
        dz_init = d_start - self.d[layer_s]
        dt_init = 2/self.g[layer_s]*log(ss_start/self.c[layer_s])
        dt_init += 2/self.g[layer_s]*log((1+sin(th[layer_s]))/(1+sin(th_start)))
        
        # B.1.3.0.5 Accumulate From the Start Layer
        sum_dx = np.cumsum(dx[layer_s:])
        sum_dt = np.cumsum(dt[layer_s:])
        sum_dz = np.cumsum(dz[layer_s:])
        
        # B.1.3.0.6 Offset to the Start Depth
        sum_dx -= dx_init
        sum_dz -= dz_init
        sum_dt -= dt_init
        
        # B.1.3.0.7 Determine the Number of Boundaries Crossed and the End Layer Index        
        n_bounds =  sum( twtt >= sum_dt[:-1])
        layer_e = n_bounds + layer_s
        
        # B.1.3.0.8 Determine Properties for the final layer from the top to the end
        t = twtt-sum_dt[n_bounds-1]

        if n_bounds >= 0:
            t = twtt-sum_dt[n_bounds-1]
        else:
            raise RuntimeError('SSP start depth in same layer as reflector - not yet implemented')
            
        th_end = 2*arctan(tanh(-t*self.g[layer_e]/4+arctanh(tan(th[layer_e]/2))))
        dx_end = r_curve[layer_e] * (sin(th_end)-sin(th[layer_e]))
        dz_end = -r_curve[layer_e] * (cos(th_end)-cos(th[layer_e])) 
        
        # B.1.3.0.9 The Final Results
        if n_bounds >= 0:
            depth = sum_dz[n_bounds-1] + dz_end + d_start
            rad_dist = sum_dx[n_bounds-1] + dx_end

        if swap:
            rad_dist = - rad_dist
            
        
        # B1.3.0.0 Return values as tuple
        return depth, rad_dist, layer_s, layer_e;            

    
    def find_reversal(self, d_start, th_start, ss_start, twtt):
        """Not implemented yet. Find ray reversal layer"""
        pass
        
        
      
    def determine_twtt(self, d_start, th_start, ss_start, depth):
        """using start depth (transducer depth), initial angle (th_start), 
        started sound speed (ss_start) and final depth (depth) find two-way travel time (twtt)"""
        # B1.3.0.0 Initialization
        dist_z = depth - d_start
        rad_dist=0
        layer_s=0
        layer_e=0
        
        # Deal with angles of incidence greater than 90 degrees
#         swap=False
#         if th_start > pi/2:
#             swap = True
#             th_start = pi - th_start

        # Determine the start layer
        layer_s = sum(d_start >= self.d) - 1
        
        # Determine the Ray Constant
        ray_c = cos(th_start)/ss_start
        
        # Calculate Ray Path Properties for Each Layer  
        delta_d = (self.d[1:] - self.d[0:-1])
        r_curve = -1/(self.g[0:]*ray_c)
        th = arccos(self.c[0:]*ray_c)
        
        dx = r_curve * (sin(th[1:]) - sin(th[0:-1]))
        dz = delta_d     
        hm = 2/self.g*log(self.c[1:]/self.c[0:-1])
        dt = hm+2/self.g*log((1+sin(th[0:-1]))/(1+sin(th[1:])))  
        
        # Determine properties for start layer from the top to the start
        dx_init = r_curve[layer_s]*(sin(th_start)-sin(th[layer_s]))
        dz_init = d_start - self.d[layer_s]
        dt_init = 2/self.g[layer_s]*log(ss_start/self.c[layer_s])
        dt_init += 2/self.g[layer_s]*log((1+sin(th[layer_s]))/(1+sin(th_start)))
        
        # Accumulate From the Start Layer
        sum_dx = np.cumsum(dx[layer_s:])
        sum_dt = np.cumsum(dt[layer_s:])
        sum_dz = np.cumsum(dz[layer_s:])
        
        # Offset to the Start Depth
        sum_dx -= dx_init
        sum_dz -= dz_init
        sum_dt -= dt_init
        
        # B.1.3.1.0 Determine the Number of Boundaries Crossed and the End Layer Index
        layer_e = sum( depth >= np.cumsum(dz))
        n_bounds = layer_e - layer_s 
        
        # B.1.3.1.1 Determine the Vertical Distance Traversed in the Last Layer
        d_z = depth - self.d[layer_e]
        
        # B.1.3.1.2 Determine the Sound Speed at the End
        c_end = self.c[layer_e]+self.g[layer_e]*d_z
        
        # B.1.3.1.3 Determine the Depression Angle th_end At the End
        th_end = arccos(ray_c*c_end)
        
        # B.1.3.1.4 Determine the final TWTT and dx
        d_t = (d_z/sin(th[layer_e]))/self.c[layer_e]*2
        dx_end = r_curve[layer_e] * (sin(th_end)-sin(th[layer_e]))

        if n_bounds >= 0:
            twtt = sum_dt[n_bounds-1]+d_t
            rad_dist = sum_dx[n_bounds-1] + dx_end
        
        # B1.3.0.0 Return values as tuple
        return twtt, rad_dist, layer_s, layer_e; 
    
    
    ### B.2.3.1 drawing the profiles 
    def draw(self, full_profile=False, ax1=False, depth_range=False, ss_range=False, label=True):
        """Draw SV profile stored in the SSP object instance"""
        if ax1 == False:
            fig, ax1 = plt.subplots()   
            
        if full_profile:
            if depth_range == False:
                depth_range = (min(self.d), max(self.d))
            if ss_range == False:
                ss_range = (min(self.c), max(self.c))
            plt.plot(self.c[0:], self.d[0:])
        else:
            if depth_range == False:
                depth_range = (min(self.d[0:-1]), max(self.d[0:-1]))
            if ss_range == False:
                ss_range = (min(self.c[0:-1]), max(self.c[0:-1]))
            plt.plot(self.c[1:-1], self.d[1:-1])
            
        plt.ylim(depth_range)
        plt.xlim(ss_range)
        
        if label:
            plt.ylabel('← Depth [m]')
        else:
            labels = [item.get_text() for item in ax1.get_yticklabels()]
            empty_string_labels = ['']*len(labels)
            ax1.set_yticklabels(empty_string_labels)
            
        plt.xlabel('Sound Speed [m/s] →')
        ax1.invert_yaxis()
        ax1.xaxis.tick_top()
        ax1.xaxis.set_label_position('bottom')
        
        # Set the title from the file name that contained the data
        ax1.title.set_text(os.path.splitext(self.metadata['name'])[0])
        