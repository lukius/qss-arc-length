from arclength.poly import PolyArcLength


class QSS3ArcLength(object):

    # Arc length calculation for QSS3 numerical integrator.

    def __init__(self, v_x, v_y):
        # v_x and v_y are lists of tuples of the form
        # (q_i, t0_i, t1_i)
        # where q_i contains the coefficients of the polynomial that
        # approximates x (or y) between t0_i and t1_i. These tuples
        # are expected to be sorted in ascending order of the t0s.
        self.v_x = v_x
        self.v_y = v_y

    def _add_section(self, t0, t1, sec_x, sec_y):
        # For every polynomial section of q_x and q_y whose start and end time
        # match, this method expands the QSS polynomials into the form
        # a_0 + a_1 * t + a_2 * t^2 and then computes the arc length of the
        # resulting curve between the start time (t0) and the end time (t1).
        
        # sec_x(t) = x_0 + x_1 * (t - t0) + x_2 * (t - t0)^2
        #          = x_0 + x_1 * t - x_1 * t0 + x_2 * [t^2 - 2*t*t0 + t0^2]
        #          = (x_0 - x_1 * t0 + x_2*t0^2) + (x_1 - 2*x_2*t0) * t  + x_2 * t^2
        
        t0sq = t0*t0

        x_0 = sec_x[0] - sec_x[1]*t0 + sec_x[2]*t0sq
        x_1 = sec_x[1] - 2*sec_x[2]*t0
        x_2 = sec_x[2]

        y_0 = sec_y[0] - sec_y[1]*t0 + sec_y[2]*t0sq
        y_1 = sec_y[1] - 2*sec_y[2]*t0
        y_2 = sec_y[2]

        x_t = [x_0, x_1, x_2]
        y_t = [y_0, y_1, y_2]

        return PolyArcLength.for_polys(x_t, y_t).value(t0, t1)
        
    def value(self):
        i = 0
        j = 0
        running_total = 0
        n = len(self.v_x)
        
        while i < n and j < n:
            q_x, t0x, t1x = self.v_x[i]
            q_y, t0y, t1y = self.v_y[j]
            
            if i == j == 0:
                # Adjust start time for the first section.
                t0x = t0y = max(t0x, t0y)
                
            # As an invariant, start times should always match.
            assert(t0x == t0y)
    
            if t1x == t1y:
                t1 = t1x
                i += 1
                j += 1
            else:
                # If end times do not match, keep the lowest one and
                # split the other section.
                t1 = min(t1x, t1y)
                if t1 == t1x:
                    self.v_y[j] = (q_y, t1, t1y)
                    i += 1
                else:
                    self.v_x[i] = (q_x, t1, t1x)
                    j += 1
            
            section_length = self._add_section(t0x, t1, q_x, q_y)
            running_total += section_length
            
        return running_total        
        
      
class QSS3ArcLengthFromLogFile(object):
    
    def __init__(self, filename, x_index, y_index):
        self.filename = filename
        # These indices should match the order of the equations in the model
        # definition.
        self.x_index = x_index
        self.y_index = y_index
        
    def _read_q_values(self):
        q_values = list()
        with open(self.filename, 'r') as _file:
            for line in _file.readlines()[1:]:
                values = map(lambda v: v.strip(), line.split('\t'))
                label, idx = values[0].split(':')
                if label == 'q':
                    idx = int(idx)
                    while idx+1 > len(q_values):
                        q_values.append(list())
                    q_values[idx].append(map(float, values[1:]))
        return q_values
    
    def _get_sections(self, values):
        q_sections = list()
        for i in xrange(len(values)):
            q_i_sections = list()
            for j, vals in enumerate(values[i]):
                if j < len(values[i])-1:
                    start_time, coeffs = vals[0], vals[2:]
                    stop_time = values[i][j+1][0]
                    q_i_sections.append((coeffs, start_time, stop_time))
            q_sections.append(q_i_sections)
        return q_sections
    
    def value(self):
        q_values = self._read_q_values()
        sections = self._get_sections(q_values)
        
        v_x = sections[self.x_index]
        v_y = sections[self.y_index]
        
        return QSS3ArcLength(v_x, v_y).value()             