$fn = 64;
union() {
	difference() {
		cube([60, 50, 15]);
		translate([25, 0, 10]) minkowski() {
			cube([10, 2, 5]);
			sphere(1);
		}
		translate([2, 2, 2]) cube([56, 46, 20]);
		translate([1, 1, 14]) cube([58, 2, 2]);
		translate([57, 32, 14]) cube([2, 16, 2]);
		translate([1, 47, 14]) cube([58, 2, 2]);
		translate([1, 1, 14]) cube([2, 48, 2]);
	}
	translate([7, 6.5, 0]) cylinder(15, .9, .9);
	translate([7, 26.5, 0]) cylinder(15, .9, .9);
	cube([12, 30, 13]);
}