$fn = 64;
union() {
	difference() {
		cube([60, 50, 5.5]);
		translate([1, 4, 0.25]) cube([53, 26, 6]);
		translate([-1, 5, -1]) cube([7, 24, 7]);
		translate([40, 40, 0]) cylinder(10, 3.5, 3.5, true);
		translate([15, 40, 0]) cylinder(10, 3.5, 3.5, true);
		translate([40, 40, 2]) cylinder(10, 6, 6);
		translate([15, 40, 2]) cylinder(10, 6, 6);
	}
	translate([1, 1, 5.5]) cube([58, 0.5, 1]);
	translate([58.5, 1, 5.5]) cube([0.5, 48, 1]);
	translate([1, 48.5, 5.5]) cube([58, 0.5, 1]);
	translate([1, 32, 5.5]) cube([0.5, 17, 1]);
}