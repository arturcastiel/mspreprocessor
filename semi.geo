a = 1;
b = 1;
c = 1;




Point(1) = {0, 0, 0, 1.0};
Point(2) = {a, 0, 0, 1.0};
Point(3) = {0, b, 0, 1.0};
Point(4) = {a, b, 0, 1.0};
Point(5) = {0, 0, c, 1.0};
Point(6) = {a, 0, b, 1.0};
Point(7) = {0, b, c, 1.0};
Point(8) = {a, b, c, 1.0};
Line(1) = {5, 6};
Line(2) = {6, 2};
Line(3) = {2, 1};
Line(4) = {1, 5};
Line(5) = {5, 7};
Line(6) = {7, 8};
Line(7) = {8, 4};
Line(8) = {4, 3};
Line(9) = {3, 7};
Line(10) = {3, 1};
Line(11) = {6, 8};
Line(12) = {2, 4};
Line Loop(1) = {1, 11, -6, -5};
Plane Surface(1) = {1};
Line Loop(2) = {5, -9, 10, 4};
Plane Surface(2) = {2};
Line Loop(3) = {6, 7, 8, 9};
Plane Surface(3) = {3};
Line Loop(4) = {10, -3, 12, 8};
Plane Surface(4) = {4};
Line Loop(5) = {3, 4, 1, 2};
Plane Surface(5) = {5};
Line Loop(6) = {2, 12, -7, -11};
Plane Surface(6) = {6};
Surface Loop(1) = {1, 5, 4, 2, 3, 6};
Volume(1) = {1};


Recombine Surface {1, 3, 6, 5, 2, 4};

//Transfinite Curve {6, 5, 1, 11, 12, 2, 3, 4, 10, 7, 8, 9} =51 Using Progression 1;
//Transfinite Surface {1};
//Transfinite Surface {2};
//Transfinite Surface {3};
//Transfinite Surface {4};
//Transfinite Surface {6};
//Transfinite Surface {5};
//Transfinite Volume {1};
Physical Line(201) = {1, 2, 3, 4};
Physical Surface(801) = {1,2,3};
Physical Surface(802) = {4,5,6};

Physical Point(101) = {1, 2, 3, 4};
Physical Point(202) = {5,6,7,8};
Physical Volume(1) = {1};


