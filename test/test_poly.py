from unittest import TestCase

from arclength.poly import PolyArcLength


class PolyArcLengthTest(TestCase):
    
    def test_poly1_arc_length(self):
        # Reference: WolframAlpha 
        # arclength of x(t) = 1 + 2*t, y(t) = 5 - 11.5*t from t = 1 to t = 2.5
        
        x_t = [1, 2]
        y_t = [5, -11.5]
        
        arclength = PolyArcLength.for_polys(x_t, y_t).value(1, 2.5)
        str_arclength = '%.4f' % arclength
        
        self.assertEquals(str_arclength, '17.5089')
        
    def test_poly2_arc_length(self):
        # Reference: WolframAlpha 
        # arclength of x(t) = 1 - 4*t + 0.1*t^2, y(t) = 2*t - 3*t^2 from t = 1.5 to t = 3
        
        x_t = [1, -4, 0.1]
        y_t = [0, 2, -3]
        
        arclength = PolyArcLength.for_polys(x_t, y_t).value(1.5, 3)
        str_arclength = '%.5f' % arclength
        
        self.assertEquals(str_arclength, '18.10166')        